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

    search_id = id_generator.get_id()
    search_maps, _ = await search_beatmap_sets(title, source, '')
    if len(search_maps) == 0:
        return '未找到相关谱面'

    search_maps = filter_and_sort_beatmap_sets(artist, title, search_maps)

    # 每页谱面数
    step = 5
    pages = [search_maps[i:i + step] for i in range(0, len(search_maps), step)]
    has_next = False
    if len(pages) > 1:
        cache_dto = SearchListCacheDTO(keyword, source, pages)
        redis.set(f'search:{search_id}', pickle.dumps(cache_dto))
        has_next = True

    return await upload_assets_and_generate_search_card(bot, guild, source, pages[0], keyword, search_id, 0, len(pages),
                                                        has_next=has_next)


async def upload_assets_and_generate_search_card(bot: Bot, guild: Guild, source: str, beatmapsets: list[BeatmapSet],
                                                 keyword: str, search_id: int, current_page: int, total_page: int,
                                                 has_next: bool = False, has_prev: bool = False):
    api = OsuApi()
    emojis = []
    # 资源上传
    kwargs = {}
    cover_url = {}
    for beatmapset in beatmapsets:
        if source == 'sayo':
            beatmapset_info = await api.get_beatmapset_info(beatmapset.id)
            beatmapset = BeatmapSet(**beatmapset_info)

        if beatmapset.cover_list:
            cover_url[str(beatmapset.id)] = beatmapset.cover_list

        beatmaps_count = len(beatmapset.beatmaps)
        if beatmaps_count > 15:
            max_diff = 14
        else:
            max_diff = 15

        for beatmap in beatmapset.beatmaps[:max_diff]:
            # 搜索卡片每个谱面最多展示15个难度，过多会折行，如果超过15个应该展示14个难度，剩下的用+n表示

            mode = beatmap.mode
            diff = beatmap.difficulty_rating
            if diff < 8:
                if kwargs.get(f'{mode}{diff}'):
                    continue
                emoji = await generate_diff_png_and_upload(bot, mode, diff, emoji=True, guild=guild)
                emojis.append(emoji)
                kwargs[f'{mode}{diff}'] = f'(emj){emoji.name}(emj)[{emoji.id}]'
            else:
                kwargs[f'{mode}{diff}'] = Assets.Sticker.DIFF.get(mode)

    oss_url = asset_service.select_asset_batch(**cover_url)
    for beatmapset_id, url in oss_url.items():
        if url:
            kwargs[f'cover{beatmapset_id}'] = url
        else:
            kwargs[f'cover{beatmapset_id}'] = await download_and_upload(bot, cover_url[beatmapset_id], force=True)

    return search_card(keyword, beatmapsets, search_id, current_page, total_page, prev=has_prev, next=has_next,
                       **kwargs), emojis
