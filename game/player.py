"""
玩家类（Human/AI），持有 HandState
"""

from core.hand_state import HandState

class Player:
    """
    玩家类
    """
    def __init__(self, name):
        """
        初始化玩家
        
        Args:
            name: 玩家名称
        """
        self.name = name
        self.hand = HandState()  # 使用HandState管理手牌
        self.folded = False  # 是否弃牌
        self.fantasy_mode = False
        self.fantasy_cards = 13  # 默认发13张牌
        self.last_top_hand = []  # 上一局的顶部手牌
        self.last_hand = None  # 上一局的完整手牌
        self.total_score = 0  # 累计积分
    
    def add_card(self, card, region='temp'):
        """
        添加卡牌到指定区域
        
        Args:
            card: 卡牌对象
            region: 区域名称，默认为'temp'
        """
        current_cards = self.hand[region].copy()
        current_cards.append(card)
        self.hand[region] = current_cards
    
    def remove_card(self, card, region='temp'):
        """
        从指定区域移除卡牌
        
        Args:
            card: 卡牌对象
            region: 区域名称，默认为'temp'
        """
        current_cards = self.hand[region].copy()
        if card in current_cards:
            current_cards.remove(card)
            self.hand[region] = current_cards
    
    def move_card(self, card, from_region, to_region):
        """
        移动卡牌从一个区域到另一个区域
        
        Args:
            card: 卡牌对象
            from_region: 源区域
            to_region: 目标区域
        """
        self.remove_card(card, from_region)
        self.add_card(card, to_region)
    
    def clear_hand(self):
        """
        清空手牌
        """
        self.hand.clear()
    
    def save_last_hand(self):
        """
        保存上一局的手牌
        """
        self.last_top_hand = self.hand['top'].copy()
        self.last_hand = {
            'top': self.hand['top'].copy(),
            'middle': self.hand['middle'].copy(),
            'bottom': self.hand['bottom'].copy()
        }
    
    def __str__(self):
        """
        字符串表示
        """
        return f"Player({self.name})"
    
    def __repr__(self):
        """
        官方表示
        """
        return self.__str__()
