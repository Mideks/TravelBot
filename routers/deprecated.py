import os
import random

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message

import db.data_loader
import texts.messages
from callback_data import SelectCity, ShowPremiumInfo, City, Category
from db.city_data import CityData
from markups import get_premium_markup, get_cities_markup, get_categories_markup, \
    get_show_premium_markup

router = Router()

cities = db.data_loader.load_all_cities('data/cities')


@router.callback_query(SelectCity.filter())
async def city_select_callback_handler(callback_query: types.CallbackQuery):
    await send_select_city_message(callback_query.message)
    await callback_query.answer()


@router.message(Command("city"))
async def city_select_command_handler(message: types.Message):
    await send_select_city_message(message)


async def send_select_city_message(message: types.Message):
    text = texts.messages.selecting_city
    city_names = [city.city_name for city in cities]

    await message.answer(text, reply_markup=get_cities_markup(city_names))


@router.callback_query(ShowPremiumInfo.filter())
async def show_premium_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.message.answer(texts.messages.premium_info, reply_markup=get_premium_markup())
    await callback_query.answer()


async def send_content(message: Message, content: CityData.Content, city: str):
    text = (f"{city} - {content.title}\n\n"
            f"{content.text}")

    # текст не поместится в одно сообщение
    if len(text) > 2048:
        # todo: разделение текста на несколько частей? кнопки?
        text = texts.messages.long_text_error
        await message.answer(text)
        return

    photo_path = content.photo
    # фотографии нет - отправляем просто текст
    if not photo_path:
        await message.answer(text, reply_markup=get_categories_markup())
        return

    if not os.path.exists(photo_path):
        await message.answer(texts.messages.photo_not_exists_error)
        print(f"photo_path = {photo_path} не существует")
        return

    photo = FSInputFile(photo_path)

    # текст не влезает в подпись - отправим отдельно
    if len(text) > 1024:
        await message.answer(text, reply_markup=get_categories_markup())
        await message.answer_photo(photo=photo, caption=text)
    else:
        await message.answer_photo(photo=photo, caption=text, reply_markup=get_categories_markup())


@router.callback_query(City.filter())
async def city_callback_handler(callback_query: types.CallbackQuery,
                                callback_data: City, state: FSMContext):
    # Извлекаем данные из callback_query

    if callback_data.is_random_city:
        city = random.choice(cities)
        city_name = city.city_name
    else:
        city_name = callback_data.city_name
        city = next((obj for obj in cities if obj.city_name == city_name), None)

    # Запоминаем выбранный город,
    await state.update_data(selected_city=city_name)

    await send_content(callback_query.message, city.description, city_name)
    await callback_query.answer()


@router.callback_query(Category.filter())
async def category_callback_handler(
        callback_query: types.CallbackQuery, callback_data: Category, state: FSMContext):
    # Извлекаем данные из callback_query
    category = callback_data.category_name

    # todo: добавить проверку на премиум у юзера
    if callback_data.is_premium:
        text = texts.messages.premium_funtionality
        await callback_query.message.answer(text, reply_markup=get_show_premium_markup())
        await callback_query.answer()
        return

    elif callback_data.is_locked:
        text = texts.messages.not_implemented_functionality
        await callback_query.message.answer(text)
        await callback_query.answer()
        return

    # Вспоминаем какой город выбрали
    data = await state.get_data()
    city_name = data["selected_city"]

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

    await send_content(callback_query.message, content, city_name)

    await callback_query.answer()
