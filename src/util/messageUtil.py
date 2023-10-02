from khl import Bot, PublicMessage


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
