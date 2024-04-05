from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import Category, City, SelectCity, ShowPremiumInfo


def get_categories_markup() -> InlineKeyboardMarkup:
    builder = \
        (InlineKeyboardBuilder()
         .button(text="История", callback_data=Category(category_name="history"))
         .button(text="💎 Легенды", callback_data=Category(category_name="legends", is_premium=True))

         .button(text="🎲 Достопримечательности", callback_data=Category(category_name="attractions"))
         .button(text="🎲 Интересные места", callback_data=Category(category_name="interesting_places"))

         .button(text="🎲 Памятники", callback_data=Category(category_name="monuments"))
         .button(text="⏳ Интересные факты", callback_data=Category(category_name="fun_facts", is_locked=True))

         .button(text="⏳ Местные праздники", callback_data=Category(category_name="holidays", is_locked=True))
         .button(text="💎 Песни", callback_data=Category(category_name="songs", is_premium=True))

         .button(text="💎 Погода", callback_data=Category(category_name="weather", is_premium=True))
         .button(text="💎 Климат", callback_data=Category(category_name="climate", is_premium=True))

         .button(text="⏳ Как добраться", callback_data=Category(category_name="way", is_locked=True))

         .adjust(2, 2, 2, 2, 2, 1))

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
