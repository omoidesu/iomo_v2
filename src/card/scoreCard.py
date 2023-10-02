from khl.card import CardMessage

from src.const import Assets
from ._modules import Modules


def score_card(score_info: dict, **kwargs):
    mode = score_info.get('mode')
    beatmap_set = score_info.get('beatmapset')
    beatmap = score_info.get('beatmap')

    title_unicode = beatmap_set.get('title_unicode').replace('*', '\\*')

    header = Modules.score_header(score_info, kwargs.get('star'))
    map_info = Modules.beatmap_info(beatmap_set, beatmap, mode, kwargs.get('cover'))
    statistics = Modules.play_statistics(score_info, kwargs.get('fc_combo'))
    pp_module = Modules.pp_module(**kwargs)
    download_module = Modules.download_module(beatmap_set.get('id'))
    music_module = Modules.music_module(kwargs.get('preview'), title_unicode, kwargs.get('cover'))

    card = Modules.card(*header, Modules.divider, map_info, Modules.divider, statistics, Modules.divider, pp_module,
                        Modules.divider, download_module, music_module, color=Assets.COLOR.get(mode))

    return CardMessage(card)
