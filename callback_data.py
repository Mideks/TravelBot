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


class LockableButton(CallbackData, prefix="lockable"):
    is_locked: Optional[bool] = True


class CategoryButton(LockableButton, prefix="category"):
    category: Optional[Category] = None
    content_index: Optional[int] = None
    is_premium: Optional[bool] = False


class CityButton(CallbackData, prefix="city"):
    city_name: Optional[str] = None
    is_random_city: Optional[bool] = False


class NavigationLocation(enum.Enum):
    Settings = "Settings"
    CityList = "CityList"
    PremiumInfo = "PremiumInfo"
    Start = "Start"
    Menu = "Menu"
    ContentList = "ContentList"

class NavigationButton(CallbackData, prefix="navigation"):
    location: NavigationLocation
