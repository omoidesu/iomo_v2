from khl.card import CardMessage, Element, Module, Struct

from src.const import Assets
from src.util import difficult_format, kmarkdown_format
from ._modules import Modules


def beatmap_set_card(beatmap_set: dict, beatmap_id: int, **kwargs):
    beatmaps = beatmap_set.get('beatmaps')
    beatmaps = sorted(beatmaps, key=lambda x: x.get('difficulty_rating'))
    osu, taiko, fruits, mania = [], [], [], []
    for beatmap in beatmaps:
        if beatmap.get('mode') == 'osu':
            osu.append(beatmap)
        elif beatmap.get('mode') == 'taiko':
            taiko.append(beatmap)
        elif beatmap.get('mode') == 'fruits':
            fruits.append(beatmap)
        elif beatmap.get('mode') == 'mania':
            mania.append(beatmap)

    beatmaps = osu + taiko + fruits + mania

    source = beatmap_set.get('source')
    artist = kmarkdown_format(beatmap_set.get('artist'))
    artist_unicode = kmarkdown_format(beatmap_set.get('artist_unicode'))
    title = kmarkdown_format(beatmap_set.get('title'))
    title_unicode = kmarkdown_format(beatmap_set.get('title_unicode'))

    head = f'{source}({artist_unicode}) - {title_unicode}' if source else f'{artist_unicode} - {title_unicode}'

    user = beatmap_set.get('user')

    header = Module.Section(
        Element.Text(f'**{Assets.Sticker.STATUS.get(beatmap_set.get("status"))}  {head}**'))

    info = Module.Context(Element.Image(kwargs.get('avatar')))
    info.append(Element.Text(
        f' [{user.get("username")}](https://osu.ppy.sh/users/{user.get("id")}) | {artist} - {title} | set id: {beatmap_set.get("id")} |'))
    struct_content = [
        Element.Text(
            f'**(font)流派: (font)[secondary]**(font){beatmap_set.get("genre", {}).get("name")}(font)[secondary]'),
        Element.Text(
            f'**(font)语言: (font)[secondary]**(font){beatmap_set.get("language", {}).get("name")}(font)[secondary]'),
        Element.Text(
            f'{Assets.Sticker.FAVOURITE} **(font)收藏数: (font)[secondary]**(font){beatmap_set.get("favourite_count")}(font)[secondary]'),
        Element.Text(
            f'{Assets.Sticker.PLAYCOUNT} **(font)游玩数: (font)[secondary]**(font){beatmap_set.get("play_count")}(font)[secondary]')
    ]

    genre = Module.Section(Struct.Paragraph(2, *struct_content))

    tags = Module.Context(Element.Text(f'**(font)tags: (font)[secondary]***{beatmap_set.get("tags")}*'))

    banner = Modules.banner(kwargs.get('cover'))

    beatmap_infos = []
    for beatmap in beatmaps:
        mode = beatmap.get('mode')
        diff = beatmap.get('difficulty_rating')
        if beatmap_id and beatmap_id == beatmap.get('id'):
            beatmap_info = Modules.beatmap_info({}, beatmap, beatmap.get('mode'), kwargs, left_mode=True)
        else:
            beatmap_info = Module.Context(Element.Image(kwargs.get(f'{mode}{diff}')))
            beatmap_info.append(Element.Text('|'))
            beatmap_info.append(Element.Image(Assets.Image.STATUS.get(beatmap.get('status'))))
            beatmap_info.append(
                Element.Text(
                    f'▸ id: {str(beatmap.get("id")).ljust(8, " ")} ▸ ★{difficult_format(diff)} ▸ 难度名: {beatmap.get("version")}'))

        beatmap_infos.append(beatmap_info)

    download_module = Modules.download_module(beatmap_set)

    music_module = Modules.music_module(kwargs.get('preview'), title_unicode, kwargs.get('cover_list'))

    return CardMessage(Modules.card(header, info, genre, tags, Modules.divider, banner, Modules.divider, *beatmap_infos,
                                    Modules.divider, download_module, music_module, color='#33AAFF'))


def beatmap_card(beatmap: dict, **kwargs):
    beatmapset = beatmap.get('beatmapset')

    source = beatmapset.get('source')
    artist = kmarkdown_format(beatmapset.get('artist'))
    artist_unicode = kmarkdown_format(beatmapset.get('artist_unicode'))
    title = kmarkdown_format(beatmapset.get('title'))
    title_unicode = kmarkdown_format(beatmapset.get('title_unicode'))

    head = f'{source}({artist_unicode}) - {title_unicode}' if source else f'{artist_unicode} - {title_unicode}'
    header = Module.Section(Element.Text(f'{Assets.Sticker.STATUS.get(beatmap.get("status"))}  **{head}**'))

    context = Module.Context(Element.Image(kwargs.get('diff')))
    context.append(Element.Text(f' | {artist} - {title}'))

    map_info = Modules.beatmap_info(beatmapset, beatmap, beatmap.get('mode'), kwargs)

    download_module = Modules.download_module(beatmapset)

    return CardMessage(
        Modules.card(header, context, Modules.divider, map_info, Modules.divider, download_module, color='#33AAFF'))
