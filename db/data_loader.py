import json
import os

from db.city_data import *


def load_city(city_path: str, city_file_name: str = 'city_data.json') -> CityData:
    # Construct the full path to the city file
    city_file_path = path.join(city_path, city_file_name)

    with open(city_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    city_data = CityData(
        city_path,
        data['city_name'],
        CityData.Description(city_path, **data['description']),
        CityData.Location(**data['location']),
        CityData.History(city_path, **data['history']),
        [CityData.Fact(city_path, **fact) for fact in data['facts']],
        CityData.Climate(city_path, **data['climate']),
        [CityData.PhotoPlace(city_path, **photo_place) for photo_place in data['photo_places']],
        [CityData.Celebrity(city_path, **celebrity) for celebrity in data['celebrities']],
        [CityData.LocalCuisine(city_path, **local_cuisine) for local_cuisine in data['local_cuisine']],
        [CityData.Nature(city_path, **nature) for nature in data['nature']],
        [CityData.Legend(city_path, **legend) for legend in data['legends']],
        [CityData.LocalHoliday(city_path, **local_holiday) for local_holiday in data['local_holidays']],
        [CityData.InterestingPlace(city_path, **interesting_place) for interesting_place in data['interesting_places']]
    )

    return city_data


def load_all_cities(parent_folder_path: str) -> list[CityData]:
    loaded_cities = []

    items_in_parent_folder = os.listdir(parent_folder_path)

    for city_folder in items_in_parent_folder:
        city_path = os.path.join(parent_folder_path, city_folder)
        city_data = load_city(city_path)
        check_photos_exists(city_data)
        loaded_cities.append(city_data)

    return loaded_cities


def check_photos_exists(city_data: CityData):
    for data in city_data.values():
        contents = []
        if isinstance(data, CityData.Content):
            contents = [data]
        elif isinstance(data, list) and len(data) != 0 and isinstance(data[0], CityData.Content):
            contents = data

        for content in contents:
            photo_path = content.photo
            if photo_path and not os.path.exists(photo_path):
                print(f"photo_path = {photo_path} не существует")

