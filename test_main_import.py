#!/usr/bin/env python3
"""
测试main.py的导入和初始化
"""

print("测试main.py的导入和初始化...")

# 测试导入
try:
    from core import Player
    from game_logic import OFCGame
    from ai_strategy import AIPlayer, AIStrategy, RLAIPlayer
    from ui import GameUI
    from fantasy_mode import FantasyModeManager
    # 从main.py导入OFCGameManager
    from main import OFCGameManager
    print("✅ 所有模块导入成功")
except Exception as e:
    print(f"❌ 导入失败: {e}")

# 测试游戏管理器初始化
try:
    print("\n测试游戏管理器初始化...")
    game_manager = OFCGameManager()
    print("✅ 游戏管理器初始化成功")
    
except Exception as e:
    print(f"❌ 游戏管理器初始化失败: {e}")

# 测试游戏设置
try:
    print("\n测试游戏设置...")
    game_manager.setup_game()
    print("✅ 游戏设置成功")
    print(f"玩家1: {game_manager.player.name}")
    print(f"玩家2: {game_manager.ai_player.name}")
except Exception as e:
    print(f"❌ 游戏设置失败: {e}")

print("\n测试完成！")
