from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel


class MapLabel(QLabel):
    clicked = QtCore.pyqtSignal()
    left_clicked = QtCore.pyqtSignal()
    right_clicked = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self._click_pos = (0, 0)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self._click_pos = ev.pos().x(), self.height() - ev.pos().y()
        self.clicked.emit()
        if ev.button() == QtCore.Qt.LeftButton:
            self.left_clicked.emit()
        elif ev.button() == QtCore.Qt.RightButton:
            self.right_clicked.emit()
        QLabel.mousePressEvent(self, ev)

    def get_click_pos(self):
        return self._click_pos
