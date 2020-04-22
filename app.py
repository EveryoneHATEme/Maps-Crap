import sys
from pprint import pprint

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPicture, QPixmap
from PyQt5.Qt import QMouseEvent

from ui import ui_main
from api import api_handler
import utils


class App(QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_connections()

        self.api_handler = api_handler.ApiHandler()

        self.address = ""
        self.postal_code = ""

        self.L = "map"
        self.ll = ""
        self.spn = ""
        self.z = ""
        self.scale = ""
        self.pt = ""
        self.pl = ""
        self.lang = "ru_RU"

    def setup_connections(self):
        self.pushButton_find.clicked.connect(self.find_object)
        self.pushButton_clear.clicked.connect(self.clear)
        self.radioButton_with_index.clicked.connect(self.display_address)
        self.radioButton_wo_index.clicked.connect(self.display_address)
        self.radioButton_map.clicked.connect(self.change_view)
        self.radioButton_sat.clicked.connect(self.change_view)
        self.radioButton_hybrid.clicked.connect(self.change_view)

    def keyReleaseEvent(self, event):
        key = event.key()
        if self.ll:
            if key == Qt.Key_PageUp:
                # zoom in
                long, lat = (float(x) for x in self.spn.split(","))
                long = max(0.001, long / 2)
                lat = max(0.001, lat / 2)
                self.spn = f"{long},{lat}"
                self.update_map()
            elif key == Qt.Key_PageDown:
                # zoom out
                long, lat = (float(x) for x in self.spn.split(","))
                long = min(180, long * 2)
                lat = min(90, lat * 2)
                self.spn = f"{long},{lat}"
                self.update_map()
            elif key == Qt.Key_Left:
                # move left {left down}
                long, lat = (float(x) for x in self.ll.split(","))
                long_spn, lat_spn = (float(x) for x in self.spn.split(","))
                long = max(-180.0, long - long_spn)
                self.ll = ",".join((str(long), str(lat)))
                self.update_map()
            elif key == Qt.Key_Right:
                # move right {left up}
                long, lat = (float(x) for x in self.ll.split(","))
                long_spn, lat_spn = (float(x) for x in self.spn.split(","))
                long = min(180.0, long + long_spn)
                self.ll = ",".join((str(long), str(lat)))
                self.update_map()
            elif key == Qt.Key_Up:
                # move up {right up)
                long, lat = (float(x) for x in self.ll.split(","))
                long_spn, lat_spn = (float(x) for x in self.spn.split(","))
                lat = min(90.0, lat + lat_spn)
                self.ll = ",".join((str(long), str(lat)))
                self.update_map()
            elif key == Qt.Key_Down:
                # move down {right down)
                long, lat = (float(x) for x in self.ll.split(","))
                long_spn, lat_spn = (float(x) for x in self.spn.split(","))
                lat = max(-90.0, lat - lat_spn)
                self.ll = ",".join((str(long), str(lat)))
                self.update_map()

    def mouseReleaseEvent(self, event):
        event: QMouseEvent
        if event.button() == Qt.LeftButton:
            # TODO: find object
            pass
        elif event.button() == Qt.RightButton:
            # TODO: find closest organization
            pass

    def update_map(self):
        img = self.api_handler.get_image(
            l=self.L,
            ll=self.ll,
            spn=self.spn,
            z=self.z,
            scale=self.scale,
            pt=self.pt,
            pl=self.pl,
            lang=self.lang
        )
        pixmap = QPixmap()
        pixmap.loadFromData(img)
        self.labelMap.setPixmap(pixmap)

    def find_object(self, ll=None):
        if self.lineEdit_request.text():
            if not ll:
                response = self.api_handler.geocoder_api_json(geocode=self.lineEdit_request.text())
                self.ll = utils.longlat_from_json(response)[0]
                self.address, self.postal_code = utils.address_from_json(response)
                long, lat = (float(x) for x in self.ll.split(","))
                long_c, lat_c = utils.bbox_from_json(response)[0]
                self.spn = f"{long - long_c},{lat - lat_c}"
                self.pt = self.ll + ",comma"
                self.update_map()
                self.display_address()
            else:
                response = self.api_handler.geocoder_api_json(geocode=ll)
                self.address, self.postal_code = utils.address_from_json(response)
                self.pt = ll + ",comma"
                self.update_map()
                self.display_address()

    def clear(self):
        self.lineEdit_request.clear()
        self.lineEdit_address.clear()
        self.labelMap.clear()
        self.ll = None
        self.address = ""
        self.postal_code = ""
        self.pt = ""

    def display_address(self):
        if self.radioButton_with_index.isChecked():
            if self.postal_code:
                self.lineEdit_address.setText(self.address + f", {self.postal_code}")
            else:
                self.lineEdit_address.setText(self.address + ", postal code unknown")
        else:
            self.lineEdit_address.setText(self.address)

    def change_view(self):
        if self.radioButton_map.isChecked():
            self.L = "map"
        elif self.radioButton_sat.isChecked():
            self.L = "sat"
        elif self.radioButton_hybrid.isChecked():
            self.L = "sat,skl"
        self.update_map()


def excepthook(exctype, value, traceback):
    return sys.__excepthook__(exctype, value, traceback)


if __name__ == "__main__":
    sys.excepthook = excepthook
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
