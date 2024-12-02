from aiogram import Router, F, types

from common.callback import (
    SelectCategoryIntoSuggestionsCallback,
)

# from helpers.user import get_state_user, set_state_user
# from helpers.into_opt import (
#     get_btns_inline_categories_into_opt,
#     get_btns_inline_channels_into_opt,
#     get_btns_inline_date_into_opt,
#     set_into_opt_date,
#     get_btns_confirm_date,
#     get_btns_time,
#     set_opt_time
# )

from helpers.into_suggestions import (
    get_btns_inline_channels_into_suggestions,
    get_btns_inline_categories_into_suggestions
)

# from prisma.models import User, IntoOpt

router = Router()

@router.callback_query(SelectCategoryIntoSuggestionsCallback.filter(F.step == "SELECT CATEGORY"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectCategoryIntoSuggestionsCallback):
    btns_inline_channels = await get_btns_inline_channels_into_suggestions(callback_data.value)
    await query.message.edit_text('Выберите канал:' , reply_markup=btns_inline_channels)
    # print("keke")
    # await query.answer("ПУК")

@router.callback_query(SelectCategoryIntoSuggestionsCallback.filter(F.step == "SELECT CHANNEL BACK"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectCategoryIntoSuggestionsCallback):
    btns_inline_categories = await get_btns_inline_categories_into_suggestions()
    await query.message.edit_text('Зайти в подборку:', reply_markup=btns_inline_categories)

