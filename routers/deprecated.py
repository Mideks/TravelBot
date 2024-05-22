from __future__ import annotations

import random
from typing import Optional

from aiogram import Router, types, F

import db.data_loader
import markups
import texts.messages
from callback_data import CityButton, CategoryButton, NavigationButton, NavigationLocation, LockableButton
from db.city_data import CityData
from markups import get_show_premium_markup
from message_sending import send_content, send_helper
from states.state_data import StateData

router = Router()

cities = db.data_loader.load_all_cities('data/cities')


@router.callback_query(CityButton.filter())
async def city_callback_handler(callback_query: types.CallbackQuery,
                                callback_data: CityButton, state_data: StateData):
    if callback_data.is_random_city:
        city = random.choice(cities)
        city_name = city.city_name
        state_data.selected_city = city_name
    else:
        if callback_data.city_name:
            city_name = callback_data.city_name
            state_data.selected_city = city_name
        else:
            city_name = state_data.selected_city

        city = next((obj for obj in cities if obj.city_name == city_name), None)

    if not city:
        await callback_query.answer(texts.messages.city_selecting_error)

    await send_content(callback_query.message, city_name, city.description, state_data)
    await callback_query.answer()


@router.callback_query(CategoryButton.filter(F.is_premium))
async def premium_only_callback_handler(callback_query: types.CallbackQuery):
    # todo: добавить проверку на премиум у юзера
    await callback_query.message.edit_text(
        texts.messages.premium_funtionality, reply_markup=get_show_premium_markup())
    await callback_query.answer()


@router.callback_query(CategoryButton.filter(F.is_locked))
@router.callback_query(LockableButton.filter(F.is_locked))
async def locked_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.answer(texts.messages.not_implemented_functionality)


@router.callback_query(CategoryButton.filter())
async def category_callback_handler(
        callback_query: types.CallbackQuery, callback_data: CategoryButton, state_data: StateData):
    cat: Optional[str] = None
    if callback_data.category:
        cat = callback_data.category.value
        state_data.selected_category = callback_data.category
    elif state_data.selected_category:
        cat = state_data.selected_category.value

    if not cat:
        await callback_query.answer(texts.messages.content_category_error)
        raise ValueError('Category does not specified')

    # Вспоминаем какой город выбрали
    city_name = state_data.selected_city

    # Заглушка на случай, если кнопка нажата после перезапуска бота
    if not city_name:
        await callback_query.answer(texts.messages.city_selecting_error)
        return

    content = get_content_category(city_name, cat)
    if isinstance(content, list):
        if callback_data.content_index:
            content = content[callback_data.content_index]
        else:
            content = random.choice(content)

    await send_content(callback_query.message, city_name, content, state_data)
    await callback_query.answer()


def get_content_category(city_name: str, category: str) -> list[CityData.Content] | CityData.Content:
    city = next((obj for obj in cities if obj.city_name == city_name), None)
    content = city[category]
    return content


@router.callback_query(NavigationButton.filter(F.location == NavigationLocation.ContentList))
async def send_content_list_handler(
        callback_query: types.CallbackQuery, state_data: StateData):
    category = state_data.selected_category
    city_name = state_data.selected_city
    if not category:
        await callback_query.answer(texts.messages.content_category_error)
        return
    elif not city_name:
        await callback_query.answer(texts.messages.city_selecting_error)
        return

    contents = get_content_category(city_name, category.value)
    await send_helper(callback_query.message, texts.messages.send_content_list, state_data,
                      markups.get_content_list_markup(contents))
