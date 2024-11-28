import asyncio
import logging
import sys
from dotenv import load_dotenv
from os import getenv
import requests
from prisma import Prisma

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import (
    commands,
    keyboard_buttons,
    chat,
    callback_common,
    callback_opt,
    callback_into_opt
)

from settings import my_commands

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

async def main() -> None:
    prisma = Prisma(auto_register=True)
    await prisma.connect()

    dp = Dispatcher()
    dp.include_routers(
        commands.router,
        keyboard_buttons.router,
        chat.router,
        callback_common.router,
        callback_opt.router,
        callback_into_opt.router
    )

    await bot.set_my_commands(my_commands, types.BotCommandScopeDefault())
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
