from khl import Bot

from src.card import bp_card
from src.const import Assets
from src.exception import OsuApiException
from src.service import OsuApi
from src.util.uploadAsset import download_and_upload


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

        for bp in bp_info:
            beatmapset = bp.get('beatmapset')
            cover = beatmapset.get('covers', {}).get('list')
            kwargs[f"cover{bp.get('id')}"] = await download_and_upload(bot,
                                                                       cover) if cover else Assets.Image.OSU_LOGO
            beatmap = bp.get('beatmap')
            beatmap_info = await api.get_beatmap_info(beatmap.get('id'))
            kwargs[f"combo{bp.get('id')}"] = beatmap_info.get('max_combo')

        return bp_card(bp_info, **kwargs)
