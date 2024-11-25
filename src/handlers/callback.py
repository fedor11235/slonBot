from aiogram import Router, F, types

from common.callback import SetCategoryCallback, CreationOptCallback

from helpers.channel import set_category_channel
from helpers.categories import categories_map
from helpers.user import get_state_user, set_state_user

from prisma.models import User, Opt

router = Router()

@router.callback_query(SetCategoryCallback.filter(F.step == "SET CATEGORY"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SetCategoryCallback):
    user_id=query.from_user.id
    await set_category_channel(callback_data.channel_id, callback_data.value)
    answer = f"Вы задали категорию {categories_map[callback_data.value]}"
    await query.message.delete()
    await query.message.answer("Канал успешно добавлен")
    await set_state_user(user_id, "АВТОРИЗИРОВАН")

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

@router.callback_query()
async def my_callback_foo(query: types.CallbackQuery):
    await query.answer("Всё остальное")