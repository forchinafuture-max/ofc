#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行大量AI对战对局的脚本
"""

from rl_ai import RLAIPlayer
from game_logic import OFCGame
import time

class RunManyGames:
    def __init__(self, num_games=100):
        self.game = OFCGame()
        self.ai1 = None
        self.ai2 = None
        self.num_games = num_games
    
    def initialize_ais(self):
        """
        初始化两个AI玩家
        """
        print(f"初始化AI玩家，准备运行{self.num_games}局对战...")
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
        玩一局完整的游戏（5轮），简化输出
        """
        if game_number % 10 == 0:
            print(f"正在进行第 {game_number} 局游戏...")
        
        try:
            # 重置游戏状态
            self.reset_game()
            
            # 开始游戏
            self.game.start_game()
            
            # 进行五轮游戏
            for round_num in range(1, 6):
                # 设置当前轮次
                self.game.table.round = round_num
                
                # 发牌
                self.game.deal_round()
                
                # 让两个AI玩家进行摆牌
                for player in self.game.players:
                    # 使用place_cards_strategy方法摆牌，auto_mode=True
                    player.place_cards_strategy(self.game, auto_mode=True)
            
            # 保存游戏记录
            self.game.save_game_record()
            
            # 两个AI都从游戏中学习
            self.ai1.learn_from_game(self.game, self.ai2, ask_for_stats=False)
            self.ai2.learn_from_game(self.game, self.ai1, ask_for_stats=False)
            
            return True
        except Exception as e:
            print(f"游戏过程中出错: {e}")
            return False
    
    def start_running(self):
        """
        开始运行指定数量的游戏
        """
        print(f"开始运行{self.num_games}局AI对战...")
        print("=" * 80)
        
        # 初始化AI玩家
        self.initialize_ais()
        
        # 记录开始时间
        start_time = time.time()
        
        # 进行指定数量的游戏
        successful_games = 0
        for i in range(1, self.num_games + 1):
            success = self.play_one_game(i)
            if success:
                successful_games += 1
        
        # 记录结束时间
        end_time = time.time()
        total_time = end_time - start_time
        
        # 显示统计信息
        print("=" * 80)
        print(f"{self.num_games}局AI对战完成！")
        print(f"成功完成: {successful_games}局")
        print(f"总耗时: {total_time:.2f}秒")
        print(f"平均每局耗时: {total_time / self.num_games:.2f}秒")
        
        # 显示AI统计信息
        print("\n" + "=" * 80)
        print("AI Player 1 统计信息:")
        self.ai1.show_stats()
        
        print("\n" + "=" * 80)
        print("AI Player 2 统计信息:")
        self.ai2.show_stats()

if __name__ == "__main__":
    # 创建并运行脚本，默认运行100局
    run_games = RunManyGames(num_games=100)
    run_games.start_running()
