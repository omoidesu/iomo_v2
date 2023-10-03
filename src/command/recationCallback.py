from khl import Bot

from src.card import score_card
from src.const import redis_recent_beatmap
from src.dao.models import OsuBeatmapSet
from src.dto import RecentListCacheDTO
from src.service import OsuApi, SayoApi, beatmap_set_service
from src.util.uploadAsset import download_and_upload, generate_diff_png_and_upload


async def reaction_callback(bot: Bot, redis_connector, channel_id: int, score_id: str, dto: RecentListCacheDTO):
    api = OsuApi()

    recent_score = await api.get_recent_score(dto.osu_id, dto.osu_mode, 50, include_fail=dto.include_fail,
                                              use_mode=True)
    if len(recent_score) == 0:
        return '找不到这个记录'

    target_score = [score for score in recent_score if score.get('id') == score_id]
    if not target_score:
        return '找不到这个记录'

    score = target_score[0]

    beatmap_set = score.get('beatmapset', {})
    kwargs = {}
    # 封面
    cover: str = beatmap_set.get('covers', {}).get('list')
    if cover is not None:
        kwargs['cover'] = await download_and_upload(bot, cover)
    # 试听
    preview = 'https:' + beatmap_set.get('preview_url')
    if preview is not None:
        kwargs['preview'] = await download_and_upload(bot, preview)

    difficult = score.get('beatmap', {}).get('difficulty_rating')
    kwargs['star'] = await generate_diff_png_and_upload(bot, dto.osu_mode, difficult)

    # 保存beatmapset
    if beatmap_set:
        beatmap_set_service.insert(OsuBeatmapSet(
            beatmapset_id=beatmap_set.get('id'), title=beatmap_set.get('title'), artist=beatmap_set.get('artist'),
            title_unicode=beatmap_set.get('title_unicode'), artist_unicode=beatmap_set.get('artist_unicode'),
            creator=beatmap_set.get('creator')
        ))

    # 调用sayo api取得max combo
    sayo_info = await SayoApi.get_beatmap_info(beatmap_set.get('id'))
    if sayo_info.get('status') == 0:
        beatmap_id = score.get('beatmap', {}).get('id')
        bid_info = [item for item in sayo_info.get('data').get('bid_data') if item.get('bid') == beatmap_id]
        if bid_info:
            kwargs['fc_combo'] = bid_info[0].get('maxcombo')

    # todo: 计算模拟pp
    kwargs['fc'] = '-'
    kwargs['95'] = '-'
    kwargs['97'] = '-'
    kwargs['98'] = '-'
    kwargs['99'] = '-'
    kwargs['ss'] = '-'

    redis_key = redis_recent_beatmap.format(guild_id=dto.guild_id, channel_id=channel_id)
    redis_connector.set(redis_key, score.get('beatmap', {}).get('id'))

    return score_card(score, **kwargs)
