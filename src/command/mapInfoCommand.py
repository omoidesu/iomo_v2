import asyncio

from khl import Bot

from src.card import beatmap_card, beatmap_set_card
from src.const import Assets
from src.service import OsuApi
from src.util.uploadAsset import generate_stars, upload_asset


async def beatmap_set_command(bot: Bot, beatmapset_id: int, beatmap_id: int = None):
    api = OsuApi()
    kwargs = {}
    tasks = []

    beatmapset = await api.get_beatmapset_info(beatmapset_id)
    covers = beatmapset.get('covers', {})
    if covers:
        tasks.append(upload_asset(bot, covers.get('cover'), kwargs, 'cover'))
        tasks.append(upload_asset(bot, covers.get('list'), kwargs, 'cover_list'))
    else:
        kwargs['cover'] = Assets.Image.DEFAULT_COVER
        kwargs['cover_list'] = Assets.Image.OSU_LOGO

    for beatmap in beatmapset.get('beatmaps'):
        mode = beatmap.get('mode')
        diff = beatmap.get('difficulty_rating')
        tasks.append(generate_stars(bot, mode, diff, kwargs, f'{mode}{diff}'))

    preview = beatmapset.get('preview_url')
    if preview:
        tasks.append(upload_asset(bot, 'https:' + preview, kwargs, 'preview'))

    avatar = beatmapset.get('user', {}).get('avatar_url')
    if avatar:
        tasks.append(upload_asset(bot, avatar, kwargs, 'avatar'))
    else:
        kwargs['avatar'] = Assets.Image.DEFAULT_AVATAR

    await asyncio.wait(tasks)
    return beatmap_set_card(beatmapset, beatmap_id, **kwargs)


async def beatmap_command(bot: Bot, beatmap_id: int):
    api = OsuApi()
    kwargs = {}
    tasks = []

    beatmap = await api.get_beatmap_info(beatmap_id)
    cover = beatmap.get('beatmapset', {}).get('covers', {}).get('list')
    if cover:
        tasks.append(asyncio.create_task(upload_asset(bot, cover, kwargs, 'cover')))
    else:
        kwargs['cover'] = Assets.Image.OSU_LOGO

    tasks.append(
        asyncio.create_task(generate_stars(bot, beatmap.get('mode'), beatmap.get('difficulty_rating'), kwargs, 'diff')))

    return beatmap_card(beatmap, **kwargs), beatmap.get('beatmapset', {}).get('id'), beatmap.get('id')
