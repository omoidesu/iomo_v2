from khl import Bot, Message

from src.command import score_command
from src.const import redis_recent_beatmap
from src.dao import Redis
from src.service import user_service
from src.util.log import save_log


async def compare_parser(bot: Bot, msg: Message):
    redis = Redis.instance().get_connection()
    redis_get = redis.get(redis_recent_beatmap.format(guild_id=msg.ctx.guild.id, channel_id=msg.ctx.channel.id))
    recent_beatmap = redis_get.decode('utf-8') if redis_get else None

    kook_id = save_log(msg)
    user = user_service.select_user(kook_id=int(kook_id))
    if user is None:
        return '你还没有绑定osu账号'

    if recent_beatmap is None:
        return '未找到该频道最近发送的成绩'

    return await score_command(bot, msg, '', '', '', recent_beatmap, 0, 0, user.osu_id, user.default_mode)
