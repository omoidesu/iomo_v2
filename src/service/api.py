import json

import aiohttp
import requests
from aiohttp import TCPConnector

from src.config import client_id, client_secret
from src.const import osu_api, redis_access_token, redis_refresh_token, sayo_api
from src.dao import Redis
from src.exception import ArgsException, NetException, OsuApiException


class OsuApi:
    _access_token: str
    _refresh_token: str
    _header: dict

    _redis = None

    """
    routers:
        /users/{user}/{mode?} 获取用户信息
        /users 获取多个用户信息
        /users/{user}/scores/recent 获取最近游玩记录
        /users/{user}/scores/best 获取bp
        /beatmaps/{beatmap_id}/scores/users/{user} 获取指定谱面成绩
        /beatmaps/{beatmap_id}/scores 获取谱面top成绩
        /beatmaps/{beatmap_id} 获取谱面信息
        /beatmapsets/{beatmapset_id} 获取谱面集信息
        /beatmapsets/search 搜索谱面集
        /matches 获取mp房间列表
        /matches/{match_id} 获取mp游戏信息
        /rankings/{mode}/{type} 获取排行榜
    """

    def __init__(self):
        self._redis = Redis.instance().get_connection()
        access_token_byte = self._redis.get(redis_access_token)
        self._access_token = access_token_byte.decode('utf-8')
        refresh_token_byte = self._redis.get(redis_refresh_token)
        self._refresh_token = refresh_token_byte.decode('utf-8') if refresh_token_byte is not None else None

        if self._access_token is None:
            self.refresh_token()

        self._header = {
            'Authorization': f'Bearer {self._access_token}'
        }

    async def refresh_token(self):
        """刷新token"""
        url = 'https://osu.ppy.sh/oauth/token'
        data = {
            'grant_type': 'refresh_token',
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': self._refresh_token
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as resp:
                if resp.status != 200:
                    raise OsuApiException(f'刷新token失败 code: {resp.status}')

                resp_json = await resp.json()

        self._access_token = resp_json['access_token']
        self._refresh_token = resp_json['refresh_token']

        self._redis.set(redis_access_token, self._access_token)
        self._redis.set(redis_refresh_token, self._refresh_token)

    async def get_user(self, user_id: str = None, mode: str = 'osu', use_mode: bool = False):
        """获取用户"""
        if user_id is None:
            raise ArgsException('user_id不能为空')

        if user_id.isdigit() or use_mode:
            url = f'{osu_api}/users/{user_id}/{mode}'
        else:
            url = f'{osu_api}/users/{user_id}'

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self._header) as resp:
                if resp.status != 200:
                    raise OsuApiException(resp.status)

                return await resp.json()

    async def get_users(self, *osu_ids):
        """获取多个用户"""
        url = f'{osu_api}/users'
        params = {
            'ids[]': osu_ids
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=self._header) as resp:
                if resp.status != 200:
                    raise OsuApiException(resp.status)

                return await resp.json()

    async def get_recent_score(self, user_id: int = None, mode: str = 'osu', limit: int = 5,
                               include_fail: bool = True, use_mode: bool = False):
        """获取最近游玩记录"""
        if user_id is None:
            raise ArgsException('user_id不能为空')

        url = f'{osu_api}/users/{user_id}/scores/recent'
        params = {
            'include_fails': 1 if include_fail else 0,
            'limit': limit
        }
        if use_mode:
            params['mode'] = mode

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=self._header) as resp:
                if resp.status != 200:
                    raise OsuApiException(resp.status)

                return await resp.json()

    async def get_best_score(self, user_id: str = None, mode: str = 'osu', limit: int = 10):
        """获取bp"""
        if user_id is None:
            raise ArgsException('user_id不能为空')

        url = f'{osu_api}/users/{user_id}/scores/best'
        params = {
            'limit': limit,
            'mode': mode
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=self._header) as resp:
                if resp.status != 200:
                    raise OsuApiException(resp.status)

                return await resp.json()

    async def get_beatmap_score(self, beatmap_id: int, user_id: int, mode: str = 'osu'):
        """获取指定谱面成绩"""
        url = f'{osu_api}/beatmaps/{beatmap_id}/scores/users/{user_id}'
        params = {
            'mode': mode
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=self._header) as resp:
                if resp.status != 200:
                    raise OsuApiException(resp.status)

                return await resp.json()

    async def get_beatmap_top_score(self, beatmap_id: int, mode: str = 'osu'):
        """获取谱面top成绩"""
        url = f'{osu_api}/beatmaps/{beatmap_id}/scores'
        params = {
            'mode': mode
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=self._header) as resp:
                if resp.status != 200:
                    raise OsuApiException(resp.status)

                return await resp.json()

    async def get_beatmap_info(self, beatmap_id: int):
        """获取谱面信息"""
        url = f'{osu_api}/beatmaps/{beatmap_id}'

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self._header) as resp:
                if resp.status != 200:
                    raise OsuApiException(resp.status)

                return await resp.json()

    async def get_beatmapset_info(self, beatmapset_id: int):
        """获取谱面集信息"""
        url = f'{osu_api}/beatmapsets/{beatmapset_id}'

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self._header) as resp:
                if resp.status != 200:
                    raise OsuApiException(resp.status)

                return await resp.json()

    async def search_beatmapset(self, keyword: str, mode: str = None, cursor_string: str = '',
                                include_unrank: bool = False):
        """搜索谱面集"""
        modes = {'osu': 0, 'taiko': 1, 'fruits': 2, 'mania': 3}

        url = f'{osu_api}/beatmapsets/search'
        params = {
            'q': keyword
        }

        if cursor_string:
            params['cursor_string'] = cursor_string

        if mode is not None:
            params['m'] = modes.get(mode)

        if include_unrank:
            params['s'] = 'any'

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=self._header) as resp:
                if resp.status != 200:
                    raise OsuApiException(resp.status)

                return await resp.json()

    async def get_match_list(self, cursor_string: str = None):
        """获取mp房间列表"""
        url = f'{osu_api}/matches'
        params = {
            'cursor_string': cursor_string
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=self._header) as resp:
                if resp.status != 200:
                    raise OsuApiException(resp.status)

                return await resp.json()

    async def get_match_event(self, match_id: int, after: str = '', limit: int = 10, no_limit: bool = False):
        """获取mp游戏信息"""
        url = f'{osu_api}/matches/{match_id}'
        params = {
            'after': after,
        }

        if not no_limit:
            params['limit'] = limit

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=self._header) as resp:
                if resp.status != 200:
                    raise OsuApiException(resp.status)

                return await resp.json()

    async def get_global_ranking(self, mode: str, country: str = None):
        """获取全球排行榜"""
        url = f'{osu_api}/rankings/{mode}/performance'
        params = {
            'country': country
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=self._header) as resp:
                if resp.status != 200:
                    raise OsuApiException(resp.status)

                return await resp.json()


class SayoApi:
    @staticmethod
    async def search(keyword: str, mode: int, offset: str = ''):
        """
            sayo api搜索谱面
            文档：https://www.showdoc.com.cn/SoulDee/3969517351482508
        """
        url = f'{sayo_api}/?post'

        data = {
            'cmd': 'beatmaplist',
            'keyword': keyword,
            'mode': mode if mode else 15,
            'type': 'search',
            'offset': 0 if not offset else offset
        }

        async with aiohttp.ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
            async with session.post(url, data=json.dumps(data)) as resp:
                if resp.status != 200:
                    raise NetException(f'搜索谱面失败 code: {resp.status}')

                return await resp.json()

    @staticmethod
    async def get_beatmap_info(keyword: str, id_mode: bool = False):
        url = f'{sayo_api}/v2/beatmapinfo'
        params = {
            'K': keyword,
            'T': 1 if id_mode else 0,
        }

        async with aiohttp.ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
            async with session.get(url, params=params) as resp:
                if resp.status != 200:
                    raise NetException(f'获取谱面信息失败 code: {resp.status}')

                return json.loads(await resp.text())

    @staticmethod
    async def download_beatmaps(beatmapset_id: int):
        url = f'https://dl.sayobot.cn/beatmaps/download/novideo/{beatmapset_id}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'referer': 'https://osu.sayobot.cn/home'
        }
        async with aiohttp.ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    raise NetException(f'下载失败 code: {resp.status}')

                return await resp.content.read()


class Chimu:
    ...
