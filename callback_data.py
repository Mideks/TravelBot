import enum

from aiogram.filters.callback_data import CallbackData


class Category(CallbackData, prefix="category"):
    category_name: str
    is_premium: bool = False
    is_locked: bool = False


class City(CallbackData, prefix="city"):
    city_name: str = None
    is_random_city: bool = False


class NavigationLocation(enum.Enum):
    SelectCity = "SelectCity"
    ShowPremiumInfo = "ShowPremiumInfo"


class NavigationButton(CallbackData, prefix="navigation"):
    location: NavigationLocation
