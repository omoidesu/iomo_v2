from khl.card import CardMessage, Element, Module, Types

from src.const import Assets, index_emojis
from src.dto import BeatmapSet
from src.util import kmarkdown_format
from ._modules import Modules


def search_card(keyword: str, beatmapsets: list[BeatmapSet], current: int, total_page: int, **kwargs):
    modules = [Module.Header(f'{keyword} 的搜索结果 ({current + 1}/{total_page})')]

    for i in range(len(beatmapsets)):
        beatmapset = beatmapsets[i]
        num = index_emojis[i]
        modules.append(Modules.divider)
        beatmapset_info = [
            f'{num} | {Assets.Sticker.STATUS.get(beatmapset.status)} **{kmarkdown_format(beatmapset.artist_unicode if beatmapset.artist_unicode else beatmapset.artist)} - {kmarkdown_format(beatmapset.title_unicode if beatmapset.title_unicode else beatmapset.title)}**',
            f'*▸ set id: {beatmapset.id} ▸ 作者: {beatmapset.creator}*',
            f'*▸ (emj)play(emj)[6147923945822473/bVLhXwDP4v05k05k]游玩数: {beatmapset.play_count} '
            f'▸ (emj)favourate(emj)[6147923945822473/PqzdX063Vj05k05k]收藏数: {beatmapset.favourite_count}*'
        ]

        stickers = '*▸* '

        try:
            for beatmap in beatmapset.beatmaps:
                key = f'{beatmap.mode}{beatmap.difficulty_rating}'
                sticker = kwargs.get(key)
                if sticker is None:
                    continue
                stickers += f'{sticker}'

            beatmaps_count = len(beatmapset.beatmaps)
            if beatmaps_count > 15:
                stickers += f'*+{beatmaps_count - 14}*'
        except AttributeError:
            pass

        beatmapset_info.append(stickers)

        cover = kwargs.get(f'cover{beatmapset.id}')
        modules.append(Module.Section(Element.Text('\n'.join(beatmapset_info), type=Types.Text.KMD),
                                      accessory=Element.Image(cover if cover else Assets.Image.OSU_LOGO,
                                                              size=Types.Size.SM),
                                      mode=Types.SectionMode.RIGHT))

    return CardMessage(Modules.card(*modules, color='#367FA3'))
