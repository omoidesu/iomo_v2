from src.dto import BeatmapSet
from src.service import OsuApi, SayoApi
from src.const import osu_source, sayo_source


async def search_beatmap_sets(keyword: str, source: str, cursor_string: str, mode: str = None,
                              include_unrank: bool = False) -> \
        tuple[list[BeatmapSet], str]:
    if source == osu_source or source == '':
        api = OsuApi()
        search_result = await api.search_beatmapset(keyword, mode=mode, cursor_string=cursor_string,
                                                    include_unrank=include_unrank)
        return [BeatmapSet(**beatmap_set) for beatmap_set in search_result.get('beatmapsets')], search_result.get(
            'cursor_string')
    elif source == sayo_source:
        mode_id = 15 if mode is None else {'osu': 1, 'taiko': 2, 'fruits': 4, 'mania': 8}[mode]
        search_result = await SayoApi.search(keyword, mode_id, cursor_string, 31 if include_unrank else 7)
        return [BeatmapSet(**{
            'id': beatmap_set.get('sid'),
            'artist': beatmap_set.get('artist'),
            'artist_unicode': beatmap_set.get('artistU'),
            'creator': beatmap_set.get('creator'),
            'favorite_count': beatmap_set.get('favourite_count'),
            'play_count': beatmap_set.get('play_count'),
            'title': beatmap_set.get('title'),
            'title_unicode': beatmap_set.get('titleU')
        }) for beatmap_set in search_result.get('data')], search_result.get('endid')


def filter_and_sort_beatmap_sets(artist: str, title: str, beatmap_sets: list[BeatmapSet]) -> list[BeatmapSet]:
    if len(beatmap_sets) == 0:
        return beatmap_sets

    if title is None:
        return sorted(beatmap_sets, key=lambda x: x.play_count, reverse=True)

    # 根据artist筛选，剔除与artist不匹配的set
    if artist:
        # 输入的是字母数字，匹配beatmap_set.artist和beatmap_set.artist_unicode
        if artist.replace(' ', '').isalnum():
            beatmap_sets = list(
                filter(lambda x: artist.lower() in x.artist.lower() or artist.lower() in x.artist_unicode.lower,
                       beatmap_sets))
        # 输入的包含其他字符，只匹配beatmap_set.artist_unicode
        else:
            beatmap_sets = list(filter(lambda x: artist.lower() in x.artist_unicode.lower, beatmap_sets))

    # 排序
    beatmap_sets = sorted(beatmap_sets, key=lambda x: x.play_count, reverse=True)

    matching_beatmaps = []
    similar_beatmaps = []
    not_matching_beatmaps = []

    # 根据title筛选，分出三部分 1. 完全匹配 2. 包含 3. 不包含
    alphabet_only = title.replace(' ', '').isalnum()

    for beatmap_set in beatmap_sets:
        if alphabet_only:
            if title.lower() == beatmap_set.title.lower() or title.lower() == beatmap_set.title_unicode.lower():
                matching_beatmaps.append(beatmap_set)
            elif title.lower() in beatmap_set.title.lower() or title.lower() in beatmap_set.title_unicode.lower():
                similar_beatmaps.append(beatmap_set)
            else:
                not_matching_beatmaps.append(beatmap_set)
        else:
            if title.lower() == beatmap_set.title_unicode.lower():
                matching_beatmaps.append(beatmap_set)
            elif title.lower() in beatmap_set.title_unicode.lower():
                similar_beatmaps.append(beatmap_set)
            else:
                not_matching_beatmaps.append(beatmap_set)

    return matching_beatmaps + similar_beatmaps + not_matching_beatmaps
