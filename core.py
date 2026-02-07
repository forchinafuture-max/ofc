import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = self.get_value()
    
    def get_value(self):
        if self.rank == 'A':
            return 14
        elif self.rank == 'K':
            return 13
        elif self.rank == 'Q':
            return 12
        elif self.rank == 'J':
            return 11
        else:
            return int(self.rank)
    
    def __repr__(self):
        # 使用ASCII字符代替Unicode花色符号，避免编码错误
        suit_map = {'♠': 'S', '♥': 'H', '♦': 'D', '♣': 'C'}
        ascii_suit = suit_map.get(self.suit, self.suit)
        return f"{self.rank}{ascii_suit}"

class Deck:
    def __init__(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['S', 'H', 'D', 'C']  # 使用ASCII字符代替Unicode花色符号
        self.cards = [Card(rank, suit) for rank in ranks for suit in suits]
        self.shuffle()
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self, num):
        return [self.cards.pop() for _ in range(num)]

class HandState:
    """
    手牌状态类，负责管理玩家的手牌状态并确保区域长度不变式
    """
    def __init__(self):
        self._hand = {
            'temp': [],
            'top': [],
            'middle': [],
            'bottom': []
        }
    
    def __getitem__(self, key):
        """
        获取手牌区域
        """
        return self._hand.get(key, [])
    
    def __setitem__(self, key, value):
        """
        设置手牌区域，确保区域长度不变式
        """
        if key == 'top':
            # 顶部区域最多3张牌
            if len(value) > 3:
                raise ValueError("顶部区域最多只能有3张牌")
        elif key in ['middle', 'bottom']:
            # 中部和底部区域最多5张牌
            if len(value) > 5:
                raise ValueError(f"{key}区域最多只能有5张牌")
        self._hand[key] = value
    
    def __contains__(self, key):
        """
        检查区域是否存在
        """
        return key in self._hand
    
    def get(self, key, default=None):
        """
        获取手牌区域，支持默认值
        """
        return self._hand.get(key, default)
    
    def copy(self):
        """
        复制手牌状态
        """
        new_hand = HandState()
        new_hand._hand = {
            'temp': self._hand['temp'].copy(),
            'top': self._hand['top'].copy(),
            'middle': self._hand['middle'].copy(),
            'bottom': self._hand['bottom'].copy()
        }
        return new_hand
    
    def items(self):
        """
        返回所有区域及其牌
        """
        return self._hand.items()
    
    def keys(self):
        """
        返回所有区域名称
        """
        return self._hand.keys()
    
    def values(self):
        """
        返回所有区域的牌
        """
        return self._hand.values()
    
    def pop(self, key, default=None):
        """
        弹出并返回指定区域的牌
        """
        return self._hand.pop(key, default)

class Player:
    def __init__(self, name, chips=1000):
        self.name = name
        self.chips = chips
        self.hand = HandState()
        self.bet = 0
        self.folded = False
        self.fantasy_mode = False
        self.last_top_hand = []
        self.total_score = 0  # 累计积分
    
    def place_bet(self, amount):
        if amount <= self.chips:
            self.chips -= amount
            self.bet += amount
            return True
        return False
    
    def reset_hand(self):
        # 保存上一局的完整手牌，用于范特西模式触发条件和爆牌检查
        self.last_hand = {
            'top': self.hand['top'].copy(),
            'middle': self.hand['middle'].copy(),
            'bottom': self.hand['bottom'].copy()
        }
        self.last_top_hand = self.hand['top'].copy()
        self.hand = HandState()
        self.bet = 0
        self.folded = False
        # 注意：不重置total_score，保持累计积分

class Table:
    def __init__(self):
        self.pot = 0
        self.current_bet = 0
        self.round = 0
        self.action_player = 0
        self.fantasy_mode = False
