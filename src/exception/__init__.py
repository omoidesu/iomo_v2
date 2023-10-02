class ArgsException(Exception):
    _message: str

    def __init__(self, message):
        super().__init__(message)
        self._message = str(message)

    @property
    def message(self):
        return self._message


class NetException(Exception):
    def __init__(self, message):
        super().__init__(message)


class OsuApiException(NetException):
    _code: int
    _message: str

    def __init__(self, code):
        self._code = code

        if code == 401:
            super().__init__('token过期')
            self._message = 'token过期'
        else:
            super().__init__(code)

    @property
    def code(self):
        return self._code

    @property
    def message(self):
        return self._message
