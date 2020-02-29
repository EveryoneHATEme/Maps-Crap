from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QRadioButton, QLineEdit
from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys


class RequestHandler:
    def __init__(self):
        self.latitude = None
        self.longitude = None
        self.delta = 0.01
        self.points = list()
        self.mode = 'map'

    def increase_map(self):
        self.delta = min(2, self.delta + 0.01)
        self.update()

    def decrease_map(self):
        self.delta = max(0.01, self.delta - 0.01)
        self.update()

    def update(self):
        pass


class MapsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.actions_handler = RequestHandler()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            self.actions_handler.increase_map()
        elif event.key() == Qt.Key_PageUp:
            self.actions_handler.decrease_map()


def excepthook(a, b, c):
    return sys.__excepthook__(a, b, c)


if __name__ == "__main__":
    sys.excepthook = excepthook
    app = QApplication(sys.argv)
    maps = MapsApp()
    maps.show()
    sys.exit(app.exec())
