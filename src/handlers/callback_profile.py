from aiogram import Router, F, types, html

from prisma.models import User, Opt

from common.callback import ProfileCallback

from helpers.profile import get_btns_profile, get_btn_back_menu

router = Router()

@router.callback_query(ProfileCallback.filter(F.step == "MY OPT"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: ProfileCallback):
    user_id=query.from_user.id

@router.callback_query(ProfileCallback.filter(F.step == "RELEASE SCHEDULE"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: ProfileCallback):
    user_id=query.from_user.id

@router.callback_query(ProfileCallback.filter(F.step == "STATISTICS"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: ProfileCallback):
    user_id=query.from_user.id
    user = await User.prisma().find_unique(
        where={
            'tg_id': user_id,
        },
        include={
            'channels': {
                'include': {
                    'opt': True
                }
            }
        }
    )
    opts = []
    opts_sum = 0
    for channel in user.channels:
      if channel.opt != None:
        opts.append(channel.opt)
    opts_count = len(opts)
    channels_count = len(user.channels)

    btns_inline = await get_btn_back_menu()
    await query.message.edit_text(f'''
{html.bold('Здесь собирается информация, показывающая насколько вы Slon')}.\n\n
{html.bold('Подписка:')} {user.tariff_plan}  действует до: {user.tariff_end}
{html.bold('Ваши каналы:')} {channels_count}
{html.bold('Создано оптов:')} {opts_count} на сумму {opts_sum}
{html.bold('Куплено оптов:')} {user.by_opt_count} на сумму {user.by_opt_sum}
{html.bold('Всего сэкономлено:')} Всего сэкономлено:  {user.total_saved}
{html.bold('Приглашено пользователей:')}  {user.invited_users}
''',  reply_markup=btns_inline)

@router.callback_query(ProfileCallback.filter(F.step == "BALANCE"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: ProfileCallback):
    user_id=query.from_user.id

@router.callback_query(ProfileCallback.filter(F.step == "MENU"))
async def my_callback_foo(query: types.CallbackQuery, callback_data: ProfileCallback):
    btns_inline_profile = await get_btns_profile()
    await query.message.edit_text('Это ваш профиль, тут вы можете:', reply_markup=btns_inline_profile)