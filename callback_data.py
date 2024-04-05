from aiogram.filters.callback_data import CallbackData


class Category(CallbackData, prefix="category"):
    category_name: str
    is_premium: bool = False
    is_locked: bool = False


class City(CallbackData, prefix="city"):
    city_name: str = None
    is_random_city: bool = False


class SelectCity(CallbackData, prefix="select_city"):
    pass


class ShowPremiumInfo(CallbackData, prefix="show_premium_info"):
    pass
