from src.const import Assets


class User:
    _id: int
    _username: str
    _flag: str
    _avatar_url: str

    def __init__(self, **kwargs):
        self._id = kwargs.get('id')
        self._username = kwargs.get('username')
        country_code = kwargs.get('country_code')
        self._flag = ''.join(map(lambda x: Assets.FLAG.get(x), country_code))
        self._avatar_url = kwargs.get('avatar_url')

    @property
    def id(self):
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def flag(self):
        return self._flag

    @property
    def avatar_url(self):
        return self._avatar_url
