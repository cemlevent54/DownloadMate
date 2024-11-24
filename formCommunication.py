import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton


class Form1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Form 1")
        self.setGeometry(100, 100, 300, 200)

        self.button = QPushButton("Form 2'yi Aç", self)
        self.button.setGeometry(100, 80, 100, 30)
        self.button.clicked.connect(self.open_form2)

    def open_form2(self):
        self.form2 = Form2()
        self.form2.show()
        self.close()


class Form2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Form 2")
        self.setGeometry(100, 100, 300, 200)

    def closeEvent(self, event):
        # Form2 kapandığında Form1'i yeniden aç
        self.form1 = Form1()
        self.form1.show()
        event.accept()  # Pencerenin kapanmasını kabul et


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form1 = Form1()
    form1.show()
    sys.exit(app.exec_())
