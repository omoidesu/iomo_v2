from khl import Bot, Guild, Message

from src.command import search_command
from src.util import construct_message_obj
from src.util.log import save_log
from ._commonParser import args_parser


async def search_parser(bot: Bot, msg: Message, guild: Guild, reply_msg_id: str, bot_id: str, *args):
    save_log(msg, *args)

    require_args = args_parser(*args)

    keyword = require_args['keyword']

    if not keyword:
        return '请输入谱面信息'

    if ' - ' in keyword:
        artist, title = keyword.split(' - ', 1)
    else:
        artist, title = '', keyword
    source = require_args['source']
    beatmap_id = require_args['beatmap_id']
    beatmapset_id = require_args['beatmap_set_id']

    if beatmap_id:
        ...
    elif beatmapset_id:
        ...

    reply_msg = construct_message_obj(bot, reply_msg_id, msg.ctx.channel.id, msg.ctx.guild.id, bot_id)

    return_items: list = list(await search_command(bot, keyword, artist, title, source, guild))
    return_items.append(reply_msg)
    return return_items