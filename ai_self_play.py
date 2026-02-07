#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI自我博弈学习程序
让AI通过与自己对战来提高经验和策略
"""

import sys
import os
import json
import random
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game.ofc_game import OFCGame
from game.player import Player
from ai.learning import RLAgent

class AISelfPlayLearner:
    def __init__(self, agent_name="SelfPlayAI", num_games=None, batch_size=150, save_interval=10):
        """
        初始化AI自我博弈学习器
        
        Args:
            agent_name: AI代理名称
            num_games: 自我博弈的游戏数量，None表示无限次数
            batch_size: 训练批次大小
            save_interval: 保存模型的游戏间隔
        """
        self.agent_name = agent_name
        self.num_games = num_games
        self.batch_size = batch_size
        self.save_interval = save_interval
        
        # 创建单个RLAgent实例，用于控制两个玩家
        self.agent = RLAgent(agent_name)
        
        # 学习统计
        self.stats = {
            "total_games": 0,
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "total_reward": 0,
            "average_reward": 0,
            "learning_steps": 0
        }
        
        # 经验存储统计
        self.experience_stats = {
            "regular_experiences": 0,
            "expert_experiences": 0,
            "error_experiences": 0
        }
    
    def create_players(self):
        """
        创建两个玩家，都由同一个RLAgent控制
        """
        player1 = Player(f"{self.agent_name}_1")
        player2 = Player(f"{self.agent_name}_2")
        return player1, player2
    
    def play_single_game(self, game_num):
        """
        进行一局AI自我博弈
        
        Args:
            game_num: 当前游戏编号
        """
        print(f"\n=== 第 {game_num} 局自我博弈开始 ===")
        
        # 创建游戏和玩家
        game = OFCGame()
        player1, player2 = self.create_players()
        
        # 添加玩家到游戏
        game.add_player(player1)
        game.add_player(player2)
        
        # 开始游戏
        game.start_game()
        
        # 第一轮发牌
        print(f"第一轮发牌完成，每个玩家获得5张牌")
        
        # 第一轮摆牌
        print("\n--- 第一轮摆牌 ---")
        self.ai_place_cards(game, player1, "Player1")
        self.ai_place_cards(game, player2, "Player2")
        # 显示第一轮摆完后的手牌
        print("\n--- 第一轮摆完后的手牌 ---")
        self.display_player_hand(player1)
        self.display_player_hand(player2)
        
        # 第二轮发牌（3张牌）
        print(f"\n第二轮发牌完成，每个玩家获得3张牌")
        for player in game.players:
            cards = game.deck.deal(3)
            for card in cards:
                player.add_card(card, 'temp')
        
        # 第二轮摆牌
        print("\n--- 第二轮摆牌 ---")
        self.ai_place_cards(game, player1, "Player1")
        self.ai_place_cards(game, player2, "Player2")
        # 显示第二轮摆完后的手牌
        print("\n--- 第二轮摆完后的手牌 ---")
        self.display_player_hand(player1)
        self.display_player_hand(player2)
        
        # 第三轮发牌（3张牌）
        print(f"\n第三轮发牌完成，每个玩家获得3张牌")
        for player in game.players:
            cards = game.deck.deal(3)
            for card in cards:
                player.add_card(card, 'temp')
        
        # 第三轮摆牌
        print("\n--- 第三轮摆牌 ---")
        self.ai_place_cards(game, player1, "Player1")
        self.ai_place_cards(game, player2, "Player2")
        # 显示第三轮摆完后的手牌
        print("\n--- 第三轮摆完后的手牌 ---")
        self.display_player_hand(player1)
        self.display_player_hand(player2)
        
        # 第四轮发牌（3张牌）
        print(f"\n第四轮发牌完成，每个玩家获得3张牌")
        for player in game.players:
            cards = game.deck.deal(3)
            for card in cards:
                player.add_card(card, 'temp')
        
        # 第四轮摆牌
        print("\n--- 第四轮摆牌 ---")
        self.ai_place_cards(game, player1, "Player1")
        self.ai_place_cards(game, player2, "Player2")
        # 显示第四轮摆完后的手牌
        print("\n--- 第四轮摆完后的手牌 ---")
        self.display_player_hand(player1)
        self.display_player_hand(player2)
        
        # 第五轮发牌（3张牌）
        print(f"\n第五轮发牌完成，每个玩家获得3张牌")
        for player in game.players:
            cards = game.deck.deal(3)
            for card in cards:
                player.add_card(card, 'temp')
        
        # 第五轮摆牌
        print("\n--- 第五轮摆牌 ---")
        self.ai_place_cards(game, player1, "Player1")
        self.ai_place_cards(game, player2, "Player2")
        # 显示第五轮摆完后的手牌
        print("\n--- 第五轮摆完后的手牌 ---\n")
        self.display_player_hand(player1)
        self.display_player_hand(player2)
        
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
                self.ai_place_cards(game, player, "Player" if player == player1 else "Player2")
        
        # 游戏结束，判定胜负
        print("\n--- 游戏结束，判定胜负 ---")
        winner = game.determine_winner()
        
        # 记录游戏结果
        if winner:
            print(f"获胜者: {winner.name}")
            if winner.name == player1.name:
                self.stats["wins"] += 1
                self.stats["losses"] += 1  # 因为是自我博弈，一个赢一个输
            else:
                self.stats["losses"] += 1
                self.stats["wins"] += 1
        else:
            print("平局")
            self.stats["draws"] += 1
        
        # 显示得分，使用与main.py相同的得分算法
        print("\n--- 得分情况 ---")
        
        if len(game.players) == 2:
            p1, p2 = game.players
            # 检查爆牌情况
            p1_busted = game.check_busted(p1)
            p2_busted = game.check_busted(p2)
            
            # 计算双方的牌型分
            p1_top_score = game.calculate_hand_score(p1.hand['top'], 'top')
            p1_middle_score = game.calculate_hand_score(p1.hand['middle'], 'middle')
            p1_bottom_score = game.calculate_hand_score(p1.hand['bottom'], 'bottom')
            p1_hand_score = p1_top_score + p1_middle_score + p1_bottom_score
            
            p2_top_score = game.calculate_hand_score(p2.hand['top'], 'top')
            p2_middle_score = game.calculate_hand_score(p2.hand['middle'], 'middle')
            p2_bottom_score = game.calculate_hand_score(p2.hand['bottom'], 'bottom')
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
                top_result = game.compare_hands(p1.hand['top'], p2.hand['top'])
                middle_result = game.compare_hands(p1.hand['middle'], p2.hand['middle'])
                bottom_result = game.compare_hands(p1.hand['bottom'], p2.hand['bottom'])
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
            
            # 显示本局得分
            print(f"{p1.name}: {p1_round_score} 分 (顶: {p1_top_score}, 中: {p1_middle_score}, 底: {p1_bottom_score})")
            print(f"{p2.name}: {p2_round_score} 分 (顶: {p2_top_score}, 中: {p2_middle_score}, 底: {p2_bottom_score})")
            
            # 显示爆牌情况
            if p1_busted:
                print(f"[爆牌] {p1.name}的手牌不符合规则！")
            if p2_busted:
                print(f"[爆牌] {p2.name}的手牌不符合规则！")
        else:
            # 多玩家情况
            for player in game.players:
                # 检查爆牌情况
                busted = game.check_busted(player)
                # 计算本局得分
                if busted:
                    round_score = 0
                    print(f"{player.name}: {round_score} 分")
                    print(f"[爆牌] {player.name}的手牌不符合规则！")
                else:
                    # 计算牌型分
                    top_score = game.calculate_hand_score(player.hand['top'], 'top')
                    middle_score = game.calculate_hand_score(player.hand['middle'], 'middle')
                    bottom_score = game.calculate_hand_score(player.hand['bottom'], 'bottom')
                    hand_score = top_score + middle_score + bottom_score
                    print(f"{player.name}: {hand_score} 分 (顶: {top_score}, 中: {middle_score}, 底: {bottom_score})")
        
        # 显示累计积分
        print("\n--- 累计积分 ---")
        for player in game.players:
            print(f"{player.name}: {player.total_score} 分")
        
        # 记录统计信息
        self.stats["total_games"] += 1
        
        # 学习步骤
        self.learn_from_game(game, player1, player2)
        
        print(f"\n=== 第 {game_num} 局自我博弈结束 ===")
        return winner
    
    def ai_place_cards(self, game, player, player_identifier):
        """
        AI自动摆牌，同时记录经验
        
        Args:
            game: 游戏对象
            player: 玩家对象
            player_identifier: 玩家标识符
        """
        temp_cards = player.hand.get('temp', [])
        print(f"{player.name} 需要摆放 {len(temp_cards)} 张牌")
        print("提示：按 'r' 键暂停游戏")
        
        # 一张一张地摆放牌
        while temp_cards:
            # 检查是否有键盘输入
            import msvcrt
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8', errors='ignore')
                if key.lower() == 'r':
                    print("\n游戏已暂停，按回车键继续...")
                    input()
                    print("游戏继续...")
            
            # 选择动作
            action = self.agent.choose_action(game, player)
            if action:
                card_index, area_index = action
                if card_index < len(temp_cards):
                    card = temp_cards[card_index]
                    areas = ['top', 'middle', 'bottom']
                    area = areas[area_index]
                    
                    # 检查区域是否已满
                    if len(player.hand.get(area, [])) < (3 if area == 'top' else 5):
                        # 执行摆牌并记录经验
                        self.execute_action_with_learning(game, player, action, area, card, player_identifier)
                        
                        # 更新临时牌列表
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
    
    def execute_action_with_learning(self, game, player, action, area, card, player_identifier):
        """
        执行动作并记录学习经验
        
        Args:
            game: 游戏对象
            player: 玩家对象
            action: 选择的动作
            area: 摆放区域
            card: 要摆放的牌
            player_identifier: 玩家标识符
        """
        # 获取当前状态
        old_state = self.agent.get_state(game, player)
        
        # 执行动作
        player.hand[area].append(card)
        player.hand['temp'].remove(card)
        
        # 获取新状态
        new_state = self.agent.get_state(game, player)
        
        # 检查是否所有牌都已摆放完成
        is_completed = not player.hand.get('temp', [])
        
        # 计算奖励
        reward = self.agent.calculate_reward(game, player, old_state, action, new_state)
        
        # 只有在摆牌完成或爆牌时才结束回合
        is_busted = game.check_busted(player)
        done = is_completed or is_busted
        
        # 获取下一个状态的可用动作
        next_actions = self.agent.get_actions(player)
        
        # 存储经验
        self.agent.store_experience(old_state, action, reward, new_state, next_actions, done)
        
        # 更新经验统计
        self.experience_stats["regular_experiences"] += 1
        
        # 记录总奖励
        self.stats["total_reward"] += reward
        
        # 从经验中学习
        if done:
            self.agent.train_from_replay(self.batch_size)
            self.stats["learning_steps"] += 1
    
    def learn_from_game(self, game, player1, player2):
        """
        从整局游戏中学习
        
        Args:
            game: 游戏对象
            player1: 玩家1
            player2: 玩家2
        """
        # 检查两个玩家是否爆牌
        player1_busted = game.check_busted(player1)
        player2_busted = game.check_busted(player2)
        
        # 如果一个玩家爆牌而另一个没有，记录错误决策
        if player1_busted and not player2_busted:
            print(f"[学习系统] {player1.name} 爆牌，记录错误决策")
            # 这里可以添加更详细的错误分析
        elif player2_busted and not player1_busted:
            print(f"[学习系统] {player2.name} 爆牌，记录错误决策")
            # 这里可以添加更详细的错误分析
        
        # 执行一次批量学习
        self.agent.train_from_replay(self.batch_size)
        self.stats["learning_steps"] += 1
    
    def card_to_str(self, card):
        """
        将牌对象转换为字符串
        """
        rank_map = {14: 'A', 13: 'K', 12: 'Q', 11: 'J', 10: 'T'}
        rank = rank_map.get(card.value, str(card.value))
        suit_map = {'S': '♠', 'H': '♥', 'D': '♦', 'C': '♣'}
        suit = suit_map.get(card.suit, card.suit)
        return f"{rank}{suit}"
    
    def run(self):
        """
        运行AI自我博弈学习程序
        """
        print("=== AI自我博弈学习程序开始 ===")
        if self.num_games is not None:
            print(f"计划进行 {self.num_games} 局自我博弈")
        else:
            print("无限次数运行，按Ctrl+C停止")
        print(f"学习参数: 批次大小={self.batch_size}, 保存间隔={self.save_interval}")
        
        start_time = datetime.now()
        game_count = 0
        
        try:
            while self.num_games is None or game_count < self.num_games:
                game_count += 1
                # 进行一局游戏
                self.play_single_game(game_count)
                
                # 定期保存模型
                if game_count % self.save_interval == 0:
                    self.save_learning_state(game_count)
                    self.display_stats(game_count)
        except KeyboardInterrupt:
            print("\n=== 程序被用户手动停止 ===")
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        # 最终保存和统计
        self.save_learning_state(game_count)
        self.display_final_stats(duration)
    
    def save_learning_state(self, game_num):
        """
        保存学习状态
        
        Args:
            game_num: 当前游戏编号
        """
        # 保存学习统计
        stats_filename = f"{self.agent_name}_selfplay_stats.json"
        with open(stats_filename, "w", encoding="utf-8") as f:
            json.dump(self.stats, f, ensure_ascii=False, indent=2)
        
        # 保存经验统计
        experience_filename = f"{self.agent_name}_experience_stats.json"
        with open(experience_filename, "w", encoding="utf-8") as f:
            json.dump(self.experience_stats, f, ensure_ascii=False, indent=2)
        
        print(f"\n=== 学习状态已保存 ({game_num} 局) ===")
    
    def display_stats(self, game_num):
        """
        显示当前学习统计
        
        Args:
            game_num: 当前游戏编号
        """
        print("\n=== 学习统计 ===")
        print(f"已完成游戏: {game_num}/{self.num_games}")
        print(f"胜率: {self.stats['wins']}/{game_num} ({self.stats['wins']/game_num*100:.2f}%)")
        print(f"平局率: {self.stats['draws']}/{game_num} ({self.stats['draws']/game_num*100:.2f}%)")
        print(f"总奖励: {self.stats['total_reward']}")
        print(f"平均奖励: {self.stats['total_reward']/game_num:.2f}")
        print(f"学习步骤: {self.stats['learning_steps']}")
        print("\n=== 经验统计 ===")
        print(f"普通经验: {self.experience_stats['regular_experiences']}")
        print(f"专家经验: {self.experience_stats['expert_experiences']}")
        print(f"错误经验: {self.experience_stats['error_experiences']}")
    
    def display_player_hand(self, player):
        """
        显示玩家当前的手牌状态
        
        Args:
            player: 玩家对象
        """
        print(f"\n{player.name} 当前手牌:")
        print(f"顶部区域: {[self.card_to_str(card) for card in player.hand.get('top', [])]}")
        print(f"中部区域: {[self.card_to_str(card) for card in player.hand.get('middle', [])]}")
        print(f"底部区域: {[self.card_to_str(card) for card in player.hand.get('bottom', [])]}")
        print(f"待摆放: {[self.card_to_str(card) for card in player.hand.get('temp', [])]}")
    
    def display_final_stats(self, duration):
        """
        显示最终学习统计
        
        Args:
            duration: 总学习时间
        """
        print("\n=== 最终学习统计 ===")
        print(f"总游戏数: {self.stats['total_games']}")
        print(f"获胜次数: {self.stats['wins']}")
        print(f"失败次数: {self.stats['losses']}")
        print(f"平局次数: {self.stats['draws']}")
        print(f"胜率: {self.stats['wins']/self.stats['total_games']*100:.2f}%")
        print(f"平局率: {self.stats['draws']/self.stats['total_games']*100:.2f}%")
        print(f"总奖励: {self.stats['total_reward']}")
        print(f"平均奖励: {self.stats['total_reward']/self.stats['total_games']:.2f}")
        print(f"学习步骤: {self.stats['learning_steps']}")
        print(f"总耗时: {duration}")
        print("\n=== 经验统计 ===")
        print(f"普通经验: {self.experience_stats['regular_experiences']}")
        print(f"专家经验: {self.experience_stats['expert_experiences']}")
        print(f"错误经验: {self.experience_stats['error_experiences']}")
        print("\n=== 学习完成 ===")

if __name__ == "__main__":
    # 创建并运行AI自我博弈学习器
    # 无限次数运行，按Ctrl+C停止
    learner = AISelfPlayLearner(
        agent_name="SelfPlayAI",
        num_games=None,
        batch_size=150,
        save_interval=5
    )
    learner.run()
