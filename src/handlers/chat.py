from aiogram import Router, F, types
from aiogram.filters import Command, CommandStart

from settings import my_keyboard_buttons, messages_no_profile, messages_help

# from dotenv import load_dotenv

from prisma.models import User, Channel
from helpers.user import getActiveUser

from bot import bot

# load_dotenv()

router = Router()

@router.message()
async def command_message_handler(message: types.Message) -> None:
    user_id = message.chat.id

    is_user_active = await getActiveUser(user_id)

    if is_user_active == False:
        text = message.text
        if text != None and '@' in text[0]:
            try:
                chat = await bot.get_chat(text)
                bot_status = await bot.get_chat_member(chat_id=chat.id, user_id=bot.id)
                user_сhannel = await Channel.prisma().create(
                    data = {
                        'channel_id': chat.id,
                        'username': chat.username,
                        'title': chat.title,
                        'admin': {
                            'connect': {
                                'tg_id': user_id
                            }
                        }
                    },
                )
                user_update = await User.prisma().update(
                    where={
                        'tg_id': user_id,
                    },
                    data={
                        'is_active': True,
                    },
                )
            except:
                await message.answer("Вы ввели некорректные данные")

        elif text != None and 'https' in text:
            username = '@' + text.split('/')[-1]
            try:
                chat = await bot.get_chat(username)
                bot_status = await bot.get_chat_member(chat_id=chat.id, user_id=bot.id)
                user_сhannel = await Channel.prisma().create(
                    data = {
                        'channel_id': chat.id,
                        'username': chat.username,
                        'title': chat.title,
                        'admin': {
                            'connect': {
                                'tg_id': user_id
                            }
                        }
                    },
                )
                user_update = await User.prisma().update(
                    where={
                        'tg_id': user_id,
                    },
                    data={
                        'is_active': True,
                    },
                )
            except:
                await message.answer("Вы ввели некорректные данные")

        elif message.forward_origin != None:
            try:
                await message.answer("Это пересланное сообщение")
                print(message.forward_origin.chat.title)
                chat_id = message.forward_origin.chat.id
                username = message.forward_origin.chat.username
                title = message.forward_origin.chat.title
                bot_status = await bot.get_chat_member(chat_id=chat_id, user_id=bot.id)
                user_сhannel = await Channel.prisma().create(
                    data = {
                        'channel_id': chat_id,
                        'username': username,
                        'title': title,
                        'admin': {
                            'connect': {
                                'tg_id': user_id
                            }
                        }
                    },
                )
                user_update = await User.prisma().update(
                    where={
                        'tg_id': user_id,
                    },
                    data={
                        'is_active': True,
                    },
                )
            except:
                await message.answer("В пересланном канале нет бота")


        else:
            await message.answer(messages_no_profile)

    else:
        await message.answer("Всё шикарно")
