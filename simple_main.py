#!/usr/bin/env python3
"""
简化版的游戏启动脚本
"""

from core import Card, Deck, Player
from game_logic import OFCGame
from ai_strategy import RLAIPlayer
from ui import GameUI

print("=======================================")
print("             OFC 扑克游戏              ")
print("=======================================")
print("正在启动游戏...")

# 创建游戏
print("\n1. 创建游戏...")
game = OFCGame()
ui = GameUI()

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

# 玩家摆牌
print("\n5. 玩家摆牌...")
if player.hand['temp']:
    ui.place_cards(player, game)

# AI摆牌
print("\n6. AI摆牌...")
if ai_player.hand['temp']:
    ui.ai_place_cards(ai_player, game, None)

# 显示最终手牌
print("\n7. 最终手牌:")
print(f"玩家a的手牌:")
print(f"顶部: {player.hand['top']}")
print(f"中部: {player.hand['middle']}")
print(f"底部: {player.hand['bottom']}")

print(f"\nAI的手牌:")
print(f"顶部: {ai_player.hand['top']}")
print(f"中部: {ai_player.hand['middle']}")
print(f"底部: {ai_player.hand['bottom']}")

print("\n=======================================")
print("游戏测试完成！")
print("=======================================")
