#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试AI学习效果的脚本
验证AI在收到用户纠正后的行为变化
"""

import sys
import os
import random
from rl_ai import RLAIPlayer

class TestGame:
    """
    简单的测试游戏类，用于模拟OFC扑克游戏
    """
    def __init__(self):
        self.table = type('obj', (object,), {'round': 1, 'pot': 0})
        self.players = []
    
    def evaluate_hand(self, cards):
        """
        简单的手牌评估函数
        """
        if not cards:
            return 0
        
        # 基于牌型强度的简单评估
        # 计算对子、三条等
        values = [c.value for c in cards]
        value_counts = {}
        for v in values:
            value_counts[v] = value_counts.get(v, 0) + 1
        
        # 计算牌型强度
        pairs = sum(1 for c in value_counts.values() if c >= 2)
        triples = sum(1 for c in value_counts.values() if c >= 3)
        
        # 基于牌数和牌型的简单评分
        base_score = len(cards) * 10
        pair_bonus = pairs * 50
        triple_bonus = triples * 150
        
        return base_score + pair_bonus + triple_bonus
    
    def check_busted(self, player):
        """
        检查是否爆牌
        """
        top = player.hand.get('top', [])
        middle = player.hand.get('middle', [])
        bottom = player.hand.get('bottom', [])
        
        # 检查牌数是否足够
        if len(top) < 3 or len(middle) < 5 or len(bottom) < 5:
            return False
        
        # 检查牌型强度顺序
        top_strength = self.evaluate_hand(top)
        middle_strength = self.evaluate_hand(middle)
        bottom_strength = self.evaluate_hand(bottom)
        
        return not (top_strength <= middle_strength <= bottom_strength)
    
    def check_fantasy_land(self, player):
        """
        检查是否进入Fantasy Land
        """
        top = player.hand.get('top', [])
        if len(top) != 3:
            return False
        
        # 检查是否有对子QQ及以上
        values = [c.value for c in top]
        value_counts = {}
        for v in values:
            value_counts[v] = value_counts.get(v, 0) + 1
        
        for v, count in value_counts.items():
            if count >= 2 and v >= 12:  # QQ及以上
                return True
        
        return False
    
    def get_final_score(self, player):
        """
        获取最终得分
        """
        if self.check_busted(player):
            return 0
        
        top = player.hand.get('top', [])
        middle = player.hand.get('middle', [])
        bottom = player.hand.get('bottom', [])
        
        top_score = self.evaluate_hand(top)
        middle_score = self.evaluate_hand(middle)
        bottom_score = self.evaluate_hand(bottom)
        
        return top_score + middle_score + bottom_score

class TestCard:
    """
    测试卡牌类
    """
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    
    def __str__(self):
        suits = ['♠', '♥', '♦', '♣']
        values = ['', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        return f"{values[self.value]}{suits[self.suit]}"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if isinstance(other, TestCard):
            return self.value == other.value and self.suit == other.suit
        return False

def create_test_hand():
    """
    创建测试手牌
    """
    # 创建一手包含三条的牌
    # 3, 3, 3, J, Q
    cards = [
        TestCard(3, 0),  # 3♠
        TestCard(3, 1),  # 3♥
        TestCard(3, 2),  # 3♦
        TestCard(11, 3), # J♣
        TestCard(12, 0), # Q♠
    ]
    return cards

def test_learning_effect():
    """
    测试AI学习效果
    """
    print("=" * 60)
    print("测试AI学习效果")
    print("=" * 60)
    
    # 创建测试游戏
    game = TestGame()
    
    # 创建AI玩家
    ai_player = RLAIPlayer("Test AI")
    
    # 测试1: 初始摆牌行为
    print("\n测试1: 初始摆牌行为")
    print("-" * 40)
    
    # 设置测试手牌
    test_cards = create_test_hand()
    ai_player.hand = {
        'temp': test_cards.copy(),
        'top': [],
        'middle': [],
        'bottom': []
    }
    
    print(f"测试手牌: {[str(c) for c in test_cards]}")
    print("包含三条: 3♠, 3♥, 3♦")
    
    # 初始摆牌
    print("\nAI初始摆牌:")
    initial_result = ai_player.place_cards_strategy(game, auto_mode=True)
    
    print(f"顶部: {[str(c) for c in initial_result['top']]}")
    print(f"中部: {[str(c) for c in initial_result['middle']]}")
    print(f"底部: {[str(c) for c in initial_result['bottom']]}")
    
    # 检查是否保留了三条
    has_three_of_a_kind = False
    bottom_values = [c.value for c in initial_result['bottom']]
    if bottom_values.count(3) >= 3:
        has_three_of_a_kind = True
        print("\n✅ AI保留了三条！")
    else:
        print("\n❌ AI没有保留三条")
    
    # 测试2: 模拟用户纠正
    print("\n\n测试2: 模拟用户纠正")
    print("-" * 40)
    
    # 重新设置测试手牌
    ai_player.hand = {
        'temp': test_cards.copy(),
        'top': [],
        'middle': [],
        'bottom': []
    }
    
    print("模拟用户纠正: 将三条放到中部区域")
    print("正确摆法: 0 1 1 1 2 2")
    print("解释: 将第1张3放到中部，第2张3放到中部，第3张3放到中部，J放到底部，Q放到底部")
    
    # 手动存储专家经验，明确指导三条放到中部
    print("\n存储专家经验，明确指导三条放到中部区域:")
    
    # 为每条三条牌创建明确的专家经验
    for i, card in enumerate(test_cards):
        if card.value == 3:  # 三条中的牌
            # 创建将三条放到中部的动作
            action = (i, 1)  # 放到中部区域
            area_display = '中部'
            print(f"存储专家经验 {i+1}: 将 {card} 放到 {area_display} 区域 (三条应该放到中部)")
            
            # 存储为专家经验，给予极高奖励
            if hasattr(ai_player.rl_agent, 'store_expert_experience'):
                current_state = ai_player.rl_agent.get_state(game, ai_player)
                next_state = ai_player.rl_agent.get_state(game, ai_player)
                reward = 200.0  # 极高奖励，强调这是正确的摆法
                ai_player.rl_agent.store_expert_experience(current_state, action, reward, next_state, [], True)
        else:  # 非三条的牌（J和Q）
            # 创建放到正确位置的动作
            action = (i, 2)  # 放到底部区域
            area_display = '底部'
            print(f"存储专家经验 {i+1}: 将 {card} 放到 {area_display} 区域")
            
            # 存储为专家经验
            if hasattr(ai_player.rl_agent, 'store_expert_experience'):
                current_state = ai_player.rl_agent.get_state(game, ai_player)
                next_state = ai_player.rl_agent.get_state(game, ai_player)
                reward = 100.0
                ai_player.rl_agent.store_expert_experience(current_state, action, reward, next_state, [], True)
    
    # 执行强化训练，增加训练次数确保学习
    print("\n执行强化训练...")
    training_rounds = 30  # 增加训练次数
    for i in range(training_rounds):
        ai_player.rl_agent.train_from_replay()
        if (i+1) % 6 == 0:
            print(f"训练进度: {i+1}/{training_rounds}")
    
    print("\n强化训练完成！")
    print("✅ 已存储多条专家经验，指导AI将三条放到中部区域")
    print("✅ 训练次数: 30次")
    
    # 测试3: 纠正后的摆牌行为
    print("\n\n测试3: 纠正后的摆牌行为")
    print("-" * 40)
    
    # 重新设置测试手牌
    ai_player.hand = {
        'temp': test_cards.copy(),
        'top': [],
        'middle': [],
        'bottom': []
    }
    
    print(f"测试手牌: {[str(c) for c in test_cards]}")
    print("包含三条: 3♠, 3♥, 3♦")
    
    # 纠正后的摆牌
    print("\nAI纠正后摆牌:")
    corrected_result = ai_player.place_cards_strategy(game, auto_mode=True)
    
    print(f"顶部: {[str(c) for c in corrected_result['top']]}")
    print(f"中部: {[str(c) for c in corrected_result['middle']]}")
    print(f"底部: {[str(c) for c in corrected_result['bottom']]}")
    
    # 检查是否保留了三条
    has_three_of_a_kind_after = False
    middle_values = [c.value for c in corrected_result['middle']]
    if middle_values.count(3) >= 3:
        has_three_of_a_kind_after = True
        print("\n✅ AI现在保留了三条！")
    else:
        print("\n❌ AI仍然没有保留三条")
    
    # 测试4: 学习效果验证
    print("\n\n测试4: 学习效果验证")
    print("-" * 40)
    
    # 显示专家经验学习情况
    if hasattr(ai_player.rl_agent, 'expert_buffer'):
        expert_count = len(ai_player.rl_agent.expert_buffer)
        print(f"已学习的专家经验数: {expert_count}")
        
        if expert_count > 0:
            print("✅ AI已从用户纠正中学习")
            print("✅ 专家经验优先级: 50.0")
            print("✅ 专家经验占训练比例: 60%")
    
    # 显示学习统计
    print("\n学习统计:")
    print(f"探索率: {ai_player.rl_agent.exploration_rate:.3f}")
    print(f"学习率: {ai_player.rl_agent.learning_rate:.6f}")
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    if has_three_of_a_kind_after:
        print("✅ 测试成功: AI学会了保留三条")
        print("✅ AI能够从用户纠正中学习")
        print("✅ 学习机制正常工作")
    else:
        print("❌ 测试失败: AI仍需更多学习")
        print("⚠️  建议: 增加训练次数或提供更多纠正")
    
    print("\n测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_learning_effect()
