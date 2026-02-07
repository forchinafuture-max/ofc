#!/usr/bin/env python3
"""
测试游戏的基本功能是否正常
"""

from core import Card, Deck, Player
from game_logic import OFCGame
from ai_strategy import RLAIPlayer

print("测试游戏基本功能...")

# 测试卡片创建
print("\n1. 测试卡片创建:")
try:
    card = Card('A', 'S')
    print(f"成功创建卡片: {card}")
    print(f"卡片值: {card.value}")
except Exception as e:
    print(f"创建卡片失败: {e}")

# 测试牌组创建
print("\n2. 测试牌组创建:")
try:
    deck = Deck()
    print(f"成功创建牌组，共有 {len(deck.cards)} 张牌")
    print(f"第一张牌: {deck.cards[0]}")
except Exception as e:
    print(f"创建牌组失败: {e}")

# 测试玩家创建
print("\n3. 测试玩家创建:")
try:
    player = Player("测试玩家")
    print(f"成功创建玩家: {player.name}")
    print(f"玩家初始筹码: {player.chips}")
except Exception as e:
    print(f"创建玩家失败: {e}")

# 测试AI玩家创建
print("\n4. 测试AI玩家创建:")
try:
    ai_player = RLAIPlayer("测试AI")
    print(f"成功创建AI玩家: {ai_player.name}")
except Exception as e:
    print(f"创建AI玩家失败: {e}")

# 测试游戏创建
print("\n5. 测试游戏创建:")
try:
    game = OFCGame()
    print(f"成功创建游戏")
    print(f"游戏牌组大小: {len(game.deck.cards)}")
except Exception as e:
    print(f"创建游戏失败: {e}")

print("\n测试完成！")
