from aiogram import Router, F, types
from aiogram.filters import Command, CommandStart
from settings import my_keyboard_buttons, messages_no_profile, messages_help, message_profile
from helpers.user import getActiveUser

router = Router()

@router.message(F.text == 'Профиль')
async def command_profile_handler(message: types.Message) -> None:
    user_id = message.chat.id
    is_user_active = await getActiveUser(user_id)
    await message.answer("Тут профиль")
    # if is_user_active == True:
    #     await message.answer(message_profile)
    # else:
    #     await message.answer(messages_no_profile)

@router.message(F.text == 'Каталог')
async def command_catalog_handler(message: types.Message) -> None:
    user_id = message.chat.id
    is_user_active = await getActiveUser(user_id)
    await message.answer("Тут каталог")
    # if is_user_active == True:
    #     await message.answer("Тут каталог")
    # else:
    #     await message.answer(messages_no_profile)

@router.message(F.text == 'Помощь')
async def command_help_handler(message: types.Message) -> None:
    await message.answer(messages_help)




