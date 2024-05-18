import random

from aiogram import Router, types, F

import db.data_loader
import texts.messages
from callback_data import CityButton, CategoryButton
from markups import get_show_premium_markup
from message_sending import send_content
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

    await send_content(callback_query.message, city_name, city.description)
    await callback_query.answer()


@router.callback_query(CategoryButton.filter(F.is_premium))
async def premium_only_callback_handler(callback_query: types.CallbackQuery):
    # todo: добавить проверку на премиум у юзера
    await callback_query.message.edit_text(
        texts.messages.premium_funtionality, reply_markup=get_show_premium_markup())
    await callback_query.answer()


@router.callback_query(CategoryButton.filter(F.is_locked))
async def locked_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.answer(texts.messages.not_implemented_functionality)


@router.callback_query(CategoryButton.filter())
async def category_callback_handler(
        callback_query: types.CallbackQuery, callback_data: CategoryButton, state_data: StateData):
    category = None
    if callback_data.category:
        category = callback_data.category.value
        state_data.selected_category = callback_data.category
    elif state_data.selected_category:
        category = state_data.selected_category.value

    if not category:
        raise ValueError('Category does not specified')

    # Вспоминаем какой город выбрали
    city_name = state_data.selected_city

    # Заглушка на случай, если кнопка нажата после перезапуска бота
    if not city_name:
        await callback_query.answer(texts.messages.city_selecting_error)
        return

    city = next((obj for obj in cities if obj.city_name == city_name), None)
    content = city[category]
    if isinstance(content, list):
        content = random.choice(content)

    await send_content(callback_query.message, city_name, content)
    await callback_query.answer()
