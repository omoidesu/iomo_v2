# redis_key
redis_access_token = 'osu_access_token'
redis_refresh_token = 'osu_refresh_token'
redis_recent_beatmap = '{guild_id}:{channel_id}:recent'
redis_reaction = '{method}:{id}'
redis_mp_room = 'mp-{}'

# api
osu_api = 'https://osu.ppy.sh/api/v2'
sayo_api = 'https://api.sayobot.cn'
pp_plus = 'https://syrin.me/pp+/u/'
osu_chan = 'https://osuchan.syrin.me/api/profiles/users/{0}/stats/0?user_id_type=username'

_osu = 'osu'
_taiko = 'taiko'
_fruits = 'fruits'
_mania = 'mania'

osu_source = 'osu'
sayo_source = 'sayo'

game_modes = (_osu, _taiko, _fruits, _mania)

index_emojis = ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣')

# 匹配更多参数
game_mode_map = {
    '0': _osu, '1': _taiko, '2': _fruits, '3': _mania,
    'osu': _osu, 'taiko': _taiko, 'mania': _mania, 'fruits': _fruits,
    'ctb': _fruits, 'catch': _fruits, 'std': _osu
}

search_source_map = {
    'osu': osu_source, 'ppy': osu_source, 'o': osu_source,
    'sayo': sayo_source, 'sy': sayo_source, 'sayobot': sayo_source, 's': sayo_source
}

no_leaderboard_status = (-2, -1, 0)
beatmap_status = {
    -2: 'graveyard', -1: 'wip', 0: 'pending', 1: 'ranked', 2: 'approved', 3: 'qualified', 4: 'loved',
    'graveyard': 'graveyard', 'wip': 'wip', 'pending': 'pending', 'ranked': 'ranked', 'approved': 'approved',
    'qualified': 'qualified', 'loved': 'loved'
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

user_homepage_pattern = r'https://osu.ppy.sh/users/\d+'

bp_index = {'100': 1, '95': 2, '90.25': 3, '85.73749999999998': 4, '81.45062499999999': 5, '77.37809374999998': 6,
            '73.50918906249998': 7, '69.83372960937497': 8, '66.34204312890623': 9, '63.02494097246091': 10,
            '59.87369392383787': 11, '56.880009227645964': 12, '54.03600876626366': 13, '51.33420832795048': 14,
            '48.76749791155295': 15, '46.329123015975306': 16, '44.012666865176534': 17, '41.812033521917705': 18,
            '39.72143184582182': 19, '37.73536025353073': 20, '35.84859224085419': 21, '34.05616262881148': 22,
            '32.3533544973709': 23, '30.73568677250236': 24, '29.198902433877237': 25, '27.738957312183377': 26,
            '26.352009446574204': 27, '25.034408974245494': 28, '23.782688525533217': 29, '22.593554099256554': 30,
            '21.463876394293727': 31, '20.39068257457904': 32, '19.371148445850086': 33, '18.402591023557584': 34,
            '17.4824614723797': 35, '16.608338398760715': 36, '15.777921478822678': 37, '14.989025404881545': 38,
            '14.239574134637467': 39, '13.527595427905592': 40, '12.851215656510313': 41, '12.208654873684797': 42,
            '11.598222130000556': 43, '11.018311023500528': 44, '10.467395472325501': 45, '9.944025698709225': 46,
            '9.446824413773763': 47, '8.974483193085076': 48, '8.52575903343082': 49, '8.09947108175928': 50,
            '7.694497527671315': 51, '7.30977265128775': 52, '6.944284018723361': 53, '6.597069817787194': 54,
            '6.267216326897833': 55, '5.953855510552941': 56, '5.656162735025293': 57, '5.3733545982740285': 58,
            '5.104686868360327': 59, '4.84945252494231': 60, '4.606979898695195': 61, '4.376630903760435': 62,
            '4.157799358572413': 63, '3.949909390643792': 64, '3.752413921111602': 65, '3.5647932250560217': 66,
            '3.3865535638032207': 67, '3.2172258856130593': 68, '3.0563645913324065': 69, '2.903546361765786': 70,
            '2.7583690436774964': 71, '2.6204505914936216': 72, '2.4894280619189404': 73, '2.3649566588229933': 74,
            '2.2467088258818437': 75, '2.134373384587751': 76, '2.0276547153583633': 77, '1.926271979590445': 78,
            '1.829958380610923': 79, '1.7384604615803767': 80, '1.651537438501358': 81, '1.5689605665762898': 82,
            '1.4905125382474753': 83, '1.4159869113351014': 84, '1.3451875657683463': 85, '1.2779281874799289': 86,
            '1.2140317781059324': 87, '1.1533301892006358': 88, '1.0956636797406039': 89, '1.0408804957535738': 90,
            '0.988836470965895': 91, '0.9393946474176': 92, '0.8924249150467202': 93, '0.8478036692943841': 94,
            '0.8054134858296649': 95, '0.7651428115381815': 96, '0.7268856709612724': 97, '0.6905413874132088': 98,
            '0.6560143180425483': 99, '0.6232136021404209': 100}


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

        LOADING = (
            'https://img.kookapp.cn/assets/2023-10/BCw58EdK0j0go04b.gif',
            'https://img.kookapp.cn/assets/2023-10/s3R4C33yew0go04b.gif',
            'https://img.kookapp.cn/assets/2023-10/4AGLagrPkn0go04b.gif',
            'https://img.kookapp.cn/assets/2023-10/t8f8IyUKci0go04b.gif',
            'https://img.kookapp.cn/assets/2023-10/3QwbaOVEY00go04b.gif',
            'https://img.kookapp.cn/assets/2023-10/EYq6hR9JYI0go04b.gif'
        )

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
        BPM = '(emj)bpm(emj)[6147923945822473/IuRZ4sJGs80fn0fn]'
        CIRCLES = '(emj)circles(emj)[6147923945822473/Fg1qywTKmC0fn0fn]'
        SLIDERS = '(emj)sliders(emj)[6147923945822473/qJeiQMdBQk0fn0fn]'
        LENGTH = '(emj)length(emj)[6147923945822473/VPfMmUrAP90fn0fn]'
        PROFILE = '(emj)profile(emj)[6147923945822473/UT3YVPbPI002s02s]'
        PLAYCOUNT = '(emj)play(emj)[6147923945822473/bVLhXwDP4v05k05k]'
        FAVOURITE = '(emj)favourate(emj)[6147923945822473/PqzdX063Vj05k05k]'

        MOD = {
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

        RANK = {
            'A': '(emj)rankA(emj)[6147923945822473/SYoDxCWt4g01900w]',
            'B': '(emj)rankB(emj)[6147923945822473/2WwpsvhGxr01900w]',
            'C': '(emj)rankC(emj)[6147923945822473/n5ce7Snn2d01900w]',
            'D': '(emj)rankD(emj)[6147923945822473/FAr2GdugIp01900w]',
            'F': '(emj)rankF(emj)[6147923945822473/7U11ztN7HN01900w]',
            'S': '(emj)rankS(emj)[6147923945822473/u3hsPoqVz301900w]',
            'SH': '(emj)rankSH(emj)[6147923945822473/5CMAVwYVoJ01900w]',
            'X': '(emj)rankX(emj)[6147923945822473/PzSpitD1h201900w]',
            'XH': '(emj)rankXH(emj)[6147923945822473/1ZsyUMviZF01900w]'
        }

        MODE = {
            _osu: '(emj)modeOSU(emj)[6147923945822473/adAvlRGhPU0rs0rs]',
            _taiko: '(emj)modeTaiko(emj)[6147923945822473/uC0ixh9gwg0rs0rs]',
            _fruits: '(emj)modeFruits(emj)[6147923945822473/eT3zJk3Dmi0rs0rs]',
            _mania: '(emj)modeMania(emj)[6147923945822473/NlwJP3fylJ0rs0rs]'
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

        DIFF = {
            'osu': '(emj)osu(emj)[8462491027363735/PX5lqCvifT0dw0dw]',
            'taiko': '(emj)taiko(emj)[8462491027363735/Bcthix30NE0dw0dw]',
            'fruits': '(emj)fruits(emj)[8462491027363735/bYaumasgZB0dw0dw]',
            'mania': '(emj)mania(emj)[8462491027363735/DcAywzHQng0dw0dw]'
        }

        STATISTICS = {
            'osu': {
                'count_300': '(emj)osu_300(emj)[8462491027363735/RFCyQ9F2Br05q03c]',
                'count_100': '(emj)osu_100(emj)[8462491027363735/lNVVxabQ5r05e036]',
                'count_50': '(emj)osu_50(emj)[8462491027363735/Kf1273LpyI03y036]',
                'count_geki': '(emj)osu_geki(emj)[8462491027363735/CVsCY4rjcp04i04k]',
                'count_katu': '(emj)osu_katu(emj)[8462491027363735/diU6rW35Yl03e03g]',
                'count_miss': '(emj)osu_miss(emj)[8462491027363735/fs3hty0W2b03m03m]'

            },

            'taiko': {
                'count_300': '(emj)taiko_300(emj)[8462491027363735/fNZwGrjeo70ao0ao]',
                'count_100': '(emj)taiko_100(emj)[8462491027363735/gE40WXpzib0ao0ao]',
                'count_miss': '(emj)taiko_miss(emj)[8462491027363735/pwAOUL8tA608w08w]',
            },

            'fruits': {
                'count_300': '(emj)fruits_300(emj)[8462491027363735/uo3Lc0029602v02w]',
                'count_100': '(emj)fruits_100(emj)[8462491027363735/LMrnKuBHHh02602t]',
                'count_katu': '(emj)fruits_katu(emj)[8462491027363735/yDSk3XFqua01o01z]',
                'count_miss': '(emj)fruits_miss(emj)[8462491027363735/vz739p9XHy02c02b]'
            },

            'mania': {
                'count_geki': '(emj)mania_geki(emj)[8462491027363735/xg8OLGrR7u0ag052]',
                'count_300': '(emj)mania_300(emj)[8462491027363735/8FP93o7iQC0ck07a]',
                'count_katu': '(emj)mania_katu(emj)[8462491027363735/YGE81JV82K0bi06o]',
                'count_100': '(emj)mania_100(emj)[8462491027363735/WAN7y7AwWk0a406g]',
                'count_50': '(emj)mania_50(emj)[8462491027363735/OLG23veds207w06a]',
                'count_miss': '(emj)mania_miss(emj)[8462491027363735/KPYhAwmthM0a205i]',
            }
        }

    class Audio:
        WELCOME = 'https://img.kookapp.cn/attachments/2023-10/07/652178e1b3d80.mp3'
