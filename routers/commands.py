from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import texts.messages
from main_old import dp
from markups import get_greeting_markup, get_premium_markup

router = Router()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    text = texts.messages.start
    await message.answer(text, reply_markup=get_greeting_markup())


@dp.message(Command("premium"))
async def premium_command_handler(message: types.Message):
    await message.answer(texts.messages.premium_info, reply_markup=get_premium_markup())
