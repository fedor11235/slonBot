from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from common.callback import CreationOptCallback

async def get_btns_inline_categories(channel_id):
    inline_kb_list = [
        [InlineKeyboardButton(text="Образование", callback_data=CreationOptCallback(channel_id=channel_id, step="ЗАДАТЬ КАТЕГОРИЮ ОБРАЗОВАНИЕ").pack())],
        [InlineKeyboardButton(text="Финансы", callback_data=CreationOptCallback(channel_id=channel_id, step="ЗАДАТЬ КАТЕГОРИЮ ФИНАНСЫ").pack()) ],
        [InlineKeyboardButton(text="Здоровье", callback_data=CreationOptCallback(channel_id=channel_id, step="ЗАДАТЬ КАТЕГОРИЮ ЗДОРОВЬЕ").pack())],
        [InlineKeyboardButton(text="Новости", callback_data=CreationOptCallback(channel_id=channel_id, step="ЗАДАТЬ КАТЕГОРИЮ НОВОСТИ").pack())],
        [InlineKeyboardButton(text="Информационные ", callback_data=CreationOptCallback(channel_id=channel_id, step="ЗАДАТЬ КАТЕГОРИЮ IT").pack())],
        [InlineKeyboardButton(text="Развлечения", callback_data=CreationOptCallback(channel_id=channel_id, step="ЗАДАТЬ КАТЕГОРИЮ РАЗВЛЕЧЕНИЯ").pack())],
        [InlineKeyboardButton(text="Психология", callback_data=CreationOptCallback(channel_id=channel_id, step="ЗАДАТЬ КАТЕГОРИЮ ПСИХОЛОГИЯ").pack())],
        [InlineKeyboardButton(text="Видосники", callback_data=CreationOptCallback(channel_id=channel_id, step="ЗАДАТЬ КАТЕГОРИЮ ВИДОСНИКИ").pack())],
        [InlineKeyboardButton(text="Авторские", callback_data=CreationOptCallback(channel_id=channel_id, step="ЗАДАТЬ КАТЕГОРИЮ АВТОРСКИЕ").pack())],
        [InlineKeyboardButton(text="Другое", callback_data=CreationOptCallback(channel_id=channel_id, step="ЗАДАТЬ КАТЕГОРИЮ ДРУГОЕ").pack())],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)