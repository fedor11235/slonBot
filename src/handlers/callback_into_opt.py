from aiogram import Router, F, types

from common.callback import SelectCategoryIntoOptCallback

from helpers.user import get_state_user, set_state_user
from helpers.into_opt import (
    get_btns_inline_categories_into_opt,
    get_btns_inline_channels_into_opt,
    get_btns_inline_date_into_opt
)

router = Router()

@router.callback_query(SelectCategoryIntoOptCallback.filter(F.step == "SELECT CHANNEL"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectCategoryIntoOptCallback):
    btns_inline_channels = await get_btns_inline_channels_into_opt(callback_data.value)
    await query.message.edit_text('Выберите канал:' , reply_markup=btns_inline_channels)

@router.callback_query(SelectCategoryIntoOptCallback.filter(F.step == "SELECT CHANNEL BACK"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectCategoryIntoOptCallback):
    btns_inline_categories = await get_btns_inline_categories_into_opt()
    await query.message.edit_text('Зайти в опт:', reply_markup=btns_inline_categories)

@router.callback_query(SelectCategoryIntoOptCallback.filter(F.step == "SELECT CHANNEL"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectCategoryIntoOptCallback):
    btns_inline_channels = await get_btns_inline_date_into_opt(int(callback_data.value))
    await query.message.edit_text('Выберите доступные для брони слоты:' , reply_markup=btns_inline_channels)

