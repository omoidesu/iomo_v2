from typing import Type

from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session

from src.config import mysql_url
from src.dao import SqlSession
from src.dao.models import Base, OsuAsset, OsuBeatmap, OsuBeatmapDiff, OsuBeatmapSet, OsuStarAsset, OsuUser, OsuUserInfo
from src.exception import ArgsException
from src.util import IdGenerator


class __SqlService:
    _session: Session
    _id_generator: IdGenerator

    def __init__(self, worker_id: int):
        self._session = SqlSession(mysql_url).session()
        self._id_generator = IdGenerator(1, worker_id)

    def new_id(self):
        return self._id_generator.get_id()

    def insert(self, obj: Base):
        if not isinstance(obj, OsuBeatmap) or not isinstance(obj, OsuBeatmapSet):
            obj.id = self.new_id()
        self._session.add(obj)
        try:
            self._session.commit()
        except IntegrityError:
            self._session.rollback()

    def insert_batch(self, objs: list[Base]):
        for obj in objs:
            if not isinstance(obj, OsuBeatmap) or not isinstance(obj, OsuBeatmapSet):
                obj.id = self.new_id()
        self._session.add_all(objs)
        self._session.commit()

    @staticmethod
    def check_args(*args):
        if len(args) == 0:
            raise ArgsException('参数全部为空')


class AssetService(__SqlService):
    def __init__(self):
        super().__init__(1)

    def select_asset(self, source_url: str):
        return self._session.query(OsuAsset).filter(OsuAsset.source_url == source_url).order_by(
            OsuAsset.create_time).first()

    def select_asset_batch(self, **kwargs) -> dict:
        """
            批量查询，kwargs中key为标志，value为source_url
            :param kwargs:
            :return: dict key为标志 value为oss_url
        """
        result = {}
        assets = self._session.query(OsuAsset).filter(OsuAsset.source_url.in_(kwargs.values())).all()
        assets_map = {asset.source_url: asset.oss_url for asset in assets}
        for key in kwargs.keys():
            if assets_map.get(kwargs[key]):
                result[key] = assets_map.get(kwargs[key])
            else:
                result[key] = None

        return result


class BeatmapService(__SqlService):
    def __init__(self):
        super().__init__(2)

    def select_beatmap(self, beatmap_id: int):
        return self._session.query(OsuBeatmap).filter(OsuBeatmap.beatmap_id == beatmap_id).first()


class BeatmapSetService(__SqlService):
    def __init__(self):
        super().__init__(3)

    def select_beatmap_set(self, beatmapset_id: int):
        return self._session.query(OsuBeatmapSet).filter(OsuBeatmapSet.beatmapset_id == beatmapset_id).first()


class BeatmapDiffService(__SqlService):
    def __init__(self):
        super().__init__(4)

    def select_beatmap_diff(self, min_pp: float, max_pp: float):
        return self._session.query(OsuBeatmapDiff).filter(or_(
            OsuBeatmapDiff.acc95.between(min_pp, max_pp),
            OsuBeatmapDiff.acc97.between(min_pp, max_pp),
            OsuBeatmapDiff.acc98.between(min_pp, max_pp),
            OsuBeatmapDiff.acc99.between(min_pp, max_pp),
            OsuBeatmapDiff.acc100.between(min_pp, max_pp)
        )).all()


class LogService(__SqlService):
    def __init__(self):
        super().__init__(5)


class StarAssertService(__SqlService):
    def __init__(self):
        super().__init__(6)

    def selectStarAssert(self, mode: str = None, star: float = None):
        if mode is None or star is None:
            raise ArgsException('mode和star不能为空')

        return self._session.query(OsuStarAsset).filter(
            OsuStarAsset.mode == mode,
            OsuStarAsset.star == star
        ).first()


class UserService(__SqlService):
    def __init__(self):
        super().__init__(7)

    def select_user(self, kook_id: int = None, osu_id: int = None, osu_name: str = None) -> Type[OsuUser] | None:
        self.check_args(osu_id, kook_id)

        filters = []
        if osu_id is not None:
            filters.append(OsuUser.osu_id == osu_id)
        if kook_id is not None:
            filters.append(OsuUser.kook_id == kook_id)
        if osu_name is not None:
            filters.append(OsuUser.osu_name == osu_name)

        return self._session.query(OsuUser).filter(*filters).first()

    def delete_user(self, kook_id: int = None, osu_id: int = None):
        self.check_args(osu_id, kook_id)

        filters = []
        if osu_id is not None:
            filters.append(OsuUser.osu_id == osu_id)
        if kook_id is not None:
            filters.append(OsuUser.kook_id == kook_id)

        self._session.query(OsuUser).filter(*filters).delete()
        self._session.commit()

    def update_user(self, kook_id: int = None, **kwargs):
        self.check_args(kook_id)

        self._session.query(OsuUser).filter(OsuUser.kook_id == kook_id).update(kwargs)
        self._session.commit()


class UserInfoService(__SqlService):
    def __init__(self):
        super().__init__(8)

    def select_user_info(self, user_id: int = None, mode: str = 'osu', day: int = 1):
        if user_id is None:
            raise ArgsException('user_id不能为空')

        user_info = self._session.query(OsuUserInfo).filter(OsuUserInfo.user_id == user_id,
                                                            OsuUserInfo.mode == mode).order_by(
            OsuUserInfo.create_time.desc()).offset(day).first()
        if user_info is None:
            return self._session.query(OsuUserInfo).filter(OsuUserInfo.user_id == user_id,
                                                           OsuUserInfo.mode == mode).order_by(
                OsuUserInfo.create_time).first()

        return user_info
