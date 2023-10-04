import json

from khl import Bot, Message, PublicMessage
from khl.card import CardMessage


def construct_message_obj(bot: Bot, msg_id: str, channel_id: str, guild_id: str, user_id: str):
    return PublicMessage(
        msg_id=msg_id,
        _gate_=bot.client.gate,
        target_id=channel_id,
        author_id=user_id,
        extra={
            'guild_id': guild_id,
            'channel_name': '',
            'author': {
                'id': user_id,
            }
        }
    )


async def update_to_card(bot: Bot, msg: Message, content: CardMessage):
    method = 'POST'
    route = 'message/update'
    json_context = {
        'msg_id': msg.id,
        'content': json.dumps(content)
    }
    try:
        await bot.client.gate.request(method=method, route=route, json=json_context)
    except:
        await msg.delete()
        await msg.ctx.channel.send(content)
