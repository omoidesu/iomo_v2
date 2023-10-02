import json

import aiohttp
import requests
from aiohttp import TCPConnector

from src.config import client_id, client_secret
from src.const import osu_api, redis_access_token, redis_refresh_token, sayo_api
from src.dao import Redis
from src.exception import ArgsException, OsuApiException


class OsuApi:
    _access_token: str
    _refresh_token: str
    _header: dict

    _redis = None

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

    def refresh_token(self):
        url = 'osu.ppy.sh/oauth/token'
        data = {
            'grant_type': 'refresh_token',
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': self._refresh_token
        }

        resp = requests.post(url, data=data)
        if resp.status_code != 200:
            raise OsuApiException(f'刷新token失败 code: {resp.status_code}')

        resp_json = resp.json()
        self._access_token = resp_json['access_token']
        self._refresh_token = resp_json['refresh_token']

        self._redis.set(redis_access_token, self._access_token)
        self._redis.set(redis_refresh_token, self._refresh_token)

    async def get_user(self, user_id: str = None, mode: str = 'osu', use_mode: bool = False):
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
                    raise OsuApiException(f'获取bp失败 code: {resp.status}')

                return await resp.json()

    async def get_beatmap_score(self, beatmap_id: int, user_id: int, mode: str = 'osu'):
        url = f'{osu_api}/beatmaps/{beatmap_id}/scores/users/{user_id}'
        params = {
            'mode': mode
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=self._header) as resp:
                if resp.status != 200:
                    raise OsuApiException(f'获取成绩失败 code: {resp.status}')

                return await resp.json()

    async def get_beatmap_top_score(self, beatmap_id: int, mode: str = 'osu'):
        url = f'{osu_api}/beatmaps/{beatmap_id}/scores'
        params = {
            'mode': mode
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=self._header) as resp:
                if resp.status != 200:
                    raise OsuApiException(f'获取成绩失败 code: {resp.status}')

                return await resp.json()

    async def get_beatmap_info(self, beatmap_id: int):
        url = f'{osu_api}/beatmaps/{beatmap_id}'

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self._header) as resp:
                if resp.status != 200:
                    raise OsuApiException(f'获取谱面信息失败 code: {resp.status}')

                return await resp.json()


class SayoApi:
    @staticmethod
    async def search(keyword: str, mode: int, beatmap_status: int):
        url = f'{sayo_api}/?post'
        data = {
            'class': beatmap_status,
            'cmd': 'beatmaplist',
            'keyword': keyword,
            'mode': mode,
            'type': 'search',
        }

        async with aiohttp.ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
            async with session.post(url, data=data) as resp:
                if resp.status != 200:
                    raise OsuApiException(f'搜索谱面失败 code: {resp.status}')

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
                    raise OsuApiException(f'获取谱面信息失败 code: {resp.status}')

                return json.loads(await resp.text())
