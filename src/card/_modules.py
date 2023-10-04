from khl.card import Card, Element, Module, Struct, Types
from khl.card.interface import _Module

from src.const import Assets
from src.util import convert_date, seconds_to_str


class Modules:
    divider = Module.Divider()

    @staticmethod
    def card(*modules, card: Card = None, color: str = '') -> Card:
        if card is None:
            card = Card()

        if color:
            card.color = color

        for module in modules:
            card.append(module)
        return card

    @staticmethod
    def download_module(beatmapset_id: int) -> _Module:
        ppy = f'[osu!](https://osu.ppy.sh/beatmapsets/{beatmapset_id}/download)'
        sayo = f'[sayobot](https://dl.sayobot.cn/beatmaps/download/novideo/{beatmapset_id})'
        chimu = f'[chimu](https://api.chimu.moe/v1/download/{beatmapset_id}?n=1)'
        btct = f'[btct](https://beatconnect.io/b/{beatmapset_id})'
        nerina = f'[nerina](https://nerina.pw/d/{beatmapset_id})'

        text = f'下载地址：{ppy} | {sayo} | {chimu} | {btct} | {nerina}'

        return Module.Context(text)

    @staticmethod
    def beatmap_info(beatmapset: dict, beatmap: dict, mode: str, cover: str) -> _Module:
        count_circles = beatmap.get('count_circles')
        count_sliders = beatmap.get('count_sliders')
        count_spinners = beatmap.get('count_spinners')
        total_notes = count_circles + count_sliders + count_spinners

        cs = beatmap.get('cs')
        ar = beatmap.get('ar')
        od = beatmap.get('accuracy')
        hp = beatmap.get('drain')
        stars = beatmap.get('difficulty_rating')

        rows = [
            f'▸作者: {beatmapset.get("creator")} ▸谱面id: {beatmap.get("id")}',
            f'▸长度: {seconds_to_str(beatmap.get("total_length"))} ▸BPM: {beatmap.get("bpm")} ▸物件数: {total_notes}',
            f'▸圈数: {count_circles} ▸滑条数: {count_sliders} ▸转盘数: {count_spinners}'
        ]

        if mode == 'taiko':
            rows.append(f'▸OD:{od} ▸HP:{hp} ▸Stars:{stars}★')
        elif mode == 'mania':
            rows.append(f'▸Keys:{cs} ▸OD:{od} ▸HP:{hp} ▸Stars:{stars}★')
        else:
            rows.append(f'▸CS:{cs} ▸AR:{ar} ▸OD:{od} ▸HP:{hp} ▸Stars:{stars}★')

        cover = Assets.Image.OSU_LOGO if not cover else cover
        return Module.Section('\n'.join(rows), accessory=Element.Image(cover, size=Types.Size.SM),
                              mode=Types.SectionMode.RIGHT)

    @staticmethod
    def score_header(score_info: dict, beatmap: dict, beatmapset: dict, difficult_image: str, position: int = 0) -> \
            list[_Module]:
        modules = []

        user = score_info.get('user')

        source = beatmapset.get('source')
        artist_unicode = beatmapset.get('artist_unicode').replace('*', '\\*')
        title_unicode = beatmapset.get('title_unicode').replace('*', '\\*')
        artist = beatmapset.get('artist').replace('*', '\\*')
        title = beatmapset.get('title').replace('*', '\\*')
        version = beatmap.get('version')

        mods = score_info.get('mods', [])
        create_at = convert_date(score_info.get('created_at'))

        # header
        artist_str = f'{source}({artist_unicode})' if source else artist_unicode
        modules.append(Module.Header(f'{artist_str} - {title_unicode} [{version}]'))

        # context1
        context1 = Module.Context(Element.Text(f'{artist} - {title} | '))
        context1.append(Element.Image(user.get('avatar_url')))
        context1.append(Element.Text(f' [{user.get("username")}](https://osu.ppy.sh/users/{user.get("id")})',
                                     type=Types.Text.KMD))
        modules.append(context1)

        # context2
        context2 = Module.Context(Element.Image(difficult_image))
        context2.append(Element.Text(' | '))
        context2.append(Element.Image(Assets.Image.STATUS.get(beatmap.get("status"))))
        context2.append(Element.Text(' | '))
        context2.append(Element.Image(Assets.Image.RANK.get(score_info.get('rank'))))
        context2.append(Element.Text(' | mods: '))
        if not mods:
            context2.append(Element.Image(Assets.Image.MOD.get('NM')))
        else:
            for mod in mods:
                context2.append(Element.Image(Assets.Image.MOD.get(mod)))
        context2.append(Element.Text(f' | {create_at}' + (f' | #{position}' if position else '')))
        modules.append(context2)

        return modules

    @staticmethod
    def play_statistics(score_info: dict, fc_combo: int) -> _Module:
        mode = score_info.get('mode')
        statistics = score_info.get('statistics')
        accuracy = round(score_info.get('accuracy') * 100, 2)

        pp = score_info.get("pp") if score_info.get("pp") is not None else 0

        paragraphs = [
            Element.Text(f'Rank **{score_info.get("rank")}**', type=Types.Text.KMD),
            Element.Text(f'**{accuracy}** %', type=Types.Text.KMD),
            Element.Text(f'{round(pp)} **pp**', type=Types.Text.KMD),
            Element.Text(f'**Score** {format(score_info.get("score"), ",")}', type=Types.Text.KMD),
            Element.Text(f'{score_info.get("max_combo")} x {f"/ **{fc_combo} x**" if fc_combo else ""}',
                         type=Types.Text.KMD),
            Element.Text(f'{("+" + "".join(score_info.get("mods", []))) if score_info.get("mods", []) else ""}',
                         type=Types.Text.KMD)
        ]

        stickers = Assets.Sticker.STATISTICS.get(mode)
        for key in stickers.keys():
            paragraphs.append(
                Element.Text(f'{stickers.get(key)}: {statistics.get(key)}', type=Types.Text.KMD)
            )
        return Module.Section(Struct.Paragraph(3, *paragraphs))

    @staticmethod
    def music_module(src: str, title: str, cover: str) -> _Module:
        return Module.File(Types.File.AUDIO, src, title, cover)

    @staticmethod
    def banner(src: str) -> _Module:
        return Module.Container(Element.Image(src))

    @staticmethod
    def pp_module(mania: bool = False, **kwargs) -> _Module:
        keys = ('95', '97', '98', '99', 'ss')
        elements = []

        if_fc = kwargs.get('fc')
        fc_str = 'max pp' if mania else 'if fc'
        if if_fc is not None:
            elements.append(Element.Text(f'**{fc_str}** : {if_fc} pp', type=Types.Text.KMD))

        for key in keys:
            pp = kwargs.get(key)
            if key != 'ss':
                elements.append(Element.Text(f'**{key}**% : {pp if pp is not None else "-"} pp', type=Types.Text.KMD))
            else:
                elements.append(Element.Text(f' ***SS***   : {pp if pp is not None else "-"} pp', type=Types.Text.KMD))

        return Module.Section(Struct.Paragraph(3, *elements))
