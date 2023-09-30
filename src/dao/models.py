# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Float, Integer, String
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class OsuAsset(Base):
    __tablename__ = 'osu_asset'
    __table_args__ = {'comment': '资源表'}

    id = Column(BigInteger, primary_key=True, comment='id')
    source_url = Column(String(500), comment='资源地址')
    oss_url = Column(String(500), comment='oss地址')
    create_time = Column(DateTime, comment='创建时间')


class OsuBeatmap(Base):
    __tablename__ = 'osu_beatmap'
    __table_args__ = {'comment': '谱面表'}

    beatmap_id = Column(BigInteger, primary_key=True, comment='谱面id')
    beatmapset_id = Column(BigInteger, comment='谱面集id')
    mode = Column(TINYINT, comment='模式')
    duration = Column(Integer, comment='时长')
    bpm = Column(Float, comment='bpm')
    diff_name = Column(String(255), comment='难度名')
    note_count = Column(Integer, comment='note数量')
    circle_count = Column(Integer, comment='圆圈数量')
    slider_count = Column(Integer, comment='滑条数量')
    spinner_count = Column(Integer, comment='转盘数量')
    create_time = Column(DateTime, comment='创建时间')


class OsuBeatmapDiff(Base):
    __tablename__ = 'osu_beatmap_diff'
    __table_args__ = {'comment': '谱面难度表'}

    id = Column(BigInteger, primary_key=True, comment='id')
    beatmap_id = Column(BigInteger, comment='谱面id')
    ar = Column(Float, comment='ar')
    cs = Column(Float, comment='cs')
    hp = Column(Float, comment='hp')
    od = Column(Float, comment='od')
    star = Column(Float, comment='难度')
    mod = Column(Integer, comment='mod')
    acc95 = Column(Float, comment='acc95')
    acc97 = Column(Float, comment='acc97')
    acc98 = Column(Float, comment='acc98')
    acc99 = Column(Float, comment='acc99')
    acc100 = Column(Float, comment='acc100')
    create_time = Column(DateTime, comment='创建时间')


class OsuBeatmapSet(Base):
    __tablename__ = 'osu_beatmap_set'
    __table_args__ = {'comment': '谱面集表'}

    beatmapset_id = Column(BigInteger, primary_key=True, comment='谱面集id')
    music = Column(String(255), comment='谱面名')
    music_unicode = Column(String(255), comment='谱面名(unicode)')
    artist = Column(String(255), comment='艺术家')
    artist_unicode = Column(String(255), comment='艺术家(unicode)')
    mapper = Column(String(255), comment='谱面作者')
    create_time = Column(DateTime, comment='创建时间')


class OsuLog(Base):
    __tablename__ = 'osu_log'
    __table_args__ = {'comment': '日志表'}

    id = Column(BigInteger, primary_key=True, comment='id')
    kook_id = Column(BigInteger, comment='kookid')
    kook_name = Column(String(255), comment='kook名')
    kook_num = Column(Integer, comment='kook数字')
    command = Column(String(255), comment='命令')
    args = Column(String(255), comment='参数')
    create_time = Column(DateTime, comment='创建时间')


class OsuStarAsset(Base):
    __tablename__ = 'osu_star_asset'
    __table_args__ = {'comment': '难度资源表'}

    id = Column(BigInteger, primary_key=True, comment='id')
    mode = Column(TINYINT, comment='模式')
    star = Column(Float, comment='难度')
    asset = Column(String(255), comment='资源')
    create_time = Column(DateTime, comment='创建时间')


class OsuUser(Base):
    __tablename__ = 'osu_user'
    __table_args__ = {'comment': '用户表'}

    id = Column(BigInteger, primary_key=True, comment='id')
    kook_id = Column(BigInteger, comment='kookid')
    osu_id = Column(BigInteger, comment='osuid')
    default_mode = Column(TINYINT, comment='默认模式')
    create_time = Column(DateTime, comment='创建时间')


class OsuUserInfo(Base):
    __tablename__ = 'osu_user_info'
    __table_args__ = {'comment': '用户信息表'}

    id = Column(BigInteger, primary_key=True, comment='id')
    user_id = Column(BigInteger, comment='用户id')
    mode = Column(TINYINT, comment='模式')
    global_rank = Column(Integer, comment='全球排名')
    county_rank = Column(Integer, comment='国家排名')
    game_level = Column(Integer, comment='游戏等级')
    level_progress = Column(Integer, comment='等级进度')
    pp = Column(Float, comment='pp')
    accuracy = Column(Float, comment='准确率')
    play_count = Column(Integer, comment='游玩次数')
    play_time = Column(Integer, comment='游玩时间')
    ssh_count = Column(Integer, comment='ssh次数')
    ss_count = Column(Integer, comment='ss次数')
    sh_count = Column(Integer, comment='sh次数')
    s_count = Column(Integer, comment='s次数')
    a_count = Column(Integer, comment='a次数')
    create_time = Column(DateTime, comment='创建时间')
