from khl import Bot

from src.card import info_card
from src.dao.models import OsuUser
from src.exception import OsuApiException
from src.service import OsuApi, user_service
from src.util.uploadAsset import download_and_upload, user_not_found_card


async def bind_command(bot: Bot, kook_id: int, username: str):
    api = OsuApi()

    try:
        user_info = await api.get_user(username)
    except OsuApiException as e:
        return await user_not_found_card(bot, e.do_except('绑定失败，请输入正确的osu用户名')), None
    else:
        user = OsuUser(kook_id=kook_id, osu_id=user_info.get('id'), osu_name=user_info.get('username'),
                       default_mode=user_info.get('playmode'))
        user_service.insert(user)

        cover = user_info.get('cover_url')
        avatar = user_info.get('avatar_url')
        kwargs = {'avatar': await download_and_upload(bot, avatar)}
        if cover is not None:
            kwargs['cover'] = await download_and_upload(bot, cover)

        return info_card(user_info, **kwargs), {str(user_info.get('id')): user.id}
