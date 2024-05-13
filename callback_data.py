import enum

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
    category: Category
    is_locked = False
    is_premium = False


class City(CallbackData, prefix="city"):
    city_name: str = None
    is_random_city: bool = False


class NavigationLocation(enum.Enum):
    SelectCity = "SelectCity"
    ShowPremiumInfo = "ShowPremiumInfo"


class NavigationButton(CallbackData, prefix="navigation"):
    location: NavigationLocation
