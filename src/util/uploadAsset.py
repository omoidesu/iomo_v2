import io
import math
import os

import aiofiles
import aiohttp
from PIL import Image
from aiohttp import TCPConnector
from khl import Bot, Guild
from meme_generator import get_meme

from src.asset import get_assets, get_user_not_found
from src.card import user_not_found_card as card
from src.const import Assets
from src.dao.models import OsuAsset, OsuStarAsset
from src.exception import NetException
from src.service import IomoApi, SayoApi, asset_service, star_asset_service


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
            else:
                raise NetException(resp.status)


async def generate_diff_png_and_upload(bot: Bot, mode: str, diff: float, emoji: bool = False, guild: Guild = None):
    stars = round(diff, 2)
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'difficulty', f'{mode}{diff}.png')

    if emoji and os.path.exists(path):
        async with aiofiles.open(path, 'rb') as f:
            return await guild.create_emoji(emoji=io.BytesIO(await f.read()), name=f'{mode}{diff}'.replace('.', ''))
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
        async with aiofiles.open(path, 'wb') as f:
            await f.write(bytes_io.getvalue())
        return await guild.create_emoji(emoji=io.BytesIO(bytes_io.getvalue()), name=f'{mode}{diff}'.replace('.', ''))

    kook_url = await bot.client.create_asset(io.BytesIO(bytes_io.getvalue()))

    star_asset_service.insert(OsuStarAsset(mode=mode, star=stars, asset=kook_url))
    return kook_url


async def good_news_generator(bot: Bot, msg: str):
    asset = asset_service.select_asset(msg)
    if asset:
        return asset.oss_url

    meme = get_meme('good_news')
    img = await meme(texts=[msg])

    kook_url = await bot.client.create_asset(img.getvalue())

    new_asset = OsuAsset(source_url=msg, oss_url=kook_url)
    asset_service.insert(new_asset)

    return kook_url


async def user_not_found(bot: Bot, msg: str):
    asset = asset_service.select_asset(msg)
    if asset:
        return asset.oss_url

    meme = get_meme('play_game')
    img = await meme(images=[get_user_not_found()], texts=[msg])

    kook_url = await bot.client.create_asset(img.getvalue())

    new_asset = OsuAsset(source_url=msg, oss_url=kook_url)
    asset_service.insert(new_asset)

    return kook_url


async def user_not_found_card(bot: Bot, msg: str):
    src = await user_not_found(bot, msg)
    return card(src)


async def upload_asset(bot: Bot, url: str, to: dict, key: str, default: str, force: bool = False, origin: bool = False):
    try:
        to[key] = await download_and_upload(bot, url, force, origin)
    except NetException:
        to[key] = default


async def generate_stars(bot: Bot, mode: str, stars: float, to: dict, key: str, emoji: bool = False,
                         guild: Guild = None):
    to[key] = await generate_diff_png_and_upload(bot, mode, stars, emoji, guild)


async def download_audio_and_upload(beatmap_set: int):
    """
    从sayobot下载谱面并将音频上传kook
    :param bot:
    :param beatmap_set: beatmap set id
    :return: kook资源地址
    """
    resource_uri = f'{beatmap_set}_audio'
    asset = asset_service.select_asset(resource_uri)
    if asset is not None:
        return asset.oss_url

    beatmap_info = await SayoApi.get_beatmap_info(str(beatmap_set), id_mode=True)
    bid_data = beatmap_info.get('data', {}).get('bid_data', [])
    if not bid_data:
        return None

    audio_file = bid_data[0].get('audio')
    try:
        resp: dict = await IomoApi.get_music_url(str(beatmap_set), audio_file)
        return resp.get('message') if resp.get('code') == 200 else None
    except:
        return None
