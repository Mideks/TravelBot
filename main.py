import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import routers
from middlewares.state_data_provider import StateDataProvider

TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main() -> None:
    dp.update.middleware(StateDataProvider())
    dp.include_router(routers.commands.router)
    dp.include_router(routers.menu.router)
    dp.include_router(routers.deprecated.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
