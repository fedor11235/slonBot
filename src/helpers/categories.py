from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from common.callback import CreationOptCallback

async def get_btns_inline_categories(channel_id):
    inline_kb_list = [
        [InlineKeyboardButton(text="Образование", callback_data=CreationOptCallback(channel_id=channel_id, step="SET CATEGORY", value="EDUCATION").pack())],
        [InlineKeyboardButton(text="Финансы", callback_data=CreationOptCallback(channel_id=channel_id, step="SET CATEGORY", value="FINANCE").pack()) ],
        [InlineKeyboardButton(text="Здоровье", callback_data=CreationOptCallback(channel_id=channel_id, step="SET CATEGORY", value="HEALTH").pack())],
        [InlineKeyboardButton(text="Новости", callback_data=CreationOptCallback(channel_id=channel_id, step="SET CATEGORY", value="NEWS").pack())],
        [InlineKeyboardButton(text="IT ", callback_data=CreationOptCallback(channel_id=channel_id, step="SET CATEGORY", value="IT").pack())],
        [InlineKeyboardButton(text="Развлечения", callback_data=CreationOptCallback(channel_id=channel_id, step="SET CATEGORY", value="ENTERTAINMENT").pack())],
        [InlineKeyboardButton(text="Психология", callback_data=CreationOptCallback(channel_id=channel_id, step="SET CATEGORY", value="PSYCHOLOGY").pack())],
        [InlineKeyboardButton(text="Видосники", callback_data=CreationOptCallback(channel_id=channel_id, step="SET CATEGORY", value="VIDEO").pack())],
        [InlineKeyboardButton(text="Авторские", callback_data=CreationOptCallback(channel_id=channel_id, step="SET CATEGORY", value="AUTHOR'S").pack())],
        [InlineKeyboardButton(text="Другое", callback_data=CreationOptCallback(channel_id=channel_id, step="SET CATEGORY", value="OTHER").pack())],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


categories_map = {
    "EDUCATION": "ОБРАЗОВАНИЕ",
    "FINANCE": "ФИНАНСЫ",
    "HEALTH": "ЗДОРОВЬЕ",
    "NEWS": "НОВОСТИ",
    "IT": "IT",
    "ENTERTAINMENT": "РАЗВЛЕЧЕНИЯ",
    "PSYCHOLOGY": "ПСИХОЛОГИЯ",
    "VIDEO": "ВИДОСНИКИ",
    "AUTHOR'S": "АВТОРСКИЕ",
    "OTHER": "ДРУГОЕ",
}