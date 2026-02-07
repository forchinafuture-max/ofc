#!/usr/bin/env python3
"""
主程序游戏脚本
玩家手动摆牌，AI自动决策，记录游戏过程到JSON文件
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game.ofc_game import OFCGame
from game.player import Player
from ai.ai_player import AIPlayer
from game.deck import Card

class MainGame:
    """主程序游戏"""
    
    def __init__(self, batch_mode=True, batch_steps_per_round=None):
        """初始化主程序游戏
        
        Args:
            batch_mode: 是否使用批处理模式
            batch_steps_per_round: 每轮的批处理步骤，格式为 {round_num: [(card_idx, area), ...]}
        """
        self.game = OFCGame()
        self.human_player = None
        self.ai_player = None
        self.batch_mode = batch_mode
        self.batch_steps_per_round = batch_steps_per_round or {}
        self.current_round = 1
        self.current_step = 0
    
    def setup_game(self):
        """设置游戏"""
        # 创建人类玩家
        self.human_player = Player("玩家a")
        
        # 创建AI玩家
        self.ai_player = AIPlayer("AI玩家", strategy_type="heuristic")
        
        # 添加玩家到游戏
        self.game.add_player(self.human_player)
        self.game.add_player(self.ai_player)
        
        print("游戏设置完成，玩家a为手动摆牌，AI玩家为自动摆牌")
    
    def display_hand(self, player):
        """显示玩家手牌"""
        print(f"\n{player.name}的手牌:")
        
        # 显示临时区域的牌
        temp_cards = player.hand['temp']
        print("临时区域:")
        for i, card in enumerate(temp_cards):
            print(f"  {i+1}. {self.card_to_str(card)}")
        
        # 显示各区域的牌
        print("顶部区域 (最多3张):")
        for card in player.hand['top']:
            print(f"  {self.card_to_str(card)}")
        
        print("中部区域 (最多5张):")
        for card in player.hand['middle']:
            print(f"  {self.card_to_str(card)}")
        
        print("底部区域 (最多5张):")
        for card in player.hand['bottom']:
            print(f"  {self.card_to_str(card)}")
    
    def card_to_str(self, card):
        """将卡牌对象转换为字符串"""
        value_map = {
            2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
            10: '10', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'
        }
        return f"{value_map.get(card.value, str(card.value))}{card.suit}"
    
    def get_user_input(self):
        """获取用户输入"""
        if self.batch_mode:
            # 批处理模式下，使用预设的步骤
            round_steps = self.batch_steps_per_round.get(self.current_round, [])
            if self.current_step < len(round_steps):
                card_idx, area = round_steps[self.current_step]
                self.current_step += 1
                print(f"批处理模式: 移动牌 {card_idx+1} 到 {area} 区域")
                return card_idx, area
            else:
                # 所有步骤都已执行完毕
                print("批处理模式: 所有摆牌步骤已执行完毕")
                return None, None
        else:
            # 交互式模式
            while True:
                try:
                    # 让用户选择要移动的牌和目标区域
                    card_idx = int(input("请输入要移动的牌的编号 (输入0结束摆牌): ")) - 1
                    if card_idx < 0:
                        return None, None
                    
                    area = input("请输入目标区域 (top/middle/bottom): ").lower()
                    if area not in ['top', 'middle', 'bottom']:
                        print("无效的区域，请重新输入")
                        continue
                    
                    return card_idx, area
                except ValueError:
                    print("无效的输入，请重新输入")
                    continue
    
    def manual_place_cards(self, player):
        """手动摆牌"""
        print(f"\n{player.name}，请开始摆牌:")
        
        while True:
            # 显示当前手牌
            self.display_hand(player)
            
            # 检查是否还有牌需要摆
            temp_cards = player.hand['temp']
            if not temp_cards:
                print("所有牌都已摆完")
                break
            
            # 获取用户输入
            card_idx, area = self.get_user_input()
            if card_idx is None:
                break
            
            # 检查牌的索引是否有效
            if card_idx >= len(temp_cards):
                print("无效的牌编号，请重新输入")
                continue
            
            # 检查目标区域是否已满
            if len(player.hand[area]) >= (3 if area == 'top' else 5):
                print(f"{area}区域已满，无法添加更多牌")
                continue
            
            # 移动牌
            card = temp_cards[card_idx]
            player.move_card(card, 'temp', area)
            print(f"已将 {self.card_to_str(card)} 移动到 {area} 区域")
    
    def play_game(self):
        """开始游戏"""
        # 设置游戏
        self.setup_game()
        
        # 开始游戏
        print("游戏开始！")
        
        # 重置游戏状态
        self.game.deck.reset()
        self.game.current_round = 0
        
        # 清空玩家手牌
        for player in self.game.players:
            player.clear_hand()
        
        # 记录游戏开始
        from core.logger import game_logger
        game_logger.start_game(self.game)
        
        # 第1轮：发5张牌并摆牌
        print("\n===== 第 1 轮 =====")
        print("发第一轮牌...")
        
        # 设置当前轮次和步骤
        self.game.current_round = 1
        self.current_round = 1
        self.current_step = 0  # 重置当前步骤
        
        # 调用游戏的发牌方法
        self.game.deal_round()
        
        # 显示人类玩家的手牌
        print("\n===== 第一轮发牌完成 =====")
        self.display_hand(self.human_player)
        
        # 人类玩家手动摆牌
        self.manual_place_cards(self.human_player)
        
        # AI玩家自动摆牌
        print("\n===== AI玩家开始摆牌 =====")
        self.ai_player.place_cards(self.game)
        
        # 第2-5轮：每轮发3张牌并摆牌
        for round_num in range(2, 6):
            print(f"\n===== 第 {round_num} 轮 =====")
            print(f"发第 {round_num} 轮牌...")
            
            # 设置当前轮次和步骤
            self.game.current_round = round_num
            self.current_round = round_num
            self.current_step = 0  # 重置当前步骤
            
            # 调用游戏的发牌方法
            self.game.deal_round()
            
            # 显示人类玩家的手牌
            print(f"\n===== 第 {round_num} 轮发牌完成 =====")
            self.display_hand(self.human_player)
            
            # 人类玩家手动摆牌
            self.manual_place_cards(self.human_player)
            
            # AI玩家自动摆牌
            print(f"\n===== AI玩家开始第 {round_num} 轮摆牌 =====")
            self.ai_player.place_cards(self.game)
        
        # 检查是否所有牌都已摆完
        for player in self.game.players:
            if player.hand['temp']:
                print(f"{player.name} 还有未摆完的牌")
        
        # 游戏结束
        print("\n===== 游戏结束 =====")
        print("五轮游戏结束，开始判定胜负")
        
        # 确定获胜者
        winner = self.game.determine_winner()
        print(f"获胜者: {winner.name if winner else '无获胜者'}")
        
        # 保存游戏记录
        from core.logger import game_logger
        game_logger.end_game(self.game, winner)
        
        # AI从游戏中学习
        if hasattr(self.ai_player, 'learn_from_game'):
            self.ai_player.learn_from_game(self.game, self.human_player)
        
        # 保存玩家的完整手牌和顶部手牌，用于Fantasy Land模式检查
        for player in self.game.players:
            if len(player.hand['top']) >= 3 and len(player.hand['middle']) >= 5 and len(player.hand['bottom']) >= 5:
                # 保存完整手牌，用于爆牌检查
                player.last_hand = {
                    'top': player.hand['top'].copy(),
                    'middle': player.hand['middle'].copy(),
                    'bottom': player.hand['bottom'].copy()
                }
                # 保存顶部手牌，用于牌型检查
                player.last_top_hand = player.hand['top']
        
        # 检查是否进入Fantasy Land模式
        for player in self.game.players:
            if hasattr(self.game, 'check_fantasy_mode'):
                self.game.check_fantasy_mode(player)
        
        # 检查是否有玩家进入范特西模式
        has_fantasy_players = any(getattr(player, 'fantasy_mode', False) for player in self.game.players)
        if has_fantasy_players:
            print("有玩家进入范特西模式，下一局将以范特西模式进行")

if __name__ == "__main__":
    # 默认使用批处理模式，为每轮设置不同的摆牌步骤
    # 第1轮：发5张牌，摆5张牌
    # 第2-5轮：每轮发3张牌，摆3张牌
    batch_steps_per_round = {
        1: [  # 第1轮：发5张牌
            (0, 'top'),    # 移动第1张牌到top区域
            (0, 'top'),    # 移动第2张牌到top区域（注意：索引会自动调整）
            (0, 'middle'), # 移动第1张剩余牌到middle区域
            (0, 'middle'), # 移动第2张剩余牌到middle区域
            (0, 'bottom'), # 移动第1张剩余牌到bottom区域
        ],
        2: [  # 第2轮：发3张牌
            (0, 'top'),    # 移动第1张牌到top区域
            (0, 'middle'), # 移动第2张牌到middle区域
            (0, 'bottom'), # 移动第3张牌到bottom区域
        ],
        3: [  # 第3轮：发3张牌
            (0, 'middle'), # 移动第1张牌到middle区域
            (0, 'middle'), # 移动第2张牌到middle区域
            (0, 'bottom'), # 移动第3张牌到bottom区域
        ],
        4: [  # 第4轮：发3张牌
            (0, 'middle'), # 移动第1张牌到middle区域
            (0, 'bottom'), # 移动第2张牌到bottom区域
            (0, 'bottom'), # 移动第3张牌到bottom区域
        ],
        5: [  # 第5轮：发3张牌
            (0, 'middle'), # 移动第1张牌到middle区域
            (0, 'bottom'), # 移动第2张牌到bottom区域
            (0, 'bottom'), # 移动第3张牌到bottom区域
        ],
    }
    
    # 创建游戏实例，使用批处理模式
    game = MainGame(batch_mode=True, batch_steps_per_round=batch_steps_per_round)
    game.play_game()
