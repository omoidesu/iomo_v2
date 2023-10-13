import asyncio

from khl import Bot

from src.card import mp_card
from src.const import Assets, redis_mp_room
from src.dao import Redis
from src.dto import MultiPlay, User
from src.exception import OsuApiException
from src.service import OsuApi
from src.util.uploadAsset import generate_stars, upload_asset


class MultiPlayCommand:
    _rooms: dict = {}
    _instance: 'MultiPlayCommand' = None
    _redis = Redis.instance().get_connection()

    @classmethod
    def instance(cls) -> 'MultiPlayCommand':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def fetch_room(self, bot: Bot, channel_id: int, room: str):
        api = OsuApi()

        if room.isdigit():
            if room in self._rooms.keys():
                return '该房间已在监听中'
            try:
                match = await api.get_match_event(int(room), no_limit=True)
            except OsuApiException as e:
                if e.code == 404:
                    ...
            else:
                events = match.get('events', [])
                if events and events[-1].get('detail', {}).get('type') == 'match-disbanded':
                    match_name = match.get('match', {}).get('name')
                    return f'房间{match_name}已关闭 请确认id是否正确'

                match_id = match.get('match', {}).get('id')
                return self.__add_jobs(bot, match, match_id, channel_id)

        cursor = ''
        match_id = 0
        page = 0

        while True:
            if page >= 20:
                break
            match_list = await api.get_match_list(cursor_string=cursor)
            matches = match_list.get('matches', [])
            cursor = match_list.get('cursor_string')

            target = list(filter(lambda x: room.lower() in x.get('name').lower(), matches))
            if target:
                match_id = target[0].get('id')
                break

            page += 1

        if match_id == 0:
            return '未找到该房间，请输入房间id'

        if match_id in self._rooms.keys():
            return '该房间已在监听中'

        match = await api.get_match_event(match_id, no_limit=True)
        events = match.get('events', [])
        if events and events[-1].get('detail', {}).get('type') == 'match-disbanded':
            match_name = match.get('match', {}).get('name')
            return f'房间{match_name}已关闭 请确认房间名称或直接输入房间id'

        return self.__add_jobs(bot, match, match_id, channel_id)

    async def get_mp_events(self, bot: Bot, match_id: int, after: str):
        obj: MultiPlay = self._rooms.get(match_id)
        channel = await bot.client.fetch_public_channel(obj.channel_id)
        api = OsuApi()

        data = await api.get_match_event(match_id, after=after)
        events = data.get('events')

        if not events:
            return None, after

        for event in events:
            event_type = event.get('detail', {}).get('type')

            # 开始游戏
            if event_type == 'other':
                game = event.get('game', {})
                # 如果没有分数，说明游戏还没结束
                if not game.get('scores'):
                    continue

                if game.get('team_type') == 'head-to-head':
                    tasks = []
                    kwargs = {}

                    users = data.get('users')
                    for user in users:
                        tasks.append(asyncio.create_task(
                            upload_asset(bot, user.get('avatar_url'), kwargs, f'avatar{user.get("id")}',
                                         Assets.Image.DEFAULT_AVATAR)))
                    user_map = {user['id']: User(**user) for user in users}

                    beatmap = game.get('beatmap', {})
                    tasks.append(asyncio.create_task(
                        generate_stars(bot, beatmap.get('mode'), beatmap.get('difficulty_rating'), kwargs, 'diff')))

                    scores = sorted(game.get('scores'), key=lambda x: x.get('score'), reverse=True)

                    cover = game.get('beatmap', {}).get('beatmapset', {}).get('covers', {}).get('cover')
                    if cover:
                        tasks.append(
                            asyncio.create_task(upload_asset(bot, cover, kwargs, 'cover', Assets.Image.DEFAULT_COVER)))
                    else:
                        kwargs['cover'] = Assets.Image.DEFAULT_COVER

                    obj.event_id = events[-1].get('id')
                    job = bot.task.scheduler.get_job(obj.job_id)
                    job.modify(args=[bot, match_id, obj.event_id])

                    await asyncio.wait(tasks)
                    await bot.client.send(channel, mp_card(game, user_map, scores, **kwargs))

            # 房间关闭
            elif event_type == 'match-disbanded':
                self.remove_room(bot, match_id, obj.channel_id)
                await bot.client.send(channel, f'{obj.match_name}房间已关闭')

    def list_room(self, channel_id: str):
        if not self._rooms:
            return '当前没有正在监听的房间'

        enter = '\n'

        return f'正在监听的房间: \n{enter.join([f"{room.match_name} ({room_id})" for room_id, room in self._rooms.items() if room.channel_id == channel_id])}'

    def remove_room(self, bot: Bot, room: int, channel_id: int):
        target_room: MultiPlay

        if str(room).isdigit():
            target_room = self._rooms.get(int(room))
            if not target_room:
                filter_rooms = list(
                    filter(lambda x: x.match_name == room and x.channel_id == channel_id, self._rooms.values()))
                if not filter_rooms:
                    return '该房间未在监听中'
                else:
                    target_room = filter_rooms[0]

        else:
            filter_rooms = list(filter(lambda x: room.lower() in x.match_name.lower() and x.channel_id == channel_id,
                                       self._rooms.values()))
            if not filter_rooms:
                return '该房间未在监听中'
            else:
                target_room = filter_rooms[0]

        bot.task.scheduler.remove_job(target_room.job_id)
        self._rooms.pop(target_room.match_id)
        self._redis.delete(redis_mp_room.format(target_room.match_id))
        return f'已停止监听房间{target_room.match_name}'

    def remove_all(self, bot: Bot):
        for room in self._rooms.values():
            bot.task.scheduler.remove_job(room.job_id)
            self._redis.delete(redis_mp_room.format(room.match_id))
        self._rooms.clear()
        return '已停止所有监听'

    def __add_jobs(self, bot: Bot, match: dict, match_id: int, channel_id: int):
        match_name = match.get('match', {}).get('name')
        last_event_id = match.get('events', [])[-1].get('id')

        job = bot.task.scheduler.add_job(self.get_mp_events, 'interval', seconds=5,
                                         args=[bot, match_id, last_event_id])
        self._rooms[match_id] = MultiPlay(match_id, match_name, last_event_id, channel_id, job.id)

        # 缓存redis并设置过期时间为8小时
        redis_key = redis_mp_room.format(match_id)
        self._redis.set(redis_key, match_id)
        self._redis.expire(redis_key, 60 * 60 * 8)
        return '已开始监听房间: ' + match_name
