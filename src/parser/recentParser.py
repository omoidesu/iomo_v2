from khl import Bot, Message

from src.command import recent_command
from src.dao.models import OsuUser
from src.service import user_service
from src.util.log import save_log
from ._commonParser import args_parser


async def recent_parser(bot: Bot, msg: Message, *args, include_fail=False):
    # 发送人kook id
    kook_id = save_log(msg, *args)

    require_args = args_parser(*args)
    osu_name = require_args['keyword']
    mods = require_args['mods']
    mode = require_args['mode']
    order = int(require_args['order'])

    target_kook_id = 0
    ls_mode = False
    if '-ls' in args:
        ls_mode = True
        osu_name = osu_name.replace('-ls', '')
    if '-list' in args:
        ls_mode = True
        osu_name = osu_name.replace('-list', '')

    # 如果有@人则查询osu信息是被@人绑定的信息
    if len(msg.mention) > 0:
        target_kook_id = int(msg.mention[0])
    # 如果用户名为空则查询的是发送人的信息
    elif osu_name == '':
        target_kook_id = int(kook_id)

    # 如果target_kook_id不是初始值则查询target_kook_id绑定的osu信息
    if target_kook_id:
        user: OsuUser = user_service.select_user(target_kook_id)
        if user is None:
            return '该用户还没有绑定osu账号', None

        osu_name = user.osu_id
        if mode == '':
            mode = user.default_mode

    return await recent_command(bot, msg, osu_name, mode, mods, order, include_fail, ls_mode)
