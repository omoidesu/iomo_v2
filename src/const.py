redis_access_token = 'osu_access_token'
redis_refresh_token = 'osu_refresh_token'

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
