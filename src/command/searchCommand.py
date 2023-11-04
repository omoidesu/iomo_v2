import asyncio
import pickle
from collections import deque

from khl import Bot, Guild, Message

from src.card import search_card, waiting_card
from src.const import Assets, index_emojis, redis_reaction
from src.dao import Redis
from src.dto import BeatmapSet, SearchListCacheDTO
from src.service import OsuApi, asset_service
from src.util import IdGenerator, construct_message_obj, filter_and_sort_beatmap_sets, search_beatmap_sets
from src.util.uploadAsset import generate_diff_png_and_upload, upload_asset, user_not_found_card


class SearchQueue:
    _instance: 'SearchQueue' = None
    _is_running: bool = False
    _queue: deque = deque()
    _redis = Redis.instance().get_connection()
    _emojis: list
    _bot: Bot = None
    _guild: Guild = None
    _id_generator = IdGenerator(1, 10)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def insert_search(self, bot: Bot, keyword: str, artist: str, title: str, source: str, guild: Guild,
                            msg: Message, bot_id: str):
        if not self._bot:
            self._bot = bot

        if not self._guild:
            self._guild = guild

        args = {
            'keyword': keyword,
            'artist': artist,
            'title': title,
            'source': source,
            'message': msg
        }
        length = len(self._queue)
        self._queue.append(args)
        if self._is_running:
            return waiting_card(f'排队中，请稍候 (前方还有{length}个等待搜索)')
        else:
            self._is_running = True
            await self._do_search(bot, bot_id)

    async def _do_search(self, bot, bot_id):
        while len(self._queue) > 0:
            args = self._queue.popleft()

            keyword = args.get('keyword')
            artist = args.get('artist')
            title = args.get('title')
            source = args.get('source')
            message: Message = args.get('message')

            search_id = self._id_generator.get_id()
            search_maps, _ = await search_beatmap_sets(title, source, '')
            if len(search_maps) == 0:
                card = await user_not_found_card(self._bot, '未找到相关谱面')
                await message.update(card)

            search_maps = filter_and_sort_beatmap_sets(artist, title, search_maps)

            # 每页谱面数
            step = 5
            pages = [search_maps[i:i + step] for i in range(0, len(search_maps), step)]

            # 上传资源并生成搜索卡片
            card, emojis = await upload_assets_and_generate_search_card(self._bot, self._guild, source, pages[0],
                                                                        keyword, 0, len(pages))

            # 卡片索引与对应谱面集id的映射
            index_beatmap = {}
            for i in range(len(pages[0])):
                index_beatmap[index_emojis[i]] = pages[0][i].id

            # 是否有下一页
            has_next = True if len(pages) > 1 else False
            cache_dto = SearchListCacheDTO(keyword, source, pages, index_beatmap, 0, message.ctx.guild.id)

            # 更新等待卡片为搜索结果
            await message.update(card)
            # 将搜索结果缓存到redis
            self._redis.set(message.id, redis_reaction.format(method="search", id=search_id))
            self._redis.set(search_id, pickle.dumps(cache_dto))

            # 生成消息对象
            search_result_message: Message = construct_message_obj(bot, message.id, message.ctx.channel.id,
                                                                   message.ctx.guild.id, bot_id)

            # 根据映射中的key添加回应
            for emoji in index_beatmap.keys():
                await search_result_message.add_reaction(emoji)

            # 如果存在下一页添加下一页的按钮
            if has_next:
                await search_result_message.add_reaction('arrow_right')

            # 删除表情
            if emojis:
                tasks = [asyncio.create_task(self._guild.delete_emoji(emoji)) for emoji in emojis]
                await asyncio.wait(tasks)

        self._is_running = False


async def upload_assets_and_generate_search_card(bot: Bot, guild: Guild, source: str, beatmapsets: list[BeatmapSet],
                                                 keyword: str, current_page: int, total_page: int):
    tasks = []
    task = []

    api = OsuApi()
    emojis = []
    # 资源上传
    kwargs = {}
    cover_url = {}
    for beatmapset in beatmapsets:
        if source == 'sayo':
            beatmapset_info = await api.get_beatmapset_info(beatmapset.id)
            beatmapset = BeatmapSet(**beatmapset_info)

        if beatmapset.cover_list:
            cover_url[str(beatmapset.id)] = beatmapset.cover_list

        beatmaps_count = len(beatmapset.beatmaps)
        if beatmaps_count > 15:
            max_diff = 14
        else:
            max_diff = 15

        for beatmap in beatmapset.beatmaps[:max_diff]:
            # 搜索卡片每个谱面最多展示15个难度，过多会折行，如果超过15个应该展示14个难度，剩下的用+n表示
            mode = beatmap.mode
            diff = beatmap.difficulty_rating
            if diff < 8:
                if f'{mode}{diff}' in task:
                    continue
                tasks.append(asyncio.create_task(__generate_diff(bot, mode, diff, guild, kwargs, emojis)))
                task.append(f'{mode}{diff}')
            else:
                kwargs[f'{mode}{diff}'] = Assets.Sticker.DIFF.get(mode)

    oss_url = asset_service.select_asset_batch(**cover_url)
    for beatmapset_id, url in oss_url.items():
        if url:
            kwargs[f'cover{beatmapset_id}'] = url
        else:
            tasks.append(
                asyncio.create_task(upload_asset(bot, cover_url.get(beatmapset_id), kwargs, f'cover{beatmapset_id}',
                                                 Assets.Image.DEFAULT_COVER)))

    await asyncio.wait(tasks)
    return search_card(keyword, beatmapsets, current_page, total_page, **kwargs), emojis


async def __generate_diff(bot, mode, diff, guild, to: dict, emojis):
    emoji = await generate_diff_png_and_upload(bot, mode, diff, emoji=True, guild=guild)
    to[f'{mode}{diff}'] = f'(emj){emoji.name}(emj)[{emoji.id}]'
    emojis.append(emoji)
