from aiogram import Router, F, types
from aiogram.filters import Command, CommandStart
from settings import my_keyboard_buttons, messages_no_profile, messages_help

router = Router()

@router.message(F.text == 'Профиль')
async def command_start_handler(message: types.Message) -> None:
    await message.answer(messages_no_profile)

@router.message(F.text == 'Каталог')
async def command_start_handler(message: types.Message) -> None:
    await message.answer(messages_no_profile)

@router.message(F.text == 'Помощь')
async def command_start_handler(message: types.Message) -> None:
    await message.answer(messages_help)
