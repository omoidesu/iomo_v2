import asyncio
from datetime import datetime

from khl import Bot

from src.card import bp_card, no_bp_card
from src.const import Assets
from src.exception import OsuApiException
from src.service import OsuApi
from src.util.uploadAsset import good_news_generator, upload_asset


async def bp_command(bot: Bot, osu_name: str, order: int, mode: str, mods: list):
    api = OsuApi()

    if not str(osu_name).isdigit():
        osu_info = await api.get_user(osu_name)
        osu_name = osu_info.get('id')
        if mode == '':
            mode = osu_info.get('playmode')

    limit = 5
    if order != 0:
        limit = order
    elif mods:
        limit = 50

    kwargs = {}

    try:
        user_bp = await api.get_best_score(osu_name, mode=mode, limit=limit)
    except OsuApiException as e:
        return e.do_except('该用户不存在')
    else:
        if len(user_bp) == 0:
            return '该用户没有bp记录'

        if order:
            bp_info = [user_bp[-1]]
        elif mods:
            if len(mods) == 1 and mods[0] == 'NM':
                bp_info = list(filter(lambda x: x.get('mods') == [], user_bp))[:5]
            elif len(mods) > 0:
                bp_info = list(filter(lambda x: set(mods).issubset(x.get('mods', [])), user_bp))[:5]
            else:
                bp_info = user_bp[:5]

            if len(bp_info) == 0:
                return f'该用户没有mod为{"".join(mods)}的bp记录'
        else:
            bp_info = user_bp[:5]

        await __bp_traverse(bot, bp_info, kwargs, api)

        return bp_card(bp_info, **kwargs)


async def bp_today_command(bot: Bot, osu_name: str, mode: str):
    api = OsuApi()

    if not str(osu_name).isdigit():
        osu_info = await api.get_user(osu_name)
        osu_name = osu_info.get('id')
        if mode == '':
            mode = osu_info.get('playmode')

    kwargs = {}

    try:
        user_bp = await api.get_best_score(osu_name, mode=mode, limit=100)
    except OsuApiException as e:
        return e.do_except('该用户不存在')
    else:
        if len(user_bp) == 0:
            return '该用户没有bp记录'

        today = datetime.now().strftime('%Y-%m-%d')
        today_bps = list(filter(lambda x: x.get('created_at').startswith(today), user_bp))

        if len(today_bps) == 0:
            username = user_bp[0].get("user").get("username")
            good_news = await good_news_generator(bot, f'{username}今天没有新bp')
            return no_bp_card(username, mode, good_news)

        await __bp_traverse(bot, today_bps, kwargs, api)

        return bp_card(today_bps, **kwargs)


async def __bp_traverse(bot: Bot, bp_list: list, to: dict, api: OsuApi):
    tasks = []
    for bp in bp_list:
        cover = bp.get('beatmapset').get('covers', {}).get('list')
        if cover:
            tasks.append(
                asyncio.create_task(upload_asset(bot, cover, to, f"cover{bp.get('id')}", Assets.Image.DEFAULT_COVER)))
        else:
            to[f"cover{bp.get('id')}"] = Assets.Image.OSU_LOGO
        tasks.append(asyncio.create_task(__get_max_combo(api, bp.get('beatmap').get('id'), to, f"combo{bp.get('id')}")))

    await asyncio.wait(tasks)


async def __get_max_combo(api: OsuApi, beatmap_id: int, to: dict, key: str):
    beatmap_info = await api.get_beatmap_info(beatmap_id)
    to[key] = beatmap_info.get('max_combo')
