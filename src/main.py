from khl import Bot, Message

from src.config import bot_token
from src.behavior.afterCommend import collect_user_info
from src.parser import (
    ping_parser,
    bind_parser,
    unbind_parser,
    info_parser
)

bot = Bot(token=bot_token)


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
