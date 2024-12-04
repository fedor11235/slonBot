from datetime import datetime, timedelta

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from common.callback import SelectCategoryIntoOptCallback, SelectDateIntoOpt, CreationIntoOptCallback, SelectTimeIntoOpt

from prisma.models import User, Channel, IntoOpt

async def get_btns_inline_categories_into_opt():
    inline_kb_list = [
        [InlineKeyboardButton(text="Все тематики", callback_data=SelectCategoryIntoOptCallback(step="SELECT CATEGORY", value="ALL").pack())],
        [InlineKeyboardButton(text="Образование", callback_data=SelectCategoryIntoOptCallback(step="SELECT CATEGORY", value="EDUCATION").pack())],
        [InlineKeyboardButton(text="Финансы", callback_data=SelectCategoryIntoOptCallback(step="SELECT CATEGORY", value="FINANCE").pack()) ],
        [InlineKeyboardButton(text="Здоровье", callback_data=SelectCategoryIntoOptCallback(step="SELECT CATEGORY", value="HEALTH").pack())],
        [InlineKeyboardButton(text="Новости", callback_data=SelectCategoryIntoOptCallback(step="SELECT CATEGORY", value="NEWS").pack())],
        [InlineKeyboardButton(text="IT ", callback_data=SelectCategoryIntoOptCallback(step="SELECT CATEGORY", value="IT").pack())],
        [InlineKeyboardButton(text="Развлечения", callback_data=SelectCategoryIntoOptCallback(step="SELECT CATEGORY", value="ENTERTAINMENT").pack())],
        [InlineKeyboardButton(text="Психология", callback_data=SelectCategoryIntoOptCallback(step="SELECT CATEGORY", value="PSYCHOLOGY").pack())],
        [InlineKeyboardButton(text="Видосники", callback_data=SelectCategoryIntoOptCallback(step="SELECT CATEGORY", value="VIDEO").pack())],
        [InlineKeyboardButton(text="Авторские", callback_data=SelectCategoryIntoOptCallback(step="SELECT CATEGORY", value="AUTHOR'S").pack())],
        [InlineKeyboardButton(text="Другое", callback_data=SelectCategoryIntoOptCallback(step="SELECT CATEGORY", value="OTHER").pack())],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def get_btns_inline_channels_into_opt(category):
    channels = []
    inline_kb_list = []

    if category == 'ALL':
        channels = await Channel.prisma().find_many(
            include={
                'opt': True
            }
        )
    else:
        channels = await Channel.prisma().find_many(
            where={
                'category': category,
            },
            include={
                'opt': True
            }
        )

    for channel in channels:
        if channel.opt:
            inline_kb_list.append(
                [InlineKeyboardButton(text=channel.title, callback_data=SelectCategoryIntoOptCallback(step="SELECT CHANNEL", value=str(channel.channel_id)).pack())],
            )

    inline_kb_list.append(
        [InlineKeyboardButton(text="Назад", callback_data=SelectCategoryIntoOptCallback(step="SELECT CHANNEL BACK", value="").pack())],
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def get_btns_inline_date_into_opt(user_id, page=0):
    user = await User.prisma().find_unique(
        where={
            'tg_id': user_id,
        }
    ) 
    into_opt = await IntoOpt.prisma().find_unique(
        where={
            'id': user.into_opt_edit,
        },
        include={
            'channel': {
                "include": {
                    "opt": True
                }
            },
        },
    )

    today = datetime.today() + timedelta(days=page * 10)

    date_list = [(today + timedelta(days=i)).date() for i in range(10)]

    inline_kb_list = [
        [
            InlineKeyboardButton(text="Дата", callback_data=SelectDateIntoOpt(channel_id=user.into_opt_edit, step="EMPTY", value="", page=page).pack()),
            InlineKeyboardButton(text="Утро", callback_data=SelectDateIntoOpt(channel_id=user.into_opt_edit, step="EMPTY", value="", page=page).pack()),
            InlineKeyboardButton(text="День", callback_data=SelectDateIntoOpt(channel_id=user.into_opt_edit, step="EMPTY", value="", page=page).pack()),
            InlineKeyboardButton(text="Вечер", callback_data=SelectDateIntoOpt(channel_id=user.into_opt_edit, step="EMPTY", value="", page=page).pack()),
        ]
    ]

    for date in date_list:
        date_allowed_array = []
        date_selected_array = []
        if into_opt.channel.opt.date != None:
            date_allowed_array = into_opt.channel.opt.date.split(' ')
        if into_opt.date != None:
            date_selected_array = into_opt.date.split(' ')

        inline_kb_list.append([
            InlineKeyboardButton(text=str(date.strftime("%d.%m")), callback_data=SelectDateIntoOpt(channel_id=user.into_opt_edit, step="EMPTY", value="", page=page).pack()),
            InlineKeyboardButton(text=f"{('✅' if f'{date}/УТРО' in date_selected_array else ' ') if f'{date}/УТРО' in date_allowed_array else '❌'}", callback_data=SelectDateIntoOpt(channel_id=user.into_opt_edit, step=f"{'INOPT SELECT DATE' if f'{date}/УТРО' in date_allowed_array else 'EMPTY'}", value=f"{date}/УТРО", page=page).pack()),
            InlineKeyboardButton(text=f"{('✅' if f'{date}/ДЕНЬ' in date_selected_array else ' ')  if f'{date}/ДЕНЬ' in date_allowed_array else '❌'}", callback_data=SelectDateIntoOpt(channel_id=user.into_opt_edit, step=f"{'INOPT SELECT DATE' if f'{date}/ДЕНЬ' in date_allowed_array else 'EMPTY'}", value=f"{date}/ДЕНЬ", page=page).pack()),
            InlineKeyboardButton(text=f"{('✅' if f'{date}/ВЕЧЕР' in date_selected_array else ' ')  if f'{date}/ВЕЧЕР' in date_allowed_array else '❌'}", callback_data=SelectDateIntoOpt(channel_id=user.into_opt_edit, step=f"{'INOPT SELECT DATE' if f'{date}/ВЕЧЕР' in date_allowed_array else 'EMPTY'}", value=f"{date}/ВЕЧЕР", page=page).pack()),
        ])
    
    inline_kb_list.append([
        InlineKeyboardButton(text="Больше дат", callback_data=SelectDateIntoOpt(channel_id=user.into_opt_edit, step="MORE DATE", value="" , page=page + 1).pack()),
        InlineKeyboardButton(text="Подтвердить", callback_data=SelectDateIntoOpt(channel_id=user.into_opt_edit, step="CONFIRM DATE", value="", page=page).pack()),
    ])

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def set_into_opt_date(user_id, date):
    user = await User.prisma().find_unique(
        where={
            'tg_id': user_id,
        }
    ) 

    into_opt = await IntoOpt.prisma().find_unique(
        where={
            'id': user.into_opt_edit,
        },
    )
    date_array = []
    if into_opt.date != None:
        date_array = into_opt.date.split(' ')

    if date in date_array:
        date_array.remove(date)

    else:
        date_array.append(date)

    date_str = None

    if len(date_array) > 0:
        date_str = ' '.join(date_array)

    into_opt = await IntoOpt.prisma().update(
        where={
            'id': user.into_opt_edit,
        },
        data={
            "date": date_str,
        },
    )

async def get_btns_confirm_date(channel_id):
    inline_kb_list = [
        [
            InlineKeyboardButton(text="Изменить", callback_data=CreationIntoOptCallback(channel_id=channel_id, step="DATE CHANGE", value="").pack()),
            InlineKeyboardButton(text="Подтвердить", callback_data=CreationIntoOptCallback(channel_id=channel_id, step="DATE SAVE", value="").pack()),
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def get_btns_time(user_id):
    user = await User.prisma().find_unique(
        where={
            'tg_id': user_id,
        },
    ) 
    into_opt = await IntoOpt.prisma().find_unique(
        where={
            'id': user.into_opt_edit,
        },
        include={
            'channel': {
                "include": {
                    "opt": True
                }
            },
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
            InlineKeyboardButton(text="Утро", callback_data=SelectTimeIntoOpt(channel_id=user.opt_edit, step="EMPTY", value="").pack()),
            InlineKeyboardButton(text="День", callback_data=SelectTimeIntoOpt(channel_id=user.opt_edit, step="EMPTY", value="").pack()),
            InlineKeyboardButton(text="Вечер", callback_data=SelectTimeIntoOpt(channel_id=user.opt_edit, step="EMPTY", value="").pack()),
        ]
    ]

    for time_row in time_list:
        btn_time_row = []
        for time in time_row:
            time_selected_array = []
            time_allowed_array = []
            if into_opt.channel.opt.time != None:
                time_allowed_array = into_opt.channel.opt.time.split(' ')
            if into_opt.time != None:
                time_selected_array = into_opt.time.split(' ')
            btn_time_row.append(
                InlineKeyboardButton(text=f"{(f'{time} ✅' if time in time_selected_array else time) if time in time_allowed_array else f'{time} ❌'}", callback_data=SelectTimeIntoOpt(channel_id=user.opt_edit, step=f"{'INOPT SELECT TIME' if time in time_allowed_array else 'EMPTY'}" , value=time).pack()),
            )

        inline_kb_list.append(btn_time_row)
    
    inline_kb_list.append([
        InlineKeyboardButton(text="Подтвердить", callback_data=SelectTimeIntoOpt(channel_id=user.opt_edit, step="CONFIRM TIME", value="").pack())
    ])

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def set_opt_time(user_id, time):
    user = await User.prisma().find_unique(
        where={
            'tg_id': user_id,
        }
    ) 

    into_opt = await IntoOpt.prisma().find_unique(
        where={
            'id': user.into_opt_edit,
        },
    )
    time_array = []
    if into_opt.time != None:
        time_array = into_opt.time.split(' ')

    if time in time_array:
        time_array.remove(time)

    else:
        time_array.append(time)

    time_str = None

    if len(time) > 0:
        time_str = ' '.join(time_array)

    into_opt = await IntoOpt.prisma().update(
        where={
            'id': user.into_opt_edit,
        },
        data={
            "time": time_str,
        },
    )
