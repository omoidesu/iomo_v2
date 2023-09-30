class ArgsException(Exception):
    def __init__(self, message):
        super().__init__(message)


class NetException(Exception):
    def __init__(self, message):
        super().__init__(message)


class OsuApiException(NetException):
    ...
