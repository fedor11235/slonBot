from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def get_btns_inline_categories():
    inline_kb_list = [
        [InlineKeyboardButton(text="Образование", callback_data='ЗАДАТЬ КАТЕГОРИЮ ОБРАЗОВАНИЕ')],
        [InlineKeyboardButton(text="Финансы", callback_data='ЗАДАТЬ КАТЕГОРИЮ ФИНАНСЫ')],
        [InlineKeyboardButton(text="Здоровье", callback_data='ЗАДАТЬ КАТЕГОРИЮ ЗДОРОВЬЕ')],
        [InlineKeyboardButton(text="Новости", callback_data='ЗАДАТЬ КАТЕГОРИЮ НОВОСТИ')],
        [InlineKeyboardButton(text="Информационные ", callback_data='IT')],
        [InlineKeyboardButton(text="Развлечения", callback_data='ЗАДАТЬ КАТЕГОРИЮ РАЗВЛЕЧЕНИЯ')],
        [InlineKeyboardButton(text="Психология", callback_data='ЗАДАТЬ КАТЕГОРИЮ ПСИХОЛОГИЯ')],
        [InlineKeyboardButton(text="Видосники", callback_data='ЗАДАТЬ КАТЕГОРИЮ ВИДОСНИКИ')],
        [InlineKeyboardButton(text="Авторские", callback_data='ЗАДАТЬ КАТЕГОРИЮ АВТОРСКИЕ')],
        [InlineKeyboardButton(text="Другое", callback_data='ЗАДАТЬ КАТЕГОРИЮ ДРУГОЕ')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)