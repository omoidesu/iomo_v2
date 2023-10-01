from .idGenerator import IdGenerator


def time_format(secs: int):
    minute, _ = divmod(secs, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)

    return f'{day}d {hour}h {minute}m'


def count_delta(now, history, rank=False):
    delta = now - history
    if delta > 0:
        if rank:
            return f'↓{delta}'
        return f'↑{delta}'
    elif delta < 0:
        if rank:
            return f'↑{-delta}'
        return f'↓{-delta}'
    else:
        if rank:
            return '-'
        return delta
