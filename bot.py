import asyncio
import logging
import sys
from dotenv import load_dotenv
from os import getenv
import requests
from prisma import Prisma
from prisma.models import User, Post, Chat

from aiogram import Bot, Dispatcher, html, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, ChatMemberUpdatedFilter, JOIN_TRANSITION

load_dotenv()

TOKEN = getenv("BOT_TOKEN")


dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

prisma = Prisma(auto_register=True)

@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    await message.answer(f"Привет, {html.bold(full_name)}! Ваш id {html.bold(user_id)} скопируйте и вставьте его редактор, теперь добавь меня в ваши каналы для заполнение постов в виджет")

@dp.message(F.content_type == types.ContentType.TEXT)
async def echo_handler(message: types.Message) -> None:
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    await message.answer(f"Привет, {html.bold(full_name)}! Ваш id {html.bold(user_id)} скопируйте и вставьте его редактор, теперь добавь меня в ваши каналы для заполнение постов в виджет")

@dp.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def on_user_added(message: types.Message):
    chat_type = message.chat.type
    chat_id = message.chat.id
    user_id = message.from_user.id

    print("user_id: ", user_id)

    if chat_type == "private":
        user = await User.prisma().upsert(
            where={
                'tg_id': user_id,
            },
            data={
                'create': {
                    'tg_id': user_id,
                },
                'update': {},
            },
        )
    elif chat_type == "channel":
        await bot.send_message(user_id, f"Скопируйте айдишник канала {html.bold(chat_id)} и вставьте его в редакторе виджет")
        user = await Chat.prisma().upsert(
            where={
                'chat_id': chat_id,
            },
            data={
                'create': {
                    'chat_id': chat_id,
                    'admin': {
                        'connect': {
                            'id': user_id
                        }
                    }
                },
                'update': {},
            },
        )

@dp.channel_post()
async def echo_post_handler(message: types.Message) -> None:
    chanel_id = message.chat.id
    photo_id = None
    caption = ""
    text = ""

    post = await Post.prisma().create(
        data={
                "chat_id":chanel_id,
                "photo_id":photo_id,
                "caption":caption,
                "text":text
        }
    )
    print(post)
    

async def main() -> None:
    await prisma.connect()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

# await bot.send_message(channel_id, text)

# chat_id = message.chat.id
# url=f"https://api.telegram.org/bot{TOKEN}/getUpdates"

# response = requests.get(url)
# print(response.json())

# url=f"https://api.telegram.org/bot{TOKEN}/ChatFullInfo?chat_id_={chat_id}"

# response = requests.get(url)
# print(response.json())