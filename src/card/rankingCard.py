from khl.card import Card, CardMessage, Element, Module, Struct

from src.const import Assets
from ._modules import Modules


def ranking_card(rank_info: list, country: str, mode: str):
    region = ''.join(map(lambda x: Assets.FLAG.get(x), country.upper())) if country else '全球'
    header = Module.Section(Element.Text(f'**{Assets.Sticker.MODE.get(mode)} {region} 排行榜 （模式: {mode}）**'))

    paragraphs = []

    for i in range(len(rank_info)):
        rank = rank_info[i]

        country_code = rank.get('user').get('country').get('code')
        flag = ''.join(map(lambda x: Assets.FLAG.get(x), country_code)) if country_code != 'TW' else ':tw:'
        paragraphs.append(Element.Text(f'**#{str(i + 1).rjust(2, "0")}**' + '\t' * 10 + f'{flag}'))

        username = rank.get('user').get('username')
        paragraphs.append(Element.Text(f'**{username}**'))

        pp = rank.get("pp")
        paragraphs.append(Element.Text(f'**{pp} pp**'))

    struct = Module.Section(Struct.Paragraph(3, *paragraphs))

    return CardMessage(Modules.card(header, Modules.divider, struct))
