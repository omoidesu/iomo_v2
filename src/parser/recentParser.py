from khl import Bot, Message

from src.const import game_mode_convent
from src.behavior.log import save_log
from src.exception import ArgsException
from src.behavior import mods_parser
from src.service import user_service
from src.behavior.command import recent_behavior


async def recent_parser(bot: Bot, msg: Message, *args, include_fail=False):
    # 发送人kook id
    kook_id = save_log(msg, *args)

    # 初始化变量
    mode, mod, order, ls_mode = '', [], None, False
    index = {'mode': -1, 'mod': -1, 'order': -1, 'ls': -1}
    target_kook_id = 0
    ls_mode_command = ('-list', '-ls')

    for arg in args:
        arg_index = args.index(arg)
        if not ls_mode and arg in ls_mode_command:
            ls_mode = True
            index['ls'] = arg_index
            continue
        # 查询模式
        if mode == '' and arg.startswith(':'):
            mode = arg[1:]
            if mode not in game_mode_convent.keys():
                return 'mode参数错误'
            mode = game_mode_convent.get(mode)
            index['mode'] = arg_index
            continue
        # 查询mod
        if not mod and arg.startswith('+'):
            mods: str = arg[1:]
            try:
                mod = mods_parser(mods)
                index['mod'] = arg_index
                continue
            except ArgsException as e:
                return e.message
        if not order and arg.startswith('#'):
            order = arg[1:]
            if not order.isdigit():
                return 'order参数必须为数字'
            if int(order) <= 0:
                return 'order参数不能为负数'
            order = int(order) - 1
            index['order'] = arg_index

    # 如果变量位置都是初始值则所有元素都是用户名
    if sum(index.values()) == -1 * len(index):
        osu_name = ' '.join(args)
    # 找出不是初始位置的最小值，该位置前的元素都是用户名
    else:
        osu_name = ' '.join(args[:min(i for i in index.values() if i >= 0)])

    # 如果有@人则查询osu信息是被@人绑定的信息
    if len(msg.mention) > 0:
        target_kook_id = int(msg.mention[0])
    # 如果用户名为空则查询的是发送人的信息
    elif osu_name == '':
        target_kook_id = int(kook_id)

    # 如果target_kook_id不是初始值则查询target_kook_id绑定的osu信息
    if target_kook_id:
        user = user_service.select_user(target_kook_id)
        if user is None:
            return '该用户还没有绑定osu账号'

        osu_name = user.osu_id
        if mode == '':
            mode = user.default_mode

    return await recent_behavior(bot, msg, osu_name, mode, mod, order, include_fail, ls_mode)
