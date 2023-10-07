from khl.card import CardMessage, Element, Module, Types

from src.const import Assets
from src.util import convert_date
from ._modules import Modules


def mp_card(game: dict, users: dict, scores: list, **kwargs):
    modules = []

    beatmap = game.get('beatmap')
    beatmapset = beatmap.get('beatmapset')

    artist = beatmapset.get('artist_unicode')
    title = beatmapset.get('title_unicode')
    source = beatmapset.get('source')
    version = beatmap.get('version')
    global_mods = game.get('mods')
    if not global_mods:
        global_mods = ['NM']
    end_time = convert_date(game.get('end_time'))

    header_text = f'{source}({artist} - {title})' if source else f'{artist} - {title}'
    modules.append(Module.Header(Element.Text(f'{header_text}[{version}]')))

    context = Module.Context(Element.Image(kwargs.get('diff')))
    context.append(Element.Text(' | '))
    context.append(Element.Image(Assets.Image.STATUS.get(beatmap.get('status'))))
    context.append(Element.Text(' | mods:'))
    for mod in global_mods:
        context.append(Element.Image(Assets.Image.MOD.get(mod)))
    context.append(Element.Text(f' | {end_time}'))
    modules.append(context)
    modules.append(Modules.divider)

    banner = Modules.banner(kwargs.get('cover'))
    modules.append(banner)
    modules.append(Modules.divider)

    for score in scores:
        user_id = score.get('user_id')
        user = users.get(user_id)
        section_text = f'> {user.username} {user.flag}\t'
        mods = score.get('mods')
        for mod in mods:
            section_text += f'{Assets.Sticker.MOD.get(mod)}'

        section_text += f'\n{format(score.get("score"))}\t\t{score.get("max_combo")}x\t\t{round(score.get("accuracy") * 100, 2)}%'
        section = Module.Section(Element.Text(section_text),
                                 accessory=Element.Image(kwargs.get(f'avatar{user.id}'), circle=True,
                                                         size=Types.Size.SM),
                                 mode=Types.SectionMode.LEFT)
        modules.append(section)

    return CardMessage(Modules.card(*modules, color='#87EB00'))
