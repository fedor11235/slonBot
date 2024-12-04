from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from common.callback import SetCategoryCatalogCallback, SelectCategoryCatalogCallback
from prisma.models import Channel


async def get_btns_inline_categories_catalog():
    inline_kb_list = [
        [InlineKeyboardButton(text="Все тематики", callback_data=SetCategoryCatalogCallback(step="GET CATEGORY", value="ALL").pack())],
        [InlineKeyboardButton(text="Образование", callback_data=SetCategoryCatalogCallback(step="GET CATEGORY", value="EDUCATION").pack())],
        [InlineKeyboardButton(text="Финансы", callback_data=SetCategoryCatalogCallback(step="GET CATEGORY", value="FINANCE").pack()) ],
        [InlineKeyboardButton(text="Здоровье", callback_data=SetCategoryCatalogCallback(step="GET CATEGORY", value="HEALTH").pack())],
        [InlineKeyboardButton(text="Новости", callback_data=SetCategoryCatalogCallback(step="GET CATEGORY", value="NEWS").pack())],
        [InlineKeyboardButton(text="IT ", callback_data=SetCategoryCatalogCallback(step="GET CATEGORY", value="IT").pack())],
        [InlineKeyboardButton(text="Развлечения", callback_data=SetCategoryCatalogCallback(step="GET CATEGORY", value="ENTERTAINMENT").pack())],
        [InlineKeyboardButton(text="Психология", callback_data=SetCategoryCatalogCallback(step="GET CATEGORY", value="PSYCHOLOGY").pack())],
        [InlineKeyboardButton(text="Видосники", callback_data=SetCategoryCatalogCallback(step="GET CATEGORY", value="VIDEO").pack())],
        [InlineKeyboardButton(text="Авторские", callback_data=SetCategoryCatalogCallback(step="GET CATEGORY", value="AUTHOR'S").pack())],
        [InlineKeyboardButton(text="Другое", callback_data=SetCategoryCatalogCallback(step="GET CATEGORY", value="OTHER").pack())],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def get_btns_inline_channels_catalog(category):
    channels = []
    inline_kb_list = []

    if category == 'ALL':
        channels = await Channel.prisma().find_many()
    else:
        channels = await Channel.prisma().find_many(
            where={
                'category': category,
            }
        )

    for channel in channels:
        inline_kb_list.append(
            [InlineKeyboardButton(text=channel.title, callback_data=SelectCategoryCatalogCallback(step="SELECT CHANNEL", value=str(channel.channel_id)).pack())],
        )

    inline_kb_list.append(
        [InlineKeyboardButton(text="Назад", callback_data=SelectCategoryCatalogCallback(step="SELECT CHANNEL BACK", value="").pack())],
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)