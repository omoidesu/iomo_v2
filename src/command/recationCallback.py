import asyncio

from khl import Bot

from src.card import score_card
from src.const import Assets, redis_recent_beatmap
from src.dao.models import OsuBeatmapSet
from src.dto import RecentListCacheDTO
from src.service import OsuApi, beatmap_set_service
from src.util.uploadAsset import generate_stars, upload_asset


async def reaction_callback(bot: Bot, redis_connector, channel_id: int, score_id: str, dto: RecentListCacheDTO):
    api = OsuApi()

    recent_score = await api.get_recent_score(dto.osu_id, dto.osu_mode, 50, include_fail=dto.include_fail,
                                              use_mode=True)
    if len(recent_score) == 0:
        return '找不到这个记录'

    target_score = [score for score in recent_score if score.get('id') == score_id]
    if not target_score:
        return '找不到这个记录'

    score = target_score[0]

    beatmap = score.get('beatmap', {})
    beatmap_set = score.get('beatmapset', {})
    kwargs = {}
    tasks = []
    # 封面
    cover: str = beatmap_set.get('covers', {}).get('list')
    if cover:
        tasks.append(asyncio.create_task(upload_asset(bot, cover, kwargs, 'cover')))
    else:
        kwargs['cover'] = Assets.Image.DEFAULT_COVER
    # 试听
    preview = 'https:' + beatmap_set.get('preview_url')
    if preview is not None:
        tasks.append(asyncio.create_task(upload_asset(bot, preview, kwargs, 'preview')))

    difficult = score.get('beatmap', {}).get('difficulty_rating')
    tasks.append(asyncio.create_task(generate_stars(bot, dto.osu_mode, difficult, kwargs, 'star')))

    # 保存beatmapset
    if beatmap_set:
        beatmap_set_service.insert(OsuBeatmapSet(
            beatmapset_id=beatmap_set.get('id'), title=beatmap_set.get('title'), artist=beatmap_set.get('artist'),
            title_unicode=beatmap_set.get('title_unicode'), artist_unicode=beatmap_set.get('artist_unicode'),
            creator=beatmap_set.get('creator')
        ))

    # 取得max combo
    tasks.append(asyncio.create_task(get_max_combo(api, beatmap.get('id'), kwargs, 'fc_combo')))

    # todo: 计算模拟pp
    kwargs['fc'] = '-'
    kwargs['95'] = '-'
    kwargs['97'] = '-'
    kwargs['98'] = '-'
    kwargs['99'] = '-'
    kwargs['ss'] = '-'

    redis_key = redis_recent_beatmap.format(guild_id=dto.guild_id, channel_id=channel_id)
    redis_connector.set(redis_key, score.get('beatmap', {}).get('id'))

    await asyncio.wait(tasks)
    return score_card(score, beatmap, beatmap_set, **kwargs)


async def get_max_combo(api: OsuApi, beatmap_id: int, to: dict, key: str):
    beatmap_info = await api.get_beatmap_info(beatmap_id)
    to[key] = beatmap_info.get('max_combo')
