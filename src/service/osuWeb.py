import aiohttp

from src.exception import NetException


async def search(keyword: str):
    url = 'https://osu.ppy.sh/beatmapsets/search'
    params = {
        'q': keyword
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status != 200:
                raise NetException(f'搜索失败 code: {resp.status}')

            return await resp.text()


async def get_mp_event(room: int, after: int):
    url = f'https://osu.ppy.sh/community/matches/{room}'
    params = {
        'after': after,
        'limit': 100
    }
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as resp:
            if resp.status != 200:
                raise NetException(f'获取mp失败 code: {resp.status}')

            return await resp.json()
