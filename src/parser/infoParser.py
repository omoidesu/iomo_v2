from src.behavior.log import save_log
from src.service import user_service
from khl import Message
from src.const import game_mode_convent
from src.behavior.command import info_behavior
from khl import Bot


async def info_parser(bot: Bot, msg: Message, *args):
    # 发送人kook id
    kook_id = save_log(msg, *args)

    # 判断消息内有没有@人
    mention = False
    if len(msg.mention) > 0:
        mention = True

    # 初始化变量
    mode, day = '', 0
    mode_index, day_index = -1, -1
    target_kook_id = 0
    user_id = 0
    user = None

    for arg in args:
        # 判断查询的模式
        if mode == '' and arg.startswith(':'):
            mode = arg[1:]
            if mode not in game_mode_convent.keys():
                return 'mode参数错误'
            mode = game_mode_convent.get(mode)
            mode_index = args.index(arg)
            continue
        # 判断对比天数
        if day == 0 and arg.startswith('#'):
            day = arg[1:]
            if not day.isdigit():
                return 'day参数必须为数字'
            if int(day) <= 0:
                return 'day参数不能为负数'
            day_index = args.index(arg)

    # 如果模式位置和天数位置都是初始值则所有元素都是用户名
    if mode_index + day_index == -2:
        osu_name = ' '.join(args)
    # 如果两个位置其中有一个是初始值则不是初始值的之前元素是用户名
    elif mode_index * day_index < 0:
        osu_name = ' '.join(args[:max(mode_index, day_index)])
    # 如果两个位置都不是初始值则位置最小的之前是用户名
    else:
        osu_name = ' '.join(args[:min(mode_index, day_index)])

    # 如果有@人则查询osu信息是被@人绑定的信息
    if mention:
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
    return await info_behavior(bot, str(osu_name), mode, int(day), user_id)
