import random
import itertools

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
        return f"{self.rank}{self.suit}"

class Deck:
    def __init__(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['♠', '♥', '♦', '♣']
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
        self.hand = {'top': [], 'middle': [], 'bottom': []}
        self.bet = 0
        self.folded = False
    
    def place_bet(self, amount):
        if amount <= self.chips:
            self.chips -= amount
            self.bet += amount
            return True
        return False
    
    def reset_hand(self):
        self.hand = {'top': [], 'middle': [], 'bottom': [], 'temp': []}
        self.bet = 0
        self.folded = False

class OFCPoker:
    def __init__(self):
        self.deck = Deck()
        self.players = []
        self.pot = 0
        self.current_bet = 0
        self.round = 0
        self.action_player = 0
        self.fantasy_mode = False
    
    def add_player(self, player):
        self.players.append(player)
    
    def start_game(self):
        self.deck = Deck()
        for player in self.players:
            player.reset_hand()
        
        # 发牌 - 第一轮（开局）
        for _ in range(5):
            for player in self.players:
                card = self.deck.deal(1)[0]
                # 暂时放在临时区域，等待玩家摆牌
                if 'temp' not in player.hand:
                    player.hand['temp'] = []
                player.hand['temp'].append(card)
        
        self.pot = 0
        self.current_bet = 0
        self.round = 1
        self.action_player = 0
        self.fantasy_mode = False
        self.check_fantasy_mode()
    
    def deal_round(self):
        # 第二至第五轮发牌
        if self.round >= 2 and self.round <= 5:
            for player in self.players:
                if not player.folded:
                    # 发放3张牌
                    cards = self.deck.deal(3)
                    # 简化处理：自动分配到三个区域
                    player.hand['top'].append(cards[0])
                    player.hand['middle'].append(cards[1])
                    player.hand['bottom'].append(cards[2])
        self.round += 1
    
    def evaluate_hand(self, cards):
        # 评估手牌强度
        if len(cards) == 3:
            return self.evaluate_3_card_hand(cards)
        else:
            return self.evaluate_5_card_hand(cards)
    
    def evaluate_3_card_hand(self, cards):
        # 评估3张牌的手牌
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
        
        if is_straight and is_flush:
            return 8  # 同花顺
        elif counts == [3]:
            return 7  # 三条
        elif is_flush:
            return 6  # 同花
        elif is_straight:
            return 5  # 顺子
        elif counts == [2, 1]:
            return 4  # 一对
        else:
            return 3  # 高牌
    
    def evaluate_5_card_hand(self, cards):
        # 评估5张牌的手牌
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
        
        if is_straight and is_flush:
            # 检查皇家同花顺
            if ranks == [10, 11, 12, 13, 14]:
                return 10  # 皇家同花顺
            return 9  # 同花顺
        elif counts == [4, 1]:
            return 8  # 四条
        elif counts == [3, 2]:
            return 7  # 葫芦
        elif is_flush:
            return 6  # 同花
        elif is_straight:
            return 5  # 顺子
        elif counts == [3, 1, 1]:
            return 4  # 三条
        elif counts == [2, 2, 1]:
            return 3  # 两对
        elif counts == [2, 1, 1, 1]:
            return 2  # 一对
        else:
            return 1  # 高牌
    
    def compare_hands(self, hand1, hand2):
        # 比较两手牌的大小
        score1 = self.evaluate_hand(hand1)
        score2 = self.evaluate_hand(hand2)
        
        if score1 > score2:
            return 1
        elif score1 < score2:
            return -1
        else:
            # 分数相同时比较高牌
            ranks1 = sorted([card.value for card in hand1], reverse=True)
            ranks2 = sorted([card.value for card in hand2], reverse=True)
            
            for r1, r2 in zip(ranks1, ranks2):
                if r1 > r2:
                    return 1
                elif r1 < r2:
                    return -1
            
            return 0
    
    def check_busted(self, player):
        # 检查是否爆牌
        if len(player.hand['top']) < 3 or len(player.hand['middle']) < 5 or len(player.hand['bottom']) < 5:
            return True
        
        top_score = self.evaluate_hand(player.hand['top'])
        middle_score = self.evaluate_hand(player.hand['middle'])
        bottom_score = self.evaluate_hand(player.hand['bottom'])
        
        return not (top_score <= middle_score <= bottom_score)
    
    def calculate_score(self, player1, player2):
        # 计算两个玩家之间的得分
        if self.check_busted(player1):
            return -3  # 爆牌，全败
        if self.check_busted(player2):
            return 3  # 对手爆牌，全胜
        
        score = 0
        # 比较三个区域
        top_result = self.compare_hands(player1.hand['top'], player2.hand['top'])
        middle_result = self.compare_hands(player1.hand['middle'], player2.hand['middle'])
        bottom_result = self.compare_hands(player1.hand['bottom'], player2.hand['bottom'])
        
        score += top_result
        score += middle_result
        score += bottom_result
        
        # 三道全胜奖励
        if top_result == 1 and middle_result == 1 and bottom_result == 1:
            score += 3
        
        # 牌型分
        score += self.calculate_hand_score(player1.hand['top'], 'top')
        score += self.calculate_hand_score(player1.hand['middle'], 'middle')
        score += self.calculate_hand_score(player1.hand['bottom'], 'bottom')
        
        return score
    
    def calculate_hand_score(self, cards, region):
        # 计算牌型分
        score = 0
        hand_strength = self.evaluate_hand(cards)
        
        if region == 'top':
            # 头道牌型分
            if len(cards) >= 2:
                # 检查对子
                ranks = [card.value for card in cards]
                rank_counts = {}
                for rank in ranks:
                    rank_counts[rank] = rank_counts.get(rank, 0) + 1
                
                pairs = [r for r, c in rank_counts.items() if c >= 2]
                if pairs:
                    high_pair = max(pairs)
                    if high_pair == 12:  # QQ
                        score = 7
                    elif high_pair == 13:  # KK
                        score = 8
                    elif high_pair == 14:  # AA
                        score = 9
                    elif len([r for r, c in rank_counts.items() if c >= 3]) > 0:
                        # 三条
                        score = 10 + (max(ranks) - 2)
        elif region == 'middle':
            # 中道牌型分
            if hand_strength == 4:  # 三条
                score = 2
            elif hand_strength == 5:  # 顺子
                score = 4
            elif hand_strength == 6:  # 同花
                score = 8
            elif hand_strength == 7:  # 葫芦
                score = 12
            elif hand_strength == 8:  # 四条
                score = 20
            elif hand_strength == 9:  # 同花顺
                score = 30
            elif hand_strength == 10:  # 皇家同花顺
                score = 50
        elif region == 'bottom':
            # 尾道牌型分
            if hand_strength == 5:  # 顺子
                score = 2
            elif hand_strength == 6:  # 同花
                score = 4
            elif hand_strength == 7:  # 葫芦
                score = 6
            elif hand_strength == 8:  # 四条
                score = 10
            elif hand_strength == 9:  # 同花顺
                score = 15
            elif hand_strength == 10:  # 皇家同花顺
                score = 25
        
        return score
    
    def check_fantasy_mode(self):
        # 检查是否进入范特西模式
        for player in self.players:
            if not player.folded and len(player.hand['top']) >= 3:
                top_strength = self.evaluate_hand(player.hand['top'])
                # 头道为QQ或更大时进入范特西模式
                if top_strength >= 4:  # 至少一对
                    ranks = [card.value for card in player.hand['top']]
                    rank_counts = {}
                    for rank in ranks:
                        rank_counts[rank] = rank_counts.get(rank, 0) + 1
                    
                    pairs = [r for r, c in rank_counts.items() if c >= 2]
                    if pairs and max(pairs) >= 12:  # QQ或更大
                        self.fantasy_mode = True
                        break
    
    def determine_winner(self):
        # 确定游戏 winner
        if len(self.players) == 2:
            score1 = self.calculate_score(self.players[0], self.players[1])
            if score1 > 0:
                # 玩家0获胜，更新积分
                self.players[0].total_score += score1
                self.players[1].total_score -= score1
                return self.players[0]
            else:
                # 玩家1获胜，更新积分
                self.players[0].total_score += score1
                self.players[1].total_score -= score1
                return self.players[1]
        else:
            # 简化处理：返回得分最高的玩家
            best_score = -float('inf')
            winner = None
            for i, player in enumerate(self.players):
                if player.folded:
                    continue
                total_score = 0
                for j, other_player in enumerate(self.players):
                    if i != j and not other_player.folded:
                        player_score = self.calculate_score(player, other_player)
                        total_score += player_score
                        # 更新积分
                        player.total_score += player_score
                        other_player.total_score -= player_score
                if total_score > best_score:
                    best_score = total_score
                    winner = player
            return winner
