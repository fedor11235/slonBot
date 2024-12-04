from aiogram import Router, F, types

from common.callback import SetCategoryCatalogCallback

from helpers.categories import categories_map
from helpers.user import set_state_user

# from prisma.models import User

router = Router()

@router.callback_query(SetCategoryCatalogCallback.filter(F.step == "SET CATEGORY"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SetCategoryCatalogCallback):
    user_id=query.from_user.id
    await set_category_channel(callback_data.channel_id, callback_data.value)
    answer = f"Вы задали категорию {categories_map[callback_data.value]}"
    await query.message.edit_text(answer)
    # await set_state_user(user_id, "АВТОРИЗИРОВАН")
