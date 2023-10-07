from khl import Bot, Message

from src.command import bind_command
from src.config import osu_guild, osu_guild_role
from src.const import game_mode_map
from src.service import user_service
from src.util.log import save_log


async def bind_parser(bot: Bot, msg: Message, *args):
    kook_id = save_log(msg, *args)

    if len(args) == 0:
        return '绑定失败，请输入你的osu用户名', None

    user = user_service.select_user(kook_id=int(kook_id))
    if user is not None:
        return f'你已经绑定了玩家{user.osu_name}', None

    username = ' '.join(args)

    return await bind_command(bot, kook_id, username)


async def unbind_parser(msg: Message, *args):
    kook_id = save_log(msg, *args)
    if kook_id != '565510950':
        return '如需要解绑请联系(met)565510950(met)'

    user = user_service.select_user(kook_id=int(kook_id))
    if user is None:
        return '你还没有绑定osu账号'

    user_service.delete_user(kook_id=int(kook_id))
    return '解绑成功'


async def mode_parser(msg: Message, *args):
    kook_id = save_log(msg, *args)

    if len(args) == 0:
        return '请指定模式'

    if not args[0].startswith(':'):
        return '模式错误, 模式前需要加上冒号，如:osu'

    mode = game_mode_map.get(args[0][1:])
    if mode is None:
        return '模式错误, 请指定正确的模式'

    user = user_service.select_user(kook_id=int(kook_id))
    if not user:
        return '你还没有绑定osu账号'

    if msg.ctx.guild.id == osu_guild:
        old_mode = user.default_mode
        try:
            await msg.ctx.guild.revoke_role(kook_id, osu_guild_role.get(old_mode))
        except:
            ...
        await msg.ctx.guild.grant_role(kook_id, osu_guild_role.get(mode))

    user_service.update_user(kook_id=int(kook_id), default_mode=mode)
    return f'你的默认模式已设置为{mode}'
