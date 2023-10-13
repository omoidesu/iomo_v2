import asyncio

from khl import Bot, Message

from src.card import score_card
from src.const import Assets, redis_recent_beatmap
from src.dao import Redis
from src.dao.models import OsuBeatmapSet
from src.exception import OsuApiException
from src.service import OsuApi, beatmap_set_service, simulate_pp_if_fc, simulate_pp_with_accuracy
from src.util import filter_and_sort_beatmap_sets, search_beatmap_sets
from src.util.uploadAsset import generate_stars, upload_asset, user_not_found_card


async def score_command(bot: Bot, msg: Message, artist: str, title: str, source: str, beatmap_id: int,
                        beatmapset_id: int, order: int, osu_name: str, mode: str, order_mode: bool = False):
    api = OsuApi()

    if order_mode and not order:
        return '未知错误: 参数order解析为空'

    if order_mode and order > 50:
        return 'order参数过大'

    if not order_mode and not osu_name:
        return '未知错误: 参数osu_name解析为空'

    if not order_mode and not str(osu_name).isdigit():
        try:
            osu_info = await api.get_user(osu_name)
        except OsuApiException as e:
            return await user_not_found_card(bot, e.do_except(f'找不到名为{osu_name}的玩家'))
        else:
            osu_name = osu_info.get('id')
            if mode == '':
                mode = osu_info.get('playmode')

    if beatmap_id:
        beatmap_info = await api.get_beatmap_info(beatmap_id)
        beatmapset_info = beatmap_info.get('beatmapset')
        beatmaps = [beatmap_info]
    elif beatmapset_id:
        beatmaps, beatmapset_info = await get_beatmaps_by_beatmapset_id(api, beatmapset_id, mode)
        if isinstance(beatmaps, str):
            return beatmaps
    else:
        search_maps, _ = await search_beatmap_sets(title, source, '', mode if mode == 'osu' else None)
        if len(search_maps) == 0:
            return '未找到相关谱面'
        search_maps = filter_and_sort_beatmap_sets(artist, title, search_maps)
        beatmapset_id = search_maps[0].id
        beatmaps, beatmapset_info = await get_beatmaps_by_beatmapset_id(api, beatmapset_id, mode)
        if isinstance(beatmaps, str):
            return beatmaps

    if len(beatmaps) == 0:
        return '未找到相关谱面'

    if order_mode:
        beatmap_info = beatmaps[0]
        top_score_json = await api.get_beatmap_top_score(beatmap_info.get('id'), mode)
        top_scores = top_score_json.get('scores')
        if len(top_scores) == 0:
            return '该谱面没有排行榜'

        # order的数字由用户输入
        if order - 1 > len(top_scores):
            return f'该谱面只有{len(top_scores)}条成绩'

        score_info = top_scores[order - 1]
        return await upload_assets_and_generate_card(bot, msg, score_info, beatmap_info, beatmapset_info, order, mode)

    for beatmap_info in beatmaps:
        try:
            score_info = await api.get_beatmap_score(beatmap_info.get('id'), osu_name, mode=mode)
        except OsuApiException as e:
            if e.code == 404:
                continue
            e.do_except('')
        else:
            return await upload_assets_and_generate_card(bot, msg, score_info.get('score'), beatmap_info,
                                                         beatmapset_info, score_info.get('position'), mode)

    return '未找到相关谱面'


async def get_beatmaps_by_beatmapset_id(api, beatmapset_id: int, mode: str):
    try:
        beatmapset_info = await api.get_beatmapset_info(beatmapset_id)
    except OsuApiException as e:
        return e.do_except('该谱面集不存在'), None
    else:
        # 谱面状态为0: pending, -1: wip, -2: graveyard不记录成绩
        if beatmapset_info.get('ranked') <= 0:
            return '该谱面没有排行榜', None
        beatmaps = beatmapset_info.get('beatmaps')
        if mode:
            beatmaps = filter(lambda x: x.get('mode') == mode, beatmaps)
        beatmaps = sorted(beatmaps, key=lambda x: x.get('difficulty_rating'), reverse=True)
        return beatmaps, beatmapset_info


async def upload_assets_and_generate_card(bot: Bot, msg: Message, score: dict, beatmap: dict, beatmap_set: dict,
                                          position: int, mode: str):
    redis = Redis.instance().get_connection()

    kwargs = {'position': position}

    tasks = []

    cover: str = beatmap_set.get('covers', {}).get('list')
    if cover:
        tasks.append(asyncio.create_task(upload_asset(bot, cover, kwargs, 'cover', Assets.Image.DEFAULT_COVER)))
    else:
        kwargs['cover'] = Assets.Image.OSU_LOGO
    # 试听
    if beatmap_set.get('preview_url'):
        tasks.append(
            asyncio.create_task(
                upload_asset(bot, 'https:' + beatmap_set.get('preview_url'), kwargs, 'preview', Assets.Audio.WELCOME)))

    difficult = beatmap.get('difficulty_rating')
    tasks.append(
        asyncio.create_task(generate_stars(bot, mode if mode else beatmap.get('mode'), difficult, kwargs, 'star')))

    beatmap_set_service.insert(OsuBeatmapSet(
        beatmapset_id=beatmap_set.get('id'), title=beatmap_set.get('title'), artist=beatmap_set.get('artist'),
        title_unicode=beatmap_set.get('title_unicode'), artist_unicode=beatmap_set.get('artist_unicode'),
        creator=beatmap_set.get('creator')
    ))

    kwargs['fc_combo'] = beatmap.get('max_combo')

    if mode != 'mania':
        beatmap_id = beatmap.get('id')
        mods = score.get('mods')
        statistics = score.get('statistics')
        await simulate_pp_with_accuracy(beatmap_id, 100, mode, '')
        tasks.append(asyncio.create_task(simulate_if_fc(beatmap_id, mode, mods, statistics, kwargs, 'fc')))
        tasks.append(asyncio.create_task(get_osu_pp(beatmap_id, 95, mode, mods, kwargs, '95')))
        tasks.append(asyncio.create_task(get_osu_pp(beatmap_id, 97, mode, mods, kwargs, '97')))
        tasks.append(asyncio.create_task(get_osu_pp(beatmap_id, 98, mode, mods, kwargs, '98')))
        tasks.append(asyncio.create_task(get_osu_pp(beatmap_id, 99, mode, mods, kwargs, '99')))
        tasks.append(asyncio.create_task(get_osu_pp(beatmap_id, 100, mode, mods, kwargs, 'ss')))

    redis_key = redis_recent_beatmap.format(guild_id=msg.ctx.guild.id, channel_id=msg.ctx.channel.id)
    redis.set(redis_key, beatmap.get('id'))

    await asyncio.wait(tasks)
    return score_card(score, beatmap, beatmap_set, **kwargs)


async def get_osu_pp(beatmap_id: int, accuracy: float, mode: str, mods: str, to: dict, key: str):
    to[key] = await simulate_pp_with_accuracy(beatmap_id, accuracy, mode, mods)


async def simulate_if_fc(beatmap_id: int, mode: str, mods: list, statistics: dict, to: dict, key: str):
    to[key] = await simulate_pp_if_fc(beatmap_id, mode, mods, statistics)
