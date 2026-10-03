# -*- coding: utf-8 -*-
"""
권수(1~36권)별 주요 세력 판도 데이터셋
- 《대망》은 도쿠가와 이에야스의 생애(1542~1616)를 다룬 대하소설로,
  실제 전국시대 역사의 흐름을 바탕으로 권별 시기를 근사하여 구성하였습니다.
- 아래 데이터는 "참고용 근사치"이며, 실제 읽고 있는 번역판의 권 구성에 따라
  연도/세력 범위가 다를 수 있습니다. 필요에 따라 PERIODS 값을 직접 수정해
  보고 있는 판본에 맞출 수 있습니다.
"""

FACTIONS = {
    "imagawa": {"name": "이마가와 (이마가와 요시모토)", "color": "#9467bd"},
    "oda": {"name": "오다 (오다 노부나가)", "color": "#d62728"},
    "tokugawa": {"name": "도쿠가와 (도쿠가와 이에야스)", "color": "#1f77b4"},
    "takeda": {"name": "다케다 (다케다 신겐/가츠요리)", "color": "#2ca02c"},
    "uesugi": {"name": "우에스기 (우에스기 겐신/가게카츠)", "color": "#8c564b"},
    "hojo": {"name": "호조 (호조 우지야스/우지마사)", "color": "#e377c2"},
    "mori": {"name": "모리 (모리 모토나리/데루모토)", "color": "#7f7f7f"},
    "akechi": {"name": "아케치 (아케치 미츠히데)", "color": "#bcbd22"},
    "toyotomi": {"name": "도요토미 (도요토미 히데요시)", "color": "#ff7f0e"},
    "shimazu": {"name": "시마즈", "color": "#17becf"},
    "date": {"name": "다테 (다테 마사무네)", "color": "#aec7e8"},
    "otomo": {"name": "오토모", "color": "#c49c94"},
    "chosokabe": {"name": "조소카베", "color": "#f7b6d2"},
    "other": {"name": "기타/군소 다이묘", "color": "#9c9c9c"},
    "unknown": {"name": "미상", "color": "#4a4a4a"},
}

# 각 period: (시작권, 끝권, 시작연도, 끝연도, 시대 라벨, {province_id: faction_key})
# 명시되지 않은 율령국은 자동으로 "unknown" 처리됩니다.
PERIODS = [
    {
        "volumes": (1, 4),
        "years": (1551, 1560),
        "label": "군웅할거 · 오케하자마 전야",
        "note": "이마가와 가문의 인질로 성장하는 다케치요(훗날 이에야스) 시기.",
        "territories": {
            51: "imagawa", 52: "imagawa", 53: "imagawa", 54: "imagawa",  # 미카와·토토우미·스루가·이즈
            44: "oda",  # 오와리
            45: "oda", 41: "oda",
            56: "takeda", 57: "takeda",
            55: "hojo", 58: "hojo", 59: "hojo", 60: "hojo",
            65: "uesugi",
            18: "mori", 16: "mori", 17: "mori",
            68: "date", 67: "date",
        },
    },
    {
        "volumes": (5, 9),
        "years": (1560, 1570),
        "label": "오케하자마 이후 · 오다-도쿠가와 동맹",
        "note": "오케하자마 전투로 이마가와 몰락, 이에야스 미카와 독립 및 오다와 동맹.",
        "territories": {
            51: "tokugawa", 52: "tokugawa", 41: "tokugawa",
            44: "oda", 45: "oda", 42: "oda", 43: "oda", 38: "oda", 40: "oda",
            53: "takeda", 56: "takeda", 57: "takeda",
            55: "hojo", 58: "hojo", 59: "hojo", 60: "hojo", 54: "hojo",
            65: "uesugi", 64: "uesugi",
            18: "mori", 16: "mori", 17: "mori", 19: "mori",
            68: "date", 67: "date",
        },
    },
    {
        "volumes": (10, 14),
        "years": (1570, 1575),
        "label": "나가시노 전투 전후",
        "note": "다케다 신겐 사망, 가츠요리의 남진과 나가시노 전투 패배.",
        "territories": {
            51: "tokugawa", 52: "tokugawa", 41: "tokugawa", 42: "tokugawa",
            44: "oda", 45: "oda", 43: "oda", 38: "oda", 40: "oda", 37: "oda", 33: "oda",
            53: "takeda", 56: "takeda", 57: "takeda", 54: "takeda",
            55: "hojo", 58: "hojo", 59: "hojo", 60: "hojo", 61: "hojo",
            65: "uesugi", 64: "uesugi", 48: "uesugi", 47: "uesugi",
            18: "mori", 16: "mori", 17: "mori", 19: "mori", 22: "mori", 30: "mori",
            68: "date", 67: "date",
        },
    },
    {
        "volumes": (15, 18),
        "years": (1575, 1582),
        "label": "오다 노부나가 전성기 · 혼노지의 변",
        "note": "노부나가의 천하포무 절정과 혼노지의 변으로 급사.",
        "territories": {
            51: "tokugawa", 52: "tokugawa", 41: "tokugawa", 42: "tokugawa", 53: "tokugawa",
            44: "oda", 45: "oda", 43: "oda", 38: "oda", 40: "oda", 37: "oda", 33: "oda",
            34: "oda", 35: "oda", 32: "oda", 50: "oda", 46: "oda", 39: "oda",
            56: "takeda", 57: "takeda",  # 다케다 가츠요리 말기 축소
            55: "hojo", 58: "hojo", 59: "hojo", 60: "hojo", 61: "hojo", 62: "hojo", 54: "hojo",
            65: "uesugi", 64: "uesugi", 48: "uesugi", 47: "uesugi",
            18: "mori", 16: "mori", 17: "mori", 19: "mori", 22: "mori", 30: "mori", 21: "mori", 20: "mori",
            68: "date", 67: "date",
            38: "akechi",  # 혼노지의 변 직후 교토 일시 장악 (18권 말)
        },
    },
    {
        "volumes": (19, 22),
        "years": (1582, 1584),
        "label": "야마자키·시즈가타케 · 고마키나가쿠테",
        "note": "하시바 히데요시의 급부상과 이에야스-노부카츠 연합군의 고마키나가쿠테 전투.",
        "territories": {
            51: "tokugawa", 52: "tokugawa", 41: "tokugawa", 42: "tokugawa", 53: "tokugawa", 54: "tokugawa",
            44: "oda", 45: "oda",
            38: "toyotomi", 40: "toyotomi", 37: "toyotomi", 33: "toyotomi", 34: "toyotomi", 35: "toyotomi",
            32: "toyotomi", 50: "toyotomi", 46: "toyotomi", 39: "toyotomi", 43: "toyotomi", 36: "toyotomi",
            55: "hojo", 58: "hojo", 59: "hojo", 60: "hojo", 61: "hojo", 62: "hojo", 56: "hojo", 57: "hojo",
            65: "uesugi", 64: "uesugi", 48: "uesugi", 47: "uesugi",
            18: "mori", 16: "mori", 17: "mori", 19: "mori", 22: "mori", 30: "mori", 21: "mori", 20: "mori",
            68: "date", 67: "date",
        },
    },
    {
        "volumes": (23, 27),
        "years": (1584, 1590),
        "label": "도요토미 천하통일 · 오다와라 정벌",
        "note": "이에야스의 신종(臣從)과 히데요시의 규슈·오다와라 평정, 전국 통일 완성.",
        "territories": {
            51: "tokugawa", 52: "tokugawa", 41: "tokugawa", 42: "tokugawa", 53: "tokugawa", 54: "tokugawa",
            56: "tokugawa", 57: "tokugawa",
            44: "toyotomi", 45: "toyotomi", 38: "toyotomi", 40: "toyotomi", 37: "toyotomi", 33: "toyotomi",
            34: "toyotomi", 35: "toyotomi", 32: "toyotomi", 50: "toyotomi", 46: "toyotomi", 39: "toyotomi",
            43: "toyotomi", 36: "toyotomi", 27: "toyotomi", 30: "toyotomi", 22: "toyotomi",
            12: "toyotomi", 13: "chosokabe", 14: "toyotomi", 15: "toyotomi",
            18: "mori", 16: "mori", 17: "mori", 19: "mori", 21: "mori", 20: "mori",
            1: "shimazu", 2: "shimazu", 3: "shimazu",
            5: "otomo",
            55: "hojo", 58: "hojo", 59: "hojo", 60: "hojo", 61: "hojo", 62: "hojo",  # ~1590년 멸망 직전까지
            65: "uesugi", 64: "uesugi", 48: "uesugi", 47: "uesugi",
            68: "date", 67: "date",
        },
    },
    {
        "volumes": (28, 31),
        "years": (1590, 1598),
        "label": "도요토미 정권 전성기 · 간토 이봉",
        "note": "이에야스, 간토로 이봉되어 간토 8주 경영. 임진왜란(1592~1598) 발발.",
        "territories": {
            55: "tokugawa", 58: "tokugawa", 59: "tokugawa", 60: "tokugawa", 61: "tokugawa", 62: "tokugawa",
            63: "tokugawa", 64: "tokugawa",
            44: "toyotomi", 45: "toyotomi", 38: "toyotomi", 40: "toyotomi", 37: "toyotomi", 33: "toyotomi",
            34: "toyotomi", 35: "toyotomi", 32: "toyotomi", 50: "toyotomi", 46: "toyotomi", 39: "toyotomi",
            43: "toyotomi", 36: "toyotomi", 51: "toyotomi", 52: "toyotomi", 41: "toyotomi", 42: "toyotomi",
            53: "toyotomi", 54: "toyotomi", 56: "toyotomi", 57: "toyotomi",
            18: "mori", 16: "mori", 17: "mori", 19: "mori", 21: "mori", 20: "mori",
            1: "shimazu", 2: "shimazu", 3: "shimazu",
            68: "date", 67: "date",
            65: "uesugi", 48: "uesugi", 47: "uesugi",
        },
    },
    {
        "volumes": (32, 34),
        "years": (1598, 1600),
        "label": "히데요시 사망 · 세키가하라 전투",
        "note": "히데요시 사후 동군(이에야스)과 서군(미츠나리)의 대결, 세키가하라 전투로 귀결.",
        "territories": {
            55: "tokugawa", 58: "tokugawa", 59: "tokugawa", 60: "tokugawa", 61: "tokugawa", 62: "tokugawa",
            63: "tokugawa", 64: "tokugawa", 40: "tokugawa", 44: "tokugawa", 45: "tokugawa",
            51: "tokugawa", 52: "tokugawa", 41: "tokugawa", 42: "tokugawa", 53: "tokugawa", 54: "tokugawa",
            56: "tokugawa", 57: "tokugawa",
            38: "toyotomi", 37: "toyotomi", 33: "toyotomi", 34: "toyotomi", 35: "toyotomi",
            18: "mori", 16: "mori", 17: "mori",
            65: "uesugi", 48: "uesugi", 47: "uesugi",
            68: "date", 67: "date",
            1: "shimazu", 2: "shimazu",
        },
    },
    {
        "volumes": (35, 36),
        "years": (1600, 1616),
        "label": "에도 막부 개창 · 오사카 전투",
        "note": "세키가하라 승리 후 에도 막부 수립, 오사카 전투(1614~1615)로 도요토미 가문 멸망.",
        "territories": {
            55: "tokugawa", 58: "tokugawa", 59: "tokugawa", 60: "tokugawa", 61: "tokugawa", 62: "tokugawa",
            63: "tokugawa", 64: "tokugawa", 40: "tokugawa", 44: "tokugawa", 45: "tokugawa",
            51: "tokugawa", 52: "tokugawa", 41: "tokugawa", 42: "tokugawa", 53: "tokugawa", 54: "tokugawa",
            56: "tokugawa", 57: "tokugawa", 38: "tokugawa", 37: "tokugawa", 33: "tokugawa", 34: "tokugawa",
            35: "tokugawa", 65: "tokugawa", 32: "tokugawa", 50: "tokugawa", 39: "tokugawa",
            18: "mori", 16: "mori", 17: "mori",
            68: "date", 67: "date",
            1: "shimazu", 2: "shimazu",
            36: "toyotomi",  # 오사카 전투 직전까지 도요토미 가문 잔존 영지(기이 일부 상징)
        },
    },
]


def get_period(volume: int) -> dict:
    """특정 권수가 속한 시대(period)를 반환"""
    for period in PERIODS:
        lo, hi = period["volumes"]
        if lo <= volume <= hi:
            return period
    return PERIODS[-1] if volume > PERIODS[-1]["volumes"][1] else PERIODS[0]


def get_territory_map(volume: int) -> dict:
    """해당 권수 기준 province_id -> faction_key 딕셔너리 (미지정은 unknown)"""
    period = get_period(volume)
    return period["territories"]


def get_year_label(volume: int) -> str:
    period = get_period(volume)
    lo, hi = period["years"]
    return f"{lo}년 ~ {hi}년"
