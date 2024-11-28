from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from common.callback import SelectCategoryIntoOptCallback

from prisma.models import Channel

async def get_btns_inline_categories_into_opt():
    inline_kb_list = [
        [InlineKeyboardButton(text="Все тематики", callback_data=SelectCategoryIntoOptCallback(step="SELECT CATEGORY", value="ALL").pack())],
        [InlineKeyboardButton(text="Образование", callback_data=SelectCategoryIntoOptCallback(step="SELECT CATEGORY", value="EDUCATION").pack())],
        [InlineKeyboardButton(text="Финансы", callback_data=SelectCategoryIntoOptCallback(step="SELECT CATEGORY", value="FINANCE").pack()) ],
        [InlineKeyboardButton(text="Здоровье", callback_data=SelectCategoryIntoOptCallback(step="SELECT CATEGORY", value="HEALTH").pack())],
        [InlineKeyboardButton(text="Новости", callback_data=SelectCategoryIntoOptCallback(step="SELECT CATEGORY", value="NEWS").pack())],
        [InlineKeyboardButton(text="IT ", callback_data=SelectCategoryIntoOptCallback(step="SELECT CATEGORY", value="IT").pack())],
        [InlineKeyboardButton(text="Развлечения", callback_data=SelectCategoryIntoOptCallback(step="SELECT CATEGORY", value="ENTERTAINMENT").pack())],
        [InlineKeyboardButton(text="Психология", callback_data=SelectCategoryIntoOptCallback(step="SELECT CATEGORY", value="PSYCHOLOGY").pack())],
        [InlineKeyboardButton(text="Видосники", callback_data=SelectCategoryIntoOptCallback(step="SELECT CATEGORY", value="VIDEO").pack())],
        [InlineKeyboardButton(text="Авторские", callback_data=SelectCategoryIntoOptCallback(step="SELECT CATEGORY", value="AUTHOR'S").pack())],
        [InlineKeyboardButton(text="Другое", callback_data=SelectCategoryIntoOptCallback(step="SELECT CATEGORY", value="OTHER").pack())],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def get_btns_inline_channels_into_opt(category):
    channels = []
    inline_kb_list = []

    if category == 'ALL':
        channels = await Channel.prisma().find_many(
            # include={
            #     'opt': True
            # }
        )
    else:
        channels = await Channel.prisma().find_many(
            where={
                'category': category,
            },
        )

    for channel in channels:
        inline_kb_list.append(
            [InlineKeyboardButton(text=channel.title, callback_data=SelectCategoryIntoOptCallback(step="SELECT CHANNEL", value=str(channel.channel_id)).pack())],
        )

    inline_kb_list.append(
        [InlineKeyboardButton(text="Назад", callback_data=SelectCategoryIntoOptCallback(step="SELECT CHANNEL BACK", value="").pack())],
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def get_btns_inline_date_into_opt(category):