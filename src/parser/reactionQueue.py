import json
from collections import deque

from khl import Bot

from src.command import reaction_callback
from src.dao import Redis
from src.dto import RecentListCacheDTO
from src.util import construct_message_obj


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

    async def insert_reaction(self, bot: Bot, bot_id: int, reaction: dict):
        self._reaction_queue.append(reaction)
        if not self._is_running:
            self._is_running = True
            await self._parse_reaction(bot, bot_id)

    async def _parse_reaction(self, bot: Bot, bot_id):
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

            dto = RecentListCacheDTO(
                **json.loads(cache.decode('utf-8').replace("'", '"').replace('True', 'true').replace('False', 'false')))
            if dto.author_id != user_id:
                continue

            score_id = dto.id_map.get(emoji_id)
            if score_id is None:
                continue

            pass_msg.append(msg_id)

            msg = construct_message_obj(bot, msg_id, channel_id, dto.guild_id, bot_id)
            await msg.delete()
            reply_msg = await reaction_callback(bot, self._redis, channel_id, score_id, dto)
            await msg.ctx.channel.send(reply_msg, quote=dto.msg_id)
            self._redis.delete(msg_id)

        self._is_running = False
