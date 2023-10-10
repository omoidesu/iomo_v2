from random import choice

from khl.card import CardMessage, Element, Module

from src.const import Assets
from ._modules import Modules


def waiting_card(head: str):
    header = Module.Header(head)
    banner = Modules.banner(choice(Assets.Image.LOADING))

    return CardMessage(Modules.card(header, Modules.divider, banner, color='#367FA3'))


def good_news_card(src: str, header: str = None):
    modules = []

    if header:
        modules.append(Module.Section(Element.Text(header)))

    modules.append(Modules.divider)
    modules.append(Modules.banner(src))

    return CardMessage(Modules.card(*modules))


def user_not_found_card(src: str):
    return CardMessage(Modules.card(Modules.banner(src)))
