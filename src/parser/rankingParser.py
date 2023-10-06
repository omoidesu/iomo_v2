from khl import Message

from src.command import ranking_command
from src.util.log import save_log
from ._commonParser import args_parser


async def ranking_parser(msg: Message, *args):
    save_log(msg, *args)

    require_args = args_parser(*args)
    country = require_args['keyword']
    mode = require_args['mode']

    if country and len(country) != 2:
        return '国家代码必须为两位'

    if not mode:
        mode = 'osu'

    return await ranking_command(country, mode)
