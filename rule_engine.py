from core import Card
from config.rules import (
    REGION_LENGTH_LIMITS, TOP_PAIR_SCORES, TOP_TRIPS_SCORES,
    MIDDLE_HAND_SCORES, BOTTOM_HAND_SCORES, FANTASY_MODE_CONFIG
)

class RuleEngine:
    """
    规则引擎类，负责处理OFC游戏的所有规则相关逻辑
    包括：手牌评估、爆牌判定、计分、幻想模式判断等
    """
    
    def evaluate_hand(self, cards):
        """
        评估手牌强度
        
        Args:
            cards: 手牌列表
            
        Returns:
            手牌强度值
        """
        if len(cards) == 3:
            return self.evaluate_3_card_hand(cards)
        elif len(cards) == 5:
            return self.evaluate_5_card_hand(cards)
        else:
            return 0
    
    def evaluate_3_card_hand(self, cards):
        """
        评估3张牌的手牌
        
        Args:
            cards: 3张牌的列表
            
        Returns:
            手牌强度值
        """
        if len(cards) < 3:
            return 0
        
        ranks = [card.value for card in cards]
        suits = [card.suit for card in cards]
        
        # 检查同花
        is_flush = all(suit == suits[0] for suit in suits)
        
        # 检查顺子
        ranks.sort()
        is_straight = True
        for i in range(1, len(ranks)):
            if ranks[i] != ranks[i-1] + 1:
                is_straight = False
                break
        
        # 检查A23轮子
        if not is_straight:
            # 检查是否有A
            has_ace = 14 in ranks
            # 检查是否有2和3
            has_2 = 2 in ranks
            has_3 = 3 in ranks
            
            # 如果是A23，视为顺子
            if has_ace and has_2 and has_3:
                is_straight = True
        
        # 检查牌型
        rank_counts = {}
        for rank in ranks:
            rank_counts[rank] = rank_counts.get(rank, 0) + 1
        
        counts = sorted(rank_counts.values(), reverse=True)
        
        if counts == [3]:
            return 2  # 三条
        elif counts == [2, 1]:
            return 1  # 一对
        else:
            return 0  # 高牌
    
    def evaluate_5_card_hand(self, cards):
        """
        评估5张牌的手牌
        
        Args:
            cards: 5张牌的列表
            
        Returns:
            手牌强度值
        """
        if len(cards) < 5:
            return 0
        
        ranks = [card.value for card in cards]
        suits = [card.suit for card in cards]
        
        # 检查同花
        is_flush = all(suit == suits[0] for suit in suits)
        
        # 检查顺子
        ranks.sort()
        is_straight = True
        for i in range(1, len(ranks)):
            if ranks[i] != ranks[i-1] + 1:
                is_straight = False
                break
        
        # 检查A2345轮子
        if not is_straight:
            # 检查是否有A
            has_ace = 14 in ranks
            # 检查是否有2、3、4、5
            has_2 = 2 in ranks
            has_3 = 3 in ranks
            has_4 = 4 in ranks
            has_5 = 5 in ranks
            
            # 如果是A2345，视为顺子
            if has_ace and has_2 and has_3 and has_4 and has_5:
                is_straight = True
        
        # 检查牌型
        rank_counts = {}
        for rank in ranks:
            rank_counts[rank] = rank_counts.get(rank, 0) + 1
        
        counts = sorted(rank_counts.values(), reverse=True)
        
        if is_straight and is_flush:
            # 检查皇家同花顺
            if ranks == [10, 11, 12, 13, 14]:
                return 9  # 皇家同花顺
            return 8  # 同花顺
        elif counts == [4, 1]:
            return 7  # 四条
        elif counts == [3, 2]:
            return 6  # 葫芦
        elif is_flush:
            return 5  # 同花
        elif is_straight:
            return 4  # 顺子
        elif counts == [3, 1, 1]:
            return 3  # 三条（大于两队）
        elif counts == [2, 2, 1]:
            return 2  # 两对
        elif counts == [2, 1, 1, 1]:
            return 1  # 一对
        else:
            return 0  # 高牌
    
    def compare_hands(self, hand1, hand2):
        """
        比较两手牌的大小
        
        Args:
            hand1: 第一手牌
            hand2: 第二手牌
            
        Returns:
            1: hand1 > hand2
            -1: hand1 < hand2
            0: hand1 == hand2
        """
        # 对于不同牌数的手牌，直接进行详细比较
        # 对于相同牌数的手牌，先比较强度值，再进行详细比较
        if len(hand1) != len(hand2):
            # 不同牌数的手牌，直接进行详细比较
            return self._compare_same_strength_hands(hand1, hand2)
        else:
            # 相同牌数的手牌，先比较强度值
            score1 = self.evaluate_hand(hand1)
            score2 = self.evaluate_hand(hand2)
            
            if score1 > score2:
                return 1
            elif score1 < score2:
                return -1
            else:
                # 分数相同时，根据牌型进行详细比较
                return self._compare_same_strength_hands(hand1, hand2)
    
    def _compare_same_strength_hands(self, hand1, hand2):
        """
        比较相同强度值的手牌
        
        Args:
            hand1: 第一手牌
            hand2: 第二手牌
            
        Returns:
            1: hand1 > hand2
            -1: hand1 < hand2
            0: hand1 == hand2
        """
        ranks1 = sorted([card.value for card in hand1], reverse=True)
        ranks2 = sorted([card.value for card in hand2], reverse=True)
        
        # 计算牌型的详细信息
        rank_counts1 = {}
        for rank in [card.value for card in hand1]:
            rank_counts1[rank] = rank_counts1.get(rank, 0) + 1
        
        rank_counts2 = {}
        for rank in [card.value for card in hand2]:
            rank_counts2[rank] = rank_counts2.get(rank, 0) + 1
        
        # 按出现次数排序（降序），然后按牌值排序（降序）
        sorted_ranks1 = sorted(rank_counts1.items(), key=lambda x: (-x[1], -x[0]))
        sorted_ranks2 = sorted(rank_counts2.items(), key=lambda x: (-x[1], -x[0]))
        
        # 比较排序后的结果
        for (r1, c1), (r2, c2) in zip(sorted_ranks1, sorted_ranks2):
            if r1 > r2:
                return 1
            elif r1 < r2:
                return -1
        
        # 如果还是相同，比较所有牌的大小（降序）
        for r1, r2 in zip(ranks1, ranks2):
            if r1 > r2:
                return 1
            elif r1 < r2:
                return -1
        
        return 0
    
    def check_busted(self, player):
        """
        检查玩家是否爆牌
        
        Args:
            player: 玩家对象
            
        Returns:
            bool: 是否爆牌
        """
        if len(player.hand['top']) < REGION_LENGTH_LIMITS['top'] or \
           len(player.hand['middle']) < REGION_LENGTH_LIMITS['middle'] or \
           len(player.hand['bottom']) < REGION_LENGTH_LIMITS['bottom']:
            return True
        
        # 直接使用compare_hands进行比较，避免强度尺度不一致的问题
        top_vs_middle = self.compare_hands(player.hand['top'], player.hand['middle'])
        middle_vs_bottom = self.compare_hands(player.hand['middle'], player.hand['bottom'])
        
        # 比较顶部和中部
        if top_vs_middle > 0:
            return True
        
        # 比较中部和底部
        if middle_vs_bottom > 0:
            return True
        
        return False
    
    def calculate_hand_score(self, cards, region):
        """
        计算牌型分
        
        Args:
            cards: 手牌列表
            region: 区域名称 ('top', 'middle', 'bottom')
            
        Returns:
            牌型分
        """
        score = 0
        
        if region == 'top':
            # 头道牌型分
            if len(cards) >= 2:
                # 检查对子
                ranks = [card.value for card in cards]
                rank_counts = {}
                for rank in ranks:
                    rank_counts[rank] = rank_counts.get(rank, 0) + 1
                
                # 检查对子
                pairs = [r for r, c in rank_counts.items() if c >= 2]
                if pairs:
                    high_pair = max(pairs)
                    # 头道对子牌型分
                    score = TOP_PAIR_SCORES.get(high_pair, 0)
                
                # 检查三条
                trips = [r for r, c in rank_counts.items() if c >= 3]
                if trips:
                    high_trip = max(trips)
                    # 头道三条牌型分
                    score = TOP_TRIPS_SCORES.get(high_trip, 0)
        elif region == 'middle' or region == 'bottom':
            # 中道和尾道牌型分
            if len(cards) < 5:
                return 0
            
            # 检查牌型
            ranks = [card.value for card in cards]
            suits = [card.suit for card in cards]
            
            # 检查同花
            is_flush = all(suit == suits[0] for suit in suits)
            
            # 检查顺子
            ranks.sort()
            is_straight = True
            for i in range(1, len(ranks)):
                if ranks[i] != ranks[i-1] + 1:
                    is_straight = False
                    break
            
            # 检查A2345轮子
            if not is_straight:
                # 检查是否有A
                has_ace = 14 in ranks
                # 检查是否有2、3、4、5
                has_2 = 2 in ranks
                has_3 = 3 in ranks
                has_4 = 4 in ranks
                has_5 = 5 in ranks
                
                # 如果是A2345，视为顺子
                if has_ace and has_2 and has_3 and has_4 and has_5:
                    is_straight = True
            
            # 检查牌型
            rank_counts = {}
            for rank in ranks:
                rank_counts[rank] = rank_counts.get(rank, 0) + 1
            
            counts = sorted(rank_counts.values(), reverse=True)
            
            # 根据区域选择计分表
            if region == 'middle':
                score_table = MIDDLE_HAND_SCORES
            else:
                score_table = BOTTOM_HAND_SCORES
            
            # 皇家同花顺
            if is_straight and is_flush and ranks == [10, 11, 12, 13, 14]:
                score = score_table['royal_flush']
            # 同花顺
            elif is_straight and is_flush:
                score = score_table['straight_flush']
            # 四条
            elif counts == [4, 1]:
                score = score_table['four_of_a_kind']
            # 葫芦
            elif counts == [3, 2]:
                score = score_table['full_house']
            # 同花
            elif is_flush:
                score = score_table['flush']
            # 顺子
            elif is_straight:
                score = score_table['straight']
            # 三条
            elif counts == [3, 1, 1]:
                score = score_table['three_of_a_kind']
            # 两对
            elif counts == [2, 2, 1]:
                score = score_table['two_pair']
            # 一对
            elif counts == [2, 1, 1, 1]:
                score = score_table['one_pair']
            # 高牌
            else:
                score = score_table['high_card']
        
        return score
    
    def check_fantasy_mode(self, player):
        """
        检查玩家是否进入范特西模式
        
        Args:
            player: 玩家对象
            
        Returns:
            bool: 是否进入范特西模式
        """
        # 检查玩家是否已经处于范特西模式
        if hasattr(player, 'fantasy_mode') and player.fantasy_mode:
            return True
        
        # 检查玩家上一局的手牌
        if hasattr(player, 'last_top_hand') and len(player.last_top_hand) >= 3:
            # 检查玩家上一局是否爆牌
            if hasattr(player, 'last_hand'):
                # 临时保存当前手牌
                temp_hand = player.hand.copy()
                # 使用上一局的手牌检查是否爆牌
                player.hand = player.last_hand
                if self.check_busted(player):
                    # 爆牌玩家不能触发范特西模式
                    player.fantasy_mode = False
                    # 恢复当前手牌
                    player.hand = temp_hand
                    return False
                # 恢复当前手牌
                player.hand = temp_hand
            
            # 根据顶部牌型决定发牌数量
            top_cards = player.last_top_hand
            # 计算顶部牌型的强度
            rank_counts = {}
            for card in top_cards:
                rank_counts[card.value] = rank_counts.get(card.value, 0) + 1
            pairs = [r for r, c in rank_counts.items() if c >= 2]
            
            if pairs:
                # 检查是否有三条或以上
                trips = [r for r, c in rank_counts.items() if c >= 3]
                if trips:
                    # 三条或以上，发17张牌
                    player.fantasy_cards = FANTASY_MODE_CONFIG['cards_by_top_hand']['trips']
                    player.fantasy_mode = True
                    return True
                else:
                    high_pair = max(pairs)
                    # 根据对子大小决定发牌数量
                    if high_pair >= 14:  # AA
                        player.fantasy_cards = FANTASY_MODE_CONFIG['cards_by_top_hand']['aa']
                        player.fantasy_mode = True
                        return True
                    elif high_pair >= 13:  # KK
                        player.fantasy_cards = FANTASY_MODE_CONFIG['cards_by_top_hand']['kk']
                        player.fantasy_mode = True
                        return True
                    elif high_pair >= 12:  # QQ
                        player.fantasy_cards = FANTASY_MODE_CONFIG['cards_by_top_hand']['qq']
                        player.fantasy_mode = True
                        return True
        
        player.fantasy_mode = False
        return False
    
    def check_fantasy_stay_condition(self, player):
        """
        检查玩家是否满足留在范特西模式的条件
        
        Args:
            player: 玩家对象
            
        Returns:
            bool: 是否满足条件
        """
        # 检查底部区域是否有4条或以上强度的牌型
        bottom_strength = self.evaluate_hand(player.hand['bottom'])
        if bottom_strength >= FANTASY_MODE_CONFIG['stay_conditions']['bottom_min_strength']:
            return True
        
        # 检查顶部区域是否有三条或以上
        top_strength = self.evaluate_hand(player.hand['top'])
        if top_strength >= FANTASY_MODE_CONFIG['stay_conditions']['top_min_strength']:
            return True
        
        return False
