import asyncio

from khl import Bot, Message

from src.card import recent_card, score_card
from src.const import Assets, redis_recent_beatmap
from src.dao import Redis
from src.dao.models import OsuBeatmapSet
from src.dto import RecentListCacheDTO
from src.exception import OsuApiException
from src.service import OsuApi, beatmap_set_service, simulate_pp_with_accuracy, simulate_pp_if_fc
from src.util.uploadAsset import generate_stars, upload_asset, user_not_found_card

redis = Redis.instance().get_connection()


async def recent_command(bot: Bot, msg: Message, osu_name: str, mode: str, mod: list, order: int, include_fail: bool,
                         ls_mode: bool):
    api = OsuApi()

    if not str(osu_name).isdigit():
        try:
            osu_info = await api.get_user(osu_name)
        except OsuApiException as e:
            return await user_not_found_card(bot, e.do_except(f'找不到名为{osu_name}的玩家')), None
        else:
            osu_name = osu_info.get('id')
            if mode == '':
                mode = osu_info.get('playmode')

    try:
        recent_score = await api.get_recent_score(osu_name, mode=mode, include_fail=include_fail, use_mode=True,
                                                  limit=20)
    except OsuApiException as e:
        return await user_not_found_card(bot, e.do_except(f'用户id:{osu_name}不存在')), None
    else:
        if len(recent_score) == 0:
            return '该用户没有最近游玩记录', None

        # 如果输入是NM则只查找没有mod的记录
        if len(mod) == 1 and mod[0] == 'NM':
            recent_score = filter(lambda x: x.get('mods') == [], recent_score)
        # 如果输入的mod不是NM则查找mod包含于输入mod的记录
        elif len(mod) > 0:
            recent_score = filter(lambda x: set(mod).issubset(x.get('mods', [])), recent_score)

        kwargs = {'mode': mode}
        tasks = []

        if ls_mode:
            kwargs['osu_name'] = recent_score[0].get('user', {}).get('username')

            recent_score = recent_score[:5]
            stars = {}
            for score in recent_score:
                difficult = score.get('beatmap', {}).get('difficulty_rating')
                tasks.append(asyncio.create_task(generate_stars(bot, mode, difficult, stars, difficult)))

                # 保存beatmapset
                beatmap_set = score.get('beatmapset', {})
                if beatmap_set:
                    beatmap_set_service.insert(OsuBeatmapSet(
                        beatmapset_id=beatmap_set.get('id'), title=beatmap_set.get('title'),
                        artist=beatmap_set.get('artist'),
                        title_unicode=beatmap_set.get('title_unicode'),
                        artist_unicode=beatmap_set.get('artist_unicode'),
                        creator=beatmap_set.get('creator')
                    ))

                cover = beatmap_set.get('covers', {}).get('list')
                if cover:
                    tasks.append(asyncio.create_task(
                        upload_asset(bot, cover, kwargs, f"{beatmap_set.get('id')}", Assets.Image.DEFAULT_COVER)))
                else:
                    kwargs[f"{beatmap_set.get('id')}"] = Assets.Image.OSU_LOGO

            await asyncio.wait(tasks)
            kwargs['stars'] = stars

            card_msg, id_map = recent_card(recent_score, **kwargs)
            dto = RecentListCacheDTO(
                id_map=id_map, osu_id=osu_name, osu_mode=mode, include_fail=include_fail, guild_id=msg.ctx.guild.id,
                author_id=msg.author_id, msg_id=msg.id
            )

            return card_msg, dto

        # 如果输入的order大于记录数则查找最后一个记录
        if order:
            if order > len(recent_score):
                score = recent_score[-1]
            else:
                score = recent_score[order - 1]
        else:
            score = recent_score[0]

        beatmap_set = score.get('beatmapset', {})
        beatmap = score.get('beatmap', {})
        kwargs = {}
        # 封面
        cover: str = beatmap_set.get('covers', {}).get('list')
        if cover is not None:
            tasks.append(asyncio.create_task(upload_asset(bot, cover, kwargs, 'cover', Assets.Image.DEFAULT_COVER)))
        # 试听
        if beatmap_set.get('preview_url') is not None:
            tasks.append(
                asyncio.create_task(upload_asset(bot, 'https:' + beatmap_set.get('preview_url'), kwargs, 'preview',
                                                 Assets.Audio.WELCOME)))

        difficult = beatmap.get('difficulty_rating')
        tasks.append(asyncio.create_task(generate_stars(bot, mode, difficult, kwargs, 'star')))

        # 保存beatmapset
        if beatmap_set:
            beatmap_set_service.insert(OsuBeatmapSet(
                beatmapset_id=beatmap_set.get('id'), title=beatmap_set.get('title'), artist=beatmap_set.get('artist'),
                title_unicode=beatmap_set.get('title_unicode'), artist_unicode=beatmap_set.get('artist_unicode'),
                creator=beatmap_set.get('creator')
            ))

        # 获取max combo
        tasks.append(asyncio.create_task(get_max_combo(api, beatmap.get('id'), kwargs, 'fc_combo')))

        if mode != 'mania':
            beatmap_id = beatmap.get('id')
            mods = score.get('mods')
            statistics = score.get('statistics')
            try:
                await simulate_pp_with_accuracy(beatmap_id, 100, mode, [])
            except:
                pass
            tasks.append(asyncio.create_task(simulate_if_fc(beatmap_id, mode, mods, statistics, kwargs)))
            tasks.append(asyncio.create_task(simulate_pp(beatmap_id, 95, mode, mods, kwargs, '95')))
            tasks.append(asyncio.create_task(simulate_pp(beatmap_id, 97, mode, mods, kwargs, '97')))
            tasks.append(asyncio.create_task(simulate_pp(beatmap_id, 98, mode, mods, kwargs, '98')))
            tasks.append(asyncio.create_task(simulate_pp(beatmap_id, 99, mode, mods, kwargs, '99')))
            tasks.append(asyncio.create_task(simulate_pp(beatmap_id, 100, mode, mods, kwargs, 'ss')))

            if 'HR' in mods:
                kwargs['cs'] = round(beatmap.get('cs') * 1.3, 2)
                kwargs['hp'] = round(beatmap.get('drain') * 1.4, 2)
            elif 'EZ' in mods:
                kwargs['cs'] = round(beatmap.get('cs') * 0.5, 2)
                kwargs['hp'] = round(beatmap.get('drain') * 0.5, 2)

        redis_key = redis_recent_beatmap.format(guild_id=msg.ctx.guild.id, channel_id=msg.ctx.channel.id)
        redis.set(redis_key, beatmap.get('id'))

        await asyncio.wait(tasks)
        return score_card(score, beatmap, beatmap_set, **kwargs), None


async def get_max_combo(api: OsuApi, beatmap_id: int, to: dict, key: str):
    beatmap_info = await api.get_beatmap_info(beatmap_id)
    to[key] = beatmap_info.get('max_combo')


async def simulate_pp(beatmap_id: int, accuracy: float, mode: str, mods: list, to: dict, key: str):
    to[key] = await simulate_pp_with_accuracy(beatmap_id, accuracy, mode, mods)


async def simulate_if_fc(beatmap_id: int, mode: str, mods: list, statistics: dict, to: dict):
    to['fc'], to['star_rating'], to['ar'], to['od'], to['if_acc'] = await simulate_pp_if_fc(beatmap_id, mode, mods,
                                                                                            statistics)
