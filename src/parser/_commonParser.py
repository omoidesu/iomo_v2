from src.const import game_mode_map, search_source_map
from src.exception import ArgsException
from src.util import mods_parser


def args_parser(*args):
    """
        从arg中解析出各参数内容和位置
        参数：
            -f source 搜索源
            -b beatmap_id
            -s beatmap_set_id
            -u username
            :mode 模式
            +mods mod
            #order 指定位置
    """
    source, beatmap_id, beatmap_set_id, username, mode, mods, order = '', '', '', '', '', [], 0
    index = {'source': -1, 'beatmap_id': -1, 'beatmap_set_id': -1, 'username': -1, 'mode': -1, 'mods': -1, 'order': -1}

    for i in range(len(args)):
        if source and beatmap_id and beatmap_set_id and username and mode and mods and order:
            break

        if i in index.values():
            continue

        arg = args[i]
        # 搜索源
        if not source and arg == '-f':
            index['source'] = i + 1
            source = args[index['source']]
            if source not in search_source_map.keys():
                raise ArgsException('source参数错误')
            source = search_source_map.get(source)
            continue
        # map id
        if not beatmap_id and arg == '-b':
            index['beatmap_id'] = i + 1
            beatmap_id = args[index['beatmap_id']]
            if not beatmap_id.isdigit():
                raise ArgsException('beatmap_id参数必须为数字')
            continue
        # set id
        if not beatmap_set_id and arg == '-s':
            index['beatmap_set_id'] = i + 1
            beatmap_set_id = args[index['beatmap_set_id']]
            if not beatmap_set_id.isdigit():
                raise ArgsException('beatmap_set_id参数必须为数字')
            continue
        # 用户名
        if not username and arg == '-u':
            index['username'] = i + 1
            username = args[index['username']]
            continue
        # 模式
        if not mode and arg.startswith(':'):
            index['mode'] = i
            mode = arg[1:]
            if mode not in game_mode_map.keys():
                raise ArgsException('mode参数错误')
            mode = game_mode_map.get(mode)
            continue
        # mod
        if not mods and arg.startswith('+'):
            index['mods'] = i
            mod = arg[1:]
            mods = mods_parser(mod)
            continue
        # order
        if not order and arg.startswith('#'):
            index['order'] = i
            order = arg[1:]
            if not order.isdigit():
                raise ArgsException('order参数必须为数字')
            order = int(order)

    # 如果变量位置都是初始值则所有元素都是关键词
    if sum(index.values()) == -1 * len(index):
        smallest_index = -1
        keyword = ' '.join(args)
    else:
        smallest_index = min(i for i in index.values() if i >= 0)
        # 上面-x参数记录的是后面的值的位置，所以要减一
        if args[smallest_index - 1] in ('-f', '-b', '-s', '-u'):
            smallest_index -= 1
        keyword = ' '.join(args[:smallest_index])

    return {
        'keyword': keyword,

        'source': source,
        'beatmap_id': beatmap_id,
        'beatmap_set_id': beatmap_set_id,
        'username': username,

        'mode': mode,
        'mods': mods,
        'order': order,

        'smallest_index': smallest_index,
    }
