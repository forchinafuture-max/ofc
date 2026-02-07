#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蒙特卡洛树搜索（MCTS）模块
用于OFC扑克游戏的决策过程
"""

import math
import random

class MCTSNode:
    """
    MCTS节点类
    """
    def __init__(self, state, parent=None, action=None):
        """
        初始化MCTS节点
        
        Args:
            state: 游戏状态
            parent: 父节点
            action: 导致当前状态的动作
        """
        self.state = state  # 游戏状态
        self.parent = parent  # 父节点
        self.action = action  # 导致当前状态的动作
        self.children = []  # 子节点
        self.visits = 0  # 访问次数
        self.value = 0  # 累计价值
        self.untried_actions = self.get_legal_actions(state)  # 未尝试的动作
    
    def get_legal_actions(self, state):
        """
        获取当前状态下的合法动作
        
        Args:
            state: 游戏状态，格式为(player, game)
            
        Returns:
            合法动作列表
        """
        if not state:
            return []
        
        player, game = state
        
        # 获取当前待摆放的牌
        temp_cards = player.hand.get('temp', [])
        if not temp_cards:
            return []
        
        # 生成所有可能的动作
        actions = []
        for i, card in enumerate(temp_cards):
            # 检查顶部区域
            if len(player.hand.get('top', [])) < 3:
                actions.append((i, 0))  # 0表示顶部区域
            
            # 检查中部区域
            if len(player.hand.get('middle', [])) < 5:
                actions.append((i, 1))  # 1表示中部区域
            
            # 检查底部区域
            if len(player.hand.get('bottom', [])) < 5:
                actions.append((i, 2))  # 2表示底部区域
        
        return actions
    
    def select_child(self):
        """
        使用UCT公式选择子节点
        
        Returns:
            选择的子节点
        """
        # 使用UCT公式选择子节点
        # UCB1公式: value/visits + c * sqrt(2*ln(parent_visits)/visits)
        c = 1.4  # 探索常数
        best_child = None
        best_score = -float('inf')
        
        for child in self.children:
            score = (child.value / child.visits) + c * math.sqrt(2 * math.log(self.visits) / child.visits)
            if score > best_score:
                best_score = score
                best_child = child
        
        return best_child
    
    def expand(self):
        """
        扩展子节点
        
        Returns:
            扩展的子节点
        """
        if not self.untried_actions:
            return self.select_child()
        
        # 选择一个未尝试的动作
        action = random.choice(self.untried_actions)
        self.untried_actions.remove(action)
        
        # 创建新的游戏状态
        new_state = self.simulate_action(self.state, action)
        
        # 创建新的子节点
        child = MCTSNode(new_state, self, action)
        self.children.append(child)
        
        return child
    
    def simulate_action(self, state, action):
        """
        模拟执行动作，返回新的游戏状态
        
        Args:
            state: 当前游戏状态，格式为(player, game)
            action: 要执行的动作，格式为(card_index, area_index)
            
        Returns:
            新的游戏状态
        """
        if not state or not action:
            return state
        
        player, game = state
        card_index, area_index = action
        
        # 创建玩家的深拷贝
        import copy
        new_player = copy.deepcopy(player)
        new_game = copy.deepcopy(game)
        
        # 获取待摆放的牌
        temp_cards = new_player.hand.get('temp', [])
        if card_index >= len(temp_cards):
            return (new_player, new_game)
        
        # 执行动作
        card = temp_cards[card_index]
        areas = ['top', 'middle', 'bottom']
        area = areas[area_index]
        
        # 检查区域是否已满
        if len(new_player.hand.get(area, [])) >= (3 if area == 'top' else 5):
            return (new_player, new_game)
        
        # 将牌放到指定区域
        new_player.hand[area].append(card)
        new_player.hand['temp'].pop(card_index)
        
        return (new_player, new_game)
    
    def simulate(self):
        """
        模拟游戏直到结束
        
        Returns:
            模拟结果的价值
        """
        if not self.state:
            return 0
        
        player, game = self.state
        
        # 模拟剩余的摆牌过程
        temp_cards = player.hand.get('temp', [])
        
        while temp_cards:
            # 随机选择一个合法动作
            legal_actions = self.get_legal_actions(self.state)
            if not legal_actions:
                break
            
            action = random.choice(legal_actions)
            self.state = self.simulate_action(self.state, action)
            player, game = self.state
            temp_cards = player.hand.get('temp', [])
        
        # 评估最终的手牌
        top_cards = player.hand.get('top', [])
        middle_cards = player.hand.get('middle', [])
        bottom_cards = player.hand.get('bottom', [])
        
        # 计算各区域的牌型强度
        try:
            top_strength = game.evaluate_hand(top_cards)
            middle_strength = game.evaluate_hand(middle_cards)
            bottom_strength = game.evaluate_hand(bottom_cards)
        except:
            # 如果评估失败，返回默认值
            top_strength = 0
            middle_strength = 0
            bottom_strength = 0
        
        # 计算价值
        value = 0
        
        # 区域强度顺序奖励
        if top_strength <= middle_strength <= bottom_strength:
            value += 1.0
        else:
            value -= 1.0
        
        # 各区域牌型强度奖励
        value += top_strength * 0.1
        value += middle_strength * 0.2
        value += bottom_strength * 0.3
        
        return value
    
    def backpropagate(self, value):
        """
        回溯价值
        
        Args:
            value: 模拟结果的价值
        """
        self.visits += 1
        self.value += value
        
        if self.parent:
            self.parent.backpropagate(-value)  # 对手的价值是相反的

class MCTS:
    """
    蒙特卡洛树搜索类
    """
    def __init__(self, iterations=1000):
        """
        初始化MCTS
        
        Args:
            iterations: 搜索迭代次数
        """
        self.iterations = iterations
    
    def search(self, initial_state):
        """
        执行MCTS搜索
        
        Args:
            initial_state: 初始游戏状态
            
        Returns:
            最佳动作
        """
        root = MCTSNode(initial_state)
        
        for _ in range(self.iterations):
            # 选择
            node = root
            while node.children and not node.untried_actions:
                node = node.select_child()
            
            # 扩展
            if node.untried_actions:
                node = node.expand()
            
            # 模拟
            value = node.simulate()
            
            # 回溯
            node.backpropagate(value)
        
        # 选择访问次数最多的子节点
        best_child = max(root.children, key=lambda c: c.visits)
        return best_child.action

    def best_action(self, root):
        """
        选择最佳动作
        
        Args:
            root: 根节点
            
        Returns:
            最佳动作
        """
        if not root.children:
            return None
        
        # 选择访问次数最多的子节点
        best_child = max(root.children, key=lambda c: c.visits)
        return best_child.action
