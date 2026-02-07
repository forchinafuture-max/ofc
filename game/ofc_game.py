"""
OFCGame 类，负责发牌、轮次、玩家调用规则接口
"""

from game.deck import Deck
from game.player import Player
from core.rules import RuleEngine

class OFCGame:
    """
    OFC游戏类
    负责游戏流程管理、发牌、轮次推进等
    """
    def __init__(self):
        """
        初始化OFC游戏
        """
        self.deck = Deck()
        self.players = []
        self.current_round = 0
        self.rule_engine = RuleEngine()  # 规则引擎实例
    
    def add_player(self, player):
        """
        添加玩家
        
        Args:
            player: 玩家对象
        """
        self.players.append(player)
    
    def start_game(self):
        """
        开始游戏
        """
        # 重置游戏状态
        self.deck.reset()
        self.current_round = 0
        
        # 清空玩家手牌
        for player in self.players:
            player.clear_hand()
        
        # 记录游戏开始
        from core.logger import game_logger
        game_logger.start_game(self)
        
        # 开始第一轮发牌
        self.deal_first_round()
    
    def deal_first_round(self):
        """
        第一轮发牌（5张牌）
        """
        self.current_round = 1
        for player in self.players:
            # 检查是否处于幻想模式
            if hasattr(player, 'fantasy_mode') and player.fantasy_mode:
                # 幻想模式下的发牌数量
                cards_to_deal = player.fantasy_cards
            else:
                # 普通模式下的发牌数量
                cards_to_deal = 5
            
            # 发牌
            cards = self.deck.deal(cards_to_deal)
            for card in cards:
                player.add_card(card, 'temp')
    
    def deal_round(self):
        """
        按轮次发牌
        第1轮：5张牌
        第2-5轮：每轮3张牌
        """
        # 确定当前轮次的发牌数量
        if self.current_round == 1:
            # 第1轮发5张牌
            base_cards_to_deal = 5
        elif 2 <= self.current_round <= 5:
            # 第2-5轮每轮发3张牌
            base_cards_to_deal = 3
        else:
            # 超出轮次范围，不发牌
            return
        
        for player in self.players:
            # 检查是否处于幻想模式
            if hasattr(player, 'fantasy_mode') and player.fantasy_mode:
                # 幻想模式下的发牌数量
                cards_to_deal = player.fantasy_cards
            else:
                # 普通模式下的发牌数量
                cards_to_deal = base_cards_to_deal
            
            # 发牌
            cards = self.deck.deal(cards_to_deal)
            for card in cards:
                player.add_card(card, 'temp')
    
    def next_round(self):
        """
        进入下一轮
        """
        self.current_round += 1
        if self.current_round > 5:
            # 游戏结束
            return False
        
        # 后续轮次的发牌逻辑
        # 注意：根据OFC规则，后续轮次的发牌和弃牌机制可能不同
        # 这里简化处理，实际实现需要根据具体规则调整
        return True
    
    def evaluate_hand(self, cards):
        """
        评估手牌强度，委托给规则引擎
        
        Args:
            cards: 手牌列表
            
        Returns:
            手牌强度值
        """
        return self.rule_engine.evaluate_hand(cards)
    
    def compare_hands(self, hand1, hand2):
        """
        比较两手牌的大小，委托给规则引擎
        
        Args:
            hand1: 第一手牌
            hand2: 第二手牌
            
        Returns:
            1: hand1 > hand2
            -1: hand1 < hand2
            0: hand1 == hand2
        """
        return self.rule_engine.compare_hands(hand1, hand2)
    
    def check_busted(self, player):
        """
        检查玩家是否爆牌，委托给规则引擎
        
        Args:
            player: 玩家对象
            
        Returns:
            bool: 是否爆牌
        """
        return self.rule_engine.check_busted(player)
    
    def calculate_hand_score(self, cards, region):
        """
        计算牌型分，委托给规则引擎
        
        Args:
            cards: 手牌列表
            region: 区域名称 ('top', 'middle', 'bottom')
            
        Returns:
            牌型分
        """
        return self.rule_engine.calculate_hand_score(cards, region)
    
    def check_fantasy_mode(self, player):
        """
        检查玩家是否进入范特西模式，委托给规则引擎
        
        Args:
            player: 玩家对象
            
        Returns:
            bool: 是否进入范特西模式
        """
        return self.rule_engine.check_fantasy_mode(player)
    
    def check_fantasy_stay_condition(self, player):
        """
        检查玩家是否满足留在范特西模式的条件，委托给规则引擎
        
        Args:
            player: 玩家对象
            
        Returns:
            bool: 是否满足条件
        """
        return self.rule_engine.check_fantasy_stay_condition(player)
    
    def calculate_total_score(self, player):
        """
        计算玩家的总得分
        
        Args:
            player: 玩家对象
            
        Returns:
            总得分
        """
        from config.loader import config_loader
        
        total_score = 0
        
        # 计算各区域的得分
        top_score = self.calculate_hand_score(player.hand['top'], 'top')
        middle_score = self.calculate_hand_score(player.hand['middle'], 'middle')
        bottom_score = self.calculate_hand_score(player.hand['bottom'], 'bottom')
        
        total_score = top_score + middle_score + bottom_score
        
        # 检查是否爆牌
        if self.check_busted(player):
            total_score = 0  # 爆牌得0分
        else:
            # 检查是否进入范特西模式
            if hasattr(player, 'fantasy_mode') and player.fantasy_mode:
                total_score += config_loader.get_scoring('fantasyland_bonus')
        
        return total_score
    
    def determine_winner(self):
        """
        确定游戏 winner
        
        Returns:
            获胜玩家对象
        """
        from config.loader import config_loader
        
        if not self.players:
            # 记录游戏结束（无玩家）
            from core.logger import game_logger
            game_logger.end_game(self, None)
            return None
        
        # 如果只有一个玩家，直接返回
        if len(self.players) == 1:
            winner = self.players[0]
            # 记录游戏结束
            from core.logger import game_logger
            game_logger.end_game(self, winner)
            return winner
        
        # 计算每个玩家的得分，排除爆牌玩家
        valid_players = [player for player in self.players if not self.check_busted(player)]
        
        if not valid_players:
            # 所有玩家都爆牌，返回第一个玩家
            winner = self.players[0]
            # 记录游戏结束
            from core.logger import game_logger
            game_logger.end_game(self, winner)
            return winner
        
        # 对于两个玩家的情况，使用与display_winner相同的得分计算逻辑
        if len(self.players) == 2:
            p1, p2 = self.players
            
            # 检查爆牌情况
            p1_busted = self.check_busted(p1)
            p2_busted = self.check_busted(p2)
            
            # 计算双方的牌型分
            p1_top_score = self.calculate_hand_score(p1.hand['top'], 'top')
            p1_middle_score = self.calculate_hand_score(p1.hand['middle'], 'middle')
            p1_bottom_score = self.calculate_hand_score(p1.hand['bottom'], 'bottom')
            p1_hand_score = p1_top_score + p1_middle_score + p1_bottom_score
            
            p2_top_score = self.calculate_hand_score(p2.hand['top'], 'top')
            p2_middle_score = self.calculate_hand_score(p2.hand['middle'], 'middle')
            p2_bottom_score = self.calculate_hand_score(p2.hand['bottom'], 'bottom')
            p2_hand_score = p2_top_score + p2_middle_score + p2_bottom_score
            
            # 计算本局得分
            if p1_busted and p2_busted:
                p1_round_score = 0
                p2_round_score = 0
            elif p1_busted:
                p1_round_score = 0
                p2_round_score = 6 + p2_hand_score  # 爆牌规则：获胜者得6分 + 牌型分
            elif p2_busted:
                p1_round_score = 6 + p1_hand_score  # 爆牌规则：获胜者得6分 + 牌型分
                p2_round_score = 0
            else:
                # 计算区域得分
                top_result = self.compare_hands(p1.hand['top'], p2.hand['top'])
                middle_result = self.compare_hands(p1.hand['middle'], p2.hand['middle'])
                bottom_result = self.compare_hands(p1.hand['bottom'], p2.hand['bottom'])
                area_score = top_result + middle_result + bottom_result
                
                # 计算得分
                score_difference = p1_hand_score - p2_hand_score
                if top_result == 1 and middle_result == 1 and bottom_result == 1:
                    # 三道全胜
                    p1_round_score = max(0, score_difference + 6)
                    p2_round_score = 0
                elif top_result == -1 and middle_result == -1 and bottom_result == -1:
                    # 三道全输
                    p1_round_score = 0
                    p2_round_score = max(0, -score_difference + 6)
                elif p1_hand_score > p2_hand_score:
                    # 玩家1赢
                    p1_round_score = max(0, score_difference + area_score)
                    p2_round_score = 0
                elif p2_hand_score > p1_hand_score:
                    # 玩家2赢
                    p1_round_score = 0
                    p2_round_score = max(0, -score_difference - area_score)
                else:
                    # 平局
                    p1_round_score = 0
                    p2_round_score = 0
            
            # 更新累计积分
            p1.total_score += p1_round_score
            p2.total_score += p2_round_score
            
            # 确定获胜者
            if p1_round_score > p2_round_score:
                winner = p1
            else:
                winner = p2
        else:
            # 多玩家情况，使用简化处理
            player_scores = []
            for player in valid_players:
                score = self.calculate_total_score(player)
                player_scores.append((score, player))
            
            # 排序并返回最高分的玩家
            player_scores.sort(reverse=True, key=lambda x: x[0])
            winner = player_scores[0][1]
            
            # 更新累计积分
            if len(player_scores) >= 2:
                winner_score = player_scores[0][0]
                loser_score = player_scores[1][0]
                score_difference = winner_score - loser_score
                
                # 获胜者获得分数差
                winner.total_score += score_difference
                # 失败者失去分数差
                loser = player_scores[1][1]
                loser.total_score -= score_difference
        
        # 记录游戏结束
        from core.logger import game_logger
        game_logger.end_game(self, winner)
        
        return winner
