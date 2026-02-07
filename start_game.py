#!/usr/bin/env python3
"""
启动游戏并显示详细运行状态
"""

import sys
import traceback

print("=======================================")
print("          启动OFC扑克游戏          ")
print("=======================================")
print("正在初始化游戏...")

# 测试导入
try:
    from main import OFCGameManager
    print("✅ 成功导入OFCGameManager")
except Exception as e:
    print(f"❌ 导入失败: {e}")
    traceback.print_exc()
    sys.exit(1)

# 启动游戏
try:
    print("\n1. 创建游戏管理器...")
    game_manager = OFCGameManager()
    print("✅ 游戏管理器创建成功")
    
    print("\n2. 设置游戏...")
    game_manager.setup_game()
    print("✅ 游戏设置成功")
    print(f"   玩家1: {game_manager.player.name}")
    print(f"   玩家2: {game_manager.ai_player.name}")
    
    print("\n3. 开始游戏...")
    print("=======================================")
    print("游戏已成功启动！")
    print("现在开始游戏主循环...")
    print("=======================================")
    
    # 开始游戏主循环
    game_manager.play_game()
    
except Exception as e:
    print(f"❌ 游戏运行失败: {e}")
    traceback.print_exc()
    sys.exit(1)
