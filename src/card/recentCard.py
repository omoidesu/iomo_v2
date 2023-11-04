from khl.card import Card, CardMessage, Element, Module, Types

from src.const import Assets, index_emojis
from src.util import kmarkdown_format
from ._modules import Modules


def recent_card(recent_score: list, **kwargs):
    name = kwargs.get('osu_name')
    stars = kwargs.get('stars')
    mode = kwargs.get('mode')

    card = Card(color=Assets.COLOR.get(mode))

    header = f'{name} 的最近游玩记录'
    card.append(Module.Header(header))
    card.append(Modules.divider)

    id_map = {}

    for score in recent_score:
        id_map[index_emojis[recent_score.index(score)]] = score.get('id')
        beatmapset = score.get('beatmapset')
        artist = kmarkdown_format(beatmapset.get('artist_unicode'))
        title = kmarkdown_format(beatmapset.get('title_unicode'))
        pp = score.get('pp') if score.get('pp') is not None else 0
        difficulty_rating = score.get('beatmap', {}).get('difficulty_rating')
        difficulty_rating_str = f'{difficulty_rating:.2f}' if difficulty_rating is not None else '0.00'
        if difficulty_rating < 10:
            difficulty_rating_str = ' ' + difficulty_rating_str

        context = Module.Context()

        context.append(Element.Text(f'{nums[recent_score.index(score)]} '))
        context.append(Element.Image(kwargs.get(str(beatmapset.get('id')), Assets.Image.OSU_LOGO)))
        context.append(Element.Text(
            f' **[{artist} - {title}](https://osu.ppy.sh/beatmapsets/{beatmapset.get("id")})**', type=Types.Text.KMD
        ))

        context.append('\n' + ' ' * 7)
        context.append(Element.Image(Assets.Image.RANK.get(score.get('rank'))))
        context.append(
            Element.Image(stars.get(difficulty_rating, Assets.Image.DIFF.get(mode))))
        context.append(Element.Text(f'**{difficulty_rating_str} ★**  |  **pp: {round(pp)}**'))

        for mod in score.get('mods', []):
            context.append(Element.Image(Assets.Image.MOD.get(mod)))

        card.append(context)
        if recent_score.index(score) != len(recent_score) - 1:
            card.append(Modules.divider)

    return CardMessage(card), id_map
