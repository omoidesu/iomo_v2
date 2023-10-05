from khl import Bot

from src.card import beatmap_set_card
from src.const import Assets
from src.service import OsuApi
from src.util.uploadAsset import download_and_upload, generate_diff_png_and_upload


async def beatmap_set_command(bot: Bot, beatmapset_id: int):
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

    return beatmap_set_card(beatmapset, **kwargs)
