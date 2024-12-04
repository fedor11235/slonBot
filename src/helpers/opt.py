from datetime import datetime, timedelta

from prisma.models import User, Opt

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from common.callback import CreationOptCallback, SelectDateOpt, SelectTimeOpt

async def set_opt(user_id, key, value):
    user = await User.prisma().find_unique(
        where={
            'tg_id': user_id,
        }
    ) 

    opt = await Opt.prisma().update(
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
    opt = await Opt.prisma().find_unique(
        where={
            'id': user.opt_edit,
        },
    )
    today = datetime.today() + timedelta(days=page * 10)

    date_list = [(today + timedelta(days=i)).date() for i in range(10)]

    inline_kb_list = [
        [
            InlineKeyboardButton(text="Дата", callback_data=SelectDateOpt(channel_id=user.opt_edit, step="EMPTY", value="", page=page).pack()),
            InlineKeyboardButton(text="Утро", callback_data=SelectDateOpt(channel_id=user.opt_edit, step="EMPTY", value="", page=page).pack()),
            InlineKeyboardButton(text="День", callback_data=SelectDateOpt(channel_id=user.opt_edit, step="EMPTY", value="", page=page).pack()),
            InlineKeyboardButton(text="Вечер", callback_data=SelectDateOpt(channel_id=user.opt_edit, step="EMPTY", value="", page=page).pack()),
        ]
    ]

    for date in date_list:
        date_str = ''
        if opt.date != None:
            date_str = opt.date.split(' ')
        inline_kb_list.append([
            InlineKeyboardButton(text=str(date.strftime("%d.%m")), callback_data=SelectDateOpt(channel_id=user.opt_edit, step="EMPTY", value="", page=page).pack()),
            InlineKeyboardButton(text=f"{'✅' if f'{date}/УТРО' in date_str else ' '}", callback_data=SelectDateOpt(channel_id=user.opt_edit, step="OPT SELECT DATE", value=f"{date}/УТРО", page=page).pack()),
            InlineKeyboardButton(text=f"{'✅' if f'{date}/ДЕНЬ' in date_str else ' '}", callback_data=SelectDateOpt(channel_id=user.opt_edit, step="OPT SELECT DATE", value=f"{date}/ДЕНЬ", page=page).pack()),
            InlineKeyboardButton(text=f"{'✅' if f'{date}/ВЕЧЕР' in date_str else ' '}", callback_data=SelectDateOpt(channel_id=user.opt_edit, step="OPT SELECT DATE", value=f"{date}/ВЕЧЕР", page=page).pack()),
        ])
    
    inline_kb_list.append([
        InlineKeyboardButton(text="Больше дат", callback_data=SelectDateOpt(channel_id=user.opt_edit, step="MORE DATE", value="" , page=page + 1).pack()),
        InlineKeyboardButton(text="Подтвердить", callback_data=SelectDateOpt(channel_id=user.opt_edit, step="CONFIRM DATE", value="", page=page).pack()),
    ])

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def set_opt_date(user_id, date):
    user = await User.prisma().find_unique(
        where={
            'tg_id': user_id,
        }
    ) 

    opt = await Opt.prisma().find_unique(
        where={
            'id': user.opt_edit,
        },
    )
    date_array = []
    if opt.date != None:
        date_array = opt.date.split(' ')

    if date in date_array:
        date_array.remove(date)

    else:
        date_array.append(date)

    date_str = None

    if len(date_array) > 0:
        date_str = ' '.join(date_array)

    opt = await Opt.prisma().update(
        where={
            'id': user.opt_edit,
        },
        data={
            "date": date_str,
        },
    )

async def get_btns_confirm_date(channel_id):
    inline_kb_list = [
        [
            InlineKeyboardButton(text="Изменить", callback_data=CreationOptCallback(channel_id=channel_id, step="DATE CHANGE", value="").pack()),
            InlineKeyboardButton(text="Подтвердить", callback_data=CreationOptCallback(channel_id=channel_id, step="DATE SAVE", value="").pack()),
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def get_btns_time(user_id):
    user = await User.prisma().find_unique(
        where={
            'tg_id': user_id,
        }
    ) 
    opt = await Opt.prisma().find_unique(
        where={
            'id': user.opt_edit,
        },
    )

    time_list = [
        ['8/10', '13/10', '18/10'],
        ['9/10', '14/10', '19/10'],
        ['10/10', '15/10', '20/10'],
        ['11/10', '16/10', '21/10'],
        ['12/10', '17/10', '22/10'],
    ]

    inline_kb_list = [
        [
            InlineKeyboardButton(text="Утро", callback_data=SelectTimeOpt(channel_id=user.opt_edit, step="EMPTY", value="").pack()),
            InlineKeyboardButton(text="День", callback_data=SelectTimeOpt(channel_id=user.opt_edit, step="EMPTY", value="").pack()),
            InlineKeyboardButton(text="Вечер", callback_data=SelectTimeOpt(channel_id=user.opt_edit, step="EMPTY", value="").pack()),
        ]
    ]

    for time_row in time_list:
        btn_time_row = []
        for time in time_row:
            time_str = ''
            if opt.time != None:
                time_str = opt.time.split(' ')
            btn_time_row.append(
                InlineKeyboardButton(text=f"{f'✅ {time}' if time in time_str else time}", callback_data=SelectTimeOpt(channel_id=user.opt_edit, step="OPT SELECT TIME", value=time).pack()),
            )
        inline_kb_list.append(btn_time_row)
    
    inline_kb_list.append([
        InlineKeyboardButton(text="Подтвердить", callback_data=SelectTimeOpt(channel_id=user.opt_edit, step="OPT CONFIRM TIME", value="").pack())
    ])

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def set_opt_time(user_id, time):
    user = await User.prisma().find_unique(
        where={
            'tg_id': user_id,
        }
    ) 

    opt = await Opt.prisma().find_unique(
        where={
            'id': user.opt_edit,
        },
    )
    time_array = []
    if opt.time != None:
        time_array = opt.time.split(' ')

    if time in time_array:
        time_array.remove(time)

    else:
        time_array.append(time)

    time_str = None

    if len(time) > 0:
        time_str = ' '.join(time_array)

    opt = await Opt.prisma().update(
        where={
            'id': user.opt_edit,
        },
        data={
            "time": time_str,
        },
    )

async def get_info_opt(user_id):
    user = await User.prisma().find_unique(
        where={
            'tg_id': user_id,
        }
    ) 

    opt = await Opt.prisma().find_unique(
        where={
            'id': user.opt_edit,
        },
        include={
            'channel': True,
        },
    )

    text = f'''
Опт от 26.11 в канале {opt.channel.title}\n
Розничная цена: {opt.retail_price}\n
Оптовая цена: {opt.wholesale_price}\n
Минимум постов: {opt.min_seats}\n
Максимум постов: {opt.max_seats}\n
Список дат: {opt.date}\n
Дедлайн: {opt.date_deadline}\n
Реквизиты: {opt.details}\n
'''
    return text

async def get_info_btn_opt(user_id):
    user = await User.prisma().find_unique(
        where={
            'tg_id': user_id,
        }
    ) 

    opt = await Opt.prisma().find_unique(
        where={
            'id': user.opt_edit,
        },
        include={
            'channel': True,
        },
    )
    inline_kb_list = [
        [
            InlineKeyboardButton(text="Изменить", callback_data=CreationOptCallback(channel_id=opt.channel.channel_id, step="OPT CHANGE", value=opt.channel.title).pack()),
            InlineKeyboardButton(text="Подтвердить", callback_data=CreationOptCallback(channel_id=opt.channel.channel_id, step="OPT SAVE", value=opt.channel.title).pack()),
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

