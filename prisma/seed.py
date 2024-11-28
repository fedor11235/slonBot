import asyncio

from prisma import Prisma
from prisma.models import Admin

prisma = Prisma(auto_register=True)

async def main():
    await prisma.connect()
    admin = await Admin.prisma().create({})
    await prisma.disconnect()

if __name__ == '__main__':
    asyncio.run(main())