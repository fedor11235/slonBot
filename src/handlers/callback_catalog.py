from aiogram import Router, F, types

from common.callback import SetCategoryCatalogCallback

from helpers.catalog import get_btns_inline_channels_catalog
from helpers.user import set_state_user

router = Router()

@router.callback_query(SetCategoryCatalogCallback.filter(F.step == "GET CATEGORY"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SetCategoryCatalogCallback):
    user_id=query.from_user.id
    btns_inline_channel = await get_btns_inline_channels_catalog(category=callback_data.value)
    await query.message.edit_text("Выберите канал:", reply_markup=btns_inline_channel)
