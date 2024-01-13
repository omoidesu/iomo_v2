import asyncio

from khl import Bot

from src.card import beatmap_card, beatmap_set_card
from src.const import Assets
from src.service import IomoApi, OsuApi
from src.util.uploadAsset import download_audio_and_upload, generate_stars, upload_asset


async def beatmap_set_command(bot: Bot, beatmapset_id: int, beatmap_id: int = None):
    api = OsuApi()
    kwargs = {}
    tasks = []

    beatmapset = await api.get_beatmapset_info(beatmapset_id)
    covers = beatmapset.get('covers', {})
    if covers:
        tasks.append(upload_asset(bot, covers.get('cover'), kwargs, 'cover', Assets.Image.DEFAULT_COVER))
        tasks.append(upload_asset(bot, covers.get('list'), kwargs, 'cover_list', Assets.Image.OSU_LOGO))
    else:
        kwargs['cover'] = Assets.Image.DEFAULT_COVER
        kwargs['cover_list'] = Assets.Image.OSU_LOGO

    for beatmap in beatmapset.get('beatmaps'):
        mode = beatmap.get('mode')
        diff = beatmap.get('difficulty_rating')
        tasks.append(generate_stars(bot, mode, diff, kwargs, f'{mode}{diff}'))

    audio_url = await download_audio_and_upload(beatmapset_id)
    if audio_url:
        kwargs['preview'] = audio_url
    else:
        preview = beatmapset.get('preview_url')
        if preview:
            tasks.append(upload_asset(bot, 'https:' + preview, kwargs, 'preview', Assets.Audio.WELCOME))

    avatar = beatmapset.get('user', {}).get('avatar_url')
    if avatar:
        tasks.append(upload_asset(bot, avatar, kwargs, 'avatar', Assets.Image.DEFAULT_AVATAR))
    else:
        kwargs['avatar'] = Assets.Image.DEFAULT_AVATAR

    tasks.append(IomoApi.download_map(str(beatmapset_id)))

    await asyncio.wait(tasks)
    return beatmap_set_card(beatmapset, beatmap_id, **kwargs)


async def beatmap_command(bot: Bot, beatmap_id: int):
    api = OsuApi()
    kwargs = {}
    tasks = []

    beatmap = await api.get_beatmap_info(beatmap_id)
    beatmapset = beatmap.get('beatmapset')
    set_id = beatmapset.get('id')
    cover = beatmapset.get('covers', {}).get('list')
    if cover:
        tasks.append(asyncio.create_task(upload_asset(bot, cover, kwargs, 'cover', Assets.Image.DEFAULT_COVER)))
    else:
        kwargs['cover'] = Assets.Image.OSU_LOGO

    tasks.append(
        asyncio.create_task(generate_stars(bot, beatmap.get('mode'), beatmap.get('difficulty_rating'), kwargs, 'diff')))

    tasks.append(IomoApi.download_map(str(set_id)))

    await asyncio.wait(tasks)
    return beatmap_card(beatmap, **kwargs), set_id, beatmap.get('id')
