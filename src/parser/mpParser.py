from khl import Bot, Message

from src.command import mp_command
from src.config import admin_id
from src.service import user_service
from src.util.log import save_log


async def mp_parser(bot: Bot, msg: Message, *args):
    kook_id = save_log(msg, *args)
    channel_id = msg.ctx.channel.id

    # 列表
    if '-ls' in args or '-list' in args:
        return mp_command.list_room(channel_id)

    # 删除监听的房间
    remove_mode = False
    room = 0
    if '-rm' in args:
        remove_mode = True
        index = args.index('-rm')
        room = args[index + 1]
    elif '-remove' in args:
        remove_mode = True
        index = args.index('-remove')
        room = args[index + 1]

    if remove_mode:
        return mp_command.remove_room(bot, room, channel_id)

    # 停止所有监听
    if '-stop' in args:
        if kook_id not in admin_id:
            return '你不是管理员，无权使用该命令'

        return mp_command.remove_all(bot)

    room = ' '.join(args)
    if room == '':
        user = user_service.select_user(kook_id=kook_id)
        if user is None:
            return '请输入房间号或房间名称'
        room = user.osu_name

    channel_id = msg.ctx.channel.id

    return await mp_command.fetch_room(bot, channel_id, room)
