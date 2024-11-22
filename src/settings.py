from aiogram import types, html

my_commands = [
    types.BotCommand(command='start', description='Рестарт бота'),
    types.BotCommand(command='channel', description='Мои каналы'),
    types.BotCommand(command='help', description='Помощь'),
    types.BotCommand(command='newopt', description='Создать опт'),
    types.BotCommand(command='getopt', description='Войти в опт'),
    types.BotCommand(command='business', description='Подборки'),
    types.BotCommand(command='profile', description='Профиль'),
    types.BotCommand(command='partners', description='Промокод')
]

my_keyboard_buttons = [
    [
      types.KeyboardButton(text="Профиль"),
    ],
    [
      types.KeyboardButton(text="Каталог"),
      types.KeyboardButton(text="Помощь")
    ]
]

messages_no_profile = f"{html.bold('Сначала создайте профиль')}\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\n\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\n\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы"
messages_help = f"{html.bold('Возникли вопросы')}?\n\nМы всегда готовы помочь вам с решением любых задач и ответить на все интересующие вопросы. Просто напишите нам: @slon_feedback"

message_profile = f'''
{html.bold('Здесь собирается информация, показывающая насколько вы Slon')}.\n\n
{html.bold('Подписка:')} {'базовый'}  действует до: {'всегда'}
{html.bold('Ваши каналы:')}   0 
{html.bold('Создано оптов:')}  0 на сумму 0
{html.bold('Куплено оптов:')} Куплено оптов: 0 на сумму 0
{html.bold('Всего сэкономлено:')} Всего сэкономлено:  0
{html.bold('Приглашено пользователей:')}  0
'''