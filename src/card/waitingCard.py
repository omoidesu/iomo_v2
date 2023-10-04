from random import choice

from khl.card import CardMessage, Module

from src.const import Assets
from ._modules import Modules


def search_waiting_card():
    header = Module.Header('正在搜索中，请稍候')
    banner = Modules.banner(choice(Assets.Image.LOADING))

    return CardMessage(Modules.card(header, Modules.divider, banner, color='#367FA3'))
