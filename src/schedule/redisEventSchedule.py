from khl import Bot

from src.command import mp_command
from src.config import redis_subscribe
from src.dao import Redis


async def redis_schedule(bot: Bot):
    pubsub = Redis.instance().pubsub
    msg = pubsub.get_message()
    if msg and msg['channel'].decode('utf-8') == redis_subscribe and isinstance(msg['data'], bytes):
        data = msg['data'].decode('utf-8')
        if data.startswith('mp-'):
            mp_command.remove_room(bot, data.replace('mp-', ''), 0)
