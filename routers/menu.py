from aiogram import Router, F
from aiogram.types import CallbackQuery

import markups
import texts
from callback_data import NavigationButton, NavigationLocation
from message_sending import send_helper

router = Router()


@router.callback_query(NavigationButton.filter(F.location == NavigationLocation.Menu))
async def start_callback(callback_query: CallbackQuery):
    await send_helper(callback_query.message, texts.messages.menu, markups.get_menu_markup())
    await callback_query.answer()
