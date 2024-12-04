from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from common.callback import ProfileCallback

async def get_btns_profile():
    inline_kb_list = [
        [InlineKeyboardButton(text="мои опты", callback_data=ProfileCallback(step="MY OPT", value="").pack())],
        [InlineKeyboardButton(text="график выходов", callback_data=ProfileCallback(step="RELEASE SCHEDULE", value="").pack())],
        [InlineKeyboardButton(text="статистика", callback_data=ProfileCallback(step="STATISTICS", value="").pack())],
        [InlineKeyboardButton(text="баланс", callback_data=ProfileCallback(step="BALANCE", value="").pack())],
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
