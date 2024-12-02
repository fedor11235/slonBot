from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from common.callback import SelectCategoryIntoSuggestionsCallback, SelectDateIntoSuggestions

from prisma.models import User, Suggestions, IntoSuggestion

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
        channels = await Suggestions.prisma().find_many()
    else:
        channels = await Suggestions.prisma().find_many(
            where={
                'category': category,
            },
        )

    for channel in channels:
        inline_kb_list.append(
            [InlineKeyboardButton(text=channel.title, callback_data=SelectCategoryIntoSuggestionsCallback(step="SELECT CHANNEL", value=str(channel.id)).pack())],
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
            "suggestions": True
        },
    )

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
        if into_suggestion.suggestions.date != None:
            date_allowed_array = into_suggestion.suggestions.date.split(' ')
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
