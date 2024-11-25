from prisma.models import User, Opt

async def set_opt(user_id, key, value):
    user = await User.prisma().find_unique(
        where={
            'tg_id': user_id,
        }
    ) 
    channel = await Opt.prisma().update(
        where={
            'id': user.opt_edit,
        },
        data={
            key: value,
        },
    )