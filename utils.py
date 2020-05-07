import math
from pprint import pprint


def get_bbox_from_geocoder(response):
    toponym = response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    return tuple(map(float, toponym["boundedBy"]["Envelope"]["lowerCorner"].split())),\
        tuple(map(float, toponym["boundedBy"]["Envelope"]["upperCorner"].split()))


def lonlat_from_json(response: dict):
    """
    :param response:
    :return: list of lonlat
    """
    result = []
    toponym = response["response"]["GeoObjectCollection"][
        "featureMember"]
    for i in toponym:
        result.append(",".join(i["GeoObject"]['Point']['pos'].split()))
    return result


def address_from_json(response: dict) -> tuple:
    """
    :param response:
    :return: address and postal code
    """
    address = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
        'GeocoderMetaData']['Address']
    return "".join(address['formatted']), address['postal_code'] if 'postal_code' in address else ''


def get_closest_object_data_from_geocoder(target_pos, coords, kind):
    """
    :param target_pos:
    :param coords:
    :param kind:
    :return: closest object name and him lonlat
    """
    target_x, target_y = target_pos
    min_distance = float('inf')
    result_lonlat = None
    closest_obj = None
    for i in coords:
        x, y = i
        dist = ((x - target_x) ** 2 + (y - target_y) ** 2) ** 0.5
        if dist < min_distance:
            min_distance = dist
            closest_obj = list(filter(lambda x: x['kind'] == kind,
                                        i['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address'][
                                            'Components']))[0]['name']
            result_lonlat = x, y
    return closest_obj, result_lonlat


def get_closest_object_data_from_search_api(response: dict):
    organization = response["features"][0]
    org_name = organization["properties"]["CompanyMetaData"]["name"]
    org_address = organization["properties"]["CompanyMetaData"]["address"]
    point = tuple(map(float, organization["geometry"]["coordinates"]))
    return {'name': org_name, 'address': org_address, 'pos': point}


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    distance = math.sqrt(dx * dx + dy * dy)
    return distance
