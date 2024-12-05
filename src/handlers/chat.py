from aiogram import Router, F, types
from aiogram.filters import Command, CommandStart

from settings import my_keyboard_buttons, messages_no_profile, messages_help

# from dotenv import load_dotenv

from prisma.models import User, Channel, Post, IntoOpt, IntoSuggestion

from helpers.user import get_state_user, set_state_user
from helpers.categories import get_btns_inline_categories
from helpers.opt import set_opt, get_btns_date, get_btns_time, get_info_opt, get_info_btn_opt

from bot import bot

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
                user_сhannel = await Channel.prisma().upsert(
                    where={
                        'channel_id': chat.id,
                    },
                    data = {
                        'create': {
                            'channel_id': chat.id,
                            'username': chat.username,
                            'title': chat.title,
                            'type': 'ПОЛЬЗОВАТЕЛЬСКИЙ',
                            'admin': {
                                'connect': {
                                    'tg_id': user_id
                                }
                            }
                        },
                        'update': {},
                    },
                )
                await set_state_user(user_id, "ЗАДАЁТ КАТЕГОРИЮ")
                btns_inline_categories = await get_btns_inline_categories(chat.id)
                await message.answer('Введите категорию канала:', reply_markup=btns_inline_categories)
            except:
                await message.answer("Вы ввели некорректные данные")

        elif text != None and 'https' in text:
            try:
                username = '@' + text.split('/')[-1]
                chat = await bot.get_chat(username)
                bot_status = await bot.get_chat_member(chat_id=chat.id, user_id=bot.id)
                user_сhannel = await Channel.prisma().upsert(
                    where={
                        'channel_id': chat.id,
                    },
                    data = {
                        'create': {
                            'channel_id': chat.id,
                            'username': chat.username,
                            'title': chat.title,
                            'type': 'ПОЛЬЗОВАТЕЛЬСКИЙ',
                            'admin': {
                                'connect': {
                                    'tg_id': user_id
                                }
                            }
                        },
                        'update': {},
                    },
                )
                await set_state_user(user_id, "ЗАДАЁТ КАТЕГОРИЮ")
                btns_inline_categories = await get_btns_inline_categories(chat.id)
                await message.answer('Введите категорию канала:', reply_markup=btns_inline_categories)
            except:
                await message.answer("В пересланном канале нет бота")

        elif message.forward_origin != None:
            try:
                chat_id = message.forward_origin.chat.id
                username = message.forward_origin.chat.username
                title = message.forward_origin.chat.title
                bot_status = await bot.get_chat_member(chat_id=chat_id, user_id=bot.id)
                user_сhannel = await Channel.prisma().upsert(
                    where={
                        'channel_id': chat_id,
                    },
                    data = {
                        'create': {
                            'channel_id': chat_id,
                            'username': username,
                            'title': title,
                            'type': 'ПОЛЬЗОВАТЕЛЬСКИЙ',
                            'admin': {
                                'connect': {
                                    'tg_id': user_id
                                }
                            }
                        },
                        'update': {},
                    },
                )
                await set_state_user(user_id, "ЗАДАЁТ КАТЕГОРИЮ")
                btns_inline_categories = await get_btns_inline_categories(chat_id)
                await message.answer('Введите категорию канала:', reply_markup=btns_inline_categories)
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

    elif user_state == "СОЗДАНИЕ ОПТА КРАИНЯЯ ДАТА ФОРМИРОВАНИЯ ОПТА":
        await set_opt(user_id, "date_deadline", message.text)
        btns_inline_time = await get_btns_time(user_id)
        await message.answer('Выберите допустимое время размещений:', reply_markup=btns_inline_time)

    elif user_state == "СОЗДАНИЕ ОПТА КРАИНЯЯ ПРИШЛИТЕ РЕКВИЗИТЫ":
        await set_opt(user_id, "details", message.text)
        text = await get_info_opt(user_id)
        btns_inline_info = await get_info_btn_opt(user_id)
        await message.answer(text, reply_markup=btns_inline_info)

    elif user_state == "ЗАПИСЬ В ОПТ СОХРАНЕНИЕ ПОСТА":
        photo_path = ""
        video_path = ""
        animation_path = ""
        caption = message.caption
        text = message.text
        media_group_id = message.media_group_id

        user = await User.prisma().find_unique(
            where={
                'tg_id': user_id,
            }
        ) 

        into_opt = await IntoOpt.prisma().find_unique(
            where={
                'id': user.into_opt_edit,
            }
        )

        if message.photo != None and len(message.photo) > 0:
            photo_id = message.photo[-1].file_id
            photo_path = photo_id
            # file_info = await bot.get_file(photo_id)
            # file_name = f'{file_info.file_path.split("/")[-1]}'
            # photo_path = file_name
            # print("file_info: ", file_info)
            # await bot.download_file(file_info.file_path, f'media/{photo_path}')

        if message.video != None :
            video_id = message.video.file_id
            video_path = video_id
            # file_info = await bot.get_file(video_id)
            # file_name = f'{file_info.file_path.split("/")[-1]}'
            # video_path = file_name
            # await bot.download_file(file_info.file_path, f'media/{video_path}')

        if message.animation != None :
            animation_id = message.animation.file_id
            animation_path = animation_id
            # file_info = await bot.get_file(animation_id)
            # file_name = f'{file_info.file_path.split("/")[-1]}'
            # animation_path = file_name
            # print("animation_path: ", animation_path)
            # await bot.download_file(file_info.file_path, f'media/{animation_path}')

        user_сhannel = await Post.prisma().create(
            data = {
                'img_id': photo_path,
                'video_id': video_path,
                'animation_id': animation_path,
                'text': text,
                'caption': caption,
                'media_group_id': media_group_id,
                'into_opt': {
                    'connect': {
                        'id': into_opt.id
                    }
                }
            },
        )

        await message.answer("Пост отправлен владельцу опта")
        await set_state_user(user_id, "АВТОРИЗИРОВАН")

    elif user_state == "ЗАПИСЬ В ПОДБОРКУ СОХРАНЕНИЕ ПОСТА":
        photo_path = ""
        video_path = ""
        animation_path = ""
        caption = message.caption
        text = message.text
        media_group_id = message.media_group_id

        user = await User.prisma().find_unique(
            where={
                'tg_id': user_id,
            }
        ) 

        into_suggestion = await IntoSuggestion.prisma().find_unique(
            where={
                'id': user.into_suggestion_edit,
            }
        )

        if message.photo != None and len(message.photo) > 0:
            photo_id = message.photo[-1].file_id
            photo_path = photo_id
            # file_info = await bot.get_file(photo_id)
            # file_name = f'{file_info.file_path.split("/")[-1]}'
            # photo_path = file_name
            # print("file_info: ", file_info)
            # await bot.download_file(file_info.file_path, f'media/{photo_path}')

        if message.video != None :
            video_id = message.video.file_id
            video_path = video_id
            # file_info = await bot.get_file(video_id)
            # file_name = f'{file_info.file_path.split("/")[-1]}'
            # video_path = file_name
            # await bot.download_file(file_info.file_path, f'media/{video_path}')

        if message.animation != None :
            animation_id = message.animation.file_id
            animation_path = animation_id
            # file_info = await bot.get_file(animation_id)
            # file_name = f'{file_info.file_path.split("/")[-1]}'
            # animation_path = file_name
            # print("animation_path: ", animation_path)
            # await bot.download_file(file_info.file_path, f'media/{animation_path}')

        user_сhannel = await Post.prisma().create(
            data = {
                'img_id': photo_path,
                'video_id': video_path,
                'animation_id': animation_path,
                'text': text,
                'caption': caption,
                'media_group_id': media_group_id,
                'into_suggestion': {
                    'connect': {
                        'id': into_suggestion.id
                    }
                }
            },
        )

        await message.answer("Пост отправлен владельцу опта")
        await set_state_user(user_id, "АВТОРИЗИРОВАН")






        
    # elif user_state == "ЗАДАЁТ КАТЕГОРИЮ":
    #     channel_id = db_redis.get('channel_id')


    else:
        await message.answer("Всё шикарно")
