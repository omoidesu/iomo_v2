from khl.card import CardMessage

from src.const import Assets
from ._modules import Modules

special_mods = ('HR', 'DT', 'EZ', 'HT', 'NC')

def score_card(score_info: dict, beatmap: dict, beatmap_set: dict, **kwargs):
    mode = score_info.get('mode')
    mods = score_info.get('mods')
    special_mode = False
    for mod in mods:
        if mod in special_mods:
            special_mode = True
            break

    title_unicode = beatmap_set.get('title_unicode').replace('*', '\\*')

    header = Modules.score_header(score_info, beatmap, beatmap_set, kwargs.get('star'), position=kwargs.get('position'))
    map_info = Modules.beatmap_info(beatmap_set, beatmap, mode, kwargs, special_mode=special_mode)
    statistics = Modules.play_statistics(score_info, kwargs.get('fc_combo'))
    pp_module = Modules.pp_module(**kwargs)
    download_module = Modules.download_module(beatmap_set)
    music_module = Modules.music_module(kwargs.get('preview'), title_unicode, kwargs.get('cover'))

    card = Modules.card(*header, Modules.divider, map_info, Modules.divider, statistics, Modules.divider, pp_module,
                        Modules.divider, download_module, music_module, color=Assets.COLOR.get(mode))

    return CardMessage(card)
