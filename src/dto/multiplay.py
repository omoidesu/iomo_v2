class MultiPlay:
    _match_id: int
    _match_name: str
    _event_id: int
    _channel_id: int
    _job_id: str

    def __init__(self, match_id, match_name, event_id, channel_id, job_id):
        self._match_id = match_id
        self._match_name = match_name
        self._event_id = event_id
        self._channel_id = channel_id
        self._job_id = job_id

    @property
    def match_id(self):
        return self._match_id

    @property
    def match_name(self):
        return self._match_name

    @property
    def event_id(self):
        return self._event_id

    @event_id.setter
    def event_id(self, event_id):
        self._event_id = event_id

    @property
    def channel_id(self):
        return self._channel_id

    @property
    def job_id(self):
        return self._job_id
