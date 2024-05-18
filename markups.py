from typing import Optional

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

import texts
from callback_data import CategoryButton, CityButton, NavigationButton, NavigationLocation, Category, LockableButton
from db.city_data import CityData


def get_categories_markup() -> InlineKeyboardMarkup:
    builder = \
        (InlineKeyboardBuilder()
         .button(text="История",
                 callback_data=CategoryButton(category=Category.History))
         .button(text="🔐 Галерея",
                 callback_data=CategoryButton(category=Category.Gallery, is_locked=True))

         .button(text="🎲 Интересные факты",
                 callback_data=CategoryButton(category=Category.InterestingFacts))
         .button(text="🎲 Места для фото",
                 callback_data=CategoryButton(category=Category.PhotoPlaces))

         .button(text="🔐 Погода сейчас",
                 callback_data=CategoryButton(category=Category.WeatherNow, is_locked=True))
         .button(text="💎 Климат",
                 callback_data=CategoryButton(category=Category.Climate, is_locked=False, is_premium=True))

         .button(text="🎲 Знаменитости",
                 callback_data=CategoryButton(category=Category.Celebrities, is_locked=False))
         .button(text="🎲 Местная кухня",
                 callback_data=CategoryButton(category=Category.LocalCuisine, is_locked=False))

         .button(text="Флора и фауна",
                 callback_data=CategoryButton(category=Category.Nature, is_locked=False))
         .button(text="🎲 Легенды",
                 callback_data=CategoryButton(category=Category.Legends, is_locked=False))

         .button(text="🎲 Интересные места",
                 callback_data=CategoryButton(category=Category.InterestingPlaces, is_locked=False))
         .button(text="🎲 Местные праздники",
                 callback_data=CategoryButton(category=Category.LocalHolidays, is_locked=False))

         .button(text="🔐 Памятники",
                 callback_data=CategoryButton(category=Category.Monuments, is_locked=True))
         .button(text="🔐 Достопримечательности",
                 callback_data=CategoryButton(category=Category.Attractions, is_locked=True))

         .button(text=texts.buttons.back_to_menu,
                 callback_data=NavigationButton(location=NavigationLocation.Menu))

         .adjust(2))

    return builder.as_markup()


def get_content_markup(
        navigation: Optional[bool] = False, link: Optional[str] = None,
        many_content: Optional[bool] = False) -> InlineKeyboardMarkup:
    menu = InlineKeyboardBuilder()
    adjust = []
    if navigation:
        navigate = InlineKeyboardBuilder()
        navigate.button(text="◀️", callback_data="todo")
        navigate.button(text="▶️", callback_data="todo")
        menu.attach(navigate)
        adjust.append(2)

    if link:
        menu.button(text="Подробнее", url=link)

    if many_content:
        other_content = InlineKeyboardBuilder()
        other_content.button(text="🎲 Показать другое", callback_data=CategoryButton())
        other_content.button(text="📋 Показать списком", callback_data="todo")
        menu.attach(other_content)

    menu.button(text=texts.buttons.back_to_city, callback_data=CityButton())

    menu.adjust(*adjust, 1)
    return menu.as_markup()


def get_content_list_markup(contents: list[CityData.Content],
                            navigation: Optional[bool] = False) -> InlineKeyboardMarkup:
    menu = InlineKeyboardBuilder()
    adjust = []
    if navigation:
        navigate = InlineKeyboardBuilder()
        navigate.button(text="◀️", callback_data="todo")
        navigate.button(text="▶️", callback_data="todo")
        menu.attach(navigate)
        adjust.append(2)

    for content in contents:
        menu.button(text=content.title, callback_data="todo")

    menu.button(text=texts.buttons.back_to_city, callback_data=CityButton())

    menu.adjust(*adjust, 1)
    return menu.as_markup()


def get_premium_markup(back: NavigationLocation) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Купить", url="https://t.me/TripTellerBot")
    builder.button(text=texts.buttons.back, callback_data=NavigationButton(location=back))

    builder.adjust(1)
    return builder.as_markup()


def get_greeting_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=texts.buttons.start_joinery,
                   callback_data=NavigationButton(location=NavigationLocation.Menu))

    return builder.as_markup()


def get_menu_markup() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.button(text=texts.buttons.city_list, callback_data=NavigationButton(location=NavigationLocation.CityList))
    kb.button(text=texts.buttons.random_city, callback_data=CityButton(is_random_city=True))
    kb.button(text=texts.buttons.my_gallery, callback_data=LockableButton(is_locked=True))
    kb.button(text=texts.buttons.premium, callback_data=NavigationButton(location=NavigationLocation.PremiumInfo))
    kb.button(text=texts.buttons.settings, callback_data=NavigationButton(location=NavigationLocation.Settings))

    kb.adjust(2, 1)
    return kb.as_markup()


def get_show_premium_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=texts.buttons.premium_more_info,
                   callback_data=NavigationButton(location=NavigationLocation.PremiumInfo))
    builder.button(text=texts.buttons.back_to_city, callback_data=CityButton())

    return builder.as_markup()


def get_cities_markup(cities: list[CityData]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    # todo: Возможно, не лучшая идея, если городов было бы много
    # Создаём по кнопке на каждый город
    builder.button(text=texts.buttons.random_city, callback_data=CityButton(is_random_city=True))
    for city in cities:
        builder.button(text=city.city_name, callback_data=CityButton(city_name=city.city_name))
    builder.adjust(1, 2)

    return builder.as_markup()
