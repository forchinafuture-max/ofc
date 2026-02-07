#!/usr/bin/env python3
"""
测试游戏的初始化和发牌，不涉及用户输入
"""

from core import Card, Deck, Player
from game_logic import OFCGame
from ai_strategy import RLAIPlayer

print("=======================================")
print("             OFC 扑克游戏              ")
print("=======================================")
print("正在测试游戏初始化和发牌...")

# 创建游戏
print("\n1. 创建游戏...")
game = OFCGame()

# 创建玩家
print("2. 创建玩家...")
player = Player("玩家a", 1000)
ai_player = RLAIPlayer("AI (中等)")

# 添加玩家到游戏
game.add_player(player)
game.add_player(ai_player)

print(f"\n玩家列表:")
print(f"- {player.name} (筹码: {player.chips})")
print(f"- {ai_player.name}")

# 开始游戏
print("\n3. 开始游戏...")
game.start_game()
print(f"游戏已开始，当前轮次: {game.table.round}")

# 发第一轮牌
print("\n4. 发第一轮牌...")
game.table.round = 1
game.deal_round()

print(f"玩家a的手牌: {player.hand['temp']}")
print(f"AI的手牌: {ai_player.hand['temp']}")

# 测试AI摆牌
print("\n5. 测试AI摆牌...")
if ai_player.hand['temp']:
    print("AI开始摆牌...")
    # 使用强化学习策略摆牌，自动模式
    result = ai_player.place_cards_strategy(game, auto_mode=True)
    print("AI摆牌完成！")
    print(f"顶部区域: {result['top']}")
    print(f"中部区域: {result['middle']}")
    print(f"底部区域: {result['bottom']}")

print("\n=======================================")
print("测试完成！")
print("游戏初始化和发牌正常工作。")
print("=======================================")
