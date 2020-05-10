from requests import get

GEOCODER_API_SERVER = "http://geocode-maps.yandex.ru/1.x/"
SEARCH_API_SERVER = "https://search-maps.yandex.ru/v1/"
MAP_API_SERVER = "http://static-maps.yandex.ru/1.x/"

GEOCODER_API_KEY = "40d1649f-0493-4b70-98ba-98533de7710b"
SEARCH_API_KEY = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"


class ApiHandler:
    @staticmethod
    def get_image(l="", bbox='', ll="", spn="", z="13", scale="", pt="", pl="", lang="ru_RU"):
        params = {
            "size": "650,450",
        }
        if l:
            params["l"] = l
        if bbox:
            params['bbox'] = bbox
        if ll:
            params["ll"] = ll
        if spn:
            params["spn"] = spn
        if z != "":
            params["z"] = z
        if scale:
            params["scale"] = scale
        if pt:
            params["pt"] = pt
        if pl:
            params["pl"] = pl
        if lang:
            params["lang"] = lang
        return get(MAP_API_SERVER, params=params).content

    @staticmethod
    def geocoder_api_json(geocode="", sco="", kind="", rspn="", ll="",
                 spn="", bbox="", results="", skip="", lang="ru_RU"):
        params = {
            "apikey": GEOCODER_API_KEY,
            "format": "json",
            "geocode": geocode
        }
        if sco:
            params["sco"] = sco
        if kind:
            params["kind"] = kind
        if rspn:
            params["rspn"] = rspn
        if ll:
            params["ll"] = ll
        if spn:
            params["spn"] = spn
        if bbox:
            params["bbox"] = bbox
        if results:
            params["results"] = results
        if skip:
            params["skip"] = skip
        if lang:
            params["lang"] = lang
        return get(GEOCODER_API_SERVER, params=params).json()

    @staticmethod
    def search_api_json(text="", type="", rspn="", ll="", spn="",
                        bbox="", results="", skip="", lang="ru_RU"):
        params = {
            "apikey": SEARCH_API_KEY,
            "text": text,
            "lang": lang,
            "type": type,
            "rspn": rspn,
            "ll": ll,
            "spn": spn,
            "bbox": bbox,
            "results": results,
            "skip": skip,
        }
        return get(SEARCH_API_SERVER, params=params).json()
