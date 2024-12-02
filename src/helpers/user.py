from prisma.models import User

async def getActiveUser(user_id):
    user = await User.prisma().find_unique(
        where={
            'tg_id': user_id,
        }
    )
    if user == None:
        return False
    is_active = user.state == "ЗАПУСТИЛ БОТА"
    return is_active

async def get_state_user(user_id):
    user = await User.prisma().find_unique(
            where={
                'tg_id': user_id,
            }
      )
    if user == None:
        return "НЕ ЗАПУСТИЛ БОТА"
    return user.state

async def set_state_user(user_id, state):
    print("set_state_user !!!!!!!!!!!!!!!!!!")
    user = await User.prisma().update(
        where={
            'tg_id': user_id,
        },
        data={
            'state': state,
        },
    )