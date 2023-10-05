import io
import math

import aiohttp
from PIL import Image
from aiohttp import TCPConnector
from khl import Bot, Guild

from src.asset import get_assets
from src.const import Assets
from src.dao.models import OsuAsset, OsuStarAsset
from src.service import asset_service, star_asset_service


async def download_and_upload(bot: Bot, resource: str, force: bool = False, origin: bool = False):
    if origin:
        return resource

    if not force:
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


async def generate_diff_png_and_upload(bot: Bot, mode: str, diff: float, emoji: bool = False, guild: Guild = None):
    stars = round(diff, 2)

    if not emoji:
        asset = star_asset_service.selectStarAssert(mode=mode, star=stars)
        if asset is not None:
            return asset.asset

    default = 115
    if 0 <= stars < 1:
        xp = 0
        default = 120
    elif 1 <= stars < 2:
        xp = 120
        default = 120
    elif 2 <= stars < 3:
        xp = 240
    elif 3 <= stars < 4:
        xp = 355
    elif 4 <= stars < 5:
        xp = 470
    elif 5 <= stars < 6:
        xp = 585
    elif 6 <= stars < 7:
        xp = 700
    elif 7 <= stars < 8:
        xp = 815
    else:
        return Assets.Sticker.DIFF.get(mode) if emoji else Assets.Image.DIFF.get(mode)

    assets = get_assets()
    x = (stars - math.floor(stars)) * default + xp
    color = Image.open(assets.get('color')).load()
    r, g, b = color[x, 1]
    # 打开底图
    im = Image.open(assets.get(mode)).convert('RGBA')
    xx, yy = im.size
    # 填充背景
    sm = Image.new('RGBA', im.size, (r, g, b))
    sm.paste(im, (0, 0, xx, yy), im)
    # 把白色变透明
    for i in range(xx):
        for z in range(yy):
            data = sm.getpixel((i, z))
            if (data.count(255) == 4):
                sm.putpixel((i, z), (255, 255, 255, 0))

    bytes_io = io.BytesIO()
    sm.save(bytes_io, format='png')
    if emoji:
        return await guild.create_emoji(emoji=io.BytesIO(bytes_io.getvalue()), name=f'{mode}{diff}'.replace('.', ''))

    kook_url = await bot.client.create_asset(io.BytesIO(bytes_io.getvalue()))

    star_asset_service.insert(OsuStarAsset(mode=mode, star=stars, asset=kook_url))
    return kook_url
