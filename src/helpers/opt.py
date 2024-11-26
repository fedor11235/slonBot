from datetime import datetime, timedelta

from prisma.models import User, Opt

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.utils.keyboard import InlineKeyboardBuilder
from common.callback import SelectDateOpt

async def set_opt(user_id, key, value):
    user = await User.prisma().find_unique(
        where={
            'tg_id': user_id,
        }
    ) 

    channel = await Opt.prisma().update(
        where={
            'id': user.opt_edit,
        },
        data={
            key: value,
        },
    )

async def get_btns_date(user_id, page=0):
    user = await User.prisma().find_unique(
        where={
            'tg_id': user_id,
        }
    ) 

    today = datetime.today() + timedelta(days=page * 10)

    date_list = [(today + timedelta(days=i)).date() for i in range(10)]

    inline_kb_list = [
        [
            InlineKeyboardButton(text="Дата", callback_data=SelectDateOpt(channel_id=user.opt_edit, step="OPT SELECT DATE", value="EMPTY").pack()),
            InlineKeyboardButton(text="Утро", callback_data=SelectDateOpt(channel_id=user.opt_edit, step="OPT SELECT DATE", value="EMPTY").pack()),
            InlineKeyboardButton(text="День", callback_data=SelectDateOpt(channel_id=user.opt_edit, step="OPT SELECT DATE", value="EMPTY").pack()),
            InlineKeyboardButton(text="Вечер", callback_data=SelectDateOpt(channel_id=user.opt_edit, step="OPT SELECT DATE", value="EMPTY").pack()),
        ]
    ]

    for date in date_list:
        inline_kb_list.append([
            InlineKeyboardButton(text=str(date.strftime("%d.%m")), callback_data=SelectDateOpt(channel_id=user.opt_edit, step="OPT SELECT DATE", value="EMPTY").pack()),
            InlineKeyboardButton(text=" ", callback_data=SelectDateOpt(channel_id=user.opt_edit, step="OPT SELECT DATE", value=f"{date}/УТРО").pack()),
            InlineKeyboardButton(text=" ", callback_data=SelectDateOpt(channel_id=user.opt_edit, step="OPT SELECT DATE", value=f"{date}/ДЕНЬ").pack()),
            InlineKeyboardButton(text=" ", callback_data=SelectDateOpt(channel_id=user.opt_edit, step="OPT SELECT DATE", value=f"{date}/ВЕЧЕР").pack()),
        ])
    
    inline_kb_list.append([
        InlineKeyboardButton(text="Больше дат", callback_data=SelectDateOpt(channel_id=user.opt_edit, step="OPT SELECT DATE", value="EMPTY").pack()),
        InlineKeyboardButton(text="Подтвердить", callback_data=SelectDateOpt(channel_id=user.opt_edit, step="OPT SELECT DATE", value="EMPTY").pack()),
    ])

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def set_opt_date(user_id, date):
    user = await User.prisma().find_unique(
        where={
            'tg_id': user_id,
        }
    ) 

    channel = await Opt.prisma().find_unique(
        where={
            'id': user.opt_edit,
        },
    )
    date_array = []
    if channel.date != None:
        date_array = channel.date.split(' ')

    if date in date_array:
        date_array.remove(date)

    else:
        date_array.append(date)

    date_str = None

    if len(date_array) > 0:
        date_str = ' '.join(date_array)

    channel = await Opt.prisma().update(
        where={
            'id': user.opt_edit,
        },
        data={
            "date": date_str,
        },
    )