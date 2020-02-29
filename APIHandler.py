import requests
from io import BytesIO
from PIL import Image, ImageQt


class RequestHandler:
    def __init__(self, settings: dict):
        self.settings = settings
        self.static_address = 'http://static-maps.yandex.ru/1.x/'

    def get_image_by_coords(self, latitude: float, longitude: float):
        params = {key: value for key, value in self.settings.items() if key in {'l', 'size', 'lang'}}
        params['ll'] = f'{latitude},{longitude}'
        response = requests.get(self.static_address, params=params)
        if not response:
            print('no response')
            return
        return ImageQt.toqpixmap(Image.open(BytesIO(response.content)))


if __name__ == '__main__':
    dct = {'l': 'map', 'size': '650,450', 'lang': 'ru_RU'}
    handler = RequestHandler(dct)
    handler.get_image_by_coords(60.597465, 56.838011)
