from aiogram import Router, F, types

from common.callback import CreationOptCallback

from helpers.channel import set_category_channel
from helpers.categories import categories_map

router = Router()

@router.callback_query(CreationOptCallback.filter(F.step == "SET CATEGORY"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: CreationOptCallback):
    await set_category_channel(callback_data.channel_id, callback_data.value)
    answer = f"Вы задали категорию {categories_map[callback_data.value]}"
    await query.answer(answer)

@router.callback_query()
async def my_callback_foo(query: types.CallbackQuery):
    await query.answer("Всё остальное")