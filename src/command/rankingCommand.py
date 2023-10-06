from aiohttp import ContentTypeError

from src.card import ranking_card
from src.service import OsuApi


async def ranking_command(country: str, mode: str):
    api = OsuApi()
    try:
        rank = await api.get_global_ranking(mode, country)
    except ContentTypeError:
        return '国家或区域代码不存在'
    else:
        ranking = rank.get('ranking')

    # 结构体最多50个元素，所以最多只能取16个。过多行会显得不美观
    return ranking_card(ranking[:15], country, mode)
