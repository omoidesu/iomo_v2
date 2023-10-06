from khl import Message


def exception_listener(name):
    def wrapper(func):
        async def inner(msg: Message, *args, **kwargs):
            print(f'"{name}: {msg.author.username}')
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                print(e)

        return inner

    return wrapper
