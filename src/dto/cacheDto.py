import json

from .beatmaps import BeatmapSet


class RecentListCacheDTO:
    _id_map: dict
    _osu_id: int
    _osu_mode: str
    _include_fail: bool
    _guild_id: str
    _author_id: str
    _msg_id: str

    def __init__(self, **kwargs):
        self._id_map = kwargs.get('id_map')
        self._osu_id = kwargs.get('osu_id')
        self._osu_mode = kwargs.get('osu_mode')
        self._include_fail = kwargs.get('include_fail')
        self._guild_id = kwargs.get('guild_id')
        self._author_id = kwargs.get('author_id')
        self._msg_id = kwargs.get('msg_id')

    def to_json_str(self) -> str:
        json_object = {}
        for key, value in self.__dict__.items():
            json_object[key[1:]] = value

        return json.dumps(json_object)

    @property
    def id_map(self):
        return self._id_map

    @property
    def osu_id(self):
        return self._osu_id

    @property
    def osu_mode(self):
        return self._osu_mode

    @property
    def include_fail(self):
        return self._include_fail

    @property
    def guild_id(self):
        return self._guild_id

    @property
    def author_id(self):
        return self._author_id

    @property
    def msg_id(self):
        return self._msg_id


class SearchListCacheDTO:
    _keyword: str
    _source: str
    _pages: list[list[BeatmapSet]]
    _reactions: dict[str, int]
    _current_page: int
    _guild_id: str

    def __init__(self, keyword: str, source: str, pages: list[list[BeatmapSet]], reactions: dict[str, int],
                 current_page: int, guild_id: str):
        self._keyword = keyword
        self._source = source
        self._pages = pages
        self._reactions = reactions
        self._current_page = current_page
        self._guild_id = guild_id

    @property
    def keyword(self):
        return self._keyword

    @property
    def source(self):
        return self._source

    @property
    def pages(self):
        return self._pages

    @property
    def reactions(self):
        return self._reactions

    @property
    def current_page(self):
        return self._current_page

    @property
    def guild_id(self):
        return self._guild_id
