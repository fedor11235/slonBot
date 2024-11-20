from aiogram import Router, F, types
from aiogram.filters import Command, CommandStart
from settings import my_keyboard_buttons, messages_no_profile, messages_help
from bot import bot

router = Router()

@router.message()
async def command_start_handler(message: types.Message) -> None:
    text = message.text
    if '@' in text:
        chat = await bot.get_chat(text)
        print("chat: ", chat)
        await message.answer("Это юзернейм")
    elif 'https' in text:
        username = '@' + text.split('/')[-1]
        chat = await bot.get_chat(username)
        print("chat: ", chat)
        await message.answer("Это ссылка")
    elif message.forward_origin != None:
        await message.answer("Это пересланное сообщение")
