#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试RLAIPlayer的摆牌策略
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rl_ai import RLAIPlayer

class MockGame:
    """
    模拟游戏类，用于测试摆牌策略
    """
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
        if 1 <= self.value <= 14:
            return f"{values[self.value-1]}{suits[self.suit]}"
        else:
            return f"Unknown{suits[self.suit]}"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if isinstance(other, MockCard):
            return self.value == other.value and self.suit == other.suit
        return False

def test_first_round_strategy():
    """
    测试第一轮摆牌策略
    """
    print("=== 测试第一轮摆牌策略 ===")
    
    # 创建AI玩家
    ai = RLAIPlayer("TestAI", chips=1000, skip_learning=True)
    
    # 初始化手牌
    ai.hand = {
        'top': [],
        'middle': [],
        'bottom': [],
        'temp': []
    }
    
    # 创建测试卡牌
    # 模拟一组手牌：包含不同强度的牌
    test_cards = [
        MockCard(14, 0),  # A♠
        MockCard(13, 1),  # K♥
        MockCard(12, 2),  # Q♦
        MockCard(11, 3),  # J♣
        MockCard(10, 0),  # 10♠
        MockCard(9, 1),   # 9♥
        MockCard(8, 2),   # 8♦
        MockCard(7, 3),   # 7♣
        MockCard(6, 0),   # 6♠
        MockCard(5, 1),   # 5♥
        MockCard(4, 2),   # 4♦
        MockCard(3, 3),   # 3♣
        MockCard(2, 0)    # 2♠
    ]
    
    # 设置临时牌
    ai.hand['temp'] = test_cards
    
    # 创建模拟游戏
    game = MockGame()
    
    # 执行摆牌策略
    result = ai.place_cards_strategy(game, auto_mode=True)
    
    # 打印结果
    print("\n测试结果:")
    print(f"顶部区域: {result['top']}")
    print(f"中部区域: {result['middle']}")
    print(f"底部区域: {result['bottom']}")
    
    # 检查各区域牌数
    assert len(result['top']) == 3, f"顶部区域应该有3张牌，实际有{len(result['top'])}张"
    assert len(result['middle']) == 5, f"中部区域应该有5张牌，实际有{len(result['middle'])}张"
    assert len(result['bottom']) == 5, f"底部区域应该有5张牌，实际有{len(result['bottom'])}张"
    
    print("\n第一轮摆牌策略测试通过！")

if __name__ == "__main__":
    test_first_round_strategy()
    print("\n所有测试完成！")
