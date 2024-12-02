from prisma import Prisma
from prisma.models import Admin, Suggestions

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
    title
):
    await prisma.connect()
    suggestions = await Suggestions.prisma().create(
        data = {
            'username': username,
            'retail_price': retail_price,
            'wholesale_price': wholesale_price,
            'min_seats': min_seats,
            'max_seats': max_seats,
            'details': details,
            'date': date,
            'time': time,
            'category': category,
            'title': title
        },
    )
    await prisma.disconnect()
    return suggestions