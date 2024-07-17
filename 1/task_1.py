import sys
from PyQt6 import QtWidgets
from calk_form import Ui_MainWindow


class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.addButton.clicked.connect(self.add)
        self.ui.subtractButton.clicked.connect(self.subtract)
        self.ui.multiplyButton.clicked.connect(self.multiply)
        self.ui.divideButton.clicked.connect(self.divide)

    def get_values(self):

        try:
            a_text = self.ui.lineEdit_a.text().replace('.', ',')
            b_text = self.ui.lineEdit_b.text().replace('.', ',')
            a = float(a_text.replace(',', '.'))
            b = float(b_text.replace(',', '.'))
            return a, b
        except ValueError:
            self.ui.result.setText("Ошибка: неверный ввод")
            return None, None

    def add(self):
        a, b = self.get_values()
        if a is not None and b is not None:
            result = a + b
            self.ui.result.setText(f"Результат: {result}")

    def subtract(self):
        a, b = self.get_values()
        if a is not None and b is not None:
            result = a - b
            self.ui.result.setText(f"Результат: {result}")

    def multiply(self):
        a, b = self.get_values()
        if a is not None and b is not None:
            result = a * b
            self.ui.result.setText(f"Результат: {result}")

    def divide(self):
        a, b = self.get_values()
        if a is not None and b is not None:
            if b != 0:
                result = a / b
                self.ui.result.setText(f"Результат: {result}")
            else:
                self.ui.result.setText("Ошибка: деление на ноль")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
