from khl import Bot

from src.card import beatmap_card, beatmap_set_card
from src.const import Assets
from src.service import OsuApi
from src.util.uploadAsset import download_and_upload, generate_diff_png_and_upload


async def beatmap_set_command(bot: Bot, beatmapset_id: int, beatmap_id: int = None):
    api = OsuApi()
    kwargs = {}

    beatmapset = await api.get_beatmapset_info(beatmapset_id)
    covers = beatmapset.get('covers', {})
    if covers:
        kwargs['cover'] = await download_and_upload(bot, covers.get('cover'))
        kwargs['cover_list'] = await download_and_upload(bot, covers.get('list'))
    else:
        kwargs['cover'] = Assets.Image.DEFAULT_COVER
        kwargs['cover_list'] = Assets.Image.OSU_LOGO

    for beatmap in beatmapset.get('beatmaps'):
        mode = beatmap.get('mode')
        diff = beatmap.get('difficulty_rating')
        kwargs[f'{mode}{diff}'] = await generate_diff_png_and_upload(bot, mode, diff)

    preview = beatmapset.get('preview_url')
    if preview:
        kwargs['preview'] = await download_and_upload(bot, 'https:' + preview)

    avatar = beatmapset.get('user', {}).get('avatar_url')
    if avatar:
        kwargs['avatar'] = await download_and_upload(bot, avatar)
    else:
        kwargs['avatar'] = Assets.Image.DEFAULT_AVATAR

    return beatmap_set_card(beatmapset, beatmap_id, **kwargs)


async def beatmap_command(bot: Bot, beatmap_id: int):
    api = OsuApi()
    kwargs = {}

    beatmap = await api.get_beatmap_info(beatmap_id)
    cover = beatmap.get('beatmapset', {}).get('covers', {}).get('list')
    kwargs['cover'] = await download_and_upload(bot, cover) if cover else Assets.Image.OSU_LOGO
    kwargs['diff'] = await generate_diff_png_and_upload(bot, beatmap.get('mode'), beatmap.get('difficulty_rating'))

    return beatmap_card(beatmap, **kwargs), beatmap.get('beatmapset', {}).get('id'), beatmap.get('id')
