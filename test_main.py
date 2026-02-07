#!/usr/bin/env python3
"""
测试main.py的运行状态
"""

import sys
import traceback

print("Python版本:", sys.version)
print("当前目录:", sys.path[0])

print("\n1. 测试导入OFCGameManager...")
try:
    from main import OFCGameManager
    print("✅ 导入OFCGameManager成功")
except Exception as e:
    print(f"❌ 导入失败: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n2. 测试创建OFCGameManager实例...")
try:
    game_manager = OFCGameManager()
    print("✅ 创建实例成功")
except Exception as e:
    print(f"❌ 创建实例失败: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n3. 测试游戏设置...")
try:
    game_manager.setup_game()
    print("✅ 游戏设置成功")
    print(f"   玩家1: {game_manager.player.name}")
    print(f"   玩家2: {game_manager.ai_player.name}")
except Exception as e:
    print(f"❌ 游戏设置失败: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n✅ 所有测试通过，游戏可以正常运行")
print("=======================================")
print("现在尝试运行游戏主循环...")
print("=======================================")

try:
    game_manager.play_game()
except Exception as e:
    print(f"❌ 游戏运行失败: {e}")
    traceback.print_exc()
    sys.exit(1)
