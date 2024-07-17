import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import math
import numpy as np
from matplotlib.figure import Figure


# Класс для создания холста с графиком на основе Matplotlib
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # Создаем фигуру и добавляем на нее оси
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)

# Класс главного окна приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Graph Plotter")  # Заголовок окна
        self.setGeometry(100, 100, 800, 600)  # Размеры окна

        # Создаем центральный виджет и устанавливаем его как центральный виджет окна
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Создаем вертикальный слой и устанавливаем его для центрального виджета
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Создаем холст для графика и добавляем его на слой
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        layout.addWidget(self.canvas)

        # Создаем панель инструментов для навигации по графику (приближение, панорамирование)
        toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(toolbar)

        # Вызываем функцию для построения графика
        self.plot_graph()

    # Функция для построения графика
    def plot_graph(self):
        # Начальная точка и шаг для x
        x_start = 0
        x_step = 0.1
        num_points = 100  # Количество точек

        # Задаем x и y
        x = np.array([x_start + i * x_step for i in range(num_points)])
        y = np.sin(x**2)  # Функция y = sin(x^2)

        # Строим точки на графике
        self.canvas.axes.plot(x, y, 'ro', label='Points')

        # Линейная интерполяция между точками
        for i in range(len(x) - 1):
            x_vals = np.linspace(x[i], x[i+1], 100)
            y_vals = np.interp(x_vals, [x[i], x[i+1]], [y[i], y[i+1]])
            self.canvas.axes.plot(x_vals, y_vals, 'b-', label='Linear' if i == 0 else "")

        self.canvas.axes.legend()  # Добавляем легенду
        self.canvas.fig.tight_layout()  # Автоматически подстраиваем элементы графика
        self.canvas.draw()  # Отображаем график


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
