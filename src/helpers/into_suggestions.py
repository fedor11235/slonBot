from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from common.callback import SelectCategoryIntoSuggestionsCallback, SelectDateIntoSuggestions, CreationIntoSuggestionsCallback, SelectTimeIntoSuggestions

from prisma.models import User, Suggestions, IntoSuggestion, Channel

async def get_btns_inline_categories_into_suggestions():
    inline_kb_list = [
        [InlineKeyboardButton(text="Все тематики", callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CATEGORY", value="ALL").pack())],
        [InlineKeyboardButton(text="Образование", callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CATEGORY", value="EDUCATION").pack())],
        [InlineKeyboardButton(text="Финансы", callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CATEGORY", value="FINANCE").pack()) ],
        [InlineKeyboardButton(text="Здоровье", callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CATEGORY", value="HEALTH").pack())],
        [InlineKeyboardButton(text="Новости", callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CATEGORY", value="NEWS").pack())],
        [InlineKeyboardButton(text="IT ", callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CATEGORY", value="IT").pack())],
        [InlineKeyboardButton(text="Развлечения", callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CATEGORY", value="ENTERTAINMENT").pack())],
        [InlineKeyboardButton(text="Психология", callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CATEGORY", value="PSYCHOLOGY").pack())],
        [InlineKeyboardButton(text="Видосники", callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CATEGORY", value="VIDEO").pack())],
        [InlineKeyboardButton(text="Авторские", callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CATEGORY", value="AUTHOR'S").pack())],
        [InlineKeyboardButton(text="Другое", callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CATEGORY", value="OTHER").pack())],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def get_btns_inline_channels_into_suggestions(category):
    channels = []
    inline_kb_list = []

    if category == 'ALL':
        channels = await Channel.prisma().find_many()
    else:
        channels = await Channel.prisma().find_many(
            where={
                'category': category,
            }
        )

    for channel in channels:
        if channel.type=='ПОДБОРКА':
            inline_kb_list.append(
                [InlineKeyboardButton(text=channel.title, callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CHANNEL", value=str(channel.channel_id)).pack())],
            )

    inline_kb_list.append(
        [InlineKeyboardButton(text="Назад", callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CHANNEL BACK", value="").pack())],
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def get_btns_inline_date_into_suggestion(user_id, page=0):
    user = await User.prisma().find_unique(
        where={
            'tg_id': user_id,
        }
    ) 
    into_suggestion = await IntoSuggestion.prisma().find_unique(
        where={
            'id': user.into_suggestion_edit,
        },
        include={
            'channel': {
                "include": {
                    "suggestions": True
                }
            },
        },
    )

    print("into_suggestion: ", into_suggestion)

    today = datetime.today() + timedelta(days=page * 10)

    date_list = [(today + timedelta(days=i)).date() for i in range(10)]

    inline_kb_list = [
        [
            InlineKeyboardButton(text="Дата", callback_data=SelectDateIntoSuggestions(channel_id=user.into_suggestion_edit, step="EMPTY", value="", page=page).pack()),
            InlineKeyboardButton(text="Утро", callback_data=SelectDateIntoSuggestions(channel_id=user.into_suggestion_edit, step="EMPTY", value="", page=page).pack()),
            InlineKeyboardButton(text="День", callback_data=SelectDateIntoSuggestions(channel_id=user.into_suggestion_edit, step="EMPTY", value="", page=page).pack()),
            InlineKeyboardButton(text="Вечер", callback_data=SelectDateIntoSuggestions(channel_id=user.into_suggestion_edit, step="EMPTY", value="", page=page).pack()),
        ]
    ]

    for date in date_list:
        date_allowed_array = []
        date_selected_array = []
        if into_suggestion.channel.suggestions.date != None:
            date_allowed_array = into_suggestion.channel.suggestions.date.split(' ')
        if into_suggestion.date != None:
            date_selected_array = into_suggestion.date.split(' ')

        inline_kb_list.append([
            InlineKeyboardButton(text=str(date.strftime("%d.%m")), callback_data=SelectDateIntoSuggestions(channel_id=user.into_suggestion_edit, step="EMPTY", value="", page=page).pack()),
            InlineKeyboardButton(text=f"{('✅' if f'{date}/УТРО' in date_selected_array else ' ') if f'{date}/УТРО' in date_allowed_array else '❌'}", callback_data=SelectDateIntoSuggestions(channel_id=user.into_suggestion_edit, step=f"{'INOPT SELECT DATE' if f'{date}/УТРО' in date_allowed_array else 'EMPTY'}", value=f"{date}/УТРО", page=page).pack()),
            InlineKeyboardButton(text=f"{('✅' if f'{date}/ДЕНЬ' in date_selected_array else ' ')  if f'{date}/ДЕНЬ' in date_allowed_array else '❌'}", callback_data=SelectDateIntoSuggestions(channel_id=user.into_suggestion_edit, step=f"{'INOPT SELECT DATE' if f'{date}/ДЕНЬ' in date_allowed_array else 'EMPTY'}", value=f"{date}/ДЕНЬ", page=page).pack()),
            InlineKeyboardButton(text=f"{('✅' if f'{date}/ВЕЧЕР' in date_selected_array else ' ')  if f'{date}/ВЕЧЕР' in date_allowed_array else '❌'}", callback_data=SelectDateIntoSuggestions(channel_id=user.into_suggestion_edit, step=f"{'INOPT SELECT DATE' if f'{date}/ВЕЧЕР' in date_allowed_array else 'EMPTY'}", value=f"{date}/ВЕЧЕР", page=page).pack()),
        ])
    
    inline_kb_list.append([
        InlineKeyboardButton(text="Больше дат", callback_data=SelectDateIntoSuggestions(channel_id=user.into_suggestion_edit, step="MORE DATE", value="" , page=page + 1).pack()),
        InlineKeyboardButton(text="Подтвердить", callback_data=SelectDateIntoSuggestions(channel_id=user.into_suggestion_edit, step="CONFIRM DATE", value="", page=page).pack()),
    ])

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def set_into_suggestion_date(user_id, date):
    user = await User.prisma().find_unique(
        where={
            'tg_id': user_id,
        }
    ) 

    into_suggestion = await IntoSuggestion.prisma().find_unique(
        where={
            'id': user.into_suggestion_edit,
        },
    )
    date_array = []
    if into_suggestion.date != None:
        date_array = into_suggestion.date.split(' ')

    if date in date_array:
        date_array.remove(date)

    else:
        date_array.append(date)

    date_str = None

    if len(date_array) > 0:
        date_str = ' '.join(date_array)

    into_suggestion = await IntoSuggestion.prisma().update(
        where={
            'id': user.into_suggestion_edit,
        },
        data={
            "date": date_str,
        },
    )

async def get_btns_confirm_date(channel_id):
    inline_kb_list = [
        [
            InlineKeyboardButton(text="Изменить", callback_data=CreationIntoSuggestionsCallback(channel_id=channel_id, step="DATE CHANGE", value="").pack()),
            InlineKeyboardButton(text="Подтвердить", callback_data=CreationIntoSuggestionsCallback(channel_id=channel_id, step="DATE SAVE", value="").pack()),
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def get_btns_time(user_id):
    user = await User.prisma().find_unique(
        where={
            'tg_id': user_id,
        },
    ) 
    into_suggestion = await IntoSuggestion.prisma().find_unique(
        where={
            'id': user.into_suggestion_edit,
        },
        include={
            'channel': {
                "include": {
                    "suggestions": True
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
            InlineKeyboardButton(text="Утро", callback_data=SelectTimeIntoSuggestions(channel_id=user.into_suggestion_edit, step="EMPTY", value="").pack()),
            InlineKeyboardButton(text="День", callback_data=SelectTimeIntoSuggestions(channel_id=user.into_suggestion_edit, step="EMPTY", value="").pack()),
            InlineKeyboardButton(text="Вечер", callback_data=SelectTimeIntoSuggestions(channel_id=user.into_suggestion_edit, step="EMPTY", value="").pack()),
        ]
    ]

    for time_row in time_list:
        btn_time_row = []
        for time in time_row:
            time_selected_array = []
            time_allowed_array = []
            if into_suggestion.channel.suggestions.time != None:
                time_allowed_array = into_suggestion.channel.suggestions.time.split(' ')
            if into_suggestion.time != None:
                time_selected_array = into_suggestion.time.split(' ')
            btn_time_row.append(
                InlineKeyboardButton(text=f"{(f'{time} ✅' if time in time_selected_array else time) if time in time_allowed_array else f'{time} ❌'}", callback_data=SelectTimeIntoSuggestions(channel_id=user.into_suggestion_edit, step=f"{'INTOSUG SELECT TIME' if time in time_allowed_array else 'EMPTY'}" , value=time).pack()),
            )

        inline_kb_list.append(btn_time_row)
    
    inline_kb_list.append([
        InlineKeyboardButton(text="Подтвердить", callback_data=SelectTimeIntoSuggestions(channel_id=user.into_suggestion_edit, step="CONFIRM TIME", value="").pack())
    ])

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def set_suggestions_time(user_id, time):
    user = await User.prisma().find_unique(
        where={
            'tg_id': user_id,
        }
    ) 

    into_suggestion = await IntoSuggestion.prisma().find_unique(
        where={
            'id': user.into_suggestion_edit,
        },
    )
    time_array = []
    if into_suggestion.time != None:
        time_array = into_suggestion.time.split(' ')

    if time in time_array:
        time_array.remove(time)

    else:
        time_array.append(time)

    time_str = None

    if len(time) > 0:
        time_str = ' '.join(time_array)

    into_suggestion = await IntoSuggestion.prisma().update(
        where={
            'id': user.into_suggestion_edit,
        },
        data={
            "time": time_str,
        },
    )

