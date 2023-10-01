import io

from src.service import asset_service, star_asset_service
from src.dao.models import OsuAsset, OsuStarAsset
from khl import Bot
import aiohttp
from aiohttp import TCPConnector


async def download_and_upload(bot: Bot, resource: str):
    asset = asset_service.select_asset(resource)
    if asset is not None:
        return asset.oss_url

    async with aiohttp.ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
        async with session.get(resource) as resp:
            if resp.status == 200:
                _bytes = await resp.content.read()
                kook_url = await bot.client.create_asset(io.BytesIO(_bytes))

                new_asset = OsuAsset(source_url=resource, oss_url=kook_url)
                asset_service.insert(new_asset)

                return kook_url
