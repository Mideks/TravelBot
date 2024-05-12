import json
from os import path
from typing import List, Optional


class CityData(dict):
    class Location:
        def __init__(self, latitude: float, longitude: float):
            self.latitude = latitude
            self.longitude = longitude

    class Content:
        def __init__(self, city_path: str, title: Optional[str] = None, text: Optional[str] = None, photo: Optional[str] = None):
            self.title = title
            self.text = text
            self._photo = photo # Store the relative path
            self._city_path = city_path # Store the city path for use in photo property

        @property
        def photo(self):
            if self._photo:
                return path.join(self._city_path, self._photo)
            return None

        @photo.setter
        def photo(self, value):
            self._photo = value

    class Fact(Content):
        pass

    class PhotoPlace(Content):
        def __init__(self, city_path: str, title: str, text: str, photo: str, location: "CityData.Location"):

            super().__init__(city_path, title, text, photo)
            self.location = location

    class Celebrity(Content):
        def __init__(self, city_path: str, title: str, text: str, photo: str, link: str):
            super().__init__(city_path, title, text, photo)
            self.link = link

    class LocalCuisine(Content):
        pass

    class Nature(Content):
        pass

    class Legend(Content):
        pass

    class LocalHoliday(Content):
        pass

    class InterestingPlace(Content):
        def __init__(self, city_path: str, title: str, text: str, photo: str, location: "CityData.Location", link: str):
            super().__init__(city_path, title, text, photo)
            self.location = location
            self.link = link

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, city_path: str, city_name: str, description: Content, location: Location, history: Content, facts: List[Fact],
                 climate: Content, photo_places: List[PhotoPlace], celebrities: List[Celebrity],
                 local_cuisine: List[LocalCuisine], nature: List[Nature], legends: List[Legend],
                 local_holidays: List[LocalHoliday], interesting_places: List[InterestingPlace]):
        self._city_path = city_path # Store the city path for use in Content subclasse
        self.city_name = city_name
        self.description = description
        self.location = location
        self.history = history
        self.facts = facts
        self.climate = climate
        self.photo_places = photo_places
        self.celebrities = celebrities
        self.local_cuisine = local_cuisine
        self.nature = nature
        self.legends = legends
        self.local_holidays = local_holidays
        self.interesting_places = interesting_places
