from aiogram import Router, F, types
from aiogram.filters import Command, CommandStart

from settings import my_keyboard_buttons, messages_no_profile, messages_help

# from dotenv import load_dotenv

from prisma.models import User, Channel

from helpers.user import get_state_user, set_state_user
from helpers.categories import get_btns_inline_categories
from helpers.opt import set_opt, get_btns_date, get_btns_time, get_info_opt, get_info_btn_opt

from bot import bot

# import redis
# db_redis = redis.Redis(host='localhost', port=6379, db=0)
# db_redis.ping()

router = Router()

@router.message()
async def command_message_handler(message: types.Message) -> None:
    user_id = message.chat.id

    user_state = await get_state_user(user_id)

    if user_state == "НЕ ЗАПУСТИЛ БОТА":
        await message.answer(messages_no_profile)

    elif user_state == "ЗАПУСТИЛ БОТА":
        text = message.text
        if text != None and '@' in text[0]:
            try:
                chat = await bot.get_chat(text)
                bot_status = await bot.get_chat_member(chat_id=chat.id, user_id=bot.id)
                user_сhannel = await Channel.prisma().create(
                    data = {
                        'channel_id': chat.id,
                        'username': chat.username,
                        'title': chat.title,
                        'admin': {
                            'connect': {
                                'tg_id': user_id
                            }
                        }
                    },
                )
                await set_state_user(user_id, "ЗАДАЁТ КАТЕГОРИЮ")
                btns_inline_categories = await get_btns_inline_categories(chat.id)
                await message.answer('Введите категорию канала:', reply_markup=btns_inline_categories)
                # db_redis.set('channel_id', chat.id)
            except:
                await message.answer("Вы ввели некорректные данные")

        elif text != None and 'https' in text:

            # try:
                username = '@' + text.split('/')[-1]
                chat = await bot.get_chat(username)
                bot_status = await bot.get_chat_member(chat_id=chat.id, user_id=bot.id)
                user_сhannel = await Channel.prisma().create(
                    data = {
                        'channel_id': chat.id,
                        'username': chat.username,
                        'title': chat.title,
                        'admin': {
                            'connect': {
                                'tg_id': user_id
                            }
                        }
                    },
                )
                await set_state_user(user_id, "ЗАДАЁТ КАТЕГОРИЮ")
                btns_inline_categories = await get_btns_inline_categories(chat.id)
                await message.answer('Введите категорию канала:', reply_markup=btns_inline_categories)
                # db_redis.set('channel_id', chat.id)
            # except:
            #     await message.answer("Вы ввели некорректные данные")

        elif message.forward_origin != None:
            try:
                chat_id = message.forward_origin.chat.id
                username = message.forward_origin.chat.username
                title = message.forward_origin.chat.title
                bot_status = await bot.get_chat_member(chat_id=chat_id, user_id=bot.id)
                user_сhannel = await Channel.prisma().create(
                    data = {
                        'channel_id': chat_id,
                        'username': username,
                        'title': title,
                        'admin': {
                            'connect': {
                                'tg_id': user_id
                            }
                        }
                    },
                )
                await set_state_user(user_id, "ЗАДАЁТ КАТЕГОРИЮ")
                btns_inline_categories = await get_btns_inline_categories(chat_id)
                await message.answer('Введите категорию канала:', reply_markup=btns_inline_categories)
                # db_redis.set('channel_id', chat_id)
            except:
                await message.answer("В пересланном канале нет бота")


        else:
            await message.answer(messages_no_profile)

    elif user_state == "СОЗДАНИЕ ОПТА РОЗНИЧНАЯЯ СТОИМОСТЬ РАЗМЕЩЕНИЯ":
        await set_opt(user_id, "retail_price", message.text)
        await message.answer('Напишите текущую(оптовую) стоимость размещения. Разница с розничной должна быть не менее 10%:')
        await set_state_user(user_id, "СОЗДАНИЕ ОПТА ОПТОВАЯ СТОИМОСТЬ РАЗМЕЩЕНИЯ")

    elif user_state == "СОЗДАНИЕ ОПТА ОПТОВАЯ СТОИМОСТЬ РАЗМЕЩЕНИЯ":
        await set_opt(user_id, "wholesale_price", message.text)
        await message.answer('Введите минимальное количество мест, необходимое для оформления опта(от 3 до 10):')
        await set_state_user(user_id, "СОЗДАНИЕ ОПТА МИНИМАЛЬНОЕ КОЛИЧЕСТВО МЕСТ")

    elif user_state == "СОЗДАНИЕ ОПТА МИНИМАЛЬНОЕ КОЛИЧЕСТВО МЕСТ":
        await set_opt(user_id, "min_seats", message.text)
        await message.answer('Введите максимальное допустимое количество мест в опте(до 30):')
        await set_state_user(user_id, "СОЗДАНИЕ ОПТА МАКСИМАЛЬНОЕ КОЛИЧЕСТВО МЕСТ")

    elif user_state == "СОЗДАНИЕ ОПТА МАКСИМАЛЬНОЕ КОЛИЧЕСТВО МЕСТ":
        await set_opt(user_id, "max_seats", message.text)
        btns_inline_date = await get_btns_date(user_id)
        await message.answer('Выберите доступные для брони слоты:' , reply_markup=btns_inline_date)
        # await set_state_user(user_id, "СОЗДАНИЕ ОПТА ДОСТУПНЫЕ СЛОТЫ")

    elif user_state == "СОЗДАНИЕ ОПТА КРАИНЯЯ ДАТА ФОРМИРОВАНИЯ ОПТА":
        await set_opt(user_id, "date_deadline", message.text)
        btns_inline_time = await get_btns_time(user_id)
        await message.answer('Выберите допустимое время размещений:', reply_markup=btns_inline_time)

    elif user_state == "СОЗДАНИЕ ОПТА КРАИНЯЯ ПРИШЛИТЕ РЕКВИЗИТЫ":
        await set_opt(user_id, "details", message.text)
        text = await get_info_opt(user_id)
        btns_inline_info = await get_info_btn_opt(user_id)
        await message.answer(text, reply_markup=btns_inline_info)







        
    # elif user_state == "ЗАДАЁТ КАТЕГОРИЮ":
    #     channel_id = db_redis.get('channel_id')


    else:
        await message.answer("Всё шикарно")
