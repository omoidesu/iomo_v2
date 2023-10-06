from khl import Bot, Message

from src.command import bp_command
from src.util.log import save_log
from ._commonParser import args_parser
from ..service import user_service


async def bp_parser(bot: Bot, msg: Message, *args):
    kook_id = save_log(msg, *args)

    require_args = args_parser(*args)
    osu_name = require_args['keyword']
    order = require_args['order']
    mode = require_args['mode']
    mods = require_args['mods']

    target_kook_id = 0
    if len(msg.mention) > 0:
        target_kook_id = int(msg.mention[0])
    elif osu_name == '':
        target_kook_id = int(kook_id)

    if target_kook_id != 0:
        user = user_service.select_user(target_kook_id)
        if user is None:
            return '该用户还没有绑定osu账号'

        osu_name = user.osu_name
        if mode == '':
            mode = user.default_mode

    return await bp_command(bot, osu_name, order, mode, mods)
