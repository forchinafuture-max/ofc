#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
显示5局AI摆牌过程的脚本
随机选择5局游戏，详细显示AI的摆牌过程
"""

from rl_ai import RLAIPlayer
from game_logic import OFCGame
import time
import random

class ShowAIPlay:
    def __init__(self):
        self.game = OFCGame()
        self.ai1 = None
        self.ai2 = None
    
    def initialize_ais(self):
        """
        初始化两个AI玩家
        """
        print("初始化AI玩家...")
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
        玩一局完整的游戏（5轮），并详细显示摆牌过程
        """
        print(f"\n" + "=" * 100)
        print(f"                第 {game_number} 局游戏开始                ")
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
                    
                    if hasattr(player, 'get_actions') and hasattr(player, 'rl_agent'):
                        # 获取当前状态
                        state = player.rl_agent.get_state(self.game, player)
                        
                        # 获取可用动作
                        actions = player.rl_agent.get_actions(player)
                        
                        # 选择动作
                        if actions:
                            # 随机选择一个动作（模拟AI的决策）
                            action = random.choice(actions)
                            print(f"选择的动作: {action}")
                            
                            # 执行动作
                            new_state, reward, done = player.rl_agent.step(self.game, player, action)
                            print(f"摆牌后状态:")
                            print(f"  顶部: {player.hand['top']}")
                            print(f"  中部: {player.hand['middle']}")
                            print(f"  底部: {player.hand['bottom']}")
                            print(f"  剩余临时牌: {player.hand['temp']}")
                        else:
                            print("没有可用动作")
            
            # 游戏结束
            print(f"\n" + "=" * 100)
            print(f"                第 {game_number} 局游戏结束                ")
            print("=" * 100)
            
            # 显示最终摆牌结果
            for player in self.game.players:
                print(f"\n{player.name}的最终摆牌:")
                print(f"  顶部: {player.hand['top']}")
                print(f"  中部: {player.hand['middle']}")
                print(f"  底部: {player.hand['bottom']}")
            
            # 保存游戏记录
            self.game.save_game_record()
            
            # 两个AI都从游戏中学习
            self.ai1.learn_from_game(self.game, self.ai2, ask_for_stats=False)
            self.ai2.learn_from_game(self.game, self.ai1, ask_for_stats=False)
            
            print(f"\n第 {game_number} 局游戏完成！")
            return True
        except Exception as e:
            print(f"游戏过程中出错: {e}")
            return False
    
    def start_showing(self):
        """
        开始显示5局AI摆牌过程
        """
        print("开始显示5局AI摆牌过程...")
        print("=" * 100)
        
        # 初始化AI玩家
        self.initialize_ais()
        
        # 进行5局游戏
        for i in range(1, 6):
            self.play_one_game(i)
            # 每局之间暂停一下，让用户有时间查看
            time.sleep(1)
        
        print("\n" + "=" * 100)
        print("              5局AI摆牌过程显示完成              ")
        print("=" * 100)

if __name__ == "__main__":
    # 创建并运行显示脚本
    show_play = ShowAIPlay()
    show_play.start_showing()
