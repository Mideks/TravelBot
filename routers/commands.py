from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import markups
import texts.messages
from callback_data import NavigationButton, NavigationLocation
from markups import get_greeting_markup, get_premium_markup, get_cities_markup
from message_sending import send_helper
from routers.deprecated import cities

router = Router()


@router.callback_query(NavigationButton.filter(F.location == NavigationLocation.Start))
async def start_callback(callback_query: types.CallbackQuery):
    await send_helper(callback_query.message, texts.messages.start, get_greeting_markup(), send_as_new=False)
    await callback_query.answer()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await send_helper(message, texts.messages.start, get_greeting_markup(), send_as_new=True)


@router.callback_query(NavigationButton.filter(F.location == NavigationLocation.PremiumInfo))
async def show_premium_callback(callback_query: types.CallbackQuery):
    back = NavigationLocation.Menu
    await send_helper(callback_query.message, texts.messages.premium_info, get_premium_markup(back))
    await callback_query.answer()


@router.message(Command("premium"))
async def premium_command_handler(message: types.Message):
    back = NavigationLocation.Menu
    await send_helper(message, texts.messages.premium_info, get_premium_markup(back), send_as_new=True)


@router.callback_query(NavigationButton.filter(F.location == NavigationLocation.CityList))
async def city_select_callback(callback_query: types.CallbackQuery):
    await send_helper(callback_query.message, texts.messages.selecting_city, get_cities_markup(cities))
    await callback_query.answer()


@router.message(Command("city"))
async def city_select_command_handler(message: types.Message):
    await send_helper(message, texts.messages.selecting_city, get_cities_markup(cities), send_as_new=True)


@router.callback_query(NavigationButton.filter(F.location == NavigationLocation.Settings))
async def settings_callback(callback_query: types.CallbackQuery):
    await send_helper(callback_query.message, texts.messages.settings, markups.get_settings_markup().as_markup())
    await callback_query.answer()


@router.message(Command("settings"))
async def settings_command_handler(message: types.Message):
    await send_helper(message, texts.messages.settings, markups.get_settings_markup().as_markup(), send_as_new=True)


@router.callback_query(NavigationButton.filter(F.location == NavigationLocation.Menu))
async def menu_callback(callback_query: types.CallbackQuery):
    await send_helper(callback_query.message, texts.messages.menu, markups.get_menu_markup())
    await callback_query.answer()


@router.message(Command("menu"))
async def menu_command_handler(message: types.Message):
    await send_helper(message, texts.messages.menu, markups.get_menu_markup())
