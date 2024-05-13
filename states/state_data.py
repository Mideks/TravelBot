from typing import Optional

from aiogram.types import Message
from pydantic import BaseModel

from callback_data import Category


class StateData(BaseModel):
    selected_category: Optional[Category] = None
    selected_city: Optional[str] = None
    bot_message: Optional[Message] = None
