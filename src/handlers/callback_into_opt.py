from aiogram import Router, F, types

from common.callback import (
    SelectCategoryIntoOptCallback,
    SelectDateIntoOpt,
    CreationIntoOptCallback,
    SelectTimeIntoOpt,
)

from helpers.user import get_state_user, set_state_user
from helpers.into_opt import (
    get_btns_inline_categories_into_opt,
    get_btns_inline_channels_into_opt,
    get_btns_inline_date_into_opt,
    set_into_opt_date,
    get_btns_confirm_date,
    get_btns_time,
    set_opt_time
)

from prisma.models import User, IntoOpt

router = Router()

@router.callback_query(SelectCategoryIntoOptCallback.filter(F.step == "SELECT CATEGORY"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectCategoryIntoOptCallback):
    btns_inline_channels = await get_btns_inline_channels_into_opt(callback_data.value)
    await query.message.edit_text('Выберите канал:' , reply_markup=btns_inline_channels)

@router.callback_query(SelectCategoryIntoOptCallback.filter(F.step == "SELECT CHANNEL BACK"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectCategoryIntoOptCallback):
    btns_inline_categories = await get_btns_inline_categories_into_opt()
    await query.message.edit_text('Зайти в опт:', reply_markup=btns_inline_categories)

@router.callback_query(SelectCategoryIntoOptCallback.filter(F.step == "SELECT CHANNEL"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectCategoryIntoOptCallback):
    user_id=query.from_user.id
    channel_id = int(callback_data.value)

    into_opt = await IntoOpt.prisma().upsert(
        where={
            'channel_id': channel_id,
        },
        data={
            'create': {
                'channel': {
                    'connect': {
                        'channel_id': channel_id
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
            'into_opt_edit': into_opt.id,
        },
    )
    btns_inline_channels = await get_btns_inline_date_into_opt(user_id)
    await query.message.edit_text('Выберите доступные для брони слоты:' , reply_markup=btns_inline_channels)

@router.callback_query(SelectDateIntoOpt.filter(F.step == "INOPT SELECT DATE"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectDateIntoOpt):
    user_id=query.from_user.id
    await set_into_opt_date(user_id, callback_data.value)
    btns_inline_date = await get_btns_inline_date_into_opt(user_id, callback_data.page)
    await query.message.edit_text('Выберите доступные для брони слоты:' , reply_markup=btns_inline_date)

@router.callback_query(SelectDateIntoOpt.filter(F.step == "MORE DATE"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectDateIntoOpt):
    user_id=query.from_user.id
    btns_inline_date = await get_btns_inline_date_into_opt(user_id, callback_data.page)
    await query.message.edit_text('Выберите доступные для брони слоты:' , reply_markup=btns_inline_date)

@router.callback_query(SelectDateIntoOpt.filter(F.step == "CONFIRM DATE"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectDateIntoOpt):
    user_id=query.from_user.id
    btns_inline_confirm = await get_btns_confirm_date(callback_data.channel_id)
    await query.message.edit_text('Звершить выбор дат?' , reply_markup=btns_inline_confirm)

@router.callback_query(CreationIntoOptCallback.filter(F.step == "DATE CHANGE"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: CreationIntoOptCallback):
    user_id=query.from_user.id
    btns_inline_date = await get_btns_inline_date_into_opt(user_id)
    await query.message.edit_text('Выберите доступные для брони слоты:' , reply_markup=btns_inline_date)

@router.callback_query(CreationIntoOptCallback.filter(F.step == "DATE SAVE"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: CreationIntoOptCallback):
    user_id=query.from_user.id
    btns_inline_time = await get_btns_time(user_id)
    await query.message.edit_text('Выберите допустимое время размещений:', reply_markup=btns_inline_time)

@router.callback_query(SelectTimeIntoOpt.filter(F.step == "INOPT SELECT TIME"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectTimeIntoOpt):
    user_id=query.from_user.id
    await set_opt_time(user_id, callback_data.value)
    btns_inline_time = await get_btns_time(user_id)
    await query.message.edit_text('Выберите допустимое время размещений:', reply_markup=btns_inline_time)

@router.callback_query(SelectTimeIntoOpt.filter(F.step == "CONFIRM TIME"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectTimeIntoOpt):
    user_id=query.from_user.id
    await query.message.edit_text('Пришлите пост:')
    await set_state_user(user_id, "ЗАПИСЬ В ПОДБОРКИ СОХРАНЕНИЕ ПОСТА")

