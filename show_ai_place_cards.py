#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用RLAIPlayer的实际摆牌方法显示摆牌过程
显示AI如何将牌分配到顶部、中部和底部三个区域
"""

from rl_ai import RLAIPlayer
from game_logic import OFCGame
import time

class ShowAIPlaceCards:
    def __init__(self):
        self.game = OFCGame()
        self.ai = None
    
    def initialize_ai(self):
        """
        初始化AI玩家
        """
        print("初始化AI玩家...")
        # 创建AI玩家，设置skip_learning=True以跳过初始JSON学习
        self.ai = RLAIPlayer("AI Player", skip_learning=True)
        print("AI玩家初始化完成！")
    
    def show_one_place_cards(self, game_number):
        """
        使用RLAIPlayer的实际摆牌方法显示一局游戏的摆牌过程
        """
        print(f"\n" + "=" * 120)
        print(f"                第 {game_number} 局游戏摆牌过程                ")
        print("=" * 120)
        
        # 重置游戏状态
        self.game = OFCGame()
        self.ai.hand = {'temp': [], 'top': [], 'middle': [], 'bottom': []}
        
        # 发牌给AI
        print(f"\n1. 发牌阶段:")
        print(f"-" * 80)
        
        # 第一轮发5张牌
        temp_cards = self.game.deck.deal(5)
        self.ai.hand['temp'] = temp_cards
        print(f"   AI拿到的牌: {temp_cards}")
        
        # 显示摆牌过程
        print(f"\n2. 摆牌过程:")
        print(f"-" * 80)
        print(f"   AI开始摆牌...")
        
        # 使用RLAIPlayer的实际摆牌方法
        self.ai.place_cards_strategy(self.game, auto_mode=True)
        
        # 显示摆牌结果
        print(f"\n3. 摆牌结果:")
        print(f"-" * 80)
        print(f"   顶部区域: {self.ai.hand['top']}")
        print(f"   中部区域: {self.ai.hand['middle']}")
        print(f"   底部区域: {self.ai.hand['bottom']}")
        
        # 检查是否爆牌
        busted = self.game.check_busted(self.ai)
        print(f"\n4. 爆牌检查:")
        print(f"-" * 80)
        print(f"   是否爆牌: {'是' if busted else '否'}")
    
    def start_showing(self):
        """
        开始显示5局游戏的摆牌过程
        """
        print("开始显示5局游戏的详细摆牌过程...")
        print("=" * 120)
        
        # 初始化AI玩家
        self.initialize_ai()
        
        # 显示5局游戏的摆牌过程
        for i in range(1, 6):
            self.show_one_place_cards(i)
            # 每局之间暂停一下，让用户有时间查看
            time.sleep(2)
        
        print("\n" + "=" * 120)
        print("              5局游戏摆牌过程显示完成              ")
        print("=" * 120)

if __name__ == "__main__":
    # 创建并运行显示脚本
    show_play = ShowAIPlaceCards()
    show_play.start_showing()
