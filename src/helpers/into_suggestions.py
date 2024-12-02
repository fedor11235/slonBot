from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from common.callback import SelectCategoryIntoSuggestionsCallback

from prisma.models import Suggestions

async def get_btns_inline_categories_into_suggestions():
    inline_kb_list = [
        [InlineKeyboardButton(text="Все тематики", callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CATEGORY", value="ALL").pack())],
        [InlineKeyboardButton(text="Образование", callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CATEGORY", value="EDUCATION").pack())],
        [InlineKeyboardButton(text="Финансы", callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CATEGORY", value="FINANCE").pack()) ],
        [InlineKeyboardButton(text="Здоровье", callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CATEGORY", value="HEALTH").pack())],
        [InlineKeyboardButton(text="Новости", callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CATEGORY", value="NEWS").pack())],
        [InlineKeyboardButton(text="IT ", callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CATEGORY", value="IT").pack())],
        [InlineKeyboardButton(text="Развлечения", callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CATEGORY", value="ENTERTAINMENT").pack())],
        [InlineKeyboardButton(text="Психология", callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CATEGORY", value="PSYCHOLOGY").pack())],
        [InlineKeyboardButton(text="Видосники", callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CATEGORY", value="VIDEO").pack())],
        [InlineKeyboardButton(text="Авторские", callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CATEGORY", value="AUTHOR'S").pack())],
        [InlineKeyboardButton(text="Другое", callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CATEGORY", value="OTHER").pack())],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def get_btns_inline_channels_into_suggestions(category):
    channels = []
    inline_kb_list = []

    if category == 'ALL':
        channels = await Suggestions.prisma().find_many()
    else:
        channels = await Suggestions.prisma().find_many(
            where={
                'category': category,
            },
        )

    for channel in channels:
        inline_kb_list.append(
            [InlineKeyboardButton(text=channel.title, callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CHANNEL", value=str(channel.id)).pack())],
        )

    inline_kb_list.append(
        [InlineKeyboardButton(text="Назад", callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CHANNEL BACK", value="").pack())],
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)