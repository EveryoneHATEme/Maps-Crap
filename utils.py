import math


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


def get_distance(p1, p2):
    radius = 6373.0

    lon1 = math.radians(p1[0])
    lat1 = math.radians(p1[1])
    lon2 = math.radians(p2[0])
    lat2 = math.radians(p2[1])

    d_lon = lon2 - lon1
    d_lat = lat2 - lat1

    a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(a ** 0.5, (1 - a) ** 0.5)

    distance = radius * c
    return distance
