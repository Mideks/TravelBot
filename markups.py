from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import Category, City, SelectCity, ShowPremiumInfo


def get_categories_markup() -> InlineKeyboardMarkup:
    builder = \
        (InlineKeyboardBuilder()
         .button(text="История", callback_data=Category(category_name="history"))
         .button(text="🔐 Галерея", callback_data=Category(category_name="", is_locked=True))

         .button(text="🎲 Интересные факты", callback_data=Category(category_name="facts"))
         .button(text="🎲 Места для фото", callback_data=Category(category_name="photo_places"))

         .button(text="🔐 Погода сейчас", callback_data=Category(category_name="", is_locked=True))
         .button(text="Климат", callback_data=Category(category_name="climate", is_locked=False))

         .button(text="🎲 Знаменитости", callback_data=Category(category_name="celebrities", is_locked=False))
         .button(text="🎲 Местная кухня", callback_data=Category(category_name="local_cuisine", is_locked=False))

         .button(text="Флора и фауна", callback_data=Category(category_name="nature", is_locked=False))
         .button(text="🎲 Легенды", callback_data=Category(category_name="legends", is_locked=False))

         .button(text="🎲 Интересные места", callback_data=Category(category_name="interesting_places", is_locked=False))
         .button(text="🎲 Местные праздники", callback_data=Category(category_name="local_holidays", is_locked=False))

         .button(text="🎲 Памятники", callback_data=Category(category_name="monuments", is_locked=False))
         .button(text="🎲 Достопримечательности", callback_data=Category(category_name="attractions", is_locked=False))

         .adjust(2))

    return builder.as_markup()


def get_premium_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Купить", url="https://t.me/TripTellerBot")

    return builder.as_markup()


def get_greeting_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Поехали!", callback_data=SelectCity())

    return builder.as_markup()


def get_show_premium_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="💎 Узнать подробности!", callback_data=ShowPremiumInfo())

    return builder.as_markup()


def get_cities_markup(cities: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    # todo: Возможно, не лучшая идея, если городов было бы много
    # Создаём по кнопке на каждый город
    builder.button(text="🎲 Случайный", callback_data=City(city_name="meow", is_random_city=True))
    for city in cities:
        builder.button(text=city, callback_data=City(city_name=city))
    builder.adjust(1, 2)

    return builder.as_markup()
