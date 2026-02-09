"""
规则引擎：评估、比较、计分、幻想模式
"""

from game.deck import Card
from config.loader import config_loader

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

    def _hand_profile(self, cards):
        """
        计算手牌档位与比较信息

        Returns:
            dict: {
                'category': 原始牌型强度,
                'category_rank': 用于跨牌数比较的强度,
                'tiebreaker': 用于同牌型比较的权重列表
            }
        """
        if len(cards) == 3:
            return self._profile_3_card(cards)
        if len(cards) == 5:
            return self._profile_5_card(cards)
        return {'category': 0, 'category_rank': 0, 'tiebreaker': []}

    def _profile_3_card(self, cards):
        if len(cards) < 3:
            return {'category': 0, 'category_rank': 0, 'tiebreaker': []}

        ranks = [card.value for card in cards]
        rank_counts = {}
        for rank in ranks:
            rank_counts[rank] = rank_counts.get(rank, 0) + 1

        counts = sorted(rank_counts.values(), reverse=True)
        sorted_ranks = sorted(rank_counts.items(), key=lambda x: (-x[1], -x[0]))

        if counts == [3]:
            # 三条
            trip_rank = sorted_ranks[0][0]
            return {
                'category': 2,
                'category_rank': 3,
                'tiebreaker': [trip_rank],
            }
        if counts == [2, 1]:
            # 一对
            pair_rank = sorted_ranks[0][0]
            kicker = sorted([r for r, c in rank_counts.items() if c == 1], reverse=True)
            return {
                'category': 1,
                'category_rank': 1,
                'tiebreaker': [pair_rank] + kicker,
            }

        # 高牌
        high_cards = sorted(ranks, reverse=True)
        return {
            'category': 0,
            'category_rank': 0,
            'tiebreaker': high_cards,
        }

    def _profile_5_card(self, cards):
        if len(cards) < 5:
            return {'category': 0, 'category_rank': 0, 'tiebreaker': []}

        ranks = [card.value for card in cards]
        suits = [card.suit for card in cards]
        ranks_sorted = sorted(ranks)

        is_flush = all(suit == suits[0] for suit in suits)
        straight_high = self._straight_high_card(ranks_sorted)
        is_straight = straight_high is not None

        rank_counts = {}
        for rank in ranks:
            rank_counts[rank] = rank_counts.get(rank, 0) + 1

        counts = sorted(rank_counts.values(), reverse=True)
        sorted_ranks = sorted(rank_counts.items(), key=lambda x: (-x[1], -x[0]))

        # 皇家同花顺 / 同花顺
        if is_straight and is_flush:
            if straight_high == 14:
                return {
                    'category': 9,
                    'category_rank': 9,
                    'tiebreaker': [straight_high],
                }
            return {
                'category': 8,
                'category_rank': 8,
                'tiebreaker': [straight_high],
            }

        # 四条
        if counts == [4, 1]:
            four_rank = sorted_ranks[0][0]
            kicker = sorted([r for r, c in rank_counts.items() if c == 1], reverse=True)
            return {
                'category': 7,
                'category_rank': 7,
                'tiebreaker': [four_rank] + kicker,
            }

        # 葫芦
        if counts == [3, 2]:
            trip_rank = sorted_ranks[0][0]
            pair_rank = sorted_ranks[1][0]
            return {
                'category': 6,
                'category_rank': 6,
                'tiebreaker': [trip_rank, pair_rank],
            }

        # 同花
        if is_flush:
            return {
                'category': 5,
                'category_rank': 5,
                'tiebreaker': sorted(ranks, reverse=True),
            }

        # 顺子
        if is_straight:
            return {
                'category': 4,
                'category_rank': 4,
                'tiebreaker': [straight_high],
            }

        # 三条
        if counts == [3, 1, 1]:
            trip_rank = sorted_ranks[0][0]
            kickers = sorted([r for r, c in rank_counts.items() if c == 1], reverse=True)
            return {
                'category': 3,
                'category_rank': 3,
                'tiebreaker': [trip_rank] + kickers,
            }

        # 两对
        if counts == [2, 2, 1]:
            pairs = [r for r, c in sorted_ranks if c == 2]
            pairs = sorted(pairs, reverse=True)
            kicker = sorted([r for r, c in rank_counts.items() if c == 1], reverse=True)
            return {
                'category': 2,
                'category_rank': 2,
                'tiebreaker': pairs + kicker,
            }

        # 一对
        if counts == [2, 1, 1, 1]:
            pair_rank = sorted_ranks[0][0]
            kickers = sorted([r for r, c in rank_counts.items() if c == 1], reverse=True)
            return {
                'category': 1,
                'category_rank': 1,
                'tiebreaker': [pair_rank] + kickers,
            }

        # 高牌
        return {
            'category': 0,
            'category_rank': 0,
            'tiebreaker': sorted(ranks, reverse=True),
        }

    def _straight_high_card(self, ranks_sorted):
        """
        计算顺子高张，A2345 视为 5 高顺
        """
        unique_ranks = sorted(set(ranks_sorted))
        if len(unique_ranks) != 5:
            return None

        if unique_ranks == [2, 3, 4, 5, 14]:
            return 5

        for i in range(1, len(unique_ranks)):
            if unique_ranks[i] != unique_ranks[i - 1] + 1:
                return None
        return unique_ranks[-1]
    
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
        profile1 = self._hand_profile(hand1)
        profile2 = self._hand_profile(hand2)

        if profile1['category_rank'] > profile2['category_rank']:
            return 1
        if profile1['category_rank'] < profile2['category_rank']:
            return -1

        return self._compare_tiebreaker(profile1['tiebreaker'], profile2['tiebreaker'])
    
    def _compare_tiebreaker(self, tiebreaker1, tiebreaker2):
        for value1, value2 in zip(tiebreaker1, tiebreaker2):
            if value1 > value2:
                return 1
            if value1 < value2:
                return -1
        if len(tiebreaker1) > len(tiebreaker2):
            return 1
        if len(tiebreaker1) < len(tiebreaker2):
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
        # 获取区域长度配置
        top_length = config_loader.get_region_length('top')
        middle_length = config_loader.get_region_length('middle')
        bottom_length = config_loader.get_region_length('bottom')
        
        # 只有当所有区域牌数足够时，才检查牌型顺序
        if len(player.hand['top']) < top_length or \
           len(player.hand['middle']) < middle_length or \
           len(player.hand['bottom']) < bottom_length:
            # 牌数不足，不是爆牌，只是游戏未完成
            return False
        
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
                    score = config_loader.get_top_pair_score(high_pair)
                
                # 检查三条
                trips = [r for r, c in rank_counts.items() if c >= 3]
                if trips:
                    high_trip = max(trips)
                    # 头道三条牌型分
                    score = config_loader.get_top_trips_score(high_trip)
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
            
            # 皇家同花顺
            if is_straight and is_flush and ranks == [10, 11, 12, 13, 14]:
                score = config_loader.get_hand_score(region, 'royal_flush')
            # 同花顺
            elif is_straight and is_flush:
                score = config_loader.get_hand_score(region, 'straight_flush')
            # 四条
            elif counts == [4, 1]:
                score = config_loader.get_hand_score(region, 'four_of_a_kind')
            # 葫芦
            elif counts == [3, 2]:
                score = config_loader.get_hand_score(region, 'full_house')
            # 同花
            elif is_flush:
                score = config_loader.get_hand_score(region, 'flush')
            # 顺子
            elif is_straight:
                score = config_loader.get_hand_score(region, 'straight')
            # 三条
            elif counts == [3, 1, 1]:
                score = config_loader.get_hand_score(region, 'three_of_a_kind')
            # 两对
            elif counts == [2, 2, 1]:
                score = config_loader.get_hand_score(region, 'two_pair')
            # 一对
            elif counts == [2, 1, 1, 1]:
                score = config_loader.get_hand_score(region, 'one_pair')
            # 高牌
            else:
                score = config_loader.get_hand_score(region, 'high_card')
        
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
            
            # 获取范特西模式配置
            cards_by_top_hand = config_loader.get_fantasy_mode_config('cards_by_top_hand')
            
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
                    # 三条或以上
                    player.fantasy_cards = cards_by_top_hand.get('trips', 13)
                    player.fantasy_mode = True
                    return True
                else:
                    high_pair = max(pairs)
                    # 根据对子大小决定发牌数量
                    if high_pair >= 14:  # AA
                        player.fantasy_cards = cards_by_top_hand.get('aa', 13)
                        player.fantasy_mode = True
                        return True
                    elif high_pair >= 13:  # KK
                        player.fantasy_cards = cards_by_top_hand.get('kk', 13)
                        player.fantasy_mode = True
                        return True
                    elif high_pair >= 12:  # QQ
                        player.fantasy_cards = cards_by_top_hand.get('qq', 13)
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
        # 获取范特西模式留驻条件
        stay_conditions = config_loader.get_fantasy_mode_config('stay_conditions')
        
        # 检查底部区域是否有4条或以上强度的牌型
        bottom_strength = self.evaluate_hand(player.hand['bottom'])
        if bottom_strength >= stay_conditions.get('bottom_min_strength', 7):
            return True
        
        # 检查顶部区域是否有三条或以上
        top_strength = self.evaluate_hand(player.hand['top'])
        if top_strength >= stay_conditions.get('top_min_strength', 2):
            return True
        
        return False
