from aiogram import Router, F, types
from aiogram.filters import Command, CommandStart
from prisma.models import User
from settings import my_keyboard_buttons, messages_no_profile, messages_help
from helpers.user import getActiveUser
from helpers.channel import get_btns_inline_channel
from helpers.into_opt import get_btns_inline_categories_into_opt
from helpers.into_suggestions import get_btns_inline_categories_into_suggestions
from helpers.catalog import get_btns_inline_categories_catalog
from helpers.my_channel import get_my_channels
from helpers.profile import get_btns_profile

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
    user_id = message.chat.id
    is_user_active = await getActiveUser(user_id)
    if is_user_active == True:
        await message.answer(messages_no_profile)
    else:
        btns_inline_my_channels = await get_my_channels(user_id)
        await message.answer('Мои каналы:', reply_markup=btns_inline_my_channels)

@router.message(Command("catalog"))
async def command_channel_handler(message: types.Message) -> None:
    user_id = message.chat.id
    is_user_active = await getActiveUser(user_id)
    if is_user_active == True:
        await message.answer(messages_no_profile)
    else:
        btns_inline_categories = await get_btns_inline_categories_catalog()
        await message.answer('Выберите категорию:', reply_markup=btns_inline_categories)

@router.message(Command("pay"))
async def command_pay_handler(message: types.Message) -> None:
    user_id = message.chat.id
    is_user_active = await getActiveUser(user_id)
    if is_user_active == True:
        await message.answer(messages_no_profile)
    else:
        await message.answer('Тут плтёжка')

@router.message(Command("newopt"))
async def command_newopt_handler(message: types.Message) -> None:
    user_id = message.chat.id
    is_user_active = await getActiveUser(user_id)
    if is_user_active == True:
        await message.answer(messages_no_profile)
    else:
        btns_inline_categories = await get_btns_inline_channel(user_id)
        await message.answer('Выберите канал в котором хотите собрать опт:', reply_markup=btns_inline_categories)

@router.message(Command("getopt"))
async def command_getopt_handler(message: types.Message) -> None:
    user_id = message.chat.id
    is_user_active = await getActiveUser(user_id)
    if is_user_active == True:
        await message.answer(messages_no_profile)
    else:
        btns_inline_categories = await get_btns_inline_categories_into_opt()
        await message.answer('Зайти в опт:', reply_markup=btns_inline_categories)

@router.message(Command("business"))
async def command_business_handler(message: types.Message) -> None:
    user_id = message.chat.id
    is_user_active = await getActiveUser(user_id)
    if is_user_active == True:
        await message.answer(messages_no_profile)
    else:
        btns_inline_categories = await get_btns_inline_categories_into_suggestions()
        await message.answer('Зайти в подборку:', reply_markup=btns_inline_categories)

@router.message(Command("profile"))
async def command_profile_handler(message: types.Message) -> None:
    user_id = message.chat.id
    is_user_active = await getActiveUser(user_id)
    if is_user_active == True:
        await message.answer(messages_no_profile)
    else:
        btns_inline_profile = await get_btns_profile()
        await message.answer('Это ваш профиль, тут вы можете:', reply_markup=btns_inline_profile)

@router.message(Command("partners"))
async def command_partners_handler(message: types.Message) -> None:
    user_id = message.chat.id
    is_user_active = await getActiveUser(user_id)
    if is_user_active == True:
        await message.answer(messages_no_profile)
    else:
        await message.answer('Тут промокоды')

@router.message(Command("help"))
async def command_help_handler(message: types.Message) -> None:
    await message.answer(messages_help)
