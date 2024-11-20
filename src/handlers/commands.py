from aiogram import Router, F, types
from aiogram.filters import Command, CommandStart
from prisma.models import User
from settings import my_keyboard_buttons, messages_no_profile, messages_help

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    tg_id = message.chat.id
    keyboard = types.ReplyKeyboardMarkup(keyboard=my_keyboard_buttons)
    await message.answer(messages_no_profile, reply_markup=keyboard)
    user = await User.prisma().upsert(
        where={
            'tg_id': tg_id,
        },
        data={
            'create': {
                'tg_id': tg_id,
            },
            'update': {},
        }
    )

@router.message(Command("channel"))
async def command_channel_handler(message: types.Message) -> None:
    await message.answer(messages_no_profile)

@router.message(Command("pay"))
async def command_pay_handler(message: types.Message) -> None:
    await message.answer(messages_no_profile)

@router.message(Command("newopt"))
async def command_newopt_handler(message: types.Message) -> None:
    await message.answer(messages_no_profile)

@router.message(Command("getopt"))
async def command_getopt_handler(message: types.Message) -> None:
    await message.answer(messages_no_profile)

@router.message(Command("business"))
async def command_business_handler(message: types.Message) -> None:
    await message.answer(messages_no_profile)

@router.message(Command("profile"))
async def command_profile_handler(message: types.Message) -> None:
    await message.answer(messages_no_profile)

@router.message(Command("partners"))
async def command_partners_handler(message: types.Message) -> None:
    await message.answer(messages_no_profile)

@router.message(Command("help"))
async def command_help_handler(message: types.Message) -> None:
    await message.answer(messages_help)
