#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI vs AI 对战测试脚本
让两个AI玩家进行10局对战并记录结果
"""

import sys
import os
import random
import json
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game.ofc_game import OFCGame
from game.player import Player
from ai.learning import RLAgent

class AIVsAITest:
    def __init__(self, num_games=10):
        self.num_games = num_games
        self.game_results = []
        self.total_scores = {"AI1": 0, "AI2": 0}
    
    def create_ai_players(self):
        """
        创建两个AI玩家
        """
        # 创建AI 1
        ai1 = Player("AI1")
        ai1_agent = RLAgent("AI1")
        
        # 创建AI 2
        ai2 = Player("AI2")
        ai2_agent = RLAgent("AI2")
        
        return ai1, ai1_agent, ai2, ai2_agent
    
    def play_single_game(self, game_num):
        """
        进行一局AI对战
        """
        print(f"\n=== 第 {game_num} 局游戏开始 ===")
        
        # 创建游戏和玩家
        game = OFCGame()
        ai1, ai1_agent, ai2, ai2_agent = self.create_ai_players()
        
        # 添加玩家到游戏
        game.add_player(ai1)
        game.add_player(ai2)
        
        # 开始游戏
        game.start_game()
        print(f"第一轮发牌完成，每个玩家获得5张牌")
        
        # 第一轮摆牌
        print("\n--- 第一轮摆牌 ---")
        self.ai_place_cards(game, ai1, ai1_agent)
        self.ai_place_cards(game, ai2, ai2_agent)
        
        # 第二轮发牌（3张牌）
        # 手动发3张牌给每个玩家
        print(f"\n第二轮发牌完成，每个玩家获得3张牌")
        for player in game.players:
            cards = game.deck.deal(3)
            for card in cards:
                player.add_card(card, 'temp')
        
        # 第二轮摆牌
        print("\n--- 第二轮摆牌 ---")
        self.ai_place_cards(game, ai1, ai1_agent)
        self.ai_place_cards(game, ai2, ai2_agent)
        
        # 第三轮发牌（2张牌）
        # 手动发2张牌给每个玩家
        print(f"\n第三轮发牌完成，每个玩家获得2张牌")
        for player in game.players:
            cards = game.deck.deal(2)
            for card in cards:
                player.add_card(card, 'temp')
        
        # 第三轮摆牌
        print("\n--- 第三轮摆牌 ---")
        self.ai_place_cards(game, ai1, ai1_agent)
        self.ai_place_cards(game, ai2, ai2_agent)
        
        # 检查是否进入Fantasy Land
        print("\n--- 检查Fantasy Land ---")
        for player in game.players:
            if game.check_fantasy_mode(player):
                player.fantasy_mode = True
                print(f"{player.name} 进入 Fantasy Land 模式！")
        
        # Fantasy Land 阶段（如果有）
        for player in game.players:
            if hasattr(player, 'fantasy_mode') and player.fantasy_mode:
                print(f"\n--- {player.name} 的 Fantasy Land 阶段 ---")
                # 发3张牌
                fantasy_cards = game.deck.deal(3)
                player.hand['temp'] = fantasy_cards
                print(f"{player.name} 获得3张Fantasy Land牌")
                # 摆牌
                self.ai_place_cards(game, player, ai1_agent if player.name == "AI1" else ai2_agent)
        
        # 游戏结束，判定胜负
        print("\n--- 游戏结束，判定胜负 ---")
        winner = game.determine_winner()
        
        # 显示结果
        if winner:
            print(f"获胜者: {winner.name}")
            self.total_scores[winner.name] += 1
        else:
            print("平局")
        
        # 显示得分
        print("\n--- 得分情况 ---")
        game_scores = {}
        for player in game.players:
            # 计算各区域得分
            top_score = game.calculate_hand_score(player.hand.get('top', []), 'top')
            middle_score = game.calculate_hand_score(player.hand.get('middle', []), 'middle')
            bottom_score = game.calculate_hand_score(player.hand.get('bottom', []), 'bottom')
            total_score = top_score + middle_score + bottom_score
            game_scores[player.name] = total_score
            print(f"{player.name} 得分: {total_score} (顶: {top_score}, 中: {middle_score}, 底: {bottom_score})")
        
        # 记录结果
        game_result = {
            "game_num": game_num,
            "winner": winner.name if winner else "平局",
            "scores": game_scores
        }
        self.game_results.append(game_result)
        
        print(f"\n=== 第 {game_num} 局游戏结束 ===")
        return game_result
    
    def ai_place_cards(self, game, player, agent):
        """
        AI玩家自动摆牌
        """
        temp_cards = player.hand.get('temp', [])
        print(f"{player.name} 需要摆放 {len(temp_cards)} 张牌")
        
        # 一张一张地摆放牌
        while temp_cards:
            # 选择动作
            action = agent.choose_action(game, player)
            if action:
                card_index, area_index = action
                if card_index < len(temp_cards):
                    card = temp_cards[card_index]
                    areas = ['top', 'middle', 'bottom']
                    area = areas[area_index]
                    
                    # 检查区域是否已满
                    if len(player.hand.get(area, [])) < (3 if area == 'top' else 5):
                        # 执行摆牌
                        player.hand[area].append(card)
                        player.hand['temp'].pop(card_index)
                        temp_cards = player.hand.get('temp', [])
                        print(f"{player.name} 将 {self.card_to_str(card)} 放到 {area} 区域")
            else:
                # 如果没有可用动作，随机摆放
                if temp_cards:
                    card = temp_cards.pop(0)
                    # 找到第一个未满的区域
                    for area in ['top', 'middle', 'bottom']:
                        max_cards = 3 if area == 'top' else 5
                        if len(player.hand.get(area, [])) < max_cards:
                            player.hand[area].append(card)
                            print(f"{player.name} 随机将 {self.card_to_str(card)} 放到 {area} 区域")
                            break
    
    def card_to_str(self, card):
        """
        将牌对象转换为字符串
        """
        rank_map = {14: 'A', 13: 'K', 12: 'Q', 11: 'J', 10: 'T'}
        rank = rank_map.get(card.value, str(card.value))
        suit_map = {'S': '♠', 'H': '♥', 'D': '♦', 'C': '♣'}
        suit = suit_map.get(card.suit, card.suit)
        return f"{rank}{suit}"
    
    def run_tests(self):
        """
        运行所有测试游戏
        """
        print("=== AI vs AI 对战测试开始 ===")
        print(f"总共将进行 {self.num_games} 局游戏")
        
        start_time = datetime.now()
        
        for i in range(1, self.num_games + 1):
            self.play_single_game(i)
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        self.display_summary(duration)
    
    def display_summary(self, duration):
        """
        显示测试结果摘要
        """
        print("\n=== 测试结果摘要 ===")
        print(f"总共进行了 {self.num_games} 局游戏")
        print(f"总耗时: {duration}")
        print(f"\n胜负统计:")
        print(f"AI1 获胜: {self.total_scores['AI1']} 局")
        print(f"AI2 获胜: {self.total_scores['AI2']} 局")
        print(f"平局: {self.num_games - self.total_scores['AI1'] - self.total_scores['AI2']} 局")
        
        print("\n每局详细结果:")
        for result in self.game_results:
            print(f"第 {result['game_num']} 局: 获胜者={result['winner']}, 得分={result['scores']}")
        
        # 保存结果到文件
        self.save_results()
    
    def save_results(self):
        """
        保存测试结果到文件
        """
        results = {
            "total_games": self.num_games,
            "total_scores": self.total_scores,
            "game_results": self.game_results,
            "timestamp": datetime.now().isoformat()
        }
        
        with open("ai_vs_ai_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print("\n测试结果已保存到 ai_vs_ai_results.json")

if __name__ == "__main__":
    test = AIVsAITest(num_games=10)
    test.run_tests()
