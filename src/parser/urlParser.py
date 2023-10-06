import re

from khl import Bot, Message

from src.command import bind_command, info_command
from src.config import osu_guild, osu_guild_role, user_channel
from src.const import user_homepage_pattern
from src.service import user_service
from src.util.log import save_log


async def osu_homepage_parser(bot: Bot, msg: Message, *args):
    command = re.findall(user_homepage_pattern, msg.content)[0]
    kook_id = save_log(msg, *args, command=command)
    osu_id = command.split('/')[-1]

    channel_id = msg.ctx.channel.id
    if channel_id in user_channel:
        user = user_service.select_user(kook_id=kook_id)
        if not user:
            result = await bind_command(bot, kook_id, osu_id)

            # osu!社区联动部分
            if msg.ctx.guild.id == osu_guild:
                user_db = user_service.select_user(kook_id=kook_id)
                mode = user_db.default_mode
                await msg.ctx.guild.grant_role(kook_id, osu_guild_role.get(mode))

            return result
        return await info_command(bot, osu_id), None

    else:
        return await info_command(bot, osu_id), None
