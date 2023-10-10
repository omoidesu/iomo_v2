from .api import OsuApi, SayoApi
from .minioClient import MinioClient
from .sqlService import AssetService, BeatmapDiffService, BeatmapService, BeatmapSetService, LogService, \
    StarAssertService, UserInfoService, UserService

asset_service = AssetService()
beatmap_service = BeatmapService()
beatmap_set_service = BeatmapSetService()
beatmap_diff_service = BeatmapDiffService()
log_service = LogService()
star_asset_service = StarAssertService()
user_service = UserService()
user_info_service = UserInfoService()
