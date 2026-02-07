#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
显示10局AI对弈过程的脚本
让两个AI进行10局对弈，并详细显示每局的过程
"""

from rl_ai import RLAIPlayer
from game_logic import OFCGame
import time
import random

class ShowAIVsAI:
    def __init__(self):
        self.game = OFCGame()
        self.ai1 = None
        self.ai2 = None
        self.total_scores = {'AI Player 1': 0, 'AI Player 2': 0}
    
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
        玩一局完整的游戏（5轮），并详细显示过程
        """
        print(f"\n" + "=" * 120)
        print(f"                第 {game_number} 局AI对弈过程                ")
        print("=" * 120)
        
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
                    
                    print(f"摆牌结果:")
                    print(f"  顶部: {player.hand['top']}")
                    print(f"  中部: {player.hand['middle']}")
                    print(f"  底部: {player.hand['bottom']}")
            
            # 游戏结束
            print(f"\n" + "=" * 120)
            print(f"                第 {game_number} 局游戏结束                ")
            print("=" * 120)
            
            # 显示最终摆牌结果
            for player in self.game.players:
                print(f"\n{player.name}的最终摆牌:")
                print(f"  顶部: {player.hand['top']}")
                print(f"  中部: {player.hand['middle']}")
                print(f"  底部: {player.hand['bottom']}")
            
            # 计算并显示积分
            print(f"\n" + "-" * 80)
            print(f"              第 {game_number} 局积分统计              ")
            print("-" * 80)
            
            game_scores = {}
            try:
                if len(self.game.players) == 2:
                    player1 = self.game.players[0]
                    player2 = self.game.players[1]
                    
                    # 使用与main游戏相同的积分规则
                    player1_score = self.game.calculate_score(player1, player2)
                    # 计算player2的得分
                    player2_score = self.game.calculate_score(player2, player1)
                    
                    game_scores[player1.name] = player1_score
                    game_scores[player2.name] = player2_score
                    
                    # 显示详细积分信息
                    print(f"{player1.name} 得分: {player1_score}")
                    print(f"{player2.name} 得分: {player2_score}")
                    
                    # 更新累计积分
                    self.total_scores[player1.name] += player1_score
                    self.total_scores[player2.name] += player2_score
                    
                    # 显示各区域牌型分
                    print(f"\n各区域牌型分:")
                    for player in self.game.players:
                        top_score = self.game.calculate_hand_score(player.hand.get('top', []), 'top')
                        middle_score = self.game.calculate_hand_score(player.hand.get('middle', []), 'middle')
                        bottom_score = self.game.calculate_hand_score(player.hand.get('bottom', []), 'bottom')
                        base_score = top_score + middle_score + bottom_score
                        is_busted = self.game.check_busted(player)
                        
                        print(f"\n{player.name}:")
                        print(f"  顶部: {top_score}, 中部: {middle_score}, 底部: {bottom_score}, 总计: {base_score}")
                        if is_busted:
                            print(f"  状态: 爆牌")
                        else:
                            print(f"  状态: 正常")
            except Exception as e:
                print(f"计算积分时出错: {e}")
                for player in self.game.players:
                    game_scores[player.name] = 0
            
            # 显示累计积分
            print(f"\n" + "-" * 80)
            print(f"              累计积分统计              ")
            print("-" * 80)
            for player_name, score in self.total_scores.items():
                print(f"{player_name}: {score}")
            
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
        开始显示20局AI对弈过程
        """
        print("开始显示20局AI对弈过程...")
        print("=" * 120)
        
        # 初始化AI玩家
        self.initialize_ais()
        
        # 进行20局游戏
        for i in range(1, 21):
            self.play_one_game(i)
            # 每局之间暂停一下，让用户有时间查看
            time.sleep(2)
        
        print("\n" + "=" * 120)
        print("              20局AI对弈过程显示完成              ")
        print("=" * 120)

if __name__ == "__main__":
    # 创建并运行显示脚本
    show_play = ShowAIVsAI()
    show_play.start_showing()
