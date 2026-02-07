#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
让AI从JSON游戏记录中学习
"""

from rl_ai import RLAIPlayer

if __name__ == "__main__":
    print("开始让AI从JSON游戏记录中学习...")
    print("=" * 80)
    
    # 创建AI玩家实例，设置skip_learning=False以确保从JSON文件中学习
    ai_player = RLAIPlayer("Learning AI", skip_learning=False)
    
    print("\n" + "=" * 80)
    print("AI学习完成！")
    print("AI现在已经从所有JSON游戏记录中学习了摆牌策略")
    print("包括优先级目录中的高得分文件")
