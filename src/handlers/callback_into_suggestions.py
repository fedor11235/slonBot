from aiogram import Router, F, types

from common.callback import (
    SelectCategoryIntoSuggestionsCallback,
    SelectDateIntoSuggestions,
    CreationIntoSuggestionsCallback,
    SelectTimeIntoSuggestions
)

from helpers.user import set_state_user
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
    get_btns_inline_categories_into_suggestions,
    get_btns_inline_date_into_suggestion,
    set_into_suggestion_date,
    get_btns_confirm_date,
    get_btns_time,
    set_suggestions_time
)

from prisma.models import User, IntoSuggestion

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

@router.callback_query(SelectCategoryIntoSuggestionsCallback.filter(F.step == "SELECT CHANNEL"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectCategoryIntoSuggestionsCallback):
    user_id=query.from_user.id
    channel_id = int(callback_data.value)

    into_suggestion = await IntoSuggestion.prisma().upsert(
        where={
            'id': channel_id,
        },
        data={
            'create': {
                'suggestions': {
                    'connect': {
                        'id': channel_id
                    }
                }
            },
            'update': {},
        }
    )

    user = await User.prisma().update(
        where={
            'tg_id': user_id,
        },
        data={
            'into_suggestion_edit': into_suggestion.id,
        },
    )
    btns_inline_channels = await get_btns_inline_date_into_suggestion(user_id)
    await query.message.edit_text('Выберите доступные для брони слоты:' , reply_markup=btns_inline_channels)


@router.callback_query(SelectDateIntoSuggestions.filter(F.step == "INOPT SELECT DATE"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectDateIntoSuggestions):
    user_id=query.from_user.id
    await set_into_suggestion_date(user_id, callback_data.value)
    btns_inline_date = await get_btns_inline_date_into_suggestion(user_id, callback_data.page)
    await query.message.edit_text('Выберите доступные для брони слоты:' , reply_markup=btns_inline_date)

@router.callback_query(SelectDateIntoSuggestions.filter(F.step == "MORE DATE"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectDateIntoSuggestions):
    user_id=query.from_user.id
    btns_inline_date = await get_btns_inline_date_into_suggestion(user_id, callback_data.page)
    await query.message.edit_text('Выберите доступные для брони слоты:' , reply_markup=btns_inline_date)

@router.callback_query(SelectDateIntoSuggestions.filter(F.step == "CONFIRM DATE"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectDateIntoSuggestions):
    user_id=query.from_user.id
    btns_inline_confirm = await get_btns_confirm_date(callback_data.channel_id)
    await query.message.edit_text('Звершить выбор дат?' , reply_markup=btns_inline_confirm)

@router.callback_query(CreationIntoSuggestionsCallback.filter(F.step == "DATE CHANGE"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: CreationIntoSuggestionsCallback):
    user_id=query.from_user.id
    btns_inline_date = await get_btns_inline_date_into_suggestion(user_id)
    await query.message.edit_text('Выберите доступные для брони слоты:' , reply_markup=btns_inline_date)

@router.callback_query(CreationIntoSuggestionsCallback.filter(F.step == "DATE SAVE"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: CreationIntoSuggestionsCallback):
    user_id=query.from_user.id
    btns_inline_time = await get_btns_time(user_id)
    await query.message.edit_text('Выберите допустимое время размещений:', reply_markup=btns_inline_time)

@router.callback_query(SelectTimeIntoSuggestions.filter(F.step == "INTOSUG SELECT TIME"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectTimeIntoSuggestions):
    user_id=query.from_user.id
    print("keke")
    await set_suggestions_time(user_id, callback_data.value)
    btns_inline_time = await get_btns_time(user_id)
    await query.message.edit_text('Выберите допустимое время размещений:', reply_markup=btns_inline_time)

@router.callback_query(SelectTimeIntoSuggestions.filter(F.step == "CONFIRM TIME"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectTimeIntoSuggestions):
    user_id=query.from_user.id
    await query.message.edit_text('Пришлите пост:')
    await set_state_user(user_id, "ЗАПИСЬ В ПОДБОРКУ СОХРАНЕНИЕ ПОСТА")

