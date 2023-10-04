from khl.card import CardMessage, Element, Module, Types

from src.const import Assets
from src.dto import BeatmapSet
from ._modules import Modules


def search_card(keyword: str, beatmapsets: list[BeatmapSet], search_id: int, current: int, prev: bool = False,
                next: bool = False, **kwargs):
    modules = [Module.Header(f'{keyword} 的搜索结果')]

    for beatmapset in beatmapsets:
        modules.append(Modules.divider)
        beatmapset_info = [
            f'**{beatmapset.title_unicode if beatmapset.title_unicode else beatmapset.title}**',
            f'*▸ artist: {beatmapset.artist_unicode if beatmapset.artist_unicode else beatmapset.artist}*',
            f'*▸ set id: {beatmapset.id} ▸ 作者: {beatmapset.creator}*',
            f'*▸ (emj)favourate(emj)[6147923945822473/PqzdX063Vj05k05k]收藏数: {beatmapset.favourite_count} '
            f'▸ (emj)play(emj)[6147923945822473/bVLhXwDP4v05k05k]游玩数: {beatmapset.play_count}*'
        ]

        cover = kwargs.get(f'cover{beatmapset.id}')
        modules.append(Module.Section(Element.Text('\n'.join(beatmapset_info), type=Types.Text.KMD),
                                      accessory=Element.Image(cover if cover else Assets.Image.OSU_LOGO,
                                                              size=Types.Size.SM),
                                      mode=Types.SectionMode.RIGHT))

        stickers = f'{Assets.Sticker.STATUS.get(beatmapset.status)} | '
        for beatmap in beatmapset.beatmaps:
            key = f'{beatmap.mode}{beatmap.difficulty_rating}'
            stickers += f'{kwargs.get(key)}'
        modules.append(Module.Section(Element.Text(stickers), accessory=Element.Button('详情', f'set:{beatmapset.id}',
                                                                                       theme=Types.Theme.PRIMARY)))

    if not prev and not next:
        return CardMessage(Modules.card(*modules, color='#367FA3'))

    modules.append(Modules.divider)
    actions = Module.ActionGroup()

    if prev:
        prev_btn = Element.Button('上一页', f'search:{search_id}:{current - 1}', theme=Types.Theme.INFO)
    else:
        prev_btn = Element.Button(' ', '', theme=Types.Theme.SECONDARY)
    actions.append(prev_btn)

    if next:
        next_btn = Element.Button('下一页', f'search:{search_id}:{current + 1}', theme=Types.Theme.INFO)
    else:
        next_btn = Element.Button(' ', '', theme=Types.Theme.SECONDARY)
    actions.append(next_btn)

    modules.append(actions)
    return CardMessage(Modules.card(*modules, color='#367FA3'))
