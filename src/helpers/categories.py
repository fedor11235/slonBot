from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from common.callback import CreationOptCallback

async def get_btns_inline_categories(channel_id):
    inline_kb_list = [
        [InlineKeyboardButton(text="Образование", callback_data=CreationOptCallback(channel_id=channel_id, step="SET CATEGORY EDUCATION").pack())],
        [InlineKeyboardButton(text="Финансы", callback_data=CreationOptCallback(channel_id=channel_id, step="SET CATEGORY EDUCATION FINANCE").pack()) ],
        [InlineKeyboardButton(text="Здоровье", callback_data=CreationOptCallback(channel_id=channel_id, step="SET CATEGORY EDUCATION HEALTH").pack())],
        [InlineKeyboardButton(text="Новости", callback_data=CreationOptCallback(channel_id=channel_id, step="SET CATEGORY EDUCATION NEWS").pack())],
        [InlineKeyboardButton(text="Информационные ", callback_data=CreationOptCallback(channel_id=channel_id, step="SET CATEGORY EDUCATION IT").pack())],
        [InlineKeyboardButton(text="Развлечения", callback_data=CreationOptCallback(channel_id=channel_id, step="SET CATEGORY EDUCATION ENTERTAINMENT").pack())],
        [InlineKeyboardButton(text="Психология", callback_data=CreationOptCallback(channel_id=channel_id, step="SET CATEGORY EDUCATION PSYCHOLOGY").pack())],
        [InlineKeyboardButton(text="Видосники", callback_data=CreationOptCallback(channel_id=channel_id, step="SET CATEGORY EDUCATION VIDEO").pack())],
        [InlineKeyboardButton(text="Авторские", callback_data=CreationOptCallback(channel_id=channel_id, step="SET CATEGORY EDUCATION AUTHOR'S").pack())],
        [InlineKeyboardButton(text="Другое", callback_data=CreationOptCallback(channel_id=channel_id, step="SET CATEGORY EDUCATION OTHER").pack())],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)