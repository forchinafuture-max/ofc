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

class Player:
    def __init__(self, name, chips=1000):
        self.name = name
        self.chips = chips
        self.hand = {'temp': [], 'top': [], 'middle': [], 'bottom': []}
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
        self.hand = {'temp': [], 'top': [], 'middle': [], 'bottom': []}
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
