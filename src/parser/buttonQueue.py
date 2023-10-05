from collections import deque

from khl import Bot, Guild

from src.dao import Redis
import pickle

from src.dto import SearchListCacheDTO
from src.util import construct_message_obj
from src.card import search_waiting_card
from src.command import beatmap_set_command, upload_assets_and_generate_search_card
from src.util.afterCommend import delete_emojis


class ButtonQueue:
    _instance: 'ButtonQueue' = None
    _button_queue: deque = deque()
    _is_running = False
    _redis = Redis.instance().get_connection()

    @classmethod
    def instance(cls) -> 'ButtonQueue':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def insert_button(self, bot: Bot, bot_id: int, event_body: dict, guild: Guild):
        self._button_queue.append(event_body)
        if not self._is_running:
            self._is_running = True
            await self._parse_button(bot, bot_id, guild)

    async def _parse_button(self, bot: Bot, bot_id, guild: Guild):
        # 已处理msg_id
        pass_msg = []

        while len(self._button_queue) > 0:
            event = self._button_queue.popleft()
            click_user_id = event.get('user_id')
            callback_value = event.get('value')
            msg_id = event.get('msg_id')
            guild_id = event.get('guild_id')
            channel_id = event.get('channel_id')

            if msg_id in pass_msg:
                continue

            if callback_value == '':
                continue

            values = callback_value.split(':')
            if len(values) == 0:
                continue

            if values[0] == 'search':
                if len(values) != 4:
                    continue

                pass_msg.append(msg_id)

                msg = construct_message_obj(bot, msg_id, channel_id, guild_id, bot_id)
                await msg.update(search_waiting_card())

                _, search_id, method, value = values

                if method == 'set':
                    reply_card = await beatmap_set_command(bot, int(value))
                    await msg.update(reply_card)
                    self._redis.delete(f'search:{search_id}')
                elif method == 'page':
                    cache = self._redis.get(f'search:{search_id}')
                    if cache is None:
                        continue

                    dto: SearchListCacheDTO = pickle.loads(cache)

                    has_next, has_prev = True, True
                    page = int(value)
                    total_pages = len(dto.pages)
                    if page == 0:
                        has_prev = False

                    if page == total_pages - 1:
                        has_next = False

                    card_msg, emojis = await upload_assets_and_generate_search_card(bot, guild, dto.source,
                                                                                    dto.pages[page], dto.keyword,
                                                                                    search_id, page, total_pages,
                                                                                    has_next=has_next,
                                                                                    has_prev=has_prev)
                    await msg.update(card_msg)
                    await delete_emojis(guild, emojis)

        self._is_running = False
