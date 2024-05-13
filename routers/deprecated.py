import random

from aiogram import Router, types, F
from aiogram.types import FSInputFile, Message

import db.data_loader
import texts.messages
from callback_data import City, Category, NavigationButton, NavigationLocation
from db.city_data import CityData
from markups import get_premium_markup, get_cities_markup, get_categories_markup, \
    get_show_premium_markup, get_content_markup
from states.state_data import StateData
from utils.content import content_text_cutter

router = Router()

cities = db.data_loader.load_all_cities('data/cities')


@router.callback_query(NavigationButton.filter(F.location == NavigationLocation.SelectCity))
async def city_select_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        texts.messages.selecting_city, reply_markup=get_cities_markup(cities))
    await callback_query.answer()


@router.callback_query(NavigationButton.filter(F.location == NavigationLocation.ShowPremiumInfo))
async def show_premium_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.message.answer(texts.messages.premium_info, reply_markup=get_premium_markup())
    await callback_query.answer()


# todo: переработать: разные категории -- разный интерфейс
async def send_content(message: Message, city: str, content: CityData.Content):
    photo_path = content.photo
    if photo_path:
        length_limit = 1024
    else:
        length_limit = 2048

    pages = content_text_cutter(city, content, length_limit)
    text = pages[0] # todo: реализовать переход по страницам

    if isinstance(content, CityData.Description):
        kb = get_categories_markup()
    else:
        kb = get_content_markup()

    # фотографии нет - отправляем просто текст
    if not photo_path:
        await message.answer(text, reply_markup=kb)
    else:
        photo = FSInputFile(photo_path)
        await message.answer_photo(photo=photo, caption=text, reply_markup=kb)


@router.callback_query(City.filter())
async def city_callback_handler(callback_query: types.CallbackQuery,
                                callback_data: City, state_data: StateData):
    if callback_data.is_random_city:
        city = random.choice(cities)
        city_name = city.city_name
    else:
        city_name = callback_data.city_name
        city = next((obj for obj in cities if obj.city_name == city_name), None)

    # Запоминаем выбранный город,
    state_data.selected_city = city_name
    await send_content(callback_query.message, city_name, city.description)
    await callback_query.answer()


@router.callback_query(Category.filter(F.is_premium))
async def premium_only_callback_handler(callback_query: types.CallbackQuery):
    # todo: добавить проверку на премиум у юзера
    text = texts.messages.premium_funtionality
    await callback_query.message.answer(text, reply_markup=get_show_premium_markup())
    await callback_query.answer()


@router.callback_query(Category.filter(F.is_locked))
async def locked_callback_handler(callback_query: types.CallbackQuery):
    text = texts.messages.not_implemented_functionality
    await callback_query.message.answer(text)
    await callback_query.answer()


@router.callback_query(Category.filter())
async def category_callback_handler(
        callback_query: types.CallbackQuery, callback_data: Category, state_data: StateData):
    # Извлекаем данные из callback_query
    category = callback_data.category_name

    # Вспоминаем какой город выбрали
    city_name = state_data.selected_city

    # Заглушка на случай, если кнопка нажата после перезапуска бота
    if not city_name:
        text = texts.messages.city_selecting_error
        await callback_query.message.answer(text)
        await callback_query.answer()
        return

    city = next((obj for obj in cities if obj.city_name == city_name), None)
    content = city[category]
    if isinstance(content, list):
        content = random.choice(content)

    await send_content(callback_query.message, city_name, content)

    await callback_query.answer()
