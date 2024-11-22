from aiogram import Router, F, types

router = Router()

@router.callback_query(F.text == "ЗАДАТЬ КАТЕГОРИЮ ОБРАЗОВАНИЕ")
async def my_callback_foo(query: types.CallbackQuery):
    await query.answer("Сука")

# @router.callback_query()
# async def my_callback_foo(query: types.CallbackQuery):
#     await query.answer("Всё остальное")