import sys
from datetime import time
from PyQt5.QtWidgets import QWidget, QApplication,\
    QMainWindow, QLabel, QSlider, QHBoxLayout, QVBoxLayout, QGridLayout,\
    QLineEdit, QTimeEdit, QSpacerItem, QPushButton, QCheckBox, QSpinBox,\
    QFrame, QStyle, QMessageBox, QSizePolicy
from PyQt5.QtCore import QTime, Qt


def warn(message):
    msg = QMessageBox()
    msg.minimumWidth = 300
    msg.setIcon(QMessageBox.Warning)
    msg.setText(message)
    msg.exec_()


def inform(message):
    msg = QMessageBox()
    msg.minimumWidth = 300
    msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    msg.exec_()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window = QWidget()
        self.slide = Slide(self)
        self.auto = AutoPanel(self)
        self.connection = ConnectPanel(self)
        self.__setup()

    def __setup(self):
        self.layout = QVBoxLayout()
        self.setCentralWidget(self.window)
        self.window.setLayout(self.layout)
        self.layout.addWidget(self.connection)
        self.layout.addWidget(QHLine())
        self.layout.addWidget(self.auto)
        self.layout.addWidget(self.slide)
        self.show()

    @property
    def is_checked(self):
        return self.auto.is_checked

    @property
    def ip(self):
        return self.connection.ip_edit.text()

    @property
    def is_simulation(self):
        return self.connection.simulate_check.checkState()

    def set_connection_state(self, state):
        self.connection.set_state(state)

    def disconnect_function_slots(self):
        self.auto.disconnect()
        self.slide.disconnect()

class ConnectPanel(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.layout = QGridLayout()
        self.__setup()
        self.set_state(True)

    def __setup(self):
        self.setLayout(self.layout)
        self.ip_edit = QLineEdit("192.168.0.1")
        self.state = QLabel()
        self.simulate_check = QCheckBox("Simulate Bulb")
        self.simulate_check.setChecked(False)
        self.button = QPushButton("Connect")

        self.layout.addWidget(QLabel("IP address"), 0, 0)
        self.layout.addWidget(self.ip_edit, 0, 1)
        self.layout.addWidget(self.button, 0, 2)
        self.layout.addWidget(self.state, 0, 3)
        self.layout.addWidget(self.simulate_check, 2, 1)

    def set_state(self, state: bool):
        if state:
            self.state.setPixmap(self.style().standardIcon(
                getattr(QStyle, 'SP_DialogApplyButton')
            ).pixmap(24, 24))
        else:
            self.state.setPixmap(self.style().standardIcon(
                getattr(QStyle, 'SP_DialogCancelButton')
            ).pixmap(24, 24))

    def set_button_callback(self, func):
        self.button.clicked.connect(func)


class AutoPanel(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.layout = QVBoxLayout()
        self.__day_start = 0
        self.__setup()

    def __setup(self):
        self.setLayout(self.layout)
        self.day = TimeEntry(self, "Daylight ", 8, 20)
        self.check = QCheckBox("Automated Control")

        self.layout.addWidget(self.check)
        self.layout.addWidget(self.day)

    @property
    def is_checked(self):
        return self.check.checkState()

    @property
    def start(self):
        return time.fromisoformat(self.day.start.toString())

    @property
    def end(self):
        return time.fromisoformat(self.day.end.toString())

    @property
    def target(self):
        return self.day.target

    def disconnect(self):
        self.check.stateChanged.disconnect()

    def set_check_callback(self, func):
        self.check.stateChanged.connect(func)

    def set_text(self, text):
        self.check.setText("Automated Control" + text)


class TimeEntry(QWidget):
    def __init__(self, parent, name, start, end):
        super().__init__(parent=parent)
        self.layout = QHBoxLayout()
        self.name = name
        self.__setup(start, end)

    def __setup(self, start, end):
        self.setLayout(self.layout)
        self.target_box = QSpinBox(parent=self)
        self.target_box.setValue(50)
        self.start_edit = QTimeEdit(parent=self)
        self.end_edit = QTimeEdit(parent=self)
        self.start_edit.setTime(QTime(start, 0))
        self.end_edit.setTime(QTime(end, 0))

        self.layout.addWidget(QLabel(self.name))
        self.layout.addWidget(self.target_box)
        self.layout.addItem(QSpacerItem(
            1, 1, QSizePolicy.Expanding, QSizePolicy.MinimumExpanding
        ))
        self.layout.addWidget(QLabel("from"))
        self.layout.addWidget(self.start_edit)
        self.layout.addWidget(QLabel(" to "))
        self.layout.addWidget(self.end_edit)

    @property
    def target(self):
        return self.target_box.value()

    @property
    def start(self):
        return self.start_edit.time()

    @property
    def end(self):
        return self.end_edit.time()


class Slide(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.layout = QHBoxLayout()
        self.__setup()

    def __setup(self):
        self.setLayout(self.layout)
        self.slider = QSlider(Qt.Horizontal, self)
        self.value = QLabel("0")

        self.layout.addWidget(QLabel("Brightness"))
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.value)

    def disconnect(self):
        self.slider.valueChanged.disconnect()
        self.slider.sliderReleased.disconnect()

    def set_change_callback(self, func):
        self.slider.valueChanged.connect(func)

    def set_release_callback(self, func):
        self.slider.sliderReleased.connect(func)

    def set_value(self, value):
        self.slider.setValue(value)
        self.value.setText(str(value))

    def get_value(self):
        return int(self.value.text())


class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class QVLine(QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)

if __name__ == "__main__":
    class Dummy(QMainWindow):
        def __init__(self):
            super().__init__()
            self.ap = AutoPanel(parent=self)
            self.setCentralWidget(self.ap)
            self.show()

    app = QApplication(sys.argv)
    dummy = Dummy()
    app.exec_()
