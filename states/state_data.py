from typing import Optional

from aiogram.types import Message


class StateData:
    selected_city: Optional[str] = None
    bot_message: Message
