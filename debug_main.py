#!/usr/bin/env python3
"""
详细测试main.py的完整流程，添加错误处理和日志
"""

import traceback

print("=======================================")
print("          调试main.py流程           ")
print("=======================================")
print("正在启动调试测试...")

# 测试导入
try:
    from core import Player
    from game_logic import OFCGame
    from ai_strategy import AIPlayer, AIStrategy, RLAIPlayer
    from ui import GameUI
    from fantasy_mode import FantasyModeManager
    from main import OFCGameManager
    print("✅ 所有模块导入成功")
except Exception as e:
    print(f"❌ 导入失败: {e}")
    traceback.print_exc()
    exit(1)

# 测试游戏运行
try:
    print("\n1. 创建游戏管理器...")
    game_manager = OFCGameManager()
    print("✅ 游戏管理器创建成功")
    
    print("\n2. 设置游戏...")
    game_manager.setup_game()
    print("✅ 游戏设置成功")
    print(f"   玩家1: {game_manager.player.name}")
    print(f"   玩家2: {game_manager.ai_player.name}")
    
    print("\n3. 开始游戏循环...")
    print("   调用play_game()方法...")
    
    # 模拟play_game的部分逻辑，添加详细日志
    print("\n   3.1 开始新游戏...")
    game_manager.game.start_game()
    print(f"      游戏已开始，当前轮次: {game_manager.game.table.round}")
    
    print("   3.2 检查范特西模式...")
    game_manager.game.check_fantasy_mode()
    has_fantasy_players = any(player.fantasy_mode for player in game_manager.game.players)
    print(f"      范特西模式: {has_fantasy_players}")
    
    if not has_fantasy_players:
        print("   3.3 第1轮：发5张牌并摆牌...")
        # 发第一轮牌
        print("      发第一轮牌...")
        game_manager.game.table.round = 1
        game_manager.game.deal_round()
        
        print(f"      玩家a的手牌: {game_manager.player.hand['temp']}")
        print(f"      AI的手牌: {game_manager.ai_player.hand['temp']}")
        
        print("   3.4 测试AI摆牌...")
        if game_manager.ai_player.hand['temp']:
            print("      AI开始摆牌...")
            # 使用强化学习策略摆牌
            result = game_manager.ai_player.place_cards_strategy(game_manager.game, auto_mode=True)
            print("      AI摆牌完成！")
            print(f"      顶部区域: {result['top']}")
            print(f"      中部区域: {result['middle']}")
            print(f"      底部区域: {result['bottom']}")
    
    print("\n✅ 游戏流程测试成功")
    print("\n=======================================")
    print("调试测试完成！")
    print("游戏的核心功能都正常工作。")
    print("\n现在尝试运行完整的游戏...")
    print("=======================================")
    
    # 尝试运行完整的游戏
    print("\n4. 运行完整游戏...")
    print("   注意：这将启动完整的游戏循环，需要用户输入")
    print("   按Ctrl+C可以退出游戏")
    
    # 直接调用run方法
    game_manager.run()
    
except KeyboardInterrupt:
    print("\n游戏已手动终止")
except Exception as e:
    print(f"❌ 游戏运行失败: {e}")
    traceback.print_exc()
