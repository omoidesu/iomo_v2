# redis_key
redis_access_token = 'osu_access_token'
redis_refresh_token = 'osu_refresh_token'
redis_recent_beatmap = '{guild_id}:{channel_id}'

# api
osu_api = 'https://osu.ppy.sh/api/v2'
sayo_api = 'https://api.sayobot.cn'
pp_plus = 'https://syrin.me/pp+/u/'
osu_chan = 'https://osuchan.syrin.me/api/profiles/users/{0}/stats/0?user_id_type=username'

_osu = 'osu'
_taiko = 'taiko'
_fruits = 'fruits'
_mania = 'mania'

game_modes = (_osu, _taiko, _fruits, _mania)

game_mode_convent = {
    '0': _osu, '1': _taiko, '2': _fruits, '3': _mania,
    'ctb': _fruits, 'catch': _fruits, 'std': _osu,
    'osu': _osu, 'taiko': _taiko, 'mania': _mania, 'fruits': _fruits
}

mods = {
    'NM': 0,
    'EZ': 1,
    'NF': 1 << 1,
    'HT': 1 << 2,
    'HR': 1 << 3,
    'SD': 1 << 4,
    'PF': 1 << 4,
    'DT': 1 << 5,
    'NC': 1 << 5,
    'HD': 1 << 6,
    'FI': 1 << 6,
    'FL': 1 << 7,
    'RX': 1 << 8,
    'AP': 1 << 9,
    'SO': 1 << 10,
    '4K': 1 << 11,
    '5K': 1 << 12,
    '6K': 1 << 13,
    '7K': 1 << 14,
    '8K': 1 << 15,
    '9K': 1 << 16,
    'MR': 1 << 17,
    'TD': 1 << 18
}


class Assets:
    COLOR = {_osu: '#EA669E', _taiko: '#E44116', _fruits: '#71368A', _mania: '#66CCFF'}

    # flag emoji in info card
    FLAG = {
        'A': '🇦', 'B': '🇧', 'C': '🇨', 'D': '🇩', 'E': '🇪', 'F': '🇫', 'G': '🇬',
        'H': '🇭', 'I': '🇮', 'J': '🇯', 'K': '🇰', 'L': '🇱', 'M': '🇲', 'N': '🇳',
        'O': '🇴', 'P': '🇵', 'Q': '🇶', 'R': '🇷', 'S': '🇸', 'T': '🇹', 'U': '🇺',
        'V': '🇻', 'W': '🇼', 'X': '🇽', 'Y': '🇾', 'Z': '🇿'
    }

    class Image:
        DEFAULT_AVATAR = 'https://img.kookapp.cn/assets/2022-09/DB3C2HLwkO03k03k.png'
        DEFAULT_COVER = 'https://img.kookapp.cn/assets/2022-09/sJPuzoIpf40p0069.png'
        OSU_LOGO = 'https://img.kookapp.cn/assets/2022-09/Hhm2wv3txG09q09q.png'
        MOD = {
            '4K': 'https://img.kaiheila.cn/assets/2021-08/24/G86hJnf5pt01900w.png',
            '5K': 'https://img.kaiheila.cn/assets/2021-08/24/DEMNjj2veT01900w.png',
            '6K': 'https://img.kaiheila.cn/assets/2021-08/24/qi3BCGpXKc01900w.png',
            '7K': 'https://img.kaiheila.cn/assets/2021-08/24/lJdTF76QXX01900w.png',
            '8K': 'https://img.kaiheila.cn/assets/2021-08/24/ZcxMoF5A4K01900w.png',
            '9K': 'https://img.kaiheila.cn/assets/2021-08/24/d16QXjsswa01900w.png',
            'AP': 'https://img.kookapp.cn/assets/2022-09/zfR8ygVGsH01900w.png',
            'DT': 'https://img.kookapp.cn/assets/2022-09/B2CIlODult01900w.png',
            'EZ': 'https://img.kookapp.cn/assets/2022-09/vMXaQeDFON01900w.png',
            'FI': 'https://img.kookapp.cn/assets/2022-09/GgeiHm2HFG01900w.png',
            'FL': 'https://img.kookapp.cn/assets/2022-09/pVcAsfXVVc01900w.png',
            'HD': 'https://img.kookapp.cn/assets/2022-09/R0MvhGpsLa01900w.png',
            'HR': 'https://img.kookapp.cn/assets/2022-09/hSM8jyOXSr01900w.png',
            'HT': 'https://img.kookapp.cn/assets/2022-09/AMstF0AGx501900w.png',
            'MR': 'https://img.kookapp.cn/assets/2022-09/vXXXfSuOXx01900w.png',
            'NC': 'https://img.kookapp.cn/assets/2022-09/HknHRO8yyP01900w.png',
            'NF': 'https://img.kookapp.cn/assets/2022-09/4HhbPa8ZsB01900w.png',
            'NM': 'https://img.kookapp.cn/assets/2022-09/T7C4KA92kR01900w.png',
            'PF': 'https://img.kookapp.cn/assets/2022-09/nkCeLVIFRa01900w.png',
            'RX': 'https://img.kookapp.cn/assets/2022-09/Rx5qEu0VYQ01900w.png',
            'SD': 'https://img.kookapp.cn/assets/2022-09/mjGk8xs9mj01900w.png',
            'SO': 'https://img.kookapp.cn/assets/2022-09/0xJf2hqmBX01900w.png',
            'TD': 'https://img.kookapp.cn/assets/2022-09/lfC8s0OUUW01800u.png'
        }
        STATUS = {
            'ranked': 'https://img.kookapp.cn/assets/2022-09/96B30px3ID01s01s.png',
            'loved': 'https://img.kookapp.cn/assets/2022-09/BB3euMaE7g01s01s.png',
            'approved': 'https://img.kookapp.cn/assets/2022-09/lJfaemtPZi01s01s.png',
            'qualified': 'https://img.kookapp.cn/assets/2022-09/Ph7sJAcq4I01s01s.png',
            'graveyard': 'https://img.kookapp.cn/assets/2022-09/loheUUkqYa01s01s.png',
            'wip': 'https://img.kookapp.cn/assets/2022-09/loheUUkqYa01s01s.png',
            'pending': 'https://img.kookapp.cn/assets/2022-09/loheUUkqYa01s01s.png'
        }
        RANK = {
            'A': 'https://img.kaiheila.cn/assets/2021-08/24/dgHYPCcpFq03g01q.png',
            'B': 'https://img.kaiheila.cn/assets/2021-08/24/WqoMKqSdYS03g01q.png',
            'C': 'https://img.kaiheila.cn/assets/2021-08/24/kgfw32J6Gn03g01q.png',
            'D': 'https://img.kaiheila.cn/assets/2021-08/24/OzS1w7hhvR03g01q.png',
            'F': 'https://img.kaiheila.cn/assets/2021-08/24/r3mbUMxNxI03g01q.png',
            'S': 'https://img.kaiheila.cn/assets/2021-08/24/3oSKxAlJRl03g01q.png',
            'SH': 'https://img.kaiheila.cn/assets/2021-08/24/eangu6qc7o03f01q.png',
            'X': 'https://img.kaiheila.cn/assets/2021-08/24/WybzjQ1Rav03g01q.png',
            'XH': 'https://img.kaiheila.cn/assets/2021-08/24/EZGszN31qZ03g01q.png'
        }
        MODE = {
            _osu: 'https://img.kaiheila.cn/assets/2021-08/YRLap3CaH30rs0rs.png',
            _taiko: 'https://img.kaiheila.cn/assets/2021-08/ft5Yli9Nrf0rs0rs.png',
            _fruits: 'https://img.kaiheila.cn/assets/2021-08/hKKvcWTHYG0rs0rs.png',
            _mania: 'https://img.kaiheila.cn/assets/2021-08/vyRb7w1Bgz0rs0rs.png'
        }

        # images for search card
        MAPPER = 'https://img.kookapp.cn/assets/2022-09/vyG3fPwPyC02s02s.png'
        FAVOURITE = 'https://img.kookapp.cn/assets/2022-09/pAIhvZURUs05k05k.png'
        PLAYCOUNT = 'https://img.kookapp.cn/assets/2022-09/Gm23EDsVfF05k05k.png'

        DIFF = {
            'osu': 'https://img.kaiheila.cn/assets/2021-08/F23yrEJKXR0dw0dw.png',
            'taiko': 'https://img.kaiheila.cn/assets/2021-08/LNETy7CryN0dw0dw.png',
            'fruits': 'https://img.kaiheila.cn/assets/2021-08/38JlboF4L70dw0dw.png',
            'mania': 'https://img.kaiheila.cn/assets/2021-08/ZpbkNfUxqo0dw0dw.png'
        }


class Sticker:
    class Misc:
        BPM = '(emj)bpm(emj)[6147923945822473/IuRZ4sJGs80fn0fn]'
        CIRCLES = '(emj)circles(emj)[6147923945822473/Fg1qywTKmC0fn0fn]'
        SLIDERS = '(emj)sliders(emj)[6147923945822473/qJeiQMdBQk0fn0fn]'
        LENGTH = '(emj)length(emj)[6147923945822473/VPfMmUrAP90fn0fn]'
        PROFILE = '(emj)profile(emj)[6147923945822473/UT3YVPbPI002s02s]'
        PLAY = '(emj)play(emj)[6147923945822473/bVLhXwDP4v05k05k]'
        FAVOURATE = '(emj)favourate(emj)[6147923945822473/PqzdX063Vj05k05k]'

    MODS = {
        'EZ': '(emj)modEZ(emj)[6147923945822473/BNm1HKXTk301900w]',
        'NF': '(emj)modNF(emj)[6147923945822473/liWefVzool01900w]',
        'HT': '(emj)modHT(emj)[6147923945822473/oVrgtIv5BW01900w]',
        'HR': '(emj)modHR(emj)[6147923945822473/oB4q89gfRE01900w]',
        'SD': '(emj)modSD(emj)[6147923945822473/K4xZkmHBOm01900w]',
        'DT': '(emj)modDT(emj)[6147923945822473/uvBekQGLHX01900w]',
        'NC': '(emj)modNC(emj)[6147923945822473/SymPZhKRlb01900w]',
        'HD': '(emj)modHD(emj)[6147923945822473/cysdyeOJId01900w]',
        'FL': '(emj)modFL(emj)[6147923945822473/GYm7PCDgou01900w]',
        'RX': '(emj)modRX(emj)[6147923945822473/aSRnt2vWQg01900w]',
        'AP': '(emj)modAP(emj)[6147923945822473/OUA0zUyX2b01900w]',
        'SO': '(emj)modSO(emj)[6147923945822473/TNVTcHV0V501900w]',
        'TD': '(emj)modTD(emj)[6147923945822473/Saao0maPAY01800u]',
        'FI': '(emj)modFI(emj)[6147923945822473/E0VrPzEsuX01900w]',
        '4K': '(emj)mod4K(emj)[6147923945822473/Askp34kfZP01900w]',
        '5K': '(emj)mod5K(emj)[6147923945822473/5PA4gUK4mB01900w]',
        '6K': '(emj)mod6K(emj)[6147923945822473/S2U1YjFAmu01900w]',
        '7K': '(emj)mod7K(emj)[6147923945822473/RGNf6tKsi701900w]',
        '8K': '(emj)mod8K(emj)[6147923945822473/OouSGtpccB01900w]',
        '9K': '(emj)mod9K(emj)[6147923945822473/gq2Ex1yTaU01900w]',
        'MR': '(emj)modMR(emj)[6147923945822473/sztiOBFLwX01900w]',
        'NM': '(emj)modNM(emj)[6147923945822473/PdcDWD2Tsg01900w]'
    }

    RANKS = {
        'A': '(emj)rankA(emj)[6147923945822473/3t1aVcRJLk03g01q]',
        'B': '(emj)rankB(emj)[6147923945822473/lu1xQGVxHc03g01q]',
        'C': '(emj)rankC(emj)[6147923945822473/QRj5ZPzUM203g01q]',
        'D': '(emj)rankD(emj)[6147923945822473/qksOqZNjle03g01q]',
        'F': '(emj)rankF(emj)[6147923945822473/HkOLe5XdJN03g01q]',
        'S': '(emj)rankS(emj)[6147923945822473/Pg9N2rp2rg03g01q]',
        'SH': '(emj)rankSH(emj)[6147923945822473/nBEToRSz4w03f01q]',
        'X': '(emj)rankX(emj)[6147923945822473/Xj41eVcF2003g01q]',
        'XH': '(emj)rankXH(emj)[6147923945822473/TQnmo93NY003g01q]'
    }

    MODES = {
        0: '(emj)modeOSU(emj)[6147923945822473/adAvlRGhPU0rs0rs]',
        1: '(emj)modeTaiko(emj)[6147923945822473/uC0ixh9gwg0rs0rs]',
        2: '(emj)modeFruits(emj)[6147923945822473/eT3zJk3Dmi0rs0rs]',
        3: '(emj)modeMania(emj)[6147923945822473/NlwJP3fylJ0rs0rs]'
    }

    STATUS = {
        'ranked': '(emj)ranked(emj)[6147923945822473/XRH8X7Jzq201s01s]',
        'approved': '(emj)approved(emj)[6147923945822473/XviIgvKOaG01s01s]',
        'qualified': '(emj)qualified(emj)[6147923945822473/G5cBjKEYut01s01s]',
        'loved': '(emj)loved(emj)[6147923945822473/76HKRBtX5Z01s01s]',
        'pending': '(emj)graveyard(emj)[6147923945822473/13i0mTUlQp01s01s]',
        'wip': '(emj)graveyard(emj)[6147923945822473/13i0mTUlQp01s01s]',
        'graveyard': '(emj)graveyard(emj)[6147923945822473/13i0mTUlQp01s01s]'
    }
