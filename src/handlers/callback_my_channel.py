from aiogram import Router, F, types
from aiogram import types, html

from common.callback import SelectMyChannelCallback

from helpers.my_channel import get_my_channel

router = Router()

@router.callback_query(SelectMyChannelCallback.filter(F.step == "SELECT CHANNEL"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: SelectMyChannelCallback):
    channel_id = int(callback_data.value)
    channel = await get_my_channel(channel_id)
    await query.message.edit_text(f'''
{html.bold('Информация о канале:')}
{html.bold('Категория:')} {channel.category}
{html.bold('Юзернейм:')} {channel.username}
{html.bold('Заголовок:')} {channel.title}
{html.bold('Айди канала:')} {channel.channel_id}
''')
