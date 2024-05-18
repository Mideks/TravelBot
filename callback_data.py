import enum
from typing import Optional

from aiogram.filters.callback_data import CallbackData


class Category(enum.Enum):
    History = "history"
    Gallery = "gallery"
    InterestingFacts = "facts"
    PhotoPlaces = "photo_places"
    WeatherNow = "weather_now"
    Climate = "climate"
    Celebrities = "celebrities"
    LocalCuisine = "local_cuisine"
    Nature = "nature"
    Legends = "legends"
    InterestingPlaces = "interesting_places"
    LocalHolidays = "local_holidays"
    Monuments = "monuments"
    Attractions = "attractions"


class CategoryButton(CallbackData, prefix="category"):
    category: Optional[Category] = None
    is_locked: Optional[bool] = False
    is_premium: Optional[bool] = False


class CityButton(CallbackData, prefix="city"):
    city_name: Optional[str] = None
    is_random_city: Optional[bool] = False


class NavigationLocation(enum.Enum):
    SelectCity = "SelectCity"
    ShowPremiumInfo = "ShowPremiumInfo"
    Start = "Start"


class NavigationButton(CallbackData, prefix="navigation"):
    location: NavigationLocation
