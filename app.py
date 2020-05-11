import sys
from decimal import Decimal
from copy import deepcopy

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

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
        self.bbox = ()
        self.ll = ""
        self.spn = ""
        self.z = 13
        self.scale = ""
        self.pt = ""
        self.pl = ""
        self.lang = "ru_RU"
        self.found = False

    def setup_connections(self):
        self.pushButton_find.clicked.connect(self.find_object)
        self.pushButton_clear.clicked.connect(self.clear)
        self.radioButton_with_index.clicked.connect(self.display_address)
        self.radioButton_wo_index.clicked.connect(self.display_address)
        self.radioButton_map.clicked.connect(self.change_view)
        self.radioButton_sat.clicked.connect(self.change_view)
        self.radioButton_hybrid.clicked.connect(self.change_view)
        self.labelMap.left_clicked.connect(self.map_left_click)
        self.labelMap.right_clicked.connect(self.map_right_click)

    def keyReleaseEvent(self, event):
        key = event.key()
        if self.found:
            if key == Qt.Key_PageUp:
                # zoom in
                delta_x = abs(self.bbox[1][0] - self.bbox[0][0]) / 5
                delta_y = abs(self.bbox[1][1] - self.bbox[0][1]) / 5
                if delta_x <= 0.0001 or delta_y <= 0.0001:
                    return

                self.bbox = ((self.bbox[0][0] + delta_x, self.bbox[0][1] + delta_y),
                             (self.bbox[1][0] - delta_x, self.bbox[1][1] - delta_y))
                self.update_map()
            elif key == Qt.Key_PageDown:
                # zoom out
                delta_x = abs(self.bbox[1][0] - self.bbox[0][0]) / 5
                delta_y = abs(self.bbox[1][1] - self.bbox[0][1]) / 5

                self.bbox = ((max(-179, self.bbox[0][0] - delta_x), max(-89, self.bbox[0][1] - delta_y)),
                             (min(179, self.bbox[1][0] + delta_x), min(89, self.bbox[1][1] + delta_y)))
                self.update_map()
            elif key == Qt.Key_Left:
                # move left {left down}
                k = abs(self.bbox[1][0] - self.bbox[0][0])
                prev_bbox = deepcopy(self.bbox)
                self.bbox = ((self.bbox[0][0] - k, self.bbox[0][1]), (self.bbox[1][0] - k, self.bbox[1][1]))
                if self.bbox[0][0] < -180:
                    self.bbox = deepcopy(prev_bbox)
                self.update_map()
            elif key == Qt.Key_Right:
                # move right {left up}
                k = abs(self.bbox[1][0] - self.bbox[0][0])
                prev_bbox = deepcopy(self.bbox)
                self.bbox = ((self.bbox[0][0] + k, self.bbox[0][1]), (self.bbox[1][0] + k, self.bbox[1][1]))
                if self.bbox[1][0] > 180:
                    self.bbox = deepcopy(prev_bbox)
                self.update_map()
            elif key == Qt.Key_Up:
                # move up {right up)
                k = abs(self.bbox[1][1] - self.bbox[0][1])
                prev_bbox = deepcopy(self.bbox)
                self.bbox = ((self.bbox[0][0], self.bbox[0][1] + k), (self.bbox[1][0], self.bbox[1][1] + k))
                if self.bbox[1][1] > 90:
                    self.bbox = deepcopy(prev_bbox)
                self.update_map()
            elif key == Qt.Key_Down:
                # move down {right down)
                k = abs(self.bbox[1][1] - self.bbox[0][1])
                prev_bbox = deepcopy(self.bbox)
                self.bbox = ((self.bbox[0][0], self.bbox[0][1] - k), (self.bbox[1][0], self.bbox[1][1] - k))
                if self.bbox[0][1] <= -90:
                    self.bbox = deepcopy(prev_bbox)
                self.update_map()

    def map_left_click(self):
        click_x, click_y = self.labelMap.get_click_pos()
        lon_per_pix = (Decimal(self.bbox[1][0]) - Decimal(self.bbox[0][0])) / self.labelMap.width()
        lat_per_pix = (Decimal(self.bbox[1][1]) - Decimal(self.bbox[0][1])) / self.labelMap.height()
        self.pt = f'{lon_per_pix * click_x + Decimal(self.bbox[0][0])},' \
                  f'{lat_per_pix * click_y + Decimal(self.bbox[0][1])},pm2rdm'
        try:
            response = self.api_handler.geocoder_api_json(geocode=f'{lon_per_pix * click_x + Decimal(self.bbox[0][0])},'
                                                                  f'{lat_per_pix * click_y + Decimal(self.bbox[0][1])}')
            self.address, self.postal_code = utils.address_from_json(response)
            self.update_map()
            self.display_address()
        except IndexError:
            return

    def map_right_click(self):
        click_x, click_y = self.labelMap.get_click_pos()
        lon_per_pix = (Decimal(self.bbox[1][0]) - Decimal(self.bbox[0][0])) / self.labelMap.width()
        lat_per_pix = (Decimal(self.bbox[1][1]) - Decimal(self.bbox[0][1])) / self.labelMap.height()
        lon, lat = lon_per_pix * click_x + Decimal(self.bbox[0][0]), lat_per_pix * click_y + Decimal(self.bbox[0][1])
        response = self.api_handler.search_api_json(text='организация',
                                                    spn="0.1,0.1",
                                                    ll=f'{lon},{lat}',
                                                    _type="biz")
        closest_org = utils.get_closest_object_data_from_search_api(response)
        if utils.get_distance((float(lon), float(lat)), closest_org["pos"]) <= 0.05:
            self.find_object(ll=f"{closest_org['pos'][0]},{closest_org['pos'][1]}")
            self.lineEdit_request.setText(closest_org["name"])

    def update_map(self):
        img = self.api_handler.get_image(
            l=self.L,
            bbox='~'.join([','.join(map(str, x)) for x in self.bbox]),
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
        if not ll:
            if not self.lineEdit_request.text():
                return
            response = self.api_handler.geocoder_api_json(geocode=self.lineEdit_request.text())
            if not response["response"]["GeoObjectCollection"]["featureMember"]:
                return
            self.ll = utils.lonlat_from_json(response)[0]
        else:
            response = self.api_handler.geocoder_api_json(geocode=ll)
            self.ll = ll
        self.bbox = utils.get_bbox_from_geocoder(response)
        self.address, self.postal_code = utils.address_from_json(response)
        self.pt = f"{self.ll},pm2rdm"
        self.found = True
        self.update_map()
        self.display_address()

    def clear(self):
        self.lineEdit_request.clear()
        self.lineEdit_address.clear()
        self.labelMap.clear()
        self.ll = None
        self.bbox = ()
        self.address = ""
        self.postal_code = ""
        self.pt = ""
        self.found = False

    def display_address(self):
        if self.radioButton_with_index.isChecked():
            if self.postal_code:
                self.lineEdit_address.setText(f"{self.address}, {self.postal_code}")
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
