from khl.card import CardMessage, Element, Module, Struct

from src.const import Assets
from src.util import difficult_format, kmarkdown_format
from ._modules import Modules


def beatmap_set_card(beatmap_set: dict, **kwargs):
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

    artist = kmarkdown_format(
        beatmap_set.get('artist_unicode') if beatmap_set.get('artist_unicode') else beatmap_set.get('artist'))
    title = kmarkdown_format(
        beatmap_set.get('title_unicode') if beatmap_set.get('title_unicode') else beatmap_set.get('title'))

    user = beatmap_set.get('user')

    header = Module.Section(
        Element.Text(f'**{Assets.Sticker.STATUS.get(beatmap_set.get("status"))}  {artist} - {title}**'))

    banner = Modules.banner(kwargs.get('cover'))

    info = Module.Context(Element.Image(user.get('avatar_url')))
    info.append(Element.Text(
        f' [{user.get("username")}](https://osu.ppy.sh/users/{user.get("id")}) | set id: {beatmap_set.get("id")} | '))
    info.append(Element.Image(Assets.Image.FAVOURITE))
    info.append(Element.Text(f' {beatmap_set.get("favourite_count")} | '))
    info.append(Element.Image(Assets.Image.PLAYCOUNT))
    info.append(Element.Text(f' {beatmap_set.get("play_count")}'))

    genre = Module.Section(
        Struct.Paragraph(2, Element.Text(
            f'**(font)流派: (font)[secondary]**(font){beatmap_set.get("genre", {}).get("name")}(font)[secondary]'),
                         Element.Text(
                             f'**(font)语言: (font)[secondary]**(font){beatmap_set.get("language", {}).get("name")}(font)[secondary]')))

    tags = Module.Context(Element.Text(f'**(font)tags: (font)[secondary]***{beatmap_set.get("tags")}*'))

    beatmap_infos = []
    for beatmap in beatmaps:
        mode = beatmap.get('mode')
        diff = beatmap.get('difficulty_rating')
        beatmap_info = Module.Context(Element.Image(Assets.Image.STATUS.get(beatmap.get('status'))))
        beatmap_info.append(Element.Image(kwargs.get(f'{mode}{diff}')))
        beatmap_info.append(
            Element.Text(
                f' | ▸ id: {str(beatmap.get("id")).ljust(7, " ")} ▸ ★{difficult_format(diff)} ▸ 难度名: {beatmap.get("version")}'))

        beatmap_infos.append(beatmap_info)

    download_module = Modules.download_module(beatmap_set.get('id'),
                                              beatmap_set.get('availability', {}).get('download_disabled'))

    music_module = Modules.music_module('https:' + beatmap_set.get('preview_url'), title, kwargs.get('cover_list'))

    return CardMessage(Modules.card(header, banner, Modules.divider, info, genre, tags, Modules.divider, *beatmap_infos,
                                    Modules.divider, download_module, music_module, color='#33AAFF'))
