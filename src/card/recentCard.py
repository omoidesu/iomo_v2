from khl.card import Card, CardMessage, Module, Element, Types
from src.const import Assets, Sticker

nums = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', ':keycap_ten:']

divider = Module.Divider()


def recent_card(recent_score: list, **kwargs):
    name = kwargs.get('osu_name')
    stars = kwargs.get('stars')
    mode = kwargs.get('mode')

    card = Card(color=Assets.COLOR.get(mode))

    header = f'{name} 的最近游玩记录'
    card.append(Module.Header(header))
    card.append(divider)

    for score in recent_score:
        beatmapset = score.get('beatmapset')
        artist = beatmapset.get('artist_unicode').replace('*', '\\*')
        title = beatmapset.get('title_unicode').replace('*', '\\*')
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

        for mod in score.get('mods', []):
            context.append(Element.Image(Assets.Image.MOD.get(mod)))

        context.append('\n' + ' ' * 7)
        context.append(Element.Image(Assets.Image.RANK.get(score.get('rank'))))
        context.append(
            Element.Image(stars.get(difficulty_rating, Assets.Image.DIFF.get(mode))))
        context.append(Element.Text(f'**{difficulty_rating_str} ★**  |  **pp: {pp}**'))

        card.append(context)
        if recent_score.index(score) != len(recent_score) - 1:
            card.append(divider)

    return CardMessage(card)
