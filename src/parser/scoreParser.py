from khl import Bot, Message

from src.command import score_command
from src.service import user_service
from src.util.log import save_log
from ._commonParser import args_parser


async def score_parser(bot: Bot, msg: Message, *args):
    # 发送人kook id
    kook_id = save_log(msg, *args)

    require_args = args_parser(*args)

    # keyword, source, beatmap_id, beatmap_set_id用于确定谱面
    keyword = require_args['keyword']
    beatmap_id = require_args['beatmap_id']
    beatmapset_id = require_args['beatmap_set_id']

    if not beatmap_id and not beatmapset_id and not keyword:
        return '请输入谱面信息'

    if ' - ' in keyword:
        artist, title = keyword.split(' - ', 1)
    else:
        artist, title = '', keyword
    source = require_args['source']

    # username, order用于确定查询的用户
    username = require_args['username']
    order = int(require_args['order'])

    # mode用于确定查询的模式
    mode = require_args['mode']

    # 用户没输入order, 则需要确定查询的用户
    if order == 0:
        target_kook_id = 0

        # 如果有@人则查询osu信息是被@人绑定的信息
        if len(msg.mention) > 0:
            target_kook_id = int(msg.mention[0])
        # 如果用户名为空则查询的是发送人的信息
        elif username == '':
            target_kook_id = int(kook_id)

        # 如果target_kook_id不是初始值则查询target_kook_id绑定的osu信息
        if target_kook_id != 0:
            user = user_service.select_user(target_kook_id)
            if user is None:
                return '该用户还没有绑定osu账号'

            username = user.osu_id
            if mode == '':
                mode = user.default_mode

        return await score_command(bot, msg, artist, title, source, beatmap_id, beatmapset_id, order, username, mode)

    # 用户输入了order, 则不需要确定查询的用户
    return await score_command(bot, msg, artist, title, source, beatmap_id, beatmapset_id, order, username, mode,
                               order_mode=True)
