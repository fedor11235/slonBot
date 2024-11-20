
from prisma.models import User

async def getActiveUser(user_id):
    user = await User.prisma().find_unique(
          where={
              'tg_id': user_id,
          }
      )
    return user.is_active