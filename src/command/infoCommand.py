import asyncio

from khl import Bot

from src.card import info_card
from src.exception import OsuApiException
from src.service import OsuApi, user_info_service, user_service
from src.util.afterCommend import collect_user_info
from src.util.uploadAsset import download_and_upload, user_not_found_card


async def info_command(bot: Bot, osu_name: str, mode: str = '', day: int = 1, user_id: int = 0):
    api = OsuApi()

    try:
        if mode == '':
            user_info = await api.get_user(osu_name)
        else:
            user_info = await api.get_user(osu_name, mode=mode, use_mode=True)
    except OsuApiException as e:
        return await user_not_found_card(bot, e.do_except(f'找不到名为{osu_name}的玩家'))
    else:
        if user_id:
            compare_info = user_info_service.select_user_info(user_id, mode=mode, day=day)
        else:
            compare_info = None

        cover = user_info.get('cover_url')
        avatar = user_info.get('avatar_url')
        kwargs = {'mode': mode, 'avatar': await download_and_upload(bot, avatar)}
        if cover is not None:
            kwargs['cover'] = await download_and_upload(bot, cover)

        return info_card(user_info, compare_user_info=compare_info, **kwargs)


async def update_osu_info():
    users = user_service.select_all_users()
    tasks = []
    for i in range(0, len(users), 50):
        id_map = {str(user.osu_id): user.id for user in users[i:i + 50]}
        tasks.append(asyncio.create_task(collect_user_info(**id_map)))

    await asyncio.wait(tasks)
