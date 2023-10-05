from khl import Bot, Message

from src.card import info_card
from src.const import game_mode_map
from src.dao.models import OsuUser
from src.exception import OsuApiException
from src.service import OsuApi, user_service
from src.util.log import save_log
from src.util.uploadAsset import download_and_upload
from .buttonQueue import ButtonQueue
from .compareParser import compare_parser
from .infoParser import info_parser
from .reactionQueue import ReactionQueue
from .recentParser import recent_parser
from .scoreParser import score_parser
from .searchParser import search_parser

reaction_queue = ReactionQueue.instance()
button_queue = ButtonQueue.instance()


def ping_parser(msg: Message, *args):
    save_log(msg, *args)
    return '(> <)'


async def bind_parser(bot: Bot, msg: Message, *args):
    kook_id = save_log(msg, *args)

    if len(args) == 0:
        return '绑定失败，请输入你的osu用户名', None

    user = user_service.select_user(kook_id=int(kook_id))
    if user is not None:
        return f'你已经绑定了玩家{user.osu_name}', None

    username = ' '.join(args)
    api = OsuApi()
    try:
        user_info = await api.get_user(username)
        user = OsuUser(kook_id=msg.author.id, osu_id=user_info.get('id'), osu_name=user_info.get('username'),
                       default_mode=user_info.get('playmode'))
        user_service.insert(user)

        cover = user_info.get('cover_url')
        kwargs = {}
        if cover is not None:
            kwargs['cover'] = await download_and_upload(bot, cover)

        return info_card(user_info, **kwargs), {str(user_info.get('id')): user.id}
    except OsuApiException as e:
        return e.do_except('绑定失败，请输入正确的osu用户名'), None


async def unbind_parser(msg: Message, *args):
    kook_id = save_log(msg, *args)
    if kook_id != '565510950':
        return '如需要解绑请联系(met)565510950(met)'

    user = user_service.select_user(kook_id=int(kook_id))
    if user is None:
        return '你还没有绑定osu账号'

    user_service.delete_user(kook_id=int(kook_id))
    return '解绑成功'


def mode_parser(msg: Message, *args):
    kook_id = save_log(msg, *args)

    if len(args) == 0:
        return '请指定模式'

    if not args[0].startswith(':'):
        return '模式错误, 模式前需要加上冒号，如:osu'

    mode = game_mode_map.get(args[0][1:])
    if mode is None:
        return '模式错误, 请指定正确的模式'

    user_service.update_user(kook_id=int(kook_id), default_mode=mode)
    return f'你的默认模式已设置为{mode}'
