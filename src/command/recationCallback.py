import asyncio

from khl import Bot

from src.card import score_card
from src.const import Assets, redis_recent_beatmap
from src.dao.models import OsuBeatmapSet
from src.dto import RecentListCacheDTO
from src.service import OsuApi, beatmap_set_service, simulate_pp_if_fc, simulate_pp_with_accuracy
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
        tasks.append(asyncio.create_task(upload_asset(bot, cover, kwargs, 'cover', Assets.Image.DEFAULT_COVER)))
    else:
        kwargs['cover'] = Assets.Image.DEFAULT_COVER
    # 试听
    preview = 'https:' + beatmap_set.get('preview_url')
    if preview is not None:
        tasks.append(asyncio.create_task(upload_asset(bot, preview, kwargs, 'preview', Assets.Audio.WELCOME)))

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

    mode = score.get('mode')

    if mode != 'mania':
        beatmap_id = beatmap.get('id')
        mods = score.get('mods')
        statistics = score.get('statistics')
        await simulate_pp_with_accuracy(beatmap_id, 100, mode, [])
        tasks.append(asyncio.create_task(simulate_if_fc(beatmap_id, mode, mods, statistics, kwargs)))
        tasks.append(asyncio.create_task(simulate_pp(beatmap_id, 95, mode, mods, kwargs, '95')))
        tasks.append(asyncio.create_task(simulate_pp(beatmap_id, 97, mode, mods, kwargs, '97')))
        tasks.append(asyncio.create_task(simulate_pp(beatmap_id, 98, mode, mods, kwargs, '98')))
        tasks.append(asyncio.create_task(simulate_pp(beatmap_id, 99, mode, mods, kwargs, '99')))
        tasks.append(asyncio.create_task(simulate_pp(beatmap_id, 100, mode, mods, kwargs, 'ss')))

        if 'HR' in mods:
            kwargs['cs'] = round(beatmap.get('cs') * 1.3, 2)
            kwargs['hp'] = round(beatmap.get('drain') * 1.4, 2)
        elif 'EZ' in mods:
            kwargs['cs'] = round(beatmap.get('cs') * 0.5, 2)
            kwargs['hp'] = round(beatmap.get('drain') * 0.5, 2)

    redis_key = redis_recent_beatmap.format(guild_id=dto.guild_id, channel_id=channel_id)
    redis_connector.set(redis_key, score.get('beatmap', {}).get('id'))

    await asyncio.wait(tasks)
    return score_card(score, beatmap, beatmap_set, **kwargs)


async def get_max_combo(api: OsuApi, beatmap_id: int, to: dict, key: str):
    beatmap_info = await api.get_beatmap_info(beatmap_id)
    to[key] = beatmap_info.get('max_combo')


async def simulate_pp(beatmap_id: int, accuracy: float, mode: str, mods: list, to: dict, key: str):
    to[key] = await simulate_pp_with_accuracy(beatmap_id, accuracy, mode, mods)


async def simulate_if_fc(beatmap_id: int, mode: str, mods: list, statistics: dict, to: dict):
    to['fc'], to['star_rating'], to['ar'], to['od'] = await simulate_pp_if_fc(beatmap_id, mode, mods, statistics)
