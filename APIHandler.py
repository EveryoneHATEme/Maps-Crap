import requests
from io import BytesIO
from PIL import Image, ImageQt


class RequestHandler:
    def __init__(self):
        self.settings = {
            'size': '650,450',
            'lang': 'ru_RU',
            'l': 'map',
            'z': '17',
            'll': '0.0,0.0'
        }
        self.points = list()
        self.delta = 0.01
        self.static_address = 'http://static-maps.yandex.ru/1.x/'
        self.latitude, self.longitude = None, None

    def set_settings(self, **kwargs):
        if 'size' in kwargs:
            self.settings['size'] = kwargs['size']
        if 'lang' in kwargs:
            self.settings['lang'] = kwargs['lang']
        if 'l' in kwargs:
            self.settings['l'] = kwargs['l']

    def set_coords(self, latitude: float, longitude: float):
        self.latitude, self.longitude = latitude, longitude

    def get_image(self):
        params = {key: value for key, value in self.settings.items() if key in {'l', 'size', 'lang'}}
        params['ll'] = f'{self.latitude},{self.longitude}'
        params['z'] = f'{self.scale}'
        response = requests.get(self.static_address, params=params)
        if not response:
            print('no response')
            return
        return ImageQt.toqpixmap(Image.open(BytesIO(response.content)))

    def increase_map(self):
        self.delta = min(2, self.delta + 0.01)
        self.update()

    def decrease_map(self):
        self.delta = max(0.01, self.delta - 0.01)
        self.update()

    def change_mode(self, mode: str):
        if mode in ('map', 'sat', 'sat,skl'):
            self.mode = mode

    def move_left(self):
        if type(self.latitude) == float:
            if self.latitude - 0.000001 in range(-180, 180):
                self.latitude -= 0.000001

    def move_right(self):
        if type(self.latitude) == float:
            if self.latitude + 0.000001 in range(-180, 180):
                self.latitude += 0.000001

    def move_up(self):
        if type(self.longitude) == float:
            if self.longitude - 0.000001 in range(-180, 180):
                self.longitude -= 0.000001

    def move_down(self):
        if type(self.longitude) == float:
            if self.longitude + 0.000001 in range(-180, 180):
                self.longitude += 0.000001

    def update(self):
        pass
