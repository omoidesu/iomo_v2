from src.behavior.uploadAsset import download_and_upload, generate_diff_png_and_upload
from src.service import OsuApi, user_info_service, beatmap_set_service
from src.exception import OsuApiException
from src.card import user_card, recent_card
from khl import Bot, Message
from src.dao import Redis
from src.const import redis_recent_beatmap
from src.dao.models import OsuBeatmapSet

redis = Redis.instance().get_connection()


async def info_behavior(bot: Bot, osu_name: str, mode: str, day: int, user_id):
    api = OsuApi()

    try:
        if mode == '':
            user_info = await api.get_user(osu_name)
        else:
            user_info = await api.get_user(osu_name, mode=mode, use_mode=True)
    except OsuApiException as e:
        if e.code == 401:
            return e.message
        elif e.code == 404:
            return '该用户不存在'
        else:
            return f'未知错误，code:{e.code}'
    else:
        if user_id:
            compare_info = user_info_service.select_user_info(user_id, mode=mode, day=day)
        else:
            compare_info = None

        cover = user_info.get('cover_url')
        kwargs = {'mode': mode}
        if cover is not None:
            kwargs['cover'] = await download_and_upload(bot, cover)

        return user_card(user_info, compare_user_info=compare_info, **kwargs)


async def recent_behavior(bot: Bot, msg: Message, osu_name: str, mode: str, mod: list, order: int, include_fail: bool,
                          ls_mode: bool):
    api = OsuApi()

    if not str(osu_name).isdigit():
        osu_info = await api.get_user(osu_name)
        osu_name = osu_info.get('id')
        if mode == '':
            mode = osu_info.get('playmode')

    try:
        recent_score = await api.get_recent_score(osu_name, mode=mode, include_fail=include_fail, use_mode=True,
                                                  limit=5 if ls_mode else 20)
    except OsuApiException as e:
        if e.code == 401:
            return e.message
        elif e.code == 404:
            return '该用户不存在'
        else:
            return f'未知错误，code:{e.code}'
    else:
        if len(recent_score) == 0:
            return '该用户没有最近游玩记录'

        # 如果输入是NM则只查找没有mod的记录
        if len(mod) == 1 and mod[0] == 'NM':
            for i in range(len(recent_score) - 1, -1, -1):
                game_play = recent_score[i]
                if game_play.get('mods', []):
                    recent_score.pop(i)
        # 如果输入的mod不是NM则查找mod包含于输入mod的记录
        elif len(mod) > 0:
            for i in range(len(recent_score) - 1, -1, -1):
                game_play = recent_score[i]
                if not set(mod).issubset(game_play.get('mods', [])):
                    recent_score.pop(i)

        kwargs = {'mode': mode}

        if ls_mode:
            kwargs['osu_name'] = recent_score[0].get('user', {}).get('username')

            recent_score = recent_score[:10]
            stars = {}
            for score in recent_score:
                difficult = score.get('beatmap', {}).get('difficulty_rating')
                stars[difficult] = await generate_diff_png_and_upload(bot, mode, difficult)

                # 保存beatmapset
                beatmap_set = score.get('beatmapset', {})
                if beatmap_set:
                    beatmap_set_service.insert(OsuBeatmapSet(
                        beatmapset_id=beatmap_set.get('id'), title=beatmap_set.get('title'),
                        artist=beatmap_set.get('artist'),
                        title_unicode=beatmap_set.get('title_unicode'),
                        artist_unicode=beatmap_set.get('artist_unicode'),
                        creator=beatmap_set.get('creator')
                    ))

                cover = beatmap_set.get('covers', {}).get('list')
                if cover is not None:
                    kwargs[f"{beatmap_set.get('id')}"] = await download_and_upload(bot, cover)

            kwargs['stars'] = stars

            return recent_card(recent_score, **kwargs)

        # # 如果输入的order大于记录数则查找最后一个记录
        # if order > len(recent_score):
        #     score = recent_score[-1]
        # else:
        #     score = recent_score[order]
        #
        # kwargs = {}
        # cover: str = score.get('beatmapset', {}).get('covers', {}).get('list')
        # if cover is not None:
        #     kwargs['cover'] = await download_and_upload(bot, cover)
        #
        # # 保存beatmapset
        # beatmap_set = score.get('beatmapset', {})
        # if beatmap_set:
        #     beatmap_set_service.insert(OsuBeatmapSet(
        #         beatmapset_id=beatmap_set.get('id'), title=beatmap_set.get('title'), artist=beatmap_set.get('artist'),
        #         title_unicode=beatmap_set.get('title_unicode'), artist_unicode=beatmap_set.get('artist_unicode'),
        #         creator=beatmap_set.get('creator')
        #     ))
        #
        # # todo: 计算模拟pp
        # kwargs['95'] = '-'
        # kwargs['97'] = '-'
        # kwargs['98'] = '-'
        # kwargs['99'] = '-'
        # kwargs['100'] = '-'
        #
        # redis_key = redis_recent_beatmap.format(guild_id=msg.ctx.guild.id, channel_id=msg.ctx.channel.id)
        # redis.set(redis_key, score.get('beatmap', {}).get('id'))

        # return
