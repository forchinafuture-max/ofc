"""
扑克牌组与发牌逻辑
"""

import random

class Card:
    """
    卡牌类
    """
    def __init__(self, value, suit):
        """
        初始化卡牌
        
        Args:
            value: 牌面值，2-14（A=14, K=13, Q=12, J=11, T=10）
            suit: 花色，'♠', '♥', '♦', '♣'
        """
        self.value = value
        self.suit = suit
    
    def __str__(self):
        """
        字符串表示
        """
        value_map = {
            14: 'A', 13: 'K', 12: 'Q', 11: 'J', 10: 'T'
        }
        value_str = value_map.get(self.value, str(self.value))
        return f"{value_str}{self.suit}"
    
    def __repr__(self):
        """
        官方表示
        """
        return self.__str__()
    
    def __eq__(self, other):
        """
        相等性比较
        """
        if not isinstance(other, Card):
            return False
        return self.value == other.value and self.suit == other.suit

class Deck:
    """
    牌组类
    """
    def __init__(self):
        """
        初始化牌组
        """
        self.cards = []
        self.reset()
    
    def reset(self):
        """
        重置牌组
        """
        self.cards = []
        # 生成52张牌
        suits = ['♠', '♥', '♦', '♣']
        values = range(2, 15)  # 2-14
        for suit in suits:
            for value in values:
                self.cards.append(Card(value, suit))
        self.shuffle()
    
    def shuffle(self):
        """
        洗牌
        """
        random.shuffle(self.cards)
    
    def deal(self, num):
        """
        发牌
        
        Args:
            num: 发牌数量
            
        Returns:
            卡牌列表
        """
        if num > len(self.cards):
            raise ValueError("牌组中的牌不足")
        return [self.cards.pop() for _ in range(num)]
    
    def __len__(self):
        """
        牌组大小
        """
        return len(self.cards)
