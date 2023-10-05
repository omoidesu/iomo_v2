from datetime import datetime

from khl.card import Card, CardMessage, Element, Module, Types

from src.const import Assets
from src.dao.models import OsuUserInfo
from src.util import count_delta, time_format
from ._modules import Modules


def info_card(user_info: dict, compare_user_info: OsuUserInfo = None, **kwargs):
    mode = kwargs.get('mode')
    if not mode:
        mode = user_info.get('playmode')
    color = user_info.get('profile_colour')

    cm = CardMessage()
    card = Card(color=Assets.COLOR.get(mode) if color is None else color)

    supporter = ' :heart:' if user_info.get('is_supporter') else ' :black_heart:'
    header = [user_info.get('username') + supporter + ' ' +
              ''.join(map(lambda x: Assets.FLAG.get(x), user_info.get('country_code'))) if user_info.get(
        'country_code') != 'TW' else ':tw:']

    global_rank = user_info.get('statistics', {'global_rank': 0}).get('global_rank')
    global_rank = 0 if global_rank is None else global_rank
    user_level = user_info.get('statistics', {'level': {'current': 0, 'progress': 0}}).get('level')
    user_level = 0 if user_level is None else user_level
    header.append(f"#{global_rank}" + (
        f"({count_delta(global_rank, compare_user_info.global_rank, rank=True)})" if compare_user_info else ''))
    header.append(f'Lv. {user_level.get("current")} ({user_level.get("progress")}%)')
    card.append(Module.Header('\t'.join(header)))

    context = [
        mode,
        f'{user_info.get("follower_count")} 个关注者'
    ]

    if compare_user_info is not None:
        interval = datetime.now() - compare_user_info.create_time
        context.append(f'对比于{interval.days}天前')
    context.append(f'[主页](https://osu.ppy.sh/users/{user_info.get("id")}/{mode})')

    card.append(Module.Context(
        Element.Image(Assets.Image.MODE.get(mode)),
        Element.Text(' | '.join(context), Types.Text.KMD)
    ))

    card.append(Modules.divider)
    card.append(Modules.banner(kwargs.get('cover', Assets.Image.DEFAULT_COVER)))
    card.append(Modules.divider)

    country_rank = user_info.get("statistics", {"country_rank": 0}).get("country_rank")
    pp = user_info.get('statistics', {'pp': 0}).get('pp')
    acc = round(user_info.get('statistics', {'hit_accuracy': 0}).get('hit_accuracy'), 2)
    play_count = user_info.get('statistics', {'play_count': 0}).get('play_count')
    play_time = user_info.get("statistics", {"play_time": 0}).get("play_time")
    section = [f'国内/区域排名\t\t#{country_rank}',
               f'pp\t\t\t\t{pp} pp' + (f' ({count_delta(pp, compare_user_info.pp)} pp)' if compare_user_info else ''),
               f'准确率\t\t\t{acc} %' + (
                   f' ({count_delta(acc, compare_user_info.accuracy)} %)' if compare_user_info else ''),
               f'游玩次数\t\t\t{play_count}' + (
                   f' ({count_delta(play_count, compare_user_info.play_count)})' if compare_user_info else ''),
               f'游玩时间\t\t\t{time_format(play_time)}'
               ]
    card.append(Module.Section(
        Element.Text('\n'.join(section), Types.Text.PLAIN),
        accessory=Element.Image(user_info.get('avatar_url'), size=Types.Size.SM),
        mode=Types.SectionMode.RIGHT
    ))
    card.append(Modules.divider)

    ssh = user_info.get('statistics', {'grade_counts': {'ssh': 0}}).get('grade_counts').get('ssh')
    ss = user_info.get('statistics', {'grade_counts': {'ss': 0}}).get('grade_counts').get('ss')
    sh = user_info.get('statistics', {'grade_counts': {'sh': 0}}).get('grade_counts').get('sh')
    s = user_info.get('statistics', {'grade_counts': {'s': 0}}).get('grade_counts').get('s')
    a = user_info.get('statistics', {'grade_counts': {'a': 0}}).get('grade_counts').get('a')
    card.append(Module.Context(
        Element.Image(Assets.Image.RANK['XH']),
        Element.Text(str(ssh) + ('\t' if ssh > 10 else '  \t'), Types.Text.PLAIN),
        Element.Image(Assets.Image.RANK['X']), Element.Text(str(ss) + ('\t' if ss > 10 else '  \t'), Types.Text.PLAIN),
        Element.Image(Assets.Image.RANK['SH']), Element.Text(str(sh) + ('\t' if sh > 10 else '  \t'), Types.Text.PLAIN),
        Element.Image(Assets.Image.RANK['S']), Element.Text(str(s) + ('\t' if s > 10 else '  \t'), Types.Text.PLAIN),
        Element.Image(Assets.Image.RANK['A']), Element.Text(str(a), Types.Text.PLAIN)
    ))

    cm.append(card)
    return cm
