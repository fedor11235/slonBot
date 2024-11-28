from prisma import Prisma
from prisma.models import Admin

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