from aiogram import Router, F, types

from common.callback import SetCategoryCallback

from helpers.channel import set_category_channel
from helpers.user import set_state_user

from prisma.models import User, Opt

router = Router()

@router.callback_query(SetCategoryCallback.filter(F.step == "SET CATEGORY"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SetCategoryCallback):
    user_id=query.from_user.id
    await set_category_channel(callback_data.channel_id, callback_data.value)
    await query.message.edit_text("Канал успешно добавлен")
    await set_state_user(user_id, "АВТОРИЗИРОВАН")
