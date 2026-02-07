"""
测试游戏初始化是否正常
"""

from game.ofc_game import OFCGame
from game.player import Player
from ai.ai_player import AIPlayer

print("测试游戏初始化...")

# 创建游戏
game = OFCGame()
print("✓ 游戏创建成功")

# 创建玩家
player = Player("玩家a")
ai_player = AIPlayer("AI", strategy_type="heuristic")
print("✓ 玩家创建成功")

# 添加玩家到游戏
game.add_player(player)
game.add_player(ai_player)
print("✓ 玩家添加成功")

# 开始游戏
game.start_game()
print("✓ 游戏开始成功")

# 检查玩家手牌
print(f"玩家a手牌数量: {len(player.hand['temp'])}")
print(f"AI手牌数量: {len(ai_player.hand['temp'])}")

print("测试完成，游戏初始化正常！")
