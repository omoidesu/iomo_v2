from src.behavior.uploadAsset import download_and_upload
from src.service import OsuApi, user_info_service
from src.exception import OsuApiException
from src.card import user_card
from khl import Bot


async def info_behavior(bot: Bot, osu_name: str, mode: str, day: int, user_id):
    api = OsuApi()

    try:
        if mode == '':
            user_info = await api.get_user(osu_name)
        else:
            user_info = await api.get_user(osu_name, mode=mode, use_mode=True)
    except OsuApiException as e:
        if e.code == 401:
            return e.message
        elif e.code == 404:
            return '该用户不存在'
        else:
            return f'未知错误，code:{e.code}'
    else:
        if user_id:
            compare_info = user_info_service.select_user_info(user_id, mode=mode, day=day)
        else:
            compare_info = None

        cover = user_info.get('cover_url')
        kwargs = {'mode': mode}
        if cover is not None:
            kwargs['cover'] = await download_and_upload(bot, cover)

        return user_card(user_info, compare_user_info=compare_info, **kwargs)
