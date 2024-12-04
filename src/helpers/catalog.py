from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from common.callback import SetCategoryCatalogCallback

async def get_btns_inline_categories_catalog():
    inline_kb_list = [
        [InlineKeyboardButton(text="Образование", callback_data=SetCategoryCatalogCallback(step="SET CATEGORY", value="EDUCATION").pack())],
        [InlineKeyboardButton(text="Финансы", callback_data=SetCategoryCatalogCallback(step="SET CATEGORY", value="FINANCE").pack()) ],
        [InlineKeyboardButton(text="Здоровье", callback_data=SetCategoryCatalogCallback(step="SET CATEGORY", value="HEALTH").pack())],
        [InlineKeyboardButton(text="Новости", callback_data=SetCategoryCatalogCallback(step="SET CATEGORY", value="NEWS").pack())],
        [InlineKeyboardButton(text="IT ", callback_data=SetCategoryCatalogCallback(step="SET CATEGORY", value="IT").pack())],
        [InlineKeyboardButton(text="Развлечения", callback_data=SetCategoryCatalogCallback(step="SET CATEGORY", value="ENTERTAINMENT").pack())],
        [InlineKeyboardButton(text="Психология", callback_data=SetCategoryCatalogCallback(step="SET CATEGORY", value="PSYCHOLOGY").pack())],
        [InlineKeyboardButton(text="Видосники", callback_data=SetCategoryCatalogCallback(step="SET CATEGORY", value="VIDEO").pack())],
        [InlineKeyboardButton(text="Авторские", callback_data=SetCategoryCatalogCallback(step="SET CATEGORY", value="AUTHOR'S").pack())],
        [InlineKeyboardButton(text="Другое", callback_data=SetCategoryCatalogCallback(step="SET CATEGORY", value="OTHER").pack())],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)