from khl import Bot, Guild, Message

from src.command import beatmap_command, beatmap_set_command, search_command
from src.util import construct_message_obj
from src.util.afterCommend import delete_emojis
from src.util.log import save_log
from ._commonParser import args_parser


async def search_parser(bot: Bot, msg: Message, guild: Guild, reply_msg_id: str, bot_id: str, *args):
    save_log(msg, *args)

    reply_msg = construct_message_obj(bot, reply_msg_id, msg.ctx.channel.id, msg.ctx.guild.id, bot_id)

    require_args = args_parser(*args)
    keyword = require_args['keyword']
    source = require_args['source']
    beatmap_id = require_args['beatmap_id']
    beatmapset_id = require_args['beatmap_set_id']

    if beatmap_id:
        card_msg, *new_args = await beatmap_command(bot, beatmap_id)
        return reply_msg, card_msg, beatmap_set_command, bot, *new_args
    elif beatmapset_id:
        return reply_msg, await beatmap_set_command(bot, beatmapset_id), None, None
    else:
        if not keyword:
            return reply_msg, '请输入谱面信息', None, None

        if ' - ' in keyword:
            artist, title = keyword.split(' - ', 1)
        else:
            artist, title = '', keyword

    card_msg, emojis = await search_command(bot, keyword, artist, title, source, guild)
    return reply_msg, card_msg, delete_emojis, emojis
