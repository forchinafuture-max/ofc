"""
规则参数、计分配置
"""

# 区域长度限制
REGION_LENGTH_LIMITS = {
    'top': 3,
    'middle': 5,
    'bottom': 5
}

# 头道对子牌型分
TOP_PAIR_SCORES = {
    6: 1,   # 66
    7: 2,   # 77
    8: 3,   # 88
    9: 4,   # 99
    10: 5,  # TT
    11: 6,  # JJ
    12: 7,  # QQ
    13: 8,  # KK
    14: 9   # AA
}

# 头道三条牌型分
TOP_TRIPS_SCORES = {
    2: 10,   # 222
    3: 11,   # 333
    4: 12,   # 444
    5: 13,   # 555
    6: 14,   # 666
    7: 15,   # 777
    8: 16,   # 888
    9: 17,   # 999
    10: 18,  # TTT
    11: 19,  # JJJ
    12: 20,  # QQQ
    13: 21,  # KKK
    14: 22   # AAA
}

# 中道牌型分
MIDDLE_HAND_SCORES = {
    'royal_flush': 50,
    'straight_flush': 30,
    'four_of_a_kind': 20,
    'full_house': 12,
    'flush': 8,
    'straight': 4,
    'three_of_a_kind': 2,
    'two_pair': 0,
    'one_pair': 0,
    'high_card': 0
}

# 底道牌型分
BOTTOM_HAND_SCORES = {
    'royal_flush': 25,
    'straight_flush': 15,
    'four_of_a_kind': 10,
    'full_house': 6,
    'flush': 4,
    'straight': 2,
    'three_of_a_kind': 0,
    'two_pair': 0,
    'one_pair': 0,
    'high_card': 0
}

# 范特西模式配置
FANTASY_MODE_CONFIG = {
    # 顶部牌型对应的发牌数量
    'cards_by_top_hand': {
        'trips': 17,  # 三条或以上，发17张牌
        'aa': 16,     # AA，发16张牌
        'kk': 15,     # KK，发15张牌
        'qq': 14      # QQ，发14张牌
    },
    # 留在范特西模式的条件
    'stay_conditions': {
        'bottom_min_strength': 7,  # 底部至少四条强度
        'top_min_strength': 2      # 顶部至少三条强度
    }
}

# MCTS配置
MCTS_CONFIG = {
    'exploration_weight': 1.0,
    'simulation_depth': 100,
    'rollout_count': 1000
}

# 奖励函数配置
REWARD_CONFIG = {
    'bust_penalty': -300,
    'fantasy_bonus': 150,
    'win_bonus': 100,
    'lose_penalty': -50,
    'placement_rewards': {
        'top': 10,
        'middle': 20,
        'bottom': 30
    }
}
