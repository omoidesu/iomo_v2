from khl import Bot, Message

from src.command import copy_bps
from src.parser._commonParser import args_parser
from src.util.log import save_log
from src.util import construct_message_obj


async def copy_parser(bot: Bot, msg: Message, waiting_msg_id: str, bot_id: str, *args):
    save_log(msg, *args)

    require_args = args_parser(*args)
    osu_name = require_args['keyword']
    mods = require_args['mods']
    mode = require_args['mode']

    waiting_msg = construct_message_obj(bot, waiting_msg_id, msg.ctx.channel.id, msg.ctx.guild.id, bot_id)

    return await copy_bps(bot, osu_name, mode, mods), waiting_msg
