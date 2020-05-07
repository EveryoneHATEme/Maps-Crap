from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel


class MapLabel(QLabel):
    clicked = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self._click_pos = (0, 0)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self._click_pos = ev.pos().x(), self.height() - ev.pos().y()
        self.clicked.emit()
        QLabel.mousePressEvent(self, ev)

    def get_click_pos(self):
        return self._click_pos
