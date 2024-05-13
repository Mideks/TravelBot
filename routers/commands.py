from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import texts.messages
from markups import get_greeting_markup, get_premium_markup, get_cities_markup
from routers.deprecated import cities

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    text = texts.messages.start
    await message.answer(text, reply_markup=get_greeting_markup())


@router.message(Command("premium"))
async def premium_command_handler(message: types.Message):
    await message.answer(texts.messages.premium_info, reply_markup=get_premium_markup())


@router.message(Command("city"))
async def city_select_command_handler(message: types.Message):
    await message.answer(texts.messages.selecting_city, reply_markup=get_cities_markup(cities))
