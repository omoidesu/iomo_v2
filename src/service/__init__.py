from .sqlService import AssetService, BeatmapService, BeatmapSetService, BeatmapDiffService, LogService, \
    StarAssertService, UserService, UserInfoService
from .api import OsuApi, SayoApi
from .osuWeb import search, get_mp_event

asset_service = AssetService()
beatmap_service = BeatmapService()
beatmap_set_service = BeatmapSetService()
beatmap_diff_service = BeatmapDiffService()
log_service = LogService()
star_asset_service = StarAssertService()
user_service = UserService()
user_info_service = UserInfoService()
