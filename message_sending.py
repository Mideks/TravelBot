from typing import Optional

from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InputFile, InputMediaPhoto

from db.city_data import CityData
from markups import get_categories_markup, get_content_markup
from states.state_data import StateData
from utils.content import content_text_cutter


# todo: переработать: разные категории -- разный интерфейс
async def send_content(message: Message, city: str, content: CityData.Content, state_data: StateData):
    photo_path = content.photo
    if photo_path:
        length_limit = 1024
    else:
        length_limit = 2048

    pages = content_text_cutter(city, content, length_limit)
    text = pages[0]  # todo: реализовать переход по страницам

    if isinstance(content, CityData.Description):
        kb = get_categories_markup()
    else:
        kb = get_content_markup(many_content=True)

    # фотографии нет - отправляем просто текст
    if not photo_path:
        await send_helper(message, text, state_data, kb)
    else:
        photo = FSInputFile(photo_path)
        await send_helper(message, text, state_data, kb, photo)


async def send_helper(message: Message, send_text: str, state_data: StateData,
                      markup: Optional[InlineKeyboardMarkup] = None,
                      photo: Optional[InputFile] = None, send_as_new: Optional[bool] = False):
    new_message = None

    if photo:
        if send_as_new or not message.photo:
            new_message = await message.answer_photo(photo=photo, caption=send_text, reply_markup=markup)
        else:
            await message.edit_media(
                media=InputMediaPhoto(media=photo, caption=send_text), reply_markup=markup)
    else:
        if send_as_new or message.photo:
            new_message = await message.answer(send_text, reply_markup=markup)
        else:
            await message.edit_text(send_text, reply_markup=markup)

    if new_message:
        if state_data.bot_message:
            await state_data.bot_message.delete()
        state_data.bot_message = new_message
