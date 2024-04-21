import json

from city_data import *


def load_city(path: str) -> CityData:
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    city_data = CityData(
        city_name=data['city_name'],
        description=Content(**data['description']),
        location=Location(**data['location']),
        history=Content(**data['history']),
        facts=[Fact(**fact) for fact in data['facts']],
        climate=Content(**data['climate']),
        photo_places=[PhotoPlace(**photo_place) for photo_place in data['photo_places']],
        celebrities=[Celebrity(**celebrity) for celebrity in data['celebrities']],
        local_cuisine=[LocalCuisine(**local_cuisine) for local_cuisine in data['local_cuisine']],
        nature=[Nature(**nature) for nature in data['nature']],
        legends=[Legend(**legend) for legend in data['legends']],
        local_holidays=[LocalHoliday(**local_holiday) for local_holiday in data['local_holidays']],
        interesting_places=[InterestingPlace(**interesting_place) for interesting_place in data['interesting_places']]
    )

    return city_data

