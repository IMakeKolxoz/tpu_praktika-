import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QGridLayout, QSpacerItem, QSizePolicy, QTextEdit
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class IntegrationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Численное интегрирование")

        # Центральный виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Основная компоновка
        self.layout = QHBoxLayout(self.central_widget)

        # Компоновка для графиков
        self.graphs_layout = QVBoxLayout()
        self.layout.addLayout(self.graphs_layout)

        # График функции
        self.figure_function = plt.figure()
        self.canvas_function = FigureCanvas(self.figure_function)
        self.graphs_layout.addWidget(self.canvas_function)

        # График сходимости
        self.figure_convergence = plt.figure()
        self.canvas_convergence = FigureCanvas(self.figure_convergence)
        self.graphs_layout.addWidget(self.canvas_convergence)

        # Компоновка для ввода и вывода
        self.io_layout = QVBoxLayout()
        self.layout.addLayout(self.io_layout)

        # Поля ввода
        self.inputs_layout = QGridLayout()

        self.label_a = QLabel("Нижний предел (a):")
        self.input_a = QLineEdit("0")
        self.label_b = QLabel("Верхний предел (b):")
        self.input_b = QLineEdit("2")
        self.label_n = QLabel("Количество точек:")
        self.input_n = QLineEdit("100")
        self.label_step = QLabel("Шаг (step):")
        self.input_step = QLineEdit("5")

        self.inputs_layout.addWidget(self.label_a, 0, 0)
        self.inputs_layout.addWidget(self.input_a, 0, 1)
        self.inputs_layout.addWidget(self.label_b, 1, 0)
        self.inputs_layout.addWidget(self.input_b, 1, 1)
        self.inputs_layout.addWidget(self.label_n, 2, 0)
        self.inputs_layout.addWidget(self.input_n, 2, 1)
        self.inputs_layout.addWidget(self.label_step, 3, 0)
        self.inputs_layout.addWidget(self.input_step, 3, 1)

        # Разделитель
        self.io_layout.addLayout(self.inputs_layout)
        self.io_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Кнопка "Начать"
        self.start_button = QPushButton("Начать")
        self.start_button.clicked.connect(self.calculate_and_plot)
        self.io_layout.addWidget(self.start_button)

        # Поля вывода
        self.output_layout = QGridLayout()

        self.label_approx = QLabel("Приближенное значение интеграла:")
        self.output_approx = QLabel("")
        self.label_exact = QLabel("Точное значение интеграла:")
        self.output_exact = QLabel("")
        self.label_error = QLabel("Погрешность:")
        self.output_error = QLabel("")
        self.label_opt_n = QLabel("Оптимальное значение N:")
        self.output_opt_n = QLabel("")

        self.output_layout.addWidget(self.label_approx, 0, 0)
        self.output_layout.addWidget(self.output_approx, 0, 1)
        self.output_layout.addWidget(self.label_exact, 1, 0)
        self.output_layout.addWidget(self.output_exact, 1, 1)
        self.output_layout.addWidget(self.label_error, 2, 0)
        self.output_layout.addWidget(self.output_error, 2, 1)
        self.output_layout.addWidget(self.label_opt_n, 3, 0)
        self.output_layout.addWidget(self.output_opt_n, 3, 1)

        # Текстовое поле для вывода значений
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.io_layout.addLayout(self.output_layout)
        self.io_layout.addWidget(self.output_text)
        self.io_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def calculate_and_plot(self):
        a = float(self.input_a.text())
        b = float(self.input_b.text())
        n = int(self.input_n.text())
        step = int(self.input_step.text())

        exact_integral = (b ** 5 / 5) - (a ** 5 / 5)
        approx_integral = midpoint_rectangular_integration(f, a, b, n)
        error = abs(approx_integral - exact_integral)

        self.output_approx.setText(f"{approx_integral:.6f}")
        self.output_exact.setText(f"{exact_integral:.6f}")
        self.output_error.setText(f"{error:.6f}")

        self.plot_function(a, b)
        self.plot_convergence(a, b, n, exact_integral, step)

    def plot_function(self, a, b):
        x = np.linspace(a, b, 400)
        y = f(x)

        self.figure_function.clear()
        ax = self.figure_function.add_subplot(111)
        ax.plot(x, y, label=r'$f(x) = x^4$')
        ax.set_title('График функции $f(x) = x^4$')
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.legend()
        ax.grid(True)

        self.canvas_function.draw()

    def plot_convergence(self, a, b, n, exact_integral, step):
        N_values = np.arange(step, n + step, step)
        integral_values = [midpoint_rectangular_integration(f, a, b, N) for N in N_values]
        deltas = [abs(approx - exact_integral) for approx in integral_values]

        self.figure_convergence.clear()
        ax = self.figure_convergence.add_subplot(111)
        ax.plot(N_values, integral_values, label='Приближенный интеграл')
        ax.axhline(y=exact_integral, color='r', linestyle='-', label='Точный интеграл')
        ax.set_title('График сходимости интегралов')
        ax.set_xlabel('N (количество точек)')
        ax.set_ylabel('Приближенное значение интеграла')
        ax.legend()
        ax.grid(True)

        self.canvas_convergence.draw()

        self.output_text.clear()
        optimal_n = None
        for N, approx, delta in zip(N_values, integral_values, deltas):
            self.output_text.append(f"N: {N}, T: {approx:.12f}, A: {exact_integral:.12f}, Delta: {delta:.12f}")
            if delta < 1e-6 and optimal_n is None:
                optimal_n = N

        if optimal_n is not None:
            self.output_opt_n.setText(f"{optimal_n}")
        else:
            self.output_opt_n.setText("Не найдено")


def f(x):
    return x ** 4


def midpoint_rectangular_integration(f, a, b, n):
    h = (b - a) / n
    integral_sum = 0.0

    for i in range(n):
        mid_point = a + h * (i + 0.5)
        integral_sum += f(mid_point)

    integral_sum *= h
    return integral_sum


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IntegrationApp()
    window.show()
    sys.exit(app.exec())
