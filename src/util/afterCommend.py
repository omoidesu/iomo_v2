from khl import Bot, Guild, GuildEmoji, Message

from src.const import game_modes
from src.dao import Redis
from src.dao.models import OsuUserInfo
from src.dto import RecentListCacheDTO
from src.service import OsuApi, user_info_service
from .messageUtil import construct_message_obj


async def collect_user_info(**kwargs):
    api = OsuApi()
    osu_infos = await api.get_users(*kwargs.keys())

    users = osu_infos.get('users', [])
    data_list = []
    for user in users:
        osu_id = user.get('id')
        user_id = kwargs.get(str(osu_id))
        statistics = user.get('statistics_rulesets')
        for mode in game_modes:
            mode_statistics = statistics.get(mode)
            if mode_statistics is None:
                data_list.append(OsuUserInfo(user_id=user_id, mode=mode))
            else:
                global_rank = mode_statistics.get('global_rank')
                game_level = mode_statistics.get('level', {'current': 0}).get('current')
                level_progress = mode_statistics.get('level', {'progress': 0}).get('progress')
                pp = mode_statistics.get('pp')
                accuracy = round(mode_statistics.get('hit_accuracy'), 2)
                play_count = mode_statistics.get('play_count')
                play_time = mode_statistics.get('play_time')
                ssh_count = mode_statistics.get('grade_counts', {'ssh': 0}).get('ssh')
                ss_count = mode_statistics.get('grade_counts', {'ss': 0}).get('ss')
                sh_count = mode_statistics.get('grade_counts', {'sh': 0}).get('sh')
                s_count = mode_statistics.get('grade_counts', {'s': 0}).get('s')
                a_count = mode_statistics.get('grade_counts', {'a': 0}).get('a')
                data_list.append(OsuUserInfo(
                    user_id=user_id, mode=mode, global_rank=global_rank, game_level=game_level,
                    level_progress=level_progress, pp=pp, accuracy=accuracy, play_count=play_count, play_time=play_time,
                    ssh_count=ssh_count, ss_count=ss_count, sh_count=sh_count, s_count=s_count, a_count=a_count
                ))

    user_info_service.insert_batch(data_list)


def cache_map_to_redis(msg_id: str, dto: RecentListCacheDTO):
    redis = Redis.instance().get_connection()

    redis.set(msg_id, dto.to_json_str())
    redis.expire(msg_id, 24 * 60 * 60)


async def add_reaction(bot: Bot, msg_id: str, raw_msg: Message, user_id: str, dto: RecentListCacheDTO):
    msg = construct_message_obj(bot, msg_id, raw_msg.ctx.channel.id, raw_msg.ctx.channel.id, user_id)

    for emoji in dto.id_map.keys():
        await msg.add_reaction(emoji)


async def delete_emojis(guild: Guild, emojis: list[GuildEmoji]):
    for emoji in emojis:
        await guild.delete_emoji(emoji)
