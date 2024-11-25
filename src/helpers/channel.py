from prisma.models import Channel

async def set_category_channel(channel_id, category):
    channel = await Channel.prisma().update(
        where={
            'channel_id': channel_id,
        },
        data={
            'category': category,
        },
    )