#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试RLAIPlayer的对战功能
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

class MockPlayer:
    """
    模拟玩家类
    """
    def __init__(self, name, chips=1000):
        self.name = name
        self.chips = chips
        self.hand = {
            'top': [],
            'middle': [],
            'bottom': [],
            'temp': []
        }
    
    def place_cards_strategy(self, game, auto_mode=False):
        """
        简单的摆牌策略
        """
        temp_cards = self.hand['temp'].copy()
        
        # 随机摆牌
        while temp_cards:
            card = temp_cards.pop()
            # 随机选择一个区域
            area = random.choice(['top', 'middle', 'bottom'])
            # 检查区域是否已满
            if len(self.hand[area]) < (3 if area == 'top' else 5):
                self.hand[area].append(card)
        
        self.hand['temp'] = []
        return {
            'top': self.hand['top'],
            'middle': self.hand['middle'],
            'bottom': self.hand['bottom']
        }

class MockGame:
    """
    模拟游戏类，用于测试对战
    """
    def __init__(self):
        self.players = []
        self.deck = []
        self.current_round = 0
        self.max_rounds = 3
    
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
            # 每轮发5张牌
            cards_to_deal = 5 if self.current_round < 3 else 3
            dealt_cards = []
            for _ in range(cards_to_deal):
                if self.deck:
                    dealt_cards.append(self.deck.pop())
            
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
        
        if len(top) < 3 or len(middle) < 5 or len(bottom) < 5:
            return True
        
        top_strength = self.evaluate_hand(top)
        middle_strength = self.evaluate_hand(middle)
        bottom_strength = self.evaluate_hand(bottom)
        
        return not (top_strength <= middle_strength <= bottom_strength)
    
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
        print("=== 开始对战测试 ===")
        
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
        for player in self.players:
            print(f"{player.name} 的最终手牌:")
            print(f"顶部: {player.hand['top']} (强度: {self.evaluate_hand(player.hand['top'])})")
            print(f"中部: {player.hand['middle']} (强度: {self.evaluate_hand(player.hand['middle'])})")
            print(f"底部: {player.hand['bottom']} (强度: {self.evaluate_hand(player.hand['bottom'])})")
            
            # 检查是否爆牌
            if self.check_busted(player):
                print(f"{player.name} 爆牌！")
            else:
                print(f"{player.name} 未爆牌")
        
        print("=== 对战测试完成 ===")

def test_battle():
    """
    测试对战
    """
    print("=== 测试RLAIPlayer对战功能 ===")
    
    # 创建游戏
    game = MockGame()
    
    # 创建RLAIPlayer
    rl_ai = RLAIPlayer("RLAI", chips=1000, skip_learning=True)
    
    # 创建模拟玩家
    mock_player = MockPlayer("MockPlayer", chips=1000)
    
    # 添加玩家到游戏
    game.add_player(rl_ai)
    game.add_player(mock_player)
    
    # 开始游戏
    game.play_game()

if __name__ == "__main__":
    test_battle()
