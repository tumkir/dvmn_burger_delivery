import requests
from environs import Env
from geopy import distance


def fetch_coordinates(apikey, place):
    base_url = 'https://geocode-maps.yandex.ru/1.x'
    params = {'geocode': place, 'apikey': apikey, 'format': 'json'}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    places_found = response.json()['response']['GeoObjectCollection']['featureMember']
    most_relevant = places_found[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(' ')
    return lon, lat


def calculate_distance(restaurant_address, client_address):
    env = Env()
    env.read_env()
    apikey = env.str('YANDEX_API_KEY')

    restaurant_coordinates = fetch_coordinates(apikey, restaurant_address)
    client_coordinates = fetch_coordinates(apikey, client_address)

    return round(distance.distance(restaurant_coordinates, client_coordinates).km, 3)
