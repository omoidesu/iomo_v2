from khl import Bot, Message

from src.card import recent_card, score_card
from src.const import redis_recent_beatmap
from src.dao import Redis
from src.dao.models import OsuBeatmapSet
from src.dto import RecentListCacheDTO
from src.exception import OsuApiException
from src.service import OsuApi, SayoApi, beatmap_set_service
from src.util.uploadAsset import download_and_upload, generate_diff_png_and_upload

redis = Redis.instance().get_connection()


async def recent_command(bot: Bot, msg: Message, osu_name: str, mode: str, mod: list, order: int, include_fail: bool,
                         ls_mode: bool):
    api = OsuApi()

    if not str(osu_name).isdigit():
        osu_info = await api.get_user(osu_name)
        osu_name = osu_info.get('id')
        if mode == '':
            mode = osu_info.get('playmode')

    try:
        recent_score = await api.get_recent_score(osu_name, mode=mode, include_fail=include_fail, use_mode=True,
                                                  limit=20)
    except OsuApiException as e:
        return e.do_except('该用户不存在'), None
    else:
        if len(recent_score) == 0:
            return '该用户没有最近游玩记录', None

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

            recent_score = recent_score[:5]
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

            card_msg, id_map = recent_card(recent_score, **kwargs)
            dto = RecentListCacheDTO(
                id_map=id_map, osu_id=osu_name, osu_mode=mode, include_fail=include_fail, guild_id=msg.ctx.guild.id,
                author_id=msg.author_id, msg_id=msg.id
            )

            return card_msg, dto

        # 如果输入的order大于记录数则查找最后一个记录
        if order:
            if order > len(recent_score):
                score = recent_score[-1]
            else:
                score = recent_score[order - 1]
        else:
            score = recent_score[0]

        beatmap_set = score.get('beatmapset', {})
        beatmap = score.get('beatmap', {})
        kwargs = {}
        # 封面
        cover: str = beatmap_set.get('covers', {}).get('list')
        if cover is not None:
            kwargs['cover'] = await download_and_upload(bot, cover)
        # 试听
        preview = 'https:' + beatmap_set.get('preview_url')
        if preview is not None:
            kwargs['preview'] = await download_and_upload(bot, preview)

        difficult = beatmap.get('difficulty_rating')
        kwargs['star'] = await generate_diff_png_and_upload(bot, mode, difficult)

        # 保存beatmapset
        if beatmap_set:
            beatmap_set_service.insert(OsuBeatmapSet(
                beatmapset_id=beatmap_set.get('id'), title=beatmap_set.get('title'), artist=beatmap_set.get('artist'),
                title_unicode=beatmap_set.get('title_unicode'), artist_unicode=beatmap_set.get('artist_unicode'),
                creator=beatmap_set.get('creator')
            ))

        # 获取max combo
        beatmap_info = await api.get_beatmap_info(beatmap.get('id'))
        kwargs['fc_combo'] = beatmap_info.get('max_combo')

        # todo: 计算模拟pp
        kwargs['fc'] = '-'
        kwargs['95'] = '-'
        kwargs['97'] = '-'
        kwargs['98'] = '-'
        kwargs['99'] = '-'
        kwargs['ss'] = '-'

        redis_key = redis_recent_beatmap.format(guild_id=msg.ctx.guild.id, channel_id=msg.ctx.channel.id)
        redis.set(redis_key, beatmap.get('id'))

        return score_card(score, beatmap, beatmap_set, **kwargs), None
