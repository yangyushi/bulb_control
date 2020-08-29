import sys
from control import Controller
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)
    control = Controller()
    app.exec_()
