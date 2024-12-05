from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from prisma.models import User, Channel

from common.callback import ProfileCallback

async def get_btn_back_channel():
    inline_kb_list = [
        [InlineKeyboardButton(text="Назад", callback_data=ProfileCallback(step="MY OPT", value="").pack())],
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
    
async def get_btn_back_menu():
    inline_kb_list = [
        [InlineKeyboardButton(text="Назад", callback_data=ProfileCallback(step="MENU", value="").pack())],
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def get_btns_profile():
    inline_kb_list = [
        [InlineKeyboardButton(text="мои опты", callback_data=ProfileCallback(step="MY OPT", value="").pack())],
        [InlineKeyboardButton(text="график выходов", callback_data=ProfileCallback(step="RELEASE SCHEDULE", value="").pack())],
        [InlineKeyboardButton(text="статистика", callback_data=ProfileCallback(step="STATISTICS", value="").pack())],
        [InlineKeyboardButton(text="баланс", callback_data=ProfileCallback(step="BALANCE", value="").pack())],
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def get_btn_my_opt(user_id):
    inline_kb_list = []
    user = await User.prisma().find_unique(
        where={
            'tg_id': user_id,
        },
        include={
            'channels': {
                'include': {
                    'opt': True
                }
            }
        }
    )
    opts = []
  
    for channel in user.channels:
        if channel.opt != None:
            inline_kb_list.append(
                [InlineKeyboardButton(text=channel.title, callback_data=ProfileCallback(step="SELECT CHANNEL", value=str(channel.channel_id)).pack())],
            )

    inline_kb_list.append(
        [InlineKeyboardButton(text="Назад", callback_data=ProfileCallback(step="MENU", value="").pack())],
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def get_my_channel(channel_id):
    channel = await Channel.prisma().find_unique(
        where={
            'channel_id': channel_id,
        }
    )

    return channel

async def get_release_schedule(user_id):
    inline_kb_list = []
    user = await User.prisma().find_unique(
        where={
            'tg_id': user_id,
        },
        include={
            'channels': {
                'include': {
                    'into_opt': True
                }
            }
        }
    )
    opts = []
    text = ""
  
    for channel in user.channels:
        if channel.into_opt != None:
            text += f"Дата: {channel.into_opt.date}. Время:{channel.into_opt.time}\n"

    return text
