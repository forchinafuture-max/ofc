"""
AI 评估函数，用于启发式策略与 MCTS 共享
"""

from config.loader import config_loader


def evaluate_player_state(player, game):
    """
    评估玩家当前状态，兼容未完成摆牌的阶段
    """
    rule_engine = game.rule_engine
    top_cards = player.hand.get('top', [])
    middle_cards = player.hand.get('middle', [])
    bottom_cards = player.hand.get('bottom', [])

    top_len = config_loader.get_region_length('top')
    middle_len = config_loader.get_region_length('middle')
    bottom_len = config_loader.get_region_length('bottom')

    is_complete = (
        len(top_cards) >= top_len
        and len(middle_cards) >= middle_len
        and len(bottom_cards) >= bottom_len
    )

    if is_complete:
        if rule_engine.check_busted(player):
            return config_loader.get_reward_config('bust_penalty')
        total_score = game.calculate_total_score(player)
        fantasy_bonus = 0
        if getattr(player, 'fantasy_mode', False):
            fantasy_bonus = config_loader.get_reward_config('fantasy_bonus')
        return total_score + fantasy_bonus

    value = 0.0
    value += _evaluate_partial_region(rule_engine, top_cards, 'top', 0.6)
    value += _evaluate_partial_region(rule_engine, middle_cards, 'middle', 0.9)
    value += _evaluate_partial_region(rule_engine, bottom_cards, 'bottom', 1.2)

    if len(top_cards) >= top_len and len(middle_cards) >= middle_len:
        if rule_engine.compare_hands(top_cards, middle_cards) > 0:
            value += config_loader.get_reward_config('bust_penalty') * 0.2

    if len(middle_cards) >= middle_len and len(bottom_cards) >= bottom_len:
        if rule_engine.compare_hands(middle_cards, bottom_cards) > 0:
            value += config_loader.get_reward_config('bust_penalty') * 0.2

    value += _high_card_bonus(top_cards) * 0.05
    value += _high_card_bonus(middle_cards) * 0.03
    value += _high_card_bonus(bottom_cards) * 0.02

    return value


def _evaluate_partial_region(rule_engine, cards, region, scale):
    if not cards:
        return 0.0

    if region == 'top' and len(cards) >= 2:
        score = rule_engine.calculate_hand_score(cards, region)
        if score:
            return score * scale

    if region in ('middle', 'bottom') and len(cards) >= 3:
        score = rule_engine.calculate_hand_score(cards, region)
        if score:
            return score * scale

    rank_counts = {}
    for card in cards:
        rank_counts[card.value] = rank_counts.get(card.value, 0) + 1

    pairs = [rank for rank, count in rank_counts.items() if count == 2]
    trips = [rank for rank, count in rank_counts.items() if count >= 3]

    value = 0.0
    if trips:
        value += max(trips) * 1.5
    if pairs:
        value += max(pairs) * 0.8

    return value * scale


def _high_card_bonus(cards):
    if not cards:
        return 0
    return sum(card.value for card in cards)
