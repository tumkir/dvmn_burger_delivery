import requests
from environs import Env
from geopy import distance

from .models import Place

env = Env()
env.read_env()
API_KEY = env.str('YANDEX_API_KEY')


def save_coordinates_to_db(address, latitude, longitude):
    Place.objects.get_or_create(
        address=address,
        latitude=latitude,
        longitude=longitude,
    )


def geocoding(address, apikey=API_KEY):
    '''
    Geocoder response structure:
    https://yandex.ru/dev/maps/geocoder/doc/desc/reference/response_structure.html#response_structure__json_response
    '''

    base_url = 'https://geocode-maps.yandex.ru/1.x'
    params = {'geocode': address, 'apikey': apikey, 'format': 'json'}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        response_data = response.json()['response']['GeoObjectCollection']
    except requests.exceptions.RequestException:
        return

    if response_data['metaDataProperty']['GeocoderResponseMetaData']['found'] == '0':
        return

    places_found = response_data['featureMember']
    most_relevant = places_found[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(' ')

    save_coordinates_to_db(address, lat, lon)

    return lat, lon


def get_coordinates(address):
    try:
        place = Place.objects.get(address=address)
        return (place.latitude, place.longitude)
    except Place.DoesNotExist:
        return geocoding(address)


def calculate_distance(restaurant_address, client_address):
    restaurant_coordinates = get_coordinates(restaurant_address)
    if not restaurant_coordinates:
        return

    client_coordinates = get_coordinates(client_address)
    if not client_coordinates:
        return

    return round(distance.distance(restaurant_coordinates, client_coordinates).km, 2)
