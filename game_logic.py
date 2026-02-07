from core import Card, Deck, Player, Table
from rule_engine import RuleEngine

class OFCGame:
    def __init__(self):
        self.deck = Deck()
        self.players = []
        self.table = Table()
        self.rule_engine = RuleEngine()
    
    def add_player(self, player):
        self.players.append(player)
    
    def start_game(self):
        # 重置游戏状态
        self.deck = Deck()
        for player in self.players:
            player.reset_hand()
        self.table = Table()
        
        # 检查是否进入范特西模式
        print("检查范特西模式...")
        self.check_fantasy_mode()
        
        self.table.round = 1
        self.table.action_player = 0
        print(f"游戏开始，当前轮次: {self.table.round}")
        print(f"范特西模式: {self.table.fantasy_mode}")
    
    def deal_round(self):
        # 发牌逻辑
        print(f"\n正在发第 {self.table.round} 轮牌...")
        if self.table.round == 1:
            # 第一轮发牌：每人5张牌
            for player in self.players:
                if not player.folded:
                    # 清空临时区域
                    player.hand['temp'] = []
                    for _ in range(5):
                        card = self.deck.deal(1)[0]
                        player.hand['temp'].append(card)
                    print(f"给{player.name}发牌: {player.hand['temp']}")
        elif self.table.round >= 2 and self.table.round <= 5:
            # 第二至第五轮发牌：每人3张牌
            for player in self.players:
                if not player.folded:
                    cards = self.deck.deal(3)
                    # 将牌放入临时区域，等待玩家选择
                    player.hand['temp'] = cards
                    print(f"给{player.name}发牌: {cards}")
        else:
            print(f"当前轮次 {self.table.round} 不需要发牌")
        
        print(f"发牌完成，轮次保持为: {self.table.round}")
    
    def evaluate_hand(self, cards):
        # 评估手牌强度，委托给规则引擎
        return self.rule_engine.evaluate_hand(cards)
    
    def evaluate_3_card_hand(self, cards):
        # 评估3张牌的手牌，委托给规则引擎
        return self.rule_engine.evaluate_3_card_hand(cards)
    
    def evaluate_5_card_hand(self, cards):
        # 评估5张牌的手牌，委托给规则引擎
        return self.rule_engine.evaluate_5_card_hand(cards)
    
    def compare_hands(self, hand1, hand2):
        # 比较两手牌的大小，委托给规则引擎
        return self.rule_engine.compare_hands(hand1, hand2)
    
    def _compare_same_strength_hands(self, hand1, hand2):
        # 比较相同强度值的手牌
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
        # 检查是否爆牌，委托给规则引擎
        return self.rule_engine.check_busted(player)
    
    def calculate_score(self, player1, player2):
        # 计算两个玩家之间的得分
        player1_busted = self.check_busted(player1)
        player2_busted = self.check_busted(player2)
        
        # 计算双方的牌型分
        player1_top_score = self.calculate_hand_score(player1.hand['top'], 'top')
        player1_middle_score = self.calculate_hand_score(player1.hand['middle'], 'middle')
        player1_bottom_score = self.calculate_hand_score(player1.hand['bottom'], 'bottom')
        player1_hand_score = player1_top_score + player1_middle_score + player1_bottom_score
        
        player2_top_score = self.calculate_hand_score(player2.hand['top'], 'top')
        player2_middle_score = self.calculate_hand_score(player2.hand['middle'], 'middle')
        player2_bottom_score = self.calculate_hand_score(player2.hand['bottom'], 'bottom')
        player2_hand_score = player2_top_score + player2_middle_score + player2_bottom_score
        
        # 计算区域得分
        top_result = self.compare_hands(player1.hand['top'], player2.hand['top'])
        middle_result = self.compare_hands(player1.hand['middle'], player2.hand['middle'])
        bottom_result = self.compare_hands(player1.hand['bottom'], player2.hand['bottom'])
        
        # 基础区域得分
        base_score = top_result + middle_result + bottom_result
        
        # 计算三道全赢附加分
        three_wins_bonus1 = 0
        if top_result == 1 and middle_result == 1 and bottom_result == 1:
            three_wins_bonus1 = 3  # 三道全赢，加3分
        
        three_wins_bonus2 = 0
        if top_result == -1 and middle_result == -1 and bottom_result == -1:
            three_wins_bonus2 = 3  # 三道全赢，加3分
        
        # 规则1：一方爆牌，另一方不爆牌
        if player1_busted and not player2_busted:
            player1_score = 0  # player1爆牌，得0分
            player2_score = 6 + player2_hand_score  # player2不爆牌，得6分和自己的牌型分
        elif player2_busted and not player1_busted:
            player1_score = 6 + player1_hand_score  # player2爆牌，player1得6分和自己的牌型分
            player2_score = 0  # player2爆牌，得0分
        # 规则2：双方都爆牌
        elif player1_busted and player2_busted:
            player1_score = 0  # 双方都0分
            player2_score = 0  # 双方都0分
        # 规则3：双方都不爆牌
        else:
            # 计算牌型分差值
            score_difference = player1_hand_score - player2_hand_score
            
            # 计算区域分（三个区域的胜负结果总和）
            area_score = base_score  # base_score = top_result + middle_result + bottom_result
            
            # 计算三道全赢附加分
            if top_result == 1 and middle_result == 1 and bottom_result == 1:
                # 玩家1三道全赢
                player1_score = max(0, score_difference + 6)  # 三道全赢，得分 = 牌型分差值 + 6分
                player2_score = 0  # 输家得0分
            elif top_result == -1 and middle_result == -1 and bottom_result == -1:
                # 玩家2三道全赢
                player2_score = max(0, -score_difference + 6)  # 三道全赢，得分 = 牌型分差值 + 6分
                player1_score = 0  # 输家得0分
            else:
                # 不是三道全赢，比较牌型分
                if player1_hand_score > player2_hand_score:
                    # 玩家1赢
                    # 赢家获得分值差+区域分
                    player1_score = max(0, score_difference + area_score)
                    player2_score = 0  # 输家得0分
                elif player2_hand_score > player1_hand_score:
                    # 玩家2赢
                    # 赢家获得分值差+区域分
                    player2_score = max(0, -score_difference - area_score)  # area_score是player1的区域分，所以player2的区域分是-area_score
                    player1_score = 0  # 输家得0分
                else:
                    # 平局，双方都得0分
                    player1_score = 0
                    player2_score = 0
        
        # 更新双方的累计积分
        player1.total_score += player1_score
        player2.total_score += player2_score
        
        return player1_score
    
    def calculate_hand_score(self, cards, region):
        # 计算牌型分，根据用户提供的规则
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
                    if high_pair == 6:  # 66
                        score = 1
                    elif high_pair == 7:  # 77
                        score = 2
                    elif high_pair == 8:  # 88
                        score = 3
                    elif high_pair == 9:  # 99
                        score = 4
                    elif high_pair == 10:  # TT
                        score = 5
                    elif high_pair == 11:  # JJ
                        score = 6
                    elif high_pair == 12:  # QQ
                        score = 7
                    elif high_pair == 13:  # KK
                        score = 8
                    elif high_pair == 14:  # AA
                        score = 9
                
                # 检查三条
                trips = [r for r, c in rank_counts.items() if c >= 3]
                if trips:
                    high_trip = max(trips)
                    # 头道三条牌型分
                    if high_trip == 2:  # 222
                        score = 10
                    elif high_trip == 3:  # 333
                        score = 11
                    elif high_trip == 4:  # 444
                        score = 12
                    elif high_trip == 5:  # 555
                        score = 13
                    elif high_trip == 6:  # 666
                        score = 14
                    elif high_trip == 7:  # 777
                        score = 15
                    elif high_trip == 8:  # 888
                        score = 16
                    elif high_trip == 9:  # 999
                        score = 17
                    elif high_trip == 10:  # TTT
                        score = 18
                    elif high_trip == 11:  # JJJ
                        score = 19
                    elif high_trip == 12:  # QQQ
                        score = 20
                    elif high_trip == 13:  # KKK
                        score = 21
                    elif high_trip == 14:  # AAA
                        score = 22
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
            
            # 检查牌型
            rank_counts = {}
            for rank in ranks:
                rank_counts[rank] = rank_counts.get(rank, 0) + 1
            
            counts = sorted(rank_counts.values(), reverse=True)
            
            # 皇家同花顺
            if is_straight and is_flush and ranks == [10, 11, 12, 13, 14]:
                if region == 'middle':
                    score = 50
                else:
                    score = 25
            # 同花顺
            elif is_straight and is_flush:
                if region == 'middle':
                    score = 30
                else:
                    score = 15
            # 四条
            elif counts == [4, 1]:
                if region == 'middle':
                    score = 20
                else:
                    score = 10
            # 葫芦
            elif counts == [3, 2]:
                if region == 'middle':
                    score = 12
                else:
                    score = 6
            # 同花
            elif is_flush:
                if region == 'middle':
                    score = 8
                else:
                    score = 4  # 底部区域同花得4分
            # 顺子
            elif is_straight:
                if region == 'middle':
                    score = 4
                else:
                    score = 2
            # 三条
            elif counts == [3, 1, 1]:
                if region == 'middle':
                    score = 2  # 中部区域三条得2分
                else:
                    score = 0  # 底部区域三条得0分
            # 两对
            elif counts == [2, 2, 1]:
                score = 0
            # 一对
            elif counts == [2, 1, 1, 1]:
                score = 0
            # 高牌
            else:
                score = 0
        
        return score
    
    def check_fantasy_mode(self):
        # 检查是否进入范特西模式
        for player in self.players:
            if not player.folded:
                # 检查玩家是否已经处于范特西模式
                if hasattr(player, 'fantasy_mode') and player.fantasy_mode:
                    # 玩家已经处于范特西模式，检查是否满足留在范特西模式的条件
                    if self.check_fantasy_stay_condition(player):
                        # 满足留在范特西模式的条件
                        print(f"{player.name}满足留在范特西模式的条件，继续以范特西模式进行游戏")
                    else:
                        # 不满足留在范特西模式的条件，退出范特西模式
                        player.fantasy_mode = False
                        print(f"{player.name}不满足留在范特西模式的条件，退出范特西模式")
                else:
                    # 玩家未处于范特西模式，检查是否满足进入范特西模式的条件
                    # 首先检查玩家上一局的手牌
                    if hasattr(player, 'last_top_hand') and len(player.last_top_hand) >= 3:
                        # 检查玩家上一局是否爆牌，爆牌不能进入范特西模式
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
                                print(f"{player.name}上一局爆牌，不能进入范特西模式")
                                continue
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
                                player.fantasy_cards = 17
                                player.fantasy_mode = True
                                print(f"{player.name}上一局顶部手牌为三条或以上，进入范特西模式，发17张牌")
                            else:
                                high_pair = max(pairs)
                                # 根据对子大小决定发牌数量
                                if high_pair >= 14:  # AA
                                    player.fantasy_cards = 16
                                    player.fantasy_mode = True
                                    print(f"{player.name}上一局顶部手牌为AA，进入范特西模式，发16张牌")
                                elif high_pair >= 13:  # KK
                                    player.fantasy_cards = 15
                                    player.fantasy_mode = True
                                    print(f"{player.name}上一局顶部手牌为KK，进入范特西模式，发15张牌")
                                elif high_pair >= 12:  # QQ
                                    player.fantasy_cards = 14
                                    player.fantasy_mode = True
                                    print(f"{player.name}上一局顶部手牌为QQ，进入范特西模式，发14张牌")
                                else:
                                    # 对子太小，不进入范特西模式
                                    player.fantasy_mode = False
                                    print(f"{player.name}上一局顶部手牌对子太小，不进入范特西模式")
                        else:
                            player.fantasy_mode = False
                            print(f"{player.name}上一局顶部手牌没有对子，不进入范特西模式")
                    else:
                        player.fantasy_mode = False
                        print(f"{player.name}上一局没有完整的顶部手牌，不进入范特西模式")
    
    def check_fantasy_stay_condition(self, player):
        """检查玩家是否满足留在范特西模式的条件，委托给规则引擎"""
        return self.rule_engine.check_fantasy_stay_condition(player)
    
    def determine_winner(self):
        # 确定游戏 winner
        if len(self.players) == 2:
            p1, p2 = self.players
            # 检查是否双方都爆牌
            p1_busted = self.check_busted(p1)
            p2_busted = self.check_busted(p2)
            if p1_busted and p2_busted:
                # 双方都爆牌，没有获胜者
                return None
            else:
                # 计算得分并返回获胜者
                score1 = self.calculate_score(p1, p2)
                if score1 > 0:
                    return p1
                else:
                    return p2
        else:
            # 多玩家情况：先计算所有玩家的得分
            # 注意：只计算一次得分，避免重复累计
            for i, player in enumerate(self.players):
                if player.folded:
                    continue
                for j, other_player in enumerate(self.players):
                    if i < j and not other_player.folded:
                        self.calculate_score(player, other_player)
            
            # 然后返回得分最高的玩家
            best_score = -float('inf')
            winner = None
            for player in self.players:
                if not player.folded and player.total_score > best_score:
                    best_score = player.total_score
                    winner = player
            return winner
    
    def save_game_record(self, filename=None):
        """保存游戏记录到JSON文件"""
        import json
        import os
        from datetime import datetime
        
        # 构建游戏记录
        record = {
            'timestamp': datetime.now().isoformat(),
            'players': [],
            'game_details': {
                'fantasy_mode': any(player.fantasy_mode for player in self.players),
                'player_count': len(self.players)
            }
        }
        
        # 添加玩家信息
        for player in self.players:
            player_record = {
                'name': player.name,
                'total_score': player.total_score,
                'hand': {
                    'top': [str(card) for card in player.hand['top']],
                    'middle': [str(card) for card in player.hand['middle']],
                    'bottom': [str(card) for card in player.hand['bottom']]
                },
                'is_ai': hasattr(player, 'difficulty'),
                'fantasy_mode': getattr(player, 'fantasy_mode', False)
            }
            record['players'].append(player_record)
        
        # 确定文件名
        if not filename:
            save_dir = 'game_records'
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            filename = f"{save_dir}/game_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # 保存到文件
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(record, f, ensure_ascii=False, indent=2)
            print(f"游戏记录已保存到: {filename}")
            return True
        except Exception as e:
            print(f"保存游戏记录失败: {e}")
            return False
