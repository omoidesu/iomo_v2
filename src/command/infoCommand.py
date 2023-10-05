from khl import Bot

from src.card import info_card
from src.exception import OsuApiException
from src.service import OsuApi, user_info_service
from src.util.uploadAsset import download_and_upload


async def info_command(bot: Bot, osu_name: str, mode: str, day: int, user_id):
    api = OsuApi()

    try:
        if mode == '':
            user_info = await api.get_user(osu_name)
        else:
            user_info = await api.get_user(osu_name, mode=mode, use_mode=True)
    except OsuApiException as e:
        return e.do_except('该用户不存在')
    else:
        if user_id:
            compare_info = user_info_service.select_user_info(user_id, mode=mode, day=day)
        else:
            compare_info = None

        cover = user_info.get('cover_url')
        kwargs = {'mode': mode}
        if cover is not None:
            kwargs['cover'] = await download_and_upload(bot, cover)

        return info_card(user_info, compare_user_info=compare_info, **kwargs)
