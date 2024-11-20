import asyncio
import logging
import sys
from dotenv import load_dotenv
from os import getenv
import requests
# from prisma import Prisma
# from prisma.models import User, Post, Chat

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import commands, keyboard_buttons
from settings import my_commands

# prisma = Prisma(auto_register=True)
    

async def main() -> None:
    # await prisma.connect()
    load_dotenv()

    TOKEN = getenv("BOT_TOKEN")

    dp = Dispatcher()
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp.include_routers(commands.router, keyboard_buttons.router)

    await bot.set_my_commands(my_commands, types.BotCommandScopeDefault())
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
