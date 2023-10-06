def test():
    def wrapper(func):
        async def inner(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                ...

        return inner

    return wrapper
