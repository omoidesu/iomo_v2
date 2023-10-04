from src.const import beatmap_status


class Beatmap:
    id: int
    difficulty_rating: float
    mode: str
    status: str
    version: str
    bpm: float
    ar: float
    cs: float
    accuracy: float  # od
    drain: float  # hp
    status: str

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.difficulty_rating = kwargs.get('difficulty_rating')
        self.mode = kwargs.get('mode')
        self.status = kwargs.get('status')
        self.version = kwargs.get('version')
        self.bpm = kwargs.get('bpm')
        self.ar = kwargs.get('ar')
        self.cs = kwargs.get('cs')
        self.accuracy = kwargs.get('accuracy')
        self.drain = kwargs.get('drain')
        self.status = beatmap_status.get(kwargs.get('status'))

    @property
    def od(self):
        return self.accuracy

    @property
    def hp(self):
        return self.drain


class BeatmapSet:
    id: int
    artist: str
    artist_unicode: str
    creator: str
    favourite_count: int
    play_count: int
    title: str
    title_unicode: str
    status: str
    cover_list: str
    beatmaps: list[Beatmap]

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.artist = kwargs.get('artist')
        self.artist_unicode = kwargs.get('artist_unicode')
        self.creator = kwargs.get('creator')
        self.favourite_count = kwargs.get('favourite_count')
        self.play_count = kwargs.get('play_count')
        self.title = kwargs.get('title')
        self.title_unicode = kwargs.get('title_unicode')
        self.status = beatmap_status.get(kwargs.get('status'))
        self.cover_list = kwargs.get('covers', {}).get('list')
        beatmap = kwargs.get('beatmaps')
        if beatmap is not None:
            self.beatmaps = [Beatmap(**b) for b in beatmap]
            self.beatmaps = sorted(self.beatmaps, key=lambda x: x.difficulty_rating)
