import random
import os
import asyncio
import logging
import sys

from aiogram.fsm.context import FSMContext
from pysondb import db

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram.types import Message, FSInputFile

from callback_data import Category, City, SelectCity, ShowPremiumInfo
from markups import (get_categories_markup, get_premium_markup, get_show_premium_markup,
                     get_cities_markup, get_greeting_markup)
import texts.messages

TOKEN = os.getenv("BOT_TOKEN")

cities_db = db.getDb("data/template.json")

dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    text = texts.messages.start
    await message.answer(text, reply_markup=get_greeting_markup())


# todo: не тут это должно быть (а может и тут...)
@dp.callback_query(SelectCity.filter())
async def city_select_callback_handler(callback_query: types.CallbackQuery, callback_data: ShowPremiumInfo):
    await send_select_city_message(callback_query.message)
    await callback_query.answer()


@dp.message(Command("city"))
async def city_select_command_handler(message: types.Message):
    await send_select_city_message(message)


async def send_select_city_message(message: types.Message):
    text = texts.messages.selecting_city
    cities = [city.get("city_name") for city in cities_db.getAll()]
    await message.answer(text, reply_markup=get_cities_markup(cities))


# todo: подписки по сути нет
@dp.callback_query(ShowPremiumInfo.filter())
async def show_premium_callback_handler(callback_query: types.CallbackQuery, callback_data: ShowPremiumInfo):
    await send_show_premium_message(callback_query.message)
    await callback_query.answer()


@dp.message(Command("premium"))
async def premium_command_handler(message: types.Message):
    await send_show_premium_message(message)


async def send_show_premium_message(message: types.Message):
    text = (texts.messages.premium_info)
    await message.answer(text, reply_markup=get_premium_markup())


async def send_content(chat_id: int, content: dict, city: str):
    text = (f"{city} - {content.get('title', '')}\n\n"
            f"{content.get('text')}")

    # текст не поместится в одно сообщение
    if len(text) > 2048:
        # todo: разделение текста на несколько частей? кнопки?
        text = texts.messages.long_text_error
        await bot.send_message(chat_id, text)
        return

    photo_path = content.get("photo")
    # фотографии нет - отправляем просто текст
    if not photo_path:
        await bot.send_message(chat_id, text, reply_markup=get_categories_markup())
        return

    if not os.path.exists(photo_path):
        await bot.send_message(chat_id, texts.messages.photo_not_exists_error)
        print(f"photo_path = {photo_path} не существует")
        return

    photo = FSInputFile(photo_path)

    # текст не влезает в подпись - отправим отдельно
    if len(text) > 1024:
        await bot.send_message(chat_id, text, reply_markup=get_categories_markup())
        await bot.send_photo(chat_id=chat_id, photo=photo, caption=text)
    else:
        await bot.send_photo(chat_id=chat_id, photo=photo, caption=text, reply_markup=get_categories_markup())

@dp.callback_query(City.filter())
async def city_callback_handler(callback_query: types.CallbackQuery,
                                callback_data: City, state: FSMContext):
    # Извлекаем данные из callback_query
    city_name = callback_data.city_name

    if callback_data.is_random_city:
        city_names = [city.get("city_name") for city in cities_db.getAll()]
        city_name = random.choice(city_names)

    city = cities_db.getByQuery({"city_name": city_name})[0]

    # Запоминаем выбранный город,
    await state.update_data(selected_city=city_name)

    await send_content(callback_query.from_user.id, city["description"], city_name)
    await callback_query.answer()


@dp.callback_query(Category.filter())
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
    else:
        city = cities_db.getByQuery({"city_name": city_name})[0]
        content = city[category]
        if isinstance(city[category], list):
            content = random.choice(content)

        await send_content(callback_query.from_user.id, content, city_name)

    await callback_query.answer()


async def main() -> None:
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
