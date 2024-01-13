import re

from khl import Bot, Event, EventTypes, Guild, Message, User

from src.card import waiting_card
from src.command import beatmap_set_command, update_osu_info
from src.config import admin_id, bot_token, emoji_guild as guild_id, playing_game_id
from src.parser import (bind_parser, bp_parser, bp_today_parser, button_queue, compare_parser, copy_parser, info_parser,
                        mode_parser, mp_parser, osu_homepage_parser, ping_parser, ranking_parser, reaction_queue,
                        recent_parser, score_parser, search_parser, unbind_parser, update_asset_parser)
from src.schedule import redis_schedule
from src.util.afterCommend import add_reaction, cache_map_to_redis, collect_user_info

bot = Bot(token=bot_token)
me: User
emoji_guild: Guild


@bot.on_startup
async def on_startup(b: Bot):
    global me
    global emoji_guild
    me = await b.client.fetch_me()
    await b.client.update_playing_game(playing_game_id)

    emoji_guild = await bot.client.fetch_guild(guild_id)
    print('bot 启动!')


@bot.command(name='prpr', aliases=['ping'], prefixes=['.', '/'])
async def ping(msg: Message, *args):
    reply = ping_parser(msg, *args)
    await msg.reply(reply)


@bot.command(name='clear')
async def clear_emoji(msg: Message):
    if msg.author.id in admin_id:
        await msg.reply(f'开始清理社区{emoji_guild.name}的所有表情')
        emoji_list = await emoji_guild.fetch_emoji_list()
        for emoji in emoji_list:
            await emoji_guild.delete_emoji(emoji)

        await msg.reply(f'清理完成，总共清理了{len(emoji_list)}个表情')
    else:
        await msg.reply('你不是管理员，无权使用该命令')


@bot.command(name='bind', prefixes=['.', '/'])
async def bind(msg: Message, *args):
    reply, id_map = await bind_parser(bot, msg, *args)
    await msg.reply(reply)
    if id_map is not None:
        await collect_user_info(**id_map)


@bot.command(name='unbind', prefixes=['.', '/'])
async def unbind(msg: Message, *args):
    reply = await unbind_parser(msg, *args)
    await msg.reply(reply)


@bot.command(name='info', prefixes=['.', '/'])
async def info(msg: Message, *args):
    reply = await info_parser(bot, msg, *args)
    await msg.reply(reply)


@bot.command(name='mode', aliases=['setmode'], prefixes=['.', '/'])
async def mode(msg: Message, *args):
    reply = await mode_parser(msg, *args)
    await msg.reply(reply)


@bot.command(name='recent', aliases=['r'], prefixes=['.', '/'])
async def recent(msg: Message, *args):
    reply, cache_dto = await recent_parser(bot, msg, *args, include_fail=True)
    reply_msg = await msg.reply(reply)
    if cache_dto is not None:
        cache_map_to_redis(reply_msg.get('msg_id'), cache_dto)
        await add_reaction(bot, reply_msg.get('msg_id'), msg, me.id, cache_dto)


@bot.command(name='precent', aliases=['p', 'pr'], prefixes=['.', '/'])
async def precent(msg: Message, *args):
    reply, cache_dto = await recent_parser(bot, msg, *args, include_fail=False)
    reply_msg = await msg.reply(reply)
    if cache_dto is not None:
        cache_map_to_redis(reply_msg.get('msg_id'), cache_dto)
        await add_reaction(bot, reply_msg.get('msg_id'), msg, me.id, cache_dto)


@bot.command(name='score', aliases=['s'], prefixes=['.', '/'])
async def score(msg: Message, *args):
    reply = await score_parser(bot, msg, *args)
    await msg.reply(reply)


@bot.command(name='compare', aliases=['c'], prefixes=['.', '/'])
async def compare(msg: Message):
    reply = await compare_parser(bot, msg)
    await msg.reply(reply)


@bot.command(name='search', prefixes=['.', '/'])
async def search(msg: Message, *args):
    waiting = await msg.reply(waiting_card('正在搜索中，请稍候'))
    waiting_msg, reply, func, *f_args = await search_parser(bot, msg, emoji_guild, waiting.get('msg_id'), me.id, *args)
    if waiting_msg:
        await waiting_msg.update(reply)
        if func:
            after = await func(*f_args)
            if after:
                await waiting_msg.update(after)


@bot.command(name='bp', prefixes=['.', '/'])
async def bp(msg: Message, *args):
    reply = await bp_parser(bot, msg, *args)
    await msg.reply(reply)


@bot.command(name='bptoday', aliases=['bpme', 't', 'today'], prefixes=['.', '/'])
async def bptoday(msg: Message, *args):
    cards = await bp_today_parser(bot, msg, *args)
    await msg.reply(cards[0])
    for card in cards[1:]:
        await msg.ctx.channel.send(card)


@bot.command(name='rank', prefixes=['.', '/'])
async def rank(msg: Message, *args):
    reply = await ranking_parser(msg, *args)
    await msg.reply(reply)


@bot.command(name='mp', prefixes=['.', '/'])
async def mp(msg: Message, *args):
    reply = await mp_parser(bot, msg, *args)
    await msg.reply(reply)


@bot.command(name='copy', aliases=['cp'], prefixes=['.', '/'])
async def copy(msg: Message, *args):
    waiting = await msg.reply(waiting_card('下载中，请稍候'))
    reply, waiting_msg = await copy_parser(bot, msg, waiting.get('msg_id'), me.id, *args)
    await waiting_msg.update(reply)


@bot.command(name='pp', prefixes=['.', '/'])
async def pp(msg: Message, *args):
    await msg.reply('该功能未完成')


@bot.command(name='music', prefixes=['.', '/'])
async def music(msg: Message, *args):
    await msg.reply('该功能未完成')


@bot.command(name='token')
async def refresh_osu_token(msg: Message):
    from src.service import OsuApi

    if msg.author.id in admin_id:
        api = OsuApi()
        await api.refresh_token()
        await msg.reply('token刷新成功')
    else:
        await msg.reply('你不是管理员，无权使用该命令')


@bot.command(name='update')
async def update(msg: Message):
    reply = await update_asset_parser(bot, msg)
    await msg.reply(reply)


@bot.command(regex=r'.+https://osu\.ppy\.sh/beatmapsets/\d+.+', prefixes=[])
async def beatmap_link(msg: Message):
    args = re.findall(r'https://osu\.ppy\.sh/beatmapsets/(\d+)(#(mania|osu|taiko|fruits)/(\d+))?', msg.content)[0]
    set_id = int(args[0])
    map_id = int(args[3]) if args[3] else None
    reply = await beatmap_set_command(bot, set_id, map_id)
    await msg.ctx.channel.send(reply)


@bot.command(regex=r'.+https://osu.ppy.sh/users/\d+.+', prefixes=[])
async def user_link(msg: Message):
    reply, id_map = await osu_homepage_parser(bot, msg)
    await msg.reply(reply)
    if id_map is not None:
        await collect_user_info(**id_map)


@bot.on_event(EventTypes.ADDED_REACTION)
async def on_added_emoji(_: Bot, e: Event):
    msg_id = e.body.get('msg_id')
    user_id = e.body.get('user_id')
    emoji_id = e.body.get('emoji').get('id')
    channel_id = e.body.get('channel_id')

    if user_id == me.id:
        return

    await reaction_queue.insert_reaction(bot, me.id, {'msg_id': msg_id, 'user_id': user_id, 'emoji_id': emoji_id,
                                                      'channel_id': channel_id}, emoji_guild)


# deprecated 因为kook调整了卡片消息中按钮的相应，故目前没有包含按钮的卡片消息，该事件暂时不会被触发
@bot.on_event(EventTypes.MESSAGE_BTN_CLICK)
async def on_btn_click(_: Bot, e: Event):
    body = e.body
    await button_queue.insert_button(bot, me.id, body, emoji_guild)


@bot.task.add_interval(seconds=1)
async def redis_event_handler():
    await redis_schedule(bot)


@bot.task.add_cron(hour=2)
async def refresh_osu_token():
    from src.service import OsuApi

    api = OsuApi()
    await api.refresh_token()


@bot.task.add_cron(hour=3)
async def update_user_info():
    await update_osu_info()


def save_cardmsg(reply):
    """卡片消息未通过验证时检查内容用"""
    import json
    import os

    with open(os.path.join(os.path.dirname(__file__), 'card_message.json'), 'w', encoding='utf-8') as f:
        json.dump(reply, f, ensure_ascii=False, indent=4)
