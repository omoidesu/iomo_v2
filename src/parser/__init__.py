from khl import Message

from src.util.log import save_log
from .bpParser import bp_parser, bp_today_parser
from .buttonQueue import ButtonQueue
from .compareParser import compare_parser
from .infoParser import info_parser
from .rankingParser import ranking_parser
from .reactionQueue import ReactionQueue
from .recentParser import recent_parser
from .scoreParser import score_parser
from .searchParser import search_parser
from .urlParser import osu_homepage_parser
from .userParser import bind_parser, mode_parser, unbind_parser

reaction_queue = ReactionQueue.instance()
button_queue = ButtonQueue.instance()


def ping_parser(msg: Message, *args):
    save_log(msg, *args)
    return '(> <)'
