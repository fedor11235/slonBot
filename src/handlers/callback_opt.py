from aiogram import Router, F, types

from common.callback import SetCategoryCallback, CreationOptCallback, SelectDateOpt, SelectTimeOpt

from helpers.channel import set_category_channel
from helpers.categories import categories_map
from helpers.user import get_state_user, set_state_user
from helpers.opt import get_btns_date, set_opt_date, get_btns_confirm_date, set_opt_time, get_btns_time

from prisma.models import User, Opt

router = Router()

@router.callback_query(CreationOptCallback.filter(F.step == "START CREATION OPT"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SetCategoryCallback):
    user_id=query.from_user.id
    answer = f"Создаём опт для канала {callback_data.value} Напишите стандартную(розничную) стоимость размещения:"
    await query.message.answer(answer)
    await set_state_user(user_id, "СОЗДАНИЕ ОПТА РОЗНИЧНАЯЯ СТОИМОСТЬ РАЗМЕЩЕНИЯ")

    opt = await Opt.prisma().upsert(
        where={
            'channel_id': callback_data.channel_id,
        },
        data={
            'create': {
                'channel': {
                    'connect': {
                        'channel_id': callback_data.channel_id
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
            'opt_edit': opt.id,
        },
    )

@router.callback_query(SelectDateOpt.filter(F.step == "OPT SELECT DATE"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectDateOpt):
    user_id=query.from_user.id
    await set_opt_date(user_id, callback_data.value)
    btns_inline_date = await get_btns_date(user_id, callback_data.page)
    await query.message.edit_text('Выберите доступные для брони слоты:' , reply_markup=btns_inline_date)

@router.callback_query(SelectDateOpt.filter(F.step == "MORE DATE"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectDateOpt):
    user_id=query.from_user.id
    btns_inline_date = await get_btns_date(user_id, callback_data.page)
    await query.message.edit_text('Выберите доступные для брони слоты:' , reply_markup=btns_inline_date)

@router.callback_query(SelectDateOpt.filter(F.step == "CONFIRM DATE"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectDateOpt):
    user_id=query.from_user.id
    btns_inline_confirm = await get_btns_confirm_date(callback_data.channel_id)
    await query.message.edit_text('Звершить выбор дат?' , reply_markup=btns_inline_confirm)

@router.callback_query(CreationOptCallback.filter(F.step == "DATE CHANGE"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: CreationOptCallback):
    user_id=query.from_user.id
    btns_inline_date = await get_btns_date(user_id)
    await query.message.edit_text('Выберите доступные для брони слоты:' , reply_markup=btns_inline_date)

@router.callback_query(CreationOptCallback.filter(F.step == "DATE SAVE"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: CreationOptCallback):
    user_id=query.from_user.id
    await query.message.edit_text('Укажите крайнюю дату формирования опта в формате 31.12. По наступлении этой даты, если опт не будет собран, он будет отменен.')
    await set_state_user(user_id, "СОЗДАНИЕ ОПТА КРАИНЯЯ ДАТА ФОРМИРОВАНИЯ ОПТА")

@router.callback_query(SelectTimeOpt.filter(F.step == "OPT SELECT TIME"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectTimeOpt):
    user_id=query.from_user.id
    await set_opt_time(user_id, callback_data.value)
    btns_inline_time = await get_btns_time(user_id)
    await query.message.edit_text('Выберите допустимое время размещений:', reply_markup=btns_inline_time)

@router.callback_query(SelectTimeOpt.filter(F.step == "OPT CONFIRM TIME"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectTimeOpt):
    user_id=query.from_user.id
    await query.message.edit_text('Пришлите реквизиты для оплаты одним сообщением:')
    await set_state_user(user_id, "СОЗДАНИЕ ОПТА КРАИНЯЯ ПРИШЛИТЕ РЕКВИЗИТЫ")

@router.callback_query(CreationOptCallback.filter(F.step == "OPT CHANGE"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: CreationOptCallback):
    user_id=query.from_user.id
    answer = f"Создаём опт для канала {callback_data.value} Напишите стандартную(розничную) стоимость размещения:"
    await query.message.edit_text(answer)
    await set_state_user(user_id, "СОЗДАНИЕ ОПТА РОЗНИЧНАЯЯ СТОИМОСТЬ РАЗМЕЩЕНИЯ")

@router.callback_query(CreationOptCallback.filter(F.step == "OPT SAVE"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: CreationOptCallback):
    user_id=query.from_user.id
    await query.message.edit_text("Поздравляем! Опт успешно создан и добавлен в каталог.")
    await set_state_user(user_id, "АВТОРИЗИРОВАН")
