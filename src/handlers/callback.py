from aiogram import Router, F, types

from common.callback import CreationOptCallback

router = Router()

@router.callback_query(CreationOptCallback.filter(F.step == "SET CATEGORY EDUCATION"))
async def my_callback_foo(query: types.CallbackQuery):
    await query.answer("ОБРАЗОВАНИЕ")

@router.callback_query()
async def my_callback_foo(query: types.CallbackQuery):
    await query.answer("Всё остальное")