#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新计算得分超过50分的文件的正确得分
"""

import os
import json
import glob

class Card:
    """卡片类，用于解析json中的卡片字符串"""
    def __init__(self, card_str):
        # 解析卡片字符串，如 "A♣" -> 值为14，花色为"♣"
        if card_str[0] == 'A':
            self.value = 14
            self.suit = card_str[1:]
        elif card_str[0] == 'K':
            self.value = 13
            self.suit = card_str[1:]
        elif card_str[0] == 'Q':
            self.value = 12
            self.suit = card_str[1:]
        elif card_str[0] == 'J':
            self.value = 11
            self.suit = card_str[1:]
        elif card_str[0] == '1':
            # 10
            self.value = 10
            self.suit = card_str[2:]
        else:
            # 2-9
            self.value = int(card_str[0])
            self.suit = card_str[1:]
    
    def __str__(self):
        return f"{self.value}{self.suit}"

class OFCScorer:
    """OFC游戏计分器"""
    def evaluate_hand(self, cards):
        # 评估手牌强度
        if len(cards) == 3:
            return self.evaluate_3_card_hand(cards)
        elif len(cards) == 5:
            return self.evaluate_5_card_hand(cards)
        else:
            return 0
    
    def evaluate_3_card_hand(self, cards):
        # 评估3张牌的手牌
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
        # 评估5张牌的手牌
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
            return 3  # 三条
        elif counts == [2, 2, 1]:
            return 2  # 两对
        elif counts == [2, 1, 1, 1]:
            return 1  # 一对
        else:
            return 0  # 高牌
    
    def compare_hands(self, hand1, hand2):
        # 比较两手牌的大小
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
    
    def check_busted(self, top_cards, middle_cards, bottom_cards):
        # 检查是否爆牌
        if len(top_cards) < 3 or len(middle_cards) < 5 or len(bottom_cards) < 5:
            return True
        
        # 计算牌型强度
        top_strength = self.evaluate_hand(top_cards)
        middle_strength = self.evaluate_hand(middle_cards)
        bottom_strength = self.evaluate_hand(bottom_cards)
        
        # 比较顶部和中部
        if top_strength > middle_strength:
            return True
        elif top_strength == middle_strength:
            # 牌型强度相同时，比较具体牌值
            top_vs_middle = self.compare_hands(top_cards, middle_cards)
            if top_vs_middle > 0:
                return True
        
        # 比较中部和底部
        if middle_strength > bottom_strength:
            return True
        elif middle_strength == bottom_strength:
            # 牌型强度相同时，比较具体牌值
            middle_vs_bottom = self.compare_hands(middle_cards, bottom_cards)
            if middle_vs_bottom > 0:
                return True
        
        return False
    
    def calculate_hand_score(self, cards, region):
        # 计算牌型分
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
    
    def calculate_score(self, player1_cards, player2_cards):
        # 计算两个玩家之间的得分
        # player1_cards: (top, middle, bottom)
        # player2_cards: (top, middle, bottom)
        
        p1_top, p1_middle, p1_bottom = player1_cards
        p2_top, p2_middle, p2_bottom = player2_cards
        
        # 检查是否爆牌
        p1_busted = self.check_busted(p1_top, p1_middle, p1_bottom)
        p2_busted = self.check_busted(p2_top, p2_middle, p2_bottom)
        
        # 计算双方的牌型分
        p1_top_score = self.calculate_hand_score(p1_top, 'top')
        p1_middle_score = self.calculate_hand_score(p1_middle, 'middle')
        p1_bottom_score = self.calculate_hand_score(p1_bottom, 'bottom')
        p1_hand_score = p1_top_score + p1_middle_score + p1_bottom_score
        
        p2_top_score = self.calculate_hand_score(p2_top, 'top')
        p2_middle_score = self.calculate_hand_score(p2_middle, 'middle')
        p2_bottom_score = self.calculate_hand_score(p2_bottom, 'bottom')
        p2_hand_score = p2_top_score + p2_middle_score + p2_bottom_score
        
        # 计算区域得分
        top_result = self.compare_hands(p1_top, p2_top)
        middle_result = self.compare_hands(p1_middle, p2_middle)
        bottom_result = self.compare_hands(p1_bottom, p2_bottom)
        
        # 基础区域得分
        base_score = top_result + middle_result + bottom_result
        
        # 规则1：一方爆牌，另一方不爆牌
        if p1_busted and not p2_busted:
            p1_score = 0  # player1爆牌，得0分
            p2_score = 6 + p2_hand_score  # player2不爆牌，得6分和自己的牌型分
        elif p2_busted and not p1_busted:
            p1_score = 6 + p1_hand_score  # player2爆牌，player1得6分和自己的牌型分
            p2_score = 0  # player2爆牌，得0分
        # 规则2：双方都爆牌
        elif p1_busted and p2_busted:
            p1_score = 0  # 双方都0分
            p2_score = 0  # 双方都0分
        # 规则3：双方都不爆牌
        else:
            # 计算牌型分差值
            score_difference = p1_hand_score - p2_hand_score
            
            # 计算区域分（三个区域的胜负结果总和）
            area_score = base_score  # base_score = top_result + middle_result + bottom_result
            
            # 计算三道全赢附加分
            if top_result == 1 and middle_result == 1 and bottom_result == 1:
                # 玩家1三道全赢
                p1_score = max(0, score_difference + 6)  # 三道全赢，得分 = 牌型分差值 + 6分
                p2_score = 0  # 输家得0分
            elif top_result == -1 and middle_result == -1 and bottom_result == -1:
                # 玩家2三道全赢
                p2_score = max(0, -score_difference + 6)  # 三道全赢，得分 = 牌型分差值 + 6分
                p1_score = 0  # 输家得0分
            else:
                # 不是三道全赢，比较牌型分
                if p1_hand_score > p2_hand_score:
                    # 玩家1赢
                    # 赢家获得分值差+区域分
                    p1_score = max(0, score_difference + area_score)
                    p2_score = 0  # 输家得0分
                elif p2_hand_score > p1_hand_score:
                    # 玩家2赢
                    # 赢家获得分值差+区域分
                    p2_score = max(0, -score_difference - area_score)  # area_score是player1的区域分，所以player2的区域分是-area_score
                    p1_score = 0  # 输家得0分
                else:
                    # 平局，双方都得0分
                    p1_score = 0
                    p2_score = 0
        
        return p1_score, p2_score

def main():
    print("正在重新计算得分超过50分的文件...")
    print("=" * 60)
    
    # 定义游戏记录目录
    game_records_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "game_records")
    
    # 检查目录是否存在
    if not os.path.exists(game_records_dir):
        print(f"错误：目录 {game_records_dir} 不存在")
        exit(1)
    
    # 查找所有json文件
    json_files = glob.glob(os.path.join(game_records_dir, "*.json"))
    print(f"找到 {len(json_files)} 个json文件")
    print("=" * 60)
    
    # 筛选得分超过50分的文件
    high_score_files = []
    scorer = OFCScorer()
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # 检查是否有玩家得分超过或等于50分
                has_high_score = False
                original_scores = []
                
                for player in data['players']:
                    if 'total_score' in player and player['total_score'] >= 50:
                        has_high_score = True
                        original_scores.append((player['name'], player['total_score']))
                
                if has_high_score:
                    # 重新计算得分
                    print(f"\n重新计算 {os.path.basename(json_file)} 的得分...")
                    print(f"原始得分: {original_scores}")
                    
                    # 解析玩家手牌
                    players_cards = []
                    for player in data['players']:
                        # 解析顶部手牌
                        top_cards = []
                        for card_str in player['hand']['top']:
                            try:
                                card = Card(card_str)
                                top_cards.append(card)
                            except:
                                pass
                        
                        # 解析中部手牌
                        middle_cards = []
                        for card_str in player['hand']['middle']:
                            try:
                                card = Card(card_str)
                                middle_cards.append(card)
                            except:
                                pass
                        
                        # 解析底部手牌
                        bottom_cards = []
                        for card_str in player['hand']['bottom']:
                            try:
                                card = Card(card_str)
                                bottom_cards.append(card)
                            except:
                                pass
                        
                        players_cards.append((top_cards, middle_cards, bottom_cards))
                    
                    # 计算得分
                    if len(players_cards) == 2:
                        p1_cards, p2_cards = players_cards
                        p1_score, p2_score = scorer.calculate_score(p1_cards, p2_cards)
                        
                        print(f"重新计算得分: 玩家1: {p1_score}, 玩家2: {p2_score}")
                        
                        # 更新文件中的得分
                        for i, player in enumerate(data['players']):
                            if i == 0:
                                player['total_score'] = p1_score
                            else:
                                player['total_score'] = p2_score
                        
                        # 保存更新后的文件
                        with open(json_file, 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                        
                        print(f"文件已更新")
                        high_score_files.append((os.path.basename(json_file), original_scores, [p1_score, p2_score]))
                    else:
                        print(f"文件 {os.path.basename(json_file)} 不是2人游戏，跳过")
        except Exception as e:
            print(f"处理文件 {os.path.basename(json_file)} 失败: {e}")
    
    # 输出结果
    print("\n" + "=" * 60)
    print("重新计算完成！")
    print(f"共处理 {len(high_score_files)} 个得分超过50分的文件")
    print("=" * 60)
    
    if high_score_files:
        print("\n处理结果：")
        print("=" * 60)
        for filename, original, recalculated in high_score_files:
            print(f"文件: {filename}")
            print(f"原始得分: {original}")
            print(f"重新计算: {recalculated}")
            print("-" * 40)

if __name__ == "__main__":
    main()
