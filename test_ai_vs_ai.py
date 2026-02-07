#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试两个RLAIPlayer之间的对战
"""

import sys
import os
import random

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rl_ai import RLAIPlayer

class MockCard:
    """
    模拟卡牌类
    """
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    
    def __str__(self):
        suits = ['♠', '♥', '♦', '♣']
        values = ['', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        # 确保value在有效范围内
        if 2 <= self.value <= 14:
            return f"{values[self.value-1]}{suits[self.suit]}"
        else:
            return f"Unknown{suits[self.suit]}"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if isinstance(other, MockCard):
            return self.value == other.value and self.suit == other.suit
        return False

class MockGame:
    """
    模拟游戏类，用于测试对战
    """
    def __init__(self):
        self.players = []
        self.deck = []
        self.current_round = 0
        self.max_rounds = 5
    
    def initialize_deck(self):
        """
        初始化牌组
        """
        self.deck = []
        for suit in range(4):
            for value in range(2, 15):
                self.deck.append(MockCard(value, suit))
        random.shuffle(self.deck)
    
    def add_player(self, player):
        """
        添加玩家
        """
        self.players.append(player)
    
    def deal_cards(self):
        """
        发牌
        """
        self.current_round += 1
        print(f"\n=== 第 {self.current_round} 轮发牌 ===")
        
        for player in self.players:
            # 第一轮发5张牌，第2-5轮发3张牌丢1张牌
            if self.current_round == 1:
                cards_to_deal = 5
                dealt_cards = []
                for _ in range(cards_to_deal):
                    if self.deck:
                        dealt_cards.append(self.deck.pop())
                player.hand['temp'] = dealt_cards
                print(f"{player.name} 获得 {len(dealt_cards)} 张牌: {dealt_cards}")
            elif 2 <= self.current_round <= 5:
                # 第2-5轮发3张牌丢1张牌
                total_cards = 3
                dealt_cards = []
                for _ in range(total_cards):
                    if self.deck:
                        dealt_cards.append(self.deck.pop())
                
                if len(dealt_cards) >= 3:
                    # 将3张牌都放入temp，让AI通过MCTS选择要丢弃的牌
                    player.hand['temp'] = dealt_cards
                    print(f"{player.name} 获得 3 张牌: {dealt_cards}")
                    print(f"{player.name} 需要选择丢弃 1 张牌")
                else:
                    player.hand['temp'] = dealt_cards
                    print(f"{player.name} 获得 {len(dealt_cards)} 张牌: {dealt_cards}")
    
    def evaluate_hand(self, cards):
        """
        模拟评估手牌强度
        """
        if not cards:
            return 0
        
        # 简单的强度计算：基于牌值总和
        total_value = sum(card.value for card in cards)
        return total_value
    
    def check_busted(self, player):
        """
        模拟检查是否爆牌
        """
        top = player.hand.get('top', [])
        middle = player.hand.get('middle', [])
        bottom = player.hand.get('bottom', [])
        
        # 只检查牌数是否正确
        if len(top) < 3 or len(middle) < 5 or len(bottom) < 5:
            return True
        
        return False
    
    def play_round(self):
        """
        玩一轮游戏
        """
        # 发牌
        self.deal_cards()
        
        # 玩家摆牌
        for player in self.players:
            print(f"\n{player.name} 开始摆牌:")
            player.place_cards_strategy(self, auto_mode=True)
            
            # 显示摆牌结果
            print(f"{player.name} 的摆牌结果:")
            print(f"顶部: {player.hand['top']}")
            print(f"中部: {player.hand['middle']}")
            print(f"底部: {player.hand['bottom']}")
    
    def play_game(self):
        """
        玩完整游戏
        """
        print("=== 开始AI对战测试 ===")
        
        # 初始化牌组
        self.initialize_deck()
        print(f"牌组已初始化，共 {len(self.deck)} 张牌")
        
        # 进行3轮游戏
        for _ in range(self.max_rounds):
            if not self.deck:
                print("牌组已用完，游戏结束")
                break
            
            self.play_round()
        
        # 游戏结束，显示结果
        print("\n=== 游戏结束 ===")
        
        # 计算本局积分
        game_scores = {}
        for player in self.players:
            print(f"{player.name} 的最终手牌:")
            print(f"顶部: {player.hand['top']}")
            print(f"中部: {player.hand['middle']}")
            print(f"底部: {player.hand['bottom']}")
            
            # 检查是否爆牌
            if self.check_busted(player):
                print(f"{player.name} 爆牌！")
                game_scores[player.name] = 0
            else:
                print(f"{player.name} 未爆牌")
                # 计算积分：基于牌型强度总和
                total_strength = self.evaluate_hand(player.hand['top']) + self.evaluate_hand(player.hand['middle']) + self.evaluate_hand(player.hand['bottom'])
                game_scores[player.name] = total_strength
        
        # 比较两个AI的表现
        if len(self.players) == 2:
            ai1 = self.players[0]
            ai2 = self.players[1]
            
            ai1_busted = self.check_busted(ai1)
            ai2_busted = self.check_busted(ai2)
            
            # 显示本局积分
            print(f"\n本局积分:")
            print(f"{ai1.name}: {game_scores.get(ai1.name, 0)}")
            print(f"{ai2.name}: {game_scores.get(ai2.name, 0)}")
            
            if ai1_busted and not ai2_busted:
                print(f"\n{ai2.name} 获胜！")
            elif not ai1_busted and ai2_busted:
                print(f"\n{ai1.name} 获胜！")
            elif not ai1_busted and not ai2_busted:
                # 比较总积分
                ai1_total = game_scores.get(ai1.name, 0)
                ai2_total = game_scores.get(ai2.name, 0)
                
                if ai1_total > ai2_total:
                    print(f"\n{ai1.name} 获胜！")
                elif ai2_total > ai1_total:
                    print(f"\n{ai2.name} 获胜！")
                else:
                    print("\n平局！")
            else:
                print("\n双方都爆牌，平局！")
        
        print("=== AI对战测试完成 ===")

def test_ai_vs_ai():
    """
    测试两个AI之间的对战
    """
    print("=== 测试RLAIPlayer vs RLAIPlayer对战功能 ===")
    print("连续运行10局游戏...")
    
    # 统计数据
    stats = {
        'total_games': 10,
        'ai1_wins': 0,
        'ai2_wins': 0,
        'draws': 0,
        'ai1_total_score': 0,
        'ai2_total_score': 0
    }
    
    for game_num in range(1, 11):
        print(f"\n\n=== 第 {game_num} 局游戏 ===")
        
        # 创建游戏
        game = MockGame()
        
        # 创建第一个RLAIPlayer
        ai1 = RLAIPlayer("AI_Player_1", chips=1000, skip_learning=True)
        
        # 创建第二个RLAIPlayer
        ai2 = RLAIPlayer("AI_Player_2", chips=1000, skip_learning=True)
        
        # 添加玩家到游戏
        game.add_player(ai1)
        game.add_player(ai2)
        
        # 开始游戏
        game.play_game()
        
        # 统计胜负和积分
        ai1_busted = game.check_busted(ai1)
        ai2_busted = game.check_busted(ai2)
        
        # 计算本局积分
        if ai1_busted:
            ai1_score = 0
        else:
            ai1_score = game.evaluate_hand(ai1.hand['top']) + game.evaluate_hand(ai1.hand['middle']) + game.evaluate_hand(ai1.hand['bottom'])
        
        if ai2_busted:
            ai2_score = 0
        else:
            ai2_score = game.evaluate_hand(ai2.hand['top']) + game.evaluate_hand(ai2.hand['middle']) + game.evaluate_hand(ai2.hand['bottom'])
        
        # 更新累计积分
        stats['ai1_total_score'] += ai1_score
        stats['ai2_total_score'] += ai2_score
        
        # 显示本局积分和累计积分
        print(f"\n本局积分:")
        print(f"{ai1.name}: {ai1_score}")
        print(f"{ai2.name}: {ai2_score}")
        print(f"\n累计积分:")
        print(f"{ai1.name}: {stats['ai1_total_score']}")
        print(f"{ai2.name}: {stats['ai2_total_score']}")
        
        # 统计胜负
        if ai1_busted and not ai2_busted:
            stats['ai2_wins'] += 1
        elif not ai1_busted and ai2_busted:
            stats['ai1_wins'] += 1
        elif not ai1_busted and not ai2_busted:
            if ai1_score > ai2_score:
                stats['ai1_wins'] += 1
            elif ai2_score > ai1_score:
                stats['ai2_wins'] += 1
            else:
                stats['draws'] += 1
        else:
            stats['draws'] += 1
    
    # 显示最终统计结果
    print("\n\n=== 10局对战统计结果 ===")
    print(f"总游戏数: {stats['total_games']}")
    print(f"AI_Player_1 获胜: {stats['ai1_wins']} 局 ({stats['ai1_wins']/stats['total_games']*100:.1f}%)")
    print(f"AI_Player_2 获胜: {stats['ai2_wins']} 局 ({stats['ai2_wins']/stats['total_games']*100:.1f}%)")
    print(f"平局: {stats['draws']} 局 ({stats['draws']/stats['total_games']*100:.1f}%)")
    print(f"\n累计积分:")
    print(f"AI_Player_1: {stats['ai1_total_score']}")
    print(f"AI_Player_2: {stats['ai2_total_score']}")
    
    # 显示最终获胜者
    if stats['ai1_wins'] > stats['ai2_wins']:
        print("\n=== 最终获胜者: AI_Player_1 ===")
    elif stats['ai2_wins'] > stats['ai1_wins']:
        print("\n=== 最终获胜者: AI_Player_2 ===")
    else:
        print("\n=== 最终结果: 平局 ===")
    
    print("=== 10局AI对战测试完成 ===")

if __name__ == "__main__":
    test_ai_vs_ai()
