import json
import os

from city_data import *


def load_city(city_path: str, city_file_name: str = 'city_data.json') -> CityData:
    # Construct the full path to the city file
    city_file_path = f"{city_path}/{city_file_name}"

    with open(city_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    city_data = CityData(
        city_path,
        data['city_name'],
        CityData.Content(city_path, **data['description']),
        CityData.Location(**data['location']),
        CityData.Content(city_path, **data['history']),
        [CityData.Fact(city_path, **fact) for fact in data['facts']],
        CityData.Content(city_path, **data['climate']),
        [CityData.PhotoPlace(city_path, **photo_place) for photo_place in data['photo_places']],
        [CityData.Celebrity(city_path, **celebrity) for celebrity in data['celebrities']],
        [CityData.LocalCuisine(city_path, **local_cuisine) for local_cuisine in data['local_cuisine']],
        [CityData.Nature(city_path, **nature) for nature in data['nature']],
        [CityData.Legend(city_path, **legend) for legend in data['legends']],
        [CityData.LocalHoliday(city_path, **local_holiday) for local_holiday in data['local_holidays']],
        [CityData.InterestingPlace(city_path, **interesting_place) for interesting_place in data['interesting_places']]
    )

    return city_data


def load_all_cities(parent_folder_path: str) -> list:
    loaded_cities = []

    items_in_parent_folder = os.listdir(parent_folder_path)

    for city_folder in items_in_parent_folder:
        city_path = os.path.join(parent_folder_path, city_folder)
        city_data = load_city(city_path)
        loaded_cities.append(city_data)

    return loaded_cities
