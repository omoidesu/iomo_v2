from khl import Bot, Event, EventTypes, Message, User

from src.config import bot_token
from src.parser import (bind_parser, info_parser, ping_parser, reaction_parser, recent_parser, unbind_parser)
from src.util.afterCommend import add_reaction, cache_map_to_redis, collect_user_info

bot = Bot(token=bot_token)
me: User


@bot.on_startup
async def on_startup(bot: Bot):
    global me
    me = await bot.client.fetch_me()


@bot.command(name='prpr', aliases=['ping'], prefixes=['.'])
async def ping(msg: Message, *args):
    reply = ping_parser(msg, *args)
    await msg.reply(reply)


@bot.command(name='bind', prefixes=['.'])
async def bind(msg: Message, *args):
    reply, id_map = await bind_parser(bot, msg, *args)
    await msg.reply(reply)
    if id_map is not None:
        await collect_user_info(**id_map)


@bot.command(name='unbind', prefixes=['.'])
async def unbind(msg: Message, *args):
    reply = await unbind_parser(msg, *args)
    await msg.reply(reply)


@bot.command(name='info', prefixes=['.'])
async def info(msg: Message, *args):
    reply = await info_parser(bot, msg, *args)
    await msg.reply(reply)


@bot.command(name='recent', aliases=['r'], prefixes=['.'])
async def recent(msg: Message, *args):
    reply, cache_dto = await recent_parser(bot, msg, *args, include_fail=True)
    reply_msg = await msg.reply(reply)
    if cache_dto is not None:
        cache_map_to_redis(reply_msg.get('msg_id'), cache_dto)
        await add_reaction(bot, reply_msg.get('msg_id'), msg, me.id, cache_dto)


@bot.command(name='precent', aliases=['p', 'pr'], prefixes=['.'])
async def precent(msg: Message, *args):
    reply, cache_dto = await recent_parser(bot, msg, *args, include_fail=False)
    reply_msg = await msg.reply(reply)
    if cache_dto is not None:
        cache_map_to_redis(reply_msg.get('msg_id'), cache_dto)
        await add_reaction(bot, reply_msg.get('msg_id'), msg, me.id, cache_dto)


@bot.on_event(EventTypes.ADDED_REACTION)
async def on_added_emoji(bot: Bot, e: Event):
    msg_id = e.body.get('msg_id')
    user_id = e.body.get('user_id')
    emoji_id = e.body.get('emoji').get('id')
    channel_id = e.body.get('channel_id')

    if user_id == me.id:
        return

    await reaction_parser.insert_reaction(bot, me.id, {'msg_id': msg_id, 'user_id': user_id, 'emoji_id': emoji_id,
                                                       'channel_id': channel_id})
