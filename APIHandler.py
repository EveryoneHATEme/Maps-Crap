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
