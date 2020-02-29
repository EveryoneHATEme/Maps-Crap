from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QRadioButton, QLineEdit
from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
from APIHandler import RequestHandler


class MapsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.actions_handler = RequestHandler()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            self.actions_handler.increase_map()
        elif event.key() == Qt.Key_PageUp:
            self.actions_handler.decrease_map()
        elif event.key() == Qt.Key_Up:
            self.actions_handler.move_up()
        elif event.key() == Qt.Key_Down:
            self.actions_handler.move_down()
        elif event.key() == Qt.Key_Left:
            self.actions_handler.move_left()
        elif event.key() == Qt.Key_Right:
            self.actions_handler.move_right()


def excepthook(a, b, c):
    return sys.__excepthook__(a, b, c)


if __name__ == "__main__":
    sys.excepthook = excepthook
    app = QApplication(sys.argv)
    maps = MapsApp()
    maps.show()
    sys.exit(app.exec())
