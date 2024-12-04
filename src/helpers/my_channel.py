from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from prisma.models import Channel

from common.callback import SelectMyChannelCallback

async def get_my_channels(admin_id):
    channels = await Channel.prisma().find_many(
        where={
            'admin_id': admin_id,
        }
    )

    inline_kb_list = []
    
    for channel in channels:
        inline_kb_list.append(
            [InlineKeyboardButton(text=channel.title, callback_data=SelectMyChannelCallback(step="SELECT CHANNEL", value=str(channel.channel_id)).pack())],
        )

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def get_my_channel(channel_id):
    channel = await Channel.prisma().find_unique(
        where={
            'channel_id': channel_id,
        }
    )

    return channel