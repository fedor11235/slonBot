from prisma import Prisma
from prisma.models import Admin, Suggestions, Channel

prisma = Prisma(auto_register=True)

async def handler_login(username, password):
    await prisma.connect()
    admin = await Admin.prisma().find_first(
        where={
            'username': username,
            'password': password,
        },
    )
    await prisma.disconnect()
    return admin

async def handler_get_suggestions():
    await prisma.connect()
    suggestions = await Suggestions.prisma().find_many()
    await prisma.disconnect()
    return suggestions

async def handler_create_suggestions(
    username,
    retail_price,
    wholesale_price,
    min_seats,
    max_seats,
    details,
    date,
    time,
    category,
    title,
    channel_id,
):
    await prisma.connect()
    channel = await Channel.prisma().upsert(
        where={
            'channel_id': channel_id,
        },
        data={
            'create': {
                'channel_id': channel_id,
                'username': username,
                'title': title,
                'category': category,
            },
            'update': {},
        }
    )
    suggestions = await Suggestions.prisma().upsert(
        where={
            'channel_id': channel_id,
        },
        data={
            'create': {
                'channel': {
                    'connect': {
                        'channel_id': channel_id
                    }
                },
                'retail_price': retail_price,
                'wholesale_price': wholesale_price,
                'min_seats': min_seats,
                'max_seats': max_seats,
                'details': details,
                'date': date,
                'time': time,
            },
            'update': {},
        }
    )
    await prisma.disconnect()
    return suggestions