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

    def __init__(self, code):
        self._code = code
        super().__init__(code)

    @property
    def code(self):
        return self._code

    def do_except(self, message: str):
        if self._code == 401:
            return 'token过期'
        elif self._code == 404:
            return message
        else:
            return f'未知错误，code:{self._code}'
