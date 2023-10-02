from .idGenerator import IdGenerator
from src.exception import ArgsException
from src.const import mods


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


def mods_parser(mod: str) -> list[str]:
    if len(mod) == 0:
        return []

    if len(mod) & 1 == 1:
        raise ArgsException('mod参数错误')

    mod = mod.upper()
    arg_mods = [mod[i:i + 2] for i in range(0, len(mod), 2)]

    if len(mods) == 1 and mods[0] == 'NM':
        return ['NM']

    ez_conflict = {'EZ': False, 'HR': False}
    nf_conflict = {'NF': False, 'SD': False, 'RX': False, 'AP': False}
    ht_conflict = {'HT': False, 'DT': False}
    sd_conflict = {'SD': False, 'PF': False}
    dt_conflict = {'DT': False, 'NC': False}
    hd_conflict = {'HD': False, 'FI': False}

    for arg_mod in arg_mods:
        if arg_mod not in mods.keys():
            raise ArgsException('mod参数错误')

        if arg_mod in ez_conflict.keys():
            if any(value for value in ez_conflict.values() if value is True):
                raise ArgsException('同时存在EZ和HR')

            ez_conflict[arg_mod] = True
        elif arg_mod in nf_conflict.keys():
            if any(value for value in nf_conflict.values() if value is True):
                raise ArgsException('同时存在NF、SD、RX或AP')

            nf_conflict[arg_mod] = True
        elif arg_mod in ht_conflict.keys():
            if any(value for value in ht_conflict.values() if value is True):
                raise ArgsException('同时存在HT和DT')

            ht_conflict[arg_mod] = True

        if arg_mod in sd_conflict.keys():
            if any(value for value in sd_conflict.values() if value is True):
                raise ArgsException('同时存在SD和PF')

            sd_conflict[arg_mod] = True
        elif arg_mod in dt_conflict.keys():
            if any(value for value in dt_conflict.values() if value is True):
                raise ArgsException('同时存在DT和NC')

            dt_conflict[arg_mod] = True
        elif arg_mod in hd_conflict.keys():
            if any(value for value in hd_conflict.values() if value is True):
                raise ArgsException('同时存在HD和FI')

            hd_conflict[arg_mod] = True

    return arg_mods
