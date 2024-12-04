from aiogram import Router, F, types

from common.callback import SetCategoryCatalogCallback, SelectCategoryCatalogCallback

from helpers.catalog import get_btns_inline_categories_catalog, get_btns_inline_channels_catalog
from helpers.user import set_state_user

from prisma.models import Channel
router = Router()

@router.callback_query(SetCategoryCatalogCallback.filter(F.step == "GET CATEGORY"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SetCategoryCatalogCallback):
    user_id=query.from_user.id
    btns_inline_channel = await get_btns_inline_channels_catalog(category=callback_data.value)
    await query.message.edit_text("Выберите канал:", reply_markup=btns_inline_channel)

@router.callback_query(SelectCategoryCatalogCallback.filter(F.step == "SELECT CHANNEL"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectCategoryCatalogCallback):
    user_id=query.from_user.id
    channel_id = int(callback_data.value)

    channel = await Channel.prisma().find_unique(
        where={
            'channel_id': channel_id,
        }
    )

    await query.message.edit_text(f'''
Информация о канале:
Категория: {channel.category}
Юзернейм: {channel.username}
Заголовок: {channel.title}
Айди канала: {channel.channel_id}
''')

@router.callback_query(SelectCategoryCatalogCallback.filter(F.step == "SELECT CHANNEL BACK"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectCategoryCatalogCallback):
    btns_inline_categories = await get_btns_inline_categories_catalog()
    await query.message.edit_text('Выберите категорию:', reply_markup=btns_inline_categories)
