"""
测试范特西模式的触发逻辑
"""

from game.player import Player
from core.rules import RuleEngine

# 创建玩家
player = Player('玩家a')

# 设置玩家的手牌（模拟上一局的结果）
# 顶部区域：AAQ（一对A，应该触发范特西模式）
player.last_top_hand = [
    type('Card', (), {'value': 14, 'suit': '♦'})(),  # A♦
    type('Card', (), {'value': 14, 'suit': '♣'})(),  # A♣
    type('Card', (), {'value': 12, 'suit': '♦'})()   # Q♦
]

# 设置完整手牌（用于爆牌检查）
hand = {
    'top': player.last_top_hand,
    'middle': [
        type('Card', (), {'value': 3, 'suit': '♥'})(),   # 3♥
        type('Card', (), {'value': 5, 'suit': '♣'})(),   # 5♣
        type('Card', (), {'value': 5, 'suit': '♥'})(),   # 5♥
        type('Card', (), {'value': 9, 'suit': '♥'})(),   # 9♥
        type('Card', (), {'value': 3, 'suit': '♠'})()    # 3♠
    ],
    'bottom': [
        type('Card', (), {'value': 10, 'suit': '♣'})(),  # T♣
        type('Card', (), {'value': 9, 'suit': '♣'})(),   # 9♣
        type('Card', (), {'value': 11, 'suit': '♦'})(),  # J♦
        type('Card', (), {'value': 7, 'suit': '♥'})(),   # 7♥
        type('Card', (), {'value': 14, 'suit': '♠'})()   # A♠
    ]
}

player.hand = hand
player.last_hand = hand

# 检查是否进入范特西模式
rule_engine = RuleEngine()
print("测试范特西模式触发逻辑...")
print(f"玩家上一局顶部手牌: AAQ (一对A)")

# 先检查爆牌情况
busted = rule_engine.check_busted(player)
print(f"爆牌检查结果: {busted}")

# 检查范特西模式
result = rule_engine.check_fantasy_mode(player)
print(f"范特西模式检查结果: {result}")
print(f'player.fantasy_mode: {getattr(player, "fantasy_mode", "未设置")}')
print(f'player.fantasy_cards: {getattr(player, "fantasy_cards", "未设置")}')

if result:
    print("✓ 成功触发范特西模式！")
else:
    print("✗ 未触发范特西模式，检查逻辑是否正确。")
