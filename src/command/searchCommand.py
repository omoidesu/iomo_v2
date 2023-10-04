import pickle

from khl import Bot, Guild

from src.card import search_card
from src.const import Assets
from src.dao import Redis
from src.dto import BeatmapSet, SearchListCacheDTO
from src.service import OsuApi, asset_service
from src.util import IdGenerator, filter_and_sort_beatmap_sets, search_beatmap_sets
from src.util.uploadAsset import download_and_upload, generate_diff_png_and_upload

id_generator = IdGenerator(1, 10)


async def search_command(bot: Bot, keyword: str, artist: str, title: str, source: str, guild: Guild):
    redis = Redis.instance().get_connection()
    api = OsuApi()
    emojis = []

    search_id = id_generator.get_id()
    search_maps, _ = await search_beatmap_sets(title, source, '')
    if len(search_maps) == 0:
        return '未找到相关谱面'

    search_maps = filter_and_sort_beatmap_sets(artist, title, search_maps)

    pages = [search_maps[i:i + 5] for i in range(0, len(search_maps), 5)]
    has_next = False
    if len(pages) > 1:
        cache_dto = SearchListCacheDTO(keyword, pages)
        redis.set(search_id, pickle.dumps(cache_dto))
        has_next = True

    # 资源上传
    kwargs = {}
    cover_url = {}
    for beatmapset in pages[0]:
        if source == 'sayo':
            beatmapset_info = await api.get_beatmapset_info(beatmapset.id)
            beatmapset = BeatmapSet(**beatmapset_info)

        if beatmapset.cover_list:
            cover_url[str(beatmapset.id)] = beatmapset.cover_list

        for beatmap in beatmapset.beatmaps:
            mode = beatmap.mode
            diff = beatmap.difficulty_rating
            if diff < 8:
                emoji = await generate_diff_png_and_upload(bot, mode, diff, emoji=True, guild=guild)
                emojis.append(emoji)
                kwargs[f'{mode}{diff}'] = f'(emj){emoji.name}(emj)[{emoji.id}]'
            else:
                kwargs[f'{mode}{diff}'] = Assets.Sticker.DIFF.get(mode)

    oss_url = asset_service.select_asset_batch(**cover_url)
    for beatmap_id, url in oss_url.items():
        if url:
            kwargs[f'cover{beatmap_id}'] = url
        else:
            kwargs[f'cover{beatmap_id}'] = await download_and_upload(bot, cover_url[beatmap_id], force=True)

    return search_card(keyword, pages[0], search_id, 0, next=has_next, **kwargs), emojis
