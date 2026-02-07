#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI自我博弈训练脚本
让两个AI玩家相互对弈10000局，每局结束后都从游戏中学习
"""

from rl_ai import RLAIPlayer
from game_logic import OFCGame
from core import Player
import time

class AISelfPlay:
    def __init__(self, rounds=10000):
        self.rounds = rounds
        self.game = OFCGame()
        self.ai1 = None
        self.ai2 = None
    
    def initialize_ais(self):
        """
        初始化两个AI玩家
        """
        print("初始化AI玩家...")
        # 创建两个AI玩家，设置skip_learning=True以跳过初始JSON学习
        # 因为我们已经在之前的步骤中让AI学习过了
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
    
    def play_one_game(self):
        """
        玩一局完整的游戏（5轮）
        """
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
                    if hasattr(player, 'get_actions') and hasattr(player, 'rl_agent'):
                        # 获取当前状态
                        state = player.rl_agent.get_state(self.game, player)
                        
                        # 获取可用动作
                        actions = player.rl_agent.get_actions(player)
                        
                        # 选择动作（这里使用随机选择，实际应该使用AI的策略）
                        if actions:
                            import random
                            action = random.choice(actions)
                            
                            # 执行动作
                            new_state, reward, done = player.rl_agent.step(self.game, player, action)
            
            # 模拟游戏结束，保存游戏记录
            self.game.save_game_record()
            
            # 两个AI都从游戏中学习
            self.ai1.learn_from_game(self.game, self.ai2)
            self.ai2.learn_from_game(self.game, self.ai1)
            
            return True
        except Exception as e:
            print(f"游戏过程中出错: {e}")
            return False
    
    def start_training(self):
        """
        开始自我博弈训练
        """
        print(f"开始AI自我博弈训练，共{self.rounds}局")
        print("=" * 80)
        
        # 初始化AI玩家
        self.initialize_ais()
        
        # 记录开始时间
        start_time = time.time()
        successful_games = 0
        failed_games = 0
        
        # 开始对弈
        for i in range(1, self.rounds + 1):
            if i % 100 == 0:
                # 每100局显示一次进度
                elapsed_time = time.time() - start_time
                games_per_minute = (i / elapsed_time) * 60
                print(f"\n=== 第{i}/{self.rounds}局对弈 ({successful_games}成功, {failed_games}失败) ===")
                print(f"当前速度: {games_per_minute:.2f}局/分钟")
                print(f"预计剩余时间: {(self.rounds - i) / games_per_minute:.2f}分钟")
                
                # 每500局保存一次学习数据
                if i % 500 == 0:
                    print("保存学习数据...")
                    self.ai1.save_learning_data()
                    self.ai2.save_learning_data()
            
            # 玩一局游戏
            if self.play_one_game():
                successful_games += 1
            else:
                failed_games += 1
        
        # 训练完成
        elapsed_time = time.time() - start_time
        print("\n" + "=" * 80)
        print(f"AI自我博弈训练完成！")
        print(f"总对局数: {self.rounds}")
        print(f"成功对局: {successful_games}")
        print(f"失败对局: {failed_games}")
        print(f"总耗时: {elapsed_time:.2f}秒")
        print(f"平均速度: {(self.rounds / elapsed_time) * 60:.2f}局/分钟")
        
        # 最终保存学习数据
        print("保存最终学习数据...")
        self.ai1.save_learning_data()
        self.ai2.save_learning_data()
        print("学习数据保存完成！")

if __name__ == "__main__":
    # 创建并运行自我博弈训练
    trainer = AISelfPlay(rounds=10000)
    trainer.start_training()
