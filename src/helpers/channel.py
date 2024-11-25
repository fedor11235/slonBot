from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from prisma.models import Channel
from common.callback import CreationOptCallback

async def set_category_channel(channel_id, category):
    channel = await Channel.prisma().update(
        where={
            'channel_id': channel_id,
        },
        data={
            'category': category,
        },
    )

async def get_btns_inline_channel(user_id):
    channels = await Channel.prisma().find_many(
        where={
            'admin_id': user_id,
        },
    )
    inline_kb_list = []
    for channel in channels:
        inline_kb_list.append([
            InlineKeyboardButton(text=channel.title, callback_data=CreationOptCallback(channel_id=channel.channel_id, step="START CREATION OPT", value=channel.title).pack())
        ])

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
