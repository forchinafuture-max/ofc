#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试奖励函数修改的脚本
"""

from rl_ai import RLAIPlayer
from game_logic import OFCGame
import time

class TestModification:
    def __init__(self, num_games=5):
        self.game = OFCGame()
        self.ai1 = None
        self.ai2 = None
        self.num_games = num_games
    
    def initialize_ais(self):
        """
        初始化两个AI玩家
        """
        print(f"初始化AI玩家，准备测试{self.num_games}局对战...")
        # 创建两个AI玩家，设置skip_learning=True以跳过初始JSON学习
        self.ai1 = RLAIPlayer("AI Player 1", skip_learning=True)
        self.ai2 = RLAIPlayer("AI Player 2", skip_learning=True)
        
        # 添加玩家到游戏
        self.game.add_player(self.ai1)
        self.game.add_player(self.ai2)
        print("AI玩家初始化完成！")
    
    def reset_game(self):
        """
        重置游戏状态
        """
        # 清空游戏中的玩家列表
        self.game.players = []
        
        # 重置AI玩家的手牌和分数
        self.ai1.hand = {'temp': [], 'top': [], 'middle': [], 'bottom': []}
        self.ai2.hand = {'temp': [], 'top': [], 'middle': [], 'bottom': []}
        self.ai1.total_score = 0
        self.ai2.total_score = 0
        
        # 重新添加玩家到游戏
        self.game.add_player(self.ai1)
        self.game.add_player(self.ai2)
    
    def play_one_game(self, game_number):
        """
        玩一局完整的游戏（5轮），并详细显示第一轮的摆牌情况
        """
        print(f"\n" + "=" * 100)
        print(f"                第 {game_number} 局测试对战                ")
        print("=" * 100)
        
        try:
            # 重置游戏状态
            self.reset_game()
            
            # 开始游戏
            self.game.start_game()
            
            # 进行五轮游戏
            for round_num in range(1, 6):
                print(f"\n" + "-" * 80)
                print(f"              第 {round_num} 轮发牌              ")
                print("-" * 80)
                
                # 设置当前轮次
                self.game.table.round = round_num
                
                # 发牌
                self.game.deal_round()
                
                # 让两个AI玩家进行摆牌
                for player in self.game.players:
                    print(f"\n{player.name}的摆牌过程:")
                    print(f"拿到的牌: {player.hand['temp']}")
                    
                    # 使用place_cards_strategy方法摆牌
                    player.place_cards_strategy(self.game, auto_mode=True)
                    
                    # 显示摆牌结果
                    print(f"摆牌结果:")
                    print(f"  顶部: {player.hand['top']}")
                    print(f"  中部: {player.hand['middle']}")
                    print(f"  底部: {player.hand['bottom']}")
            
            # 保存游戏记录
            self.game.save_game_record()
            
            # 两个AI都从游戏中学习
            self.ai1.learn_from_game(self.game, self.ai2, ask_for_stats=False)
            self.ai2.learn_from_game(self.game, self.ai1, ask_for_stats=False)
            
            print(f"\n第 {game_number} 局测试完成！")
            return True
        except Exception as e:
            print(f"游戏过程中出错: {e}")
            return False
    
    def start_testing(self):
        """
        开始测试
        """
        print(f"开始测试奖励函数修改，运行{self.num_games}局对战...")
        print("=" * 100)
        
        # 初始化AI玩家
        self.initialize_ais()
        
        # 记录开始时间
        start_time = time.time()
        
        # 进行测试
        successful_games = 0
        for i in range(1, self.num_games + 1):
            success = self.play_one_game(i)
            if success:
                successful_games += 1
        
        # 记录结束时间
        end_time = time.time()
        total_time = end_time - start_time
        
        # 显示最终统计信息
        print("\n" + "=" * 100)
        print(f"测试完成！")
        print(f"总测试局数: {self.num_games}局")
        print(f"成功完成: {successful_games}局")
        print(f"总耗时: {total_time:.2f}秒")
        print(f"平均每局耗时: {total_time / self.num_games:.2f}秒")
        print("=" * 100)

if __name__ == "__main__":
    # 创建并运行测试脚本，默认运行5局
    test_mod = TestModification(num_games=5)
    test_mod.start_testing()
