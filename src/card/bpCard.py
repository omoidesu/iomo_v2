from khl.card import CardMessage, Element, Module, Types

from src.const import Assets, bp_index
from src.util import convert_date
from ._modules import Modules


def bp_card(bp_list: dict, **kwargs):
    bp = bp_list[0]
    username = bp.get('user', {}).get('username')
    mode = bp.get('mode')

    header = Module.Section(f'{Assets.Sticker.MODE.get(mode)} **{username}的Best Performance记录**')

    bp_modules = []
    for bp_info in bp_list:
        bp_modules.append(Modules.divider)
        weight = bp_info.get('weight')
        percent = weight.get('percentage')
        index = bp_index.get(str(percent))
        pp_with_percent = round(weight.get('pp'), 2)
        context = Module.Context(Element.Text(f'**(font)BP{str(index).ljust(3)}(font)[none]** |'))
        context.append(Element.Image(Assets.Image.RANK.get(bp_info.get('rank'))))
        context.append(
            Element.Text(
                f'| **(font){bp_info.get("pp")} pp → {pp_with_percent} pp ({round(percent, 2)}%)(font)[none]**'))

        mods = bp_info.get('mods')
        if mods:
            context.append(Element.Text(' |'))
            for mod in mods:
                context.append(Element.Image(Assets.Image.MOD.get(mod)))
        bp_modules.append(context)

        beatmapset = bp_info.get('beatmapset')
        beatmap = bp_info.get('beatmap')

        bp_id = bp_info.get('id')
        rows = [
            f'**{beatmapset.get("artist_unicode")} - {beatmapset.get("title_unicode")}**',
            f'难度名: {beatmap.get("version")}\t谱面id: {beatmap.get("id")}',
            f'{bp_info.get("max_combo")}x/**{kwargs.get(f"combo{bp_id}")}x**\t\t'
            f'**{round(bp_info.get("accuracy") * 100, 2)}**%\t\t**{beatmap.get("difficulty_rating")}**★'
        ]
        bp_modules.append(
            Module.Section(Element.Text('\n'.join(rows)),
                           accessory=Element.Image(kwargs.get(f"cover{bp_id}"), size=Types.Size.SM),
                           mode=Types.SectionMode.RIGHT))

        download = Modules.download_module(beatmapset)
        download.append(Element.Text('\t' * 7 + f'{convert_date(bp_info.get("created_at"))}'))
        bp_modules.append(download)

    return CardMessage(Modules.card(header, *bp_modules, color=Assets.COLOR.get(mode)))
