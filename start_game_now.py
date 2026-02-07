#!/usr/bin/env python3
"""
跳过学习阶段，直接启动游戏
"""

import sys
import traceback
from main import OFCGameManager

print("=======================================")
print("          启动OFC扑克游戏          ")
print("=======================================")
print("正在初始化游戏...")

# 快速启动游戏
try:
    # 创建游戏管理器
    game_manager = OFCGameManager()
    print("[成功] 游戏管理器创建成功")
    
    # 设置游戏
    game_manager.setup_game()
    print("[成功] 游戏设置成功")
    print(f"   玩家1: {game_manager.player.name}")
    print(f"   玩家2: {game_manager.ai_player.name}")
    
    # 跳过学习，直接开始游戏主循环
    print("\n=======================================")
    print("跳过学习阶段，直接开始游戏")
    print("=======================================")
    print("游戏已成功启动！")
    print("现在开始游戏主循环...")
    print("=======================================")
    
    # 开始游戏主循环
    game_manager.play_game()
    
except Exception as e:
    print(f"[错误] 游戏运行失败: {e}")
    traceback.print_exc()
    sys.exit(1)
