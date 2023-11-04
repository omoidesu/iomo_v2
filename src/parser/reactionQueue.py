import asyncio
import json
import pickle
from collections import deque

from khl import Bot, Message

from src.card import waiting_card
from src.command import beatmap_set_command, reaction_callback, upload_assets_and_generate_search_card
from src.const import index_emojis, redis_reaction
from src.dao import Redis
from src.dto import RecentListCacheDTO, SearchListCacheDTO
from src.util import construct_message_obj
from src.util.messageUtil import fetch_message


class ReactionQueue:
    _instance: 'ReactionQueue' = None
    _reaction_queue: deque = deque()
    _is_running = False
    _redis = Redis.instance().get_connection()

    @classmethod
    def instance(cls) -> 'ReactionQueue':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def insert_reaction(self, bot: Bot, bot_id: int, reaction: dict, emoji_guild):
        self._reaction_queue.append(reaction)
        if len(self._reaction_queue) == 0:
            self._is_running = False
        if not self._is_running:
            self._is_running = True
            await self._parse_reaction(bot, bot_id, emoji_guild)

    async def _parse_reaction(self, bot: Bot, bot_id, emoji_guild):
        # 已处理msg_id
        pass_msg = []

        while len(self._reaction_queue) > 0:
            reaction = self._reaction_queue.popleft()
            msg_id = reaction.get('msg_id')
            user_id = reaction.get('user_id')
            emoji_id = reaction.get('emoji_id')
            channel_id = reaction.get('channel_id')

            if msg_id in pass_msg:
                continue

            cache = self._redis.get(msg_id)
            if cache is None:
                continue

            method, cache_id = cache.decode('utf-8').split(':')
            cache_dto = self._redis.get(cache_id)
            if cache_dto is None:
                continue

            if method == 'recent':
                dto: RecentListCacheDTO = RecentListCacheDTO(**json.loads(
                    cache_dto.decode('utf-8').replace("'", '"').replace('True', 'true').replace('False', 'false')))

                if dto.author_id != user_id:
                    continue

                score_id = dto.id_map.get(emoji_id)
                # 如果回应的emoji不是1-5的数字
                if score_id is None:
                    continue

                pass_msg.append(msg_id)

                msg = construct_message_obj(bot, msg_id, channel_id, dto.guild_id, bot_id)
                await msg.delete()
                reply_msg = await reaction_callback(bot, self._redis, channel_id, score_id, dto)
                await msg.ctx.channel.send(reply_msg, quote=dto.msg_id)
                self._redis.delete(msg_id)
            elif method == 'search':
                dto: SearchListCacheDTO = pickle.loads(cache_dto)
                msg = construct_message_obj(bot, msg_id, channel_id, dto.guild_id, bot_id)

                # 如果回应的emoji是向右箭头 则应该发送下一页的搜索结果
                if emoji_id == '➡':
                    # 下一页页码
                    next_page = dto.current_page + 1
                    # 如果页码大于最大页
                    if next_page >= len(dto.pages):
                        continue

                    # 标记该消息为已处理
                    pass_msg.append(msg_id)

                    # 获取目标消息，用来获取该消息回复的消息id
                    target_message = await fetch_message(bot, msg_id)
                    await msg.delete()
                    # 发送等待卡片
                    waiting_message: dict = await msg.ctx.channel.send(waiting_card('正在搜索中，请稍候'),
                                                                       quote=target_message.get('quote').get('id'))

                    waiting_msg: Message = construct_message_obj(bot, waiting_message.get('msg_id'), channel_id,
                                                                 dto.guild_id, bot_id)

                    page = dto.pages[next_page]
                    # 生成搜索结果卡片并发送
                    next_search, emojis = await upload_assets_and_generate_search_card(bot, emoji_guild, dto.source,
                                                                                       page, dto.keyword, next_page,
                                                                                       len(dto.pages))
                    await waiting_msg.update(next_search)

                    # 添加上一页的箭头回应
                    await waiting_msg.add_reaction('arrow_left')

                    # 添加序号回应
                    index_beatmap = {}
                    for i in range(len(page)):
                        index_beatmap[index_emojis[i]] = page[i].id
                        await waiting_msg.add_reaction(index_emojis[i])

                    # 如果有下一页 则添加下一页的箭头回应
                    if next_page != len(dto.pages) - 1:
                        await waiting_msg.add_reaction('arrow_right')

                    # redis中删除该条搜索相关的缓存并添加新的缓存
                    self._redis.delete(msg_id)
                    self._redis.delete(cache_id)
                    self._redis.set(waiting_message.get('msg_id'), redis_reaction.format(method="search", id=cache_id))
                    self._redis.set(cache_id, pickle.dumps(
                        SearchListCacheDTO(dto.keyword, dto.source, dto.pages, index_beatmap, next_page, dto.guild_id)))

                    # 清空表情
                    if emojis:
                        tasks = [asyncio.create_task(emoji_guild.delete_emoji(emoji)) for emoji in emojis]
                        await asyncio.wait(tasks)

                    continue
                # 同理 如果回应的emoji是向左箭头 则应该发送上一页的搜索结果
                elif emoji_id == '⬅':
                    # 上一页的页码
                    prev_page = dto.current_page - 1
                    # 如果上一页小于0
                    if prev_page < 0:
                        continue

                    # 标记该消息已处理
                    pass_msg.append(msg_id)

                    # 获取目标消息，用来获取该消息回复的消息id
                    target_message = await fetch_message(bot, msg_id)
                    await msg.delete()
                    # 发送等待卡片
                    waiting_message: dict = await msg.ctx.channel.send(waiting_card('正在搜索中，请稍候'),
                                                                       quote=target_message.get('quote').get('id'))
                    waiting_msg: Message = construct_message_obj(bot, waiting_message.get('msg_id'), channel_id,
                                                                 dto.guild_id, bot_id)

                    page = dto.pages[prev_page]
                    # 生成搜索结果卡片并发送
                    prev_search, emojis = await upload_assets_and_generate_search_card(bot, emoji_guild, dto.source,
                                                                                       page, dto.keyword, prev_page,
                                                                                       len(dto.pages))
                    await waiting_msg.update(prev_search)

                    # 如果上一页不是第一页 则添加上一页的箭头回应
                    if prev_page != 0:
                        await waiting_msg.add_reaction('arrow_left')

                    # 添加序号回应
                    index_beatmap = {}
                    for i in range(len(page)):
                        index_beatmap[index_emojis[i]] = page[i].id
                        await waiting_msg.add_reaction(index_emojis[i])

                    # 添加下一页的箭头回应
                    await waiting_msg.add_reaction('arrow_right')

                    # redis中删除该条搜索相关的缓存并添加新的缓存
                    self._redis.delete(msg_id)
                    self._redis.delete(cache_id)
                    self._redis.set(waiting_message.get('msg_id'), redis_reaction.format(method="search", id=cache_id))
                    self._redis.set(cache_id, pickle.dumps(
                        SearchListCacheDTO(dto.keyword, dto.source, dto.pages, index_beatmap, prev_page, dto.guild_id)))

                    # 清空表情
                    if emojis:
                        tasks = [asyncio.create_task(emoji_guild.delete_emoji(emoji)) for emoji in emojis]
                        await asyncio.wait(tasks)
                    continue

                beatmapset_id = dto.reactions.get(emoji_id)
                if beatmapset_id is None:
                    continue

                # 标记该消息已处理
                pass_msg.append(msg_id)

                # 获取目标消息，用来获取该消息回复的消息id
                target_message = await fetch_message(bot, msg_id)
                await msg.delete()
                # 发送等待卡片
                waiting_message: dict = await msg.ctx.channel.send(waiting_card('正在搜索中，请稍候'),
                                                                   quote=target_message.get('quote').get('id'))
                waiting_msg: Message = construct_message_obj(bot, waiting_message.get('msg_id'), channel_id,
                                                             dto.guild_id, bot_id)

                # 生成谱面集卡片并发送
                search_result_card = await beatmap_set_command(bot, beatmapset_id)
                await waiting_msg.update(search_result_card)

                # redis中删除该条搜索相关的缓存
                self._redis.delete(msg_id)
                self._redis.delete(cache_id)

        self._is_running = False
