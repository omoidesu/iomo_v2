from khl import Bot, Message

from src.command import info_command
from src.service import user_service
from src.util.log import save_log
from ._commonParser import args_parser


async def info_parser(bot: Bot, msg: Message, *args):
    # 发送人kook id
    kook_id = save_log(msg, *args)

    # 解析参数
    require_args = args_parser(*args)
    osu_name = require_args['keyword']
    mode = require_args['mode']
    day = require_args['order']

    # 初始化变量
    target_kook_id = 0
    user_id = 0
    user = None

    # 如果有@人则查询osu信息是被@人绑定的信息
    if len(msg.mention) > 0:
        target_kook_id = int(msg.mention[0])
    # 如果用户名为空则查询的是发送人的信息
    elif osu_name == '':
        target_kook_id = int(kook_id)

    # 如果target_kook_id不是初始值则查询target_kook_id绑定的osu信息
    if target_kook_id:
        user = user_service.select_user(kook_id=target_kook_id)
        if user is None:
            return '该用户还没有绑定osu账号'
    # 如果用户名不为空查询一下改用户名是否已绑定
    elif osu_name != '':
        user = user_service.select_user(osu_name=osu_name)

    # 如果查询出来的用户存在
    if user is not None:
        # 查询api使用绑定的id
        osu_name = user.osu_id
        # 用户的主键id
        user_id = user.id
        # 如果mode为空则使用用户的默认模式
        if mode == '':
            mode = user.default_mode

    day = 1 if day == 0 else day
    # 调用osu api并生成卡片
    return await info_command(bot, str(osu_name), mode, int(day), user_id)
