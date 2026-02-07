import numpy as np
import random
import json
import os
from datetime import datetime

def is_aa_on_top(top_cards):
    """
    检查顶部区域是否是AA
    """
    if len(top_cards) != 3:
        return False
    
    # 检查是否有两张A
    ace_count = 0
    for card in top_cards:
        if card.value == 14:  # A的value是14
            ace_count += 1
    
    return ace_count == 2

# 尝试导入PyTorch，如果失败则使用占位实现
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    import torch.nn.functional as F
    has_torch = True
    
    class DuelingDQN(nn.Module):
        """
        Dueling DQN神经网络，分开估计状态价值和优势函数
        """
        def __init__(self, state_dim, action_dim):
            super(DuelingDQN, self).__init__()
            
            # 共享特征提取网络
            self.feature = nn.Sequential(
                nn.Linear(state_dim, 128),
                nn.ReLU(),
                nn.Linear(128, 64),
                nn.ReLU()
            )
            
            # 价值流（估计状态价值）
            self.value_stream = nn.Sequential(
                nn.Linear(64, 32),
                nn.ReLU(),
                nn.Linear(32, 1)
            )
            
            # 优势流（估计优势函数）
            self.advantage_stream = nn.Sequential(
                nn.Linear(64, 32),
                nn.ReLU(),
                nn.Linear(32, action_dim)
            )
        
        def forward(self, state):
            features = self.feature(state)
            value = self.value_stream(features)
            advantage = self.advantage_stream(features)
            
            # 计算Q值：V(s) + (A(s,a) - mean(A(s,a)))
            q_values = value + (advantage - advantage.mean(dim=1, keepdim=True))
            return q_values
except ImportError:
    print("PyTorch导入失败，使用占位实现")
    has_torch = False
    
    class DuelingDQN:
        """
        占位实现，当PyTorch不可用时使用
        """
        def __init__(self, state_dim, action_dim):
            pass
        
        def forward(self, state):
            pass
        
        def parameters(self):
            return []

class RLAgent:
    def __init__(self, name, learning_rate=0.001, discount_factor=0.95, exploration_rate=1.0, exploration_decay=0.99):
        self.name = name
        self.initial_learning_rate = learning_rate
        self.learning_rate = 0.001  # 保持适中的学习率
        self.discount_factor = 0.99  # 增加折扣因子，更重视长期奖励
        self.exploration_rate = 1.0  # 初始探索率
        self.exploration_decay = 0.995  # 适中的探索率衰减速度
        self.min_exploration_rate = 0.2  # 保持较高的最小探索率
        self.learning_rate_decay = 0.9999  # 非常慢的学习率衰减速度
        self.min_learning_rate = 0.0005  # 保持较高的最小学习率
        
        # Q-table 用于存储状态-动作值（作为备份）
        self.q_table = {}
        
        # 目标Q-table，用于提高学习稳定性（作为备份）
        self.target_q_table = {}
        self.target_update_frequency = 50  # 减少目标网络更新频率，提高学习稳定性
        self.update_count = 0
        
        # 经验回放缓冲区
        self.replay_buffer = []
        self.buffer_size = 20000  # 增加经验回放缓冲区大小
        
        # 专家经验池
        self.expert_buffer = []  # 存储用户手动操作的经验
        self.expert_buffer_size = 8000  # 增加专家经验池大小
        self.expert_priorities = []  # 专家经验的优先级
        
        # 错误记录缓冲区
        self.error_buffer = []  # 存储AI的错误决策
        self.error_buffer_size = 3000  # 增加错误记录缓冲区大小
        self.error_priorities = []  # 错误记录的优先级
        
        # 优先经验回放相关组件
        self.use_prioritized_replay = has_torch
        self.priorities = []  # 存储经验的优先级
        self.alpha = 0.6  # 优先级权重
        self.beta = 0.4  # 重要性采样权重
        self.beta_increment = 0.001  # beta的增量
        self.epsilon = 1e-6  # 避免优先级为0
        
        # Dueling DQN相关组件
        self.use_dueling_dqn = has_torch
        self.state_dim = 32  # 状态维度：5*2+3*2+5*2+5*2+4=32（包含高级牌型特征）
        self.action_dim = 15  # 动作维度：5张牌 * 3个区域 = 15，修复溢出问题
        
        if self.use_dueling_dqn:
            # 主网络
            self.model = DuelingDQN(self.state_dim, self.action_dim)
            # 目标网络
            self.target_model = DuelingDQN(self.state_dim, self.action_dim)
            # 优化器
            self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
            # 损失函数
            self.loss_fn = nn.MSELoss()
            # 复制参数到目标网络
            self.update_target_network()
        
        # 加载学习数据
        self.load_learning_data()
    
    def update_target_network(self):
        """
        更新目标网络参数，从主网络复制
        """
        if self.use_dueling_dqn:
            self.target_model.load_state_dict(self.model.state_dict())
            print("目标网络已更新")
    
    def _evaluate_hand_strength(self, cards):
        """
        评估牌型强度，返回高级牌型特征
        """
        # 安全获取数值的辅助函数
        def safe_float(value):
            try:
                return float(value)
            except (ValueError, TypeError):
                return 0.0
        
        if len(cards) < 2:
            return [0, 0, 0, 0]
        
        # 提取牌值和花色
        values = []
        suits = []
        for card in cards:
            try:
                values.append(safe_float(card[0]))
                suits.append(safe_float(card[1]))
            except (ValueError, TypeError):
                pass
        
        if len(values) < 2:
            return [0, 0, 0, 0]
        
        # 检查对子
        value_counts = {}
        for v in values:
            value_counts[v] = value_counts.get(v, 0) + 1
        
        has_pair = 0
        has_straight = 0
        has_flush = 0
        has_high_pair = 0
        
        # 检查对子
        for count in value_counts.values():
            if count >= 2:
                has_pair = 1
                break
        
        # 检查高对子（QQ+）
        for v, count in value_counts.items():
            if count >= 2 and v >= 12:
                has_high_pair = 1
                break
        
        # 检查顺子（至少5张牌）
        if len(values) >= 5:
            sorted_values = sorted(values)
            is_straight = True
            for i in range(1, len(sorted_values)):
                if sorted_values[i] != sorted_values[i-1] + 1:
                    is_straight = False
                    break
            if is_straight:
                has_straight = 1
        
        # 检查同花（至少5张牌）
        if len(suits) >= 5:
            suit_counts = {}
            for s in suits:
                suit_counts[s] = suit_counts.get(s, 0) + 1
            for count in suit_counts.values():
                if count >= 5:
                    has_flush = 1
                    break
        
        return [has_pair, has_high_pair, has_straight, has_flush]
    
    def state_to_tensor(self, state):
        """
        将状态转换为张量，用于Dueling DQN
        增强状态表示，添加顺子、同花等高级牌型的特征提取
        """
        if not self.use_dueling_dqn:
            return None
        
        # 增强的状态编码
        state_vector = []
        
        # 安全获取数值的辅助函数
        def safe_float(value):
            try:
                return float(value)
            except (ValueError, TypeError):
                return 0.0
        
        # 编码待摆放的牌
        temp_cards = state[0]
        for i in range(5):
            if i < len(temp_cards):
                value = safe_float(temp_cards[i][0])
                suit = safe_float(temp_cards[i][1])
                state_vector.extend([value / 14.0, suit / 4.0])
            else:
                state_vector.extend([0, 0])
        
        # 编码顶部区域的牌
        top_cards = state[1]
        for i in range(3):
            if i < len(top_cards):
                value = safe_float(top_cards[i][0])
                suit = safe_float(top_cards[i][1])
                state_vector.extend([value / 14.0, suit / 4.0])
            else:
                state_vector.extend([0, 0])
        
        # 编码中部区域的牌
        middle_cards = state[2]
        for i in range(5):
            if i < len(middle_cards):
                value = safe_float(middle_cards[i][0])
                suit = safe_float(middle_cards[i][1])
                state_vector.extend([value / 14.0, suit / 4.0])
            else:
                state_vector.extend([0, 0])
        
        # 编码底部区域的牌
        bottom_cards = state[3]
        for i in range(5):
            if i < len(bottom_cards):
                value = safe_float(bottom_cards[i][0])
                suit = safe_float(bottom_cards[i][1])
                state_vector.extend([value / 14.0, suit / 4.0])
            else:
                state_vector.extend([0, 0])
        
        # 增强特征：高级牌型检测
        # 检查中部区域牌型
        middle_features = self._evaluate_hand_strength(middle_cards)
        # 检查底部区域牌型
        bottom_features = self._evaluate_hand_strength(bottom_cards)
        
        # 添加高级牌型特征
        state_vector.extend(middle_features)
        state_vector.extend(bottom_features)
        
        # 确保状态向量长度为state_dim
        while len(state_vector) < self.state_dim:
            state_vector.append(0)
        state_vector = state_vector[:self.state_dim]
        
        # 转换为张量
        state_tensor = torch.tensor(state_vector, dtype=torch.float32).unsqueeze(0)
        return state_tensor
    
    def get_state(self, game, player):
        """
        获取当前游戏状态
        状态表示：
        1. 待摆放的牌（按值排序，包含花色信息）
        2. 顶部区域的牌（按值排序，包含花色信息）
        3. 中部区域的牌（按值排序，包含花色信息）
        4. 底部区域的牌（按值排序，包含花色信息）
        5. 当前游戏轮次
        6. 玩家筹码量（如果存在）
        7. 当前锅底大小（如果存在）
        """
        # 待摆放的牌
        temp_cards = sorted(player.hand.get('temp', []), key=lambda x: (x.value, x.suit))
        temp_cards_state = tuple([(card.value, card.suit) for card in temp_cards])
        
        # 已摆放的牌
        top_cards = sorted(player.hand.get('top', []), key=lambda x: (x.value, x.suit))
        top_cards_state = tuple([(card.value, card.suit) for card in top_cards])
        
        middle_cards = sorted(player.hand.get('middle', []), key=lambda x: (x.value, x.suit))
        middle_cards_state = tuple([(card.value, card.suit) for card in middle_cards])
        
        bottom_cards = sorted(player.hand.get('bottom', []), key=lambda x: (x.value, x.suit))
        bottom_cards_state = tuple([(card.value, card.suit) for card in bottom_cards])
        
        # 当前游戏轮次
        round_num = game.table.round if hasattr(game, 'table') and hasattr(game.table, 'round') else 1
        
        # 玩家筹码量
        chips = getattr(player, 'chips', 1000)  # 默认值1000
        
        # 当前锅底大小
        pot_size = game.table.pot if hasattr(game, 'table') and hasattr(game.table, 'pot') else 0
        
        # 组合状态
        state = (temp_cards_state, top_cards_state, middle_cards_state, bottom_cards_state, round_num, chips, pot_size)
        return state
    
    def get_actions(self, player):
        """
        获取当前可用的动作
        动作表示：
        (card_index, area_index)
        card_index: 待摆放牌的索引
        area_index: 摆放区域索引（0: 顶部, 1: 中部, 2: 底部）
        """
        # 对牌进行排序，与get_state方法保持一致，确保动作索引正确
        temp_cards = sorted(player.hand.get('temp', []), key=lambda x: (x.value, x.suit))
        actions = []
        
        # 对于每张待摆放的牌，考虑所有可能的摆放区域
        for i, card in enumerate(temp_cards):
            # 顶部区域最多3张
            if len(player.hand.get('top', [])) < 3:
                actions.append((i, 0))
            
            # 中部区域最多5张
            if len(player.hand.get('middle', [])) < 5:
                actions.append((i, 1))
            
            # 底部区域最多5张
            if len(player.hand.get('bottom', [])) < 5:
                actions.append((i, 2))
        
        return actions
    
    def choose_action(self, game, player):
        """
        根据改进的策略选择动作，支持Dueling DQN
        """
        state = self.get_state(game, player)
        actions = self.get_actions(player)
        
        if not actions:
            return None
        
        # 探索
        if random.random() < self.exploration_rate:
            # 真正的随机探索，给所有动作平等的机会
            # 50%的概率完全随机选择，50%的概率基于概率选择
            if random.random() < 0.5:
                # 完全随机选择，给所有动作平等的机会
                return random.choice(actions)
            else:
                # 基于概率的探索，但降低win_prob的权重
                action_probabilities = []
                for action in actions:
                    win_prob = self.calculate_win_probability(game, player, action, state)
                    # 大幅降低win_prob的权重，增加随机性
                    prob = win_prob * 0.3 + 0.7 * (1.0 / len(actions))
                    action_probabilities.append((prob, action))
                
                # 归一化概率
                total_prob = sum(p for p, a in action_probabilities)
                normalized_probabilities = [(p/total_prob, a) for p, a in action_probabilities]
                
                # 基于概率选择动作
                rand = random.random()
                cumulative = 0
                for prob, action in normalized_probabilities:
                    cumulative += prob
                    if rand <= cumulative:
                        return action
                return random.choice(actions)
        
        # 利用
        else:
            if self.use_dueling_dqn:
                # 使用Dueling DQN选择动作
                return self._choose_action_dueling_dqn(game, player, state, actions)
            else:
                # 使用传统策略选择动作
                # 综合考虑Q值、获胜概率和牌型潜力
                action_scores = []
                for action in actions:
                    q_value = self.get_q_value(state, action)
                    win_prob = self.calculate_win_probability(game, player, action, state)
                    
                    # 模拟摆牌后的手牌状态，计算潜力
                    temp_hand = {
                        'top': player.hand.get('top', []).copy(),
                        'middle': player.hand.get('middle', []).copy(),
                        'bottom': player.hand.get('bottom', []).copy(),
                        'temp': sorted(player.hand.get('temp', []).copy(), key=lambda x: (x.value, x.suit))
                    }
                    
                    # 执行动作
                    if action:
                        card_index, area_index = action
                        if card_index < len(temp_hand['temp']):
                            card = temp_hand['temp'][card_index]
                            areas = ['top', 'middle', 'bottom']
                            area = areas[area_index]
                            temp_hand[area].append(card)
                            temp_hand['temp'].pop(card_index)
                    
                    # 计算各区域的潜在发展潜力
                    top_potential = self.calculate_card_potential(temp_hand['top'])
                    middle_potential = self.calculate_card_potential(temp_hand['middle'])
                    bottom_potential = self.calculate_card_potential(temp_hand['bottom'])
                    total_potential = top_potential + middle_potential + bottom_potential
                    
                    # 综合得分 - 调整权重，增加潜力的重要性
                    score = q_value * 0.6 + win_prob * 12 + total_potential * 8  # 降低win_prob权重，提高total_potential权重
                    action_scores.append((score, action))
                
                # 选择得分最高的动作
                action_scores.sort(reverse=True, key=lambda x: x[0])
                return action_scores[0][1]
    
    def _choose_action_dueling_dqn(self, game, player, state, actions):
        """
        使用Dueling DQN选择动作
        """
        if not self.use_dueling_dqn or not actions:
            return random.choice(actions)

        state_tensor = self.state_to_tensor(state)
        with torch.no_grad():
            q_values = self.model(state_tensor).squeeze(0)

        best_score = -float('inf')
        best_action = None

        for action in actions:
            card_idx, area_index = action
            # 修改映射逻辑：确保索引在 0-29 之间（5张待选牌 * 3个区域 = 15，剩下15个留作备用或扩展）
            # 这样 AI 学习时，每个神经元都有明确的物理意义
            action_idx = card_idx * 3 + area_index
            
            q_value = q_values[action_idx].item()
            win_prob = self.calculate_win_probability(game, player, action, state)

            # 综合得分：Q值决定长期收益，win_prob 决定短期存活，降低win_prob权重
            score = q_value * 0.7 + win_prob * 10
            
            if score > best_score:
                best_score = score
                best_action = action
                
        return best_action
    
    def get_q_value(self, state, action, use_target=False):
        """
        获取状态-动作对的Q值
        """
        q_table = self.target_q_table if use_target else self.q_table
        
        if state not in q_table:
            q_table[state] = {}
        
        if action not in q_table[state]:
            q_table[state][action] = 0.0
        
        return q_table[state][action]
    
    def choose_action_based_on_evaluations(self, game, player, top_actions, mcts_evaluations):
        """
        基于MCTS评估结果做最终决定
        """
        try:
            if not top_actions:
                # 如果没有可用动作，返回None
                return None
            
            if not mcts_evaluations:
                # 如果没有MCTS评估结果，返回第一个动作
                return top_actions[0]
            
            # 综合考虑原始分数和MCTS评估分数
            final_scores = []
            
            for i, action in enumerate(top_actions):
                # 找到该动作的MCTS评估分数
                mcts_score = 0
                for score, eval_action in mcts_evaluations:
                    if eval_action == action:
                        mcts_score = score
                        break
                
                # 获取当前状态
                current_state = self.get_state(game, player)
                
                # 计算原始分数
                q_value = self.get_q_value(current_state, action)
                win_prob = self.calculate_win_probability(game, player, action, current_state)
                
                # 模拟摆牌后的手牌状态，计算潜力
                temp_hand = {
                    'top': player.hand.get('top', []).copy(),
                    'middle': player.hand.get('middle', []).copy(),
                    'bottom': player.hand.get('bottom', []).copy(),
                    'temp': sorted(player.hand.get('temp', []).copy(), key=lambda x: (x.value, x.suit))
                }
                
                # 执行动作
                if action:
                    card_index, area_index = action
                    if card_index < len(temp_hand['temp']):
                        card = temp_hand['temp'][card_index]
                        areas = ['top', 'middle', 'bottom']
                        area = areas[area_index]
                        temp_hand[area].append(card)
                        temp_hand['temp'].pop(card_index)
                
                # 计算各区域的潜在发展潜力
                top_potential = self.calculate_card_potential(temp_hand['top'])
                middle_potential = self.calculate_card_potential(temp_hand['middle'])
                bottom_potential = self.calculate_card_potential(temp_hand['bottom'])
                total_potential = top_potential + middle_potential + bottom_potential
                
                # 综合得分，加入MCTS评估分数
                final_score = q_value * 0.6 + win_prob * 12 + total_potential * 8 + mcts_score * 0.1
                final_scores.append((final_score, action))
            
            # 按最终得分排序，返回得分最高的动作
            final_scores.sort(reverse=True, key=lambda x: x[0])
            return final_scores[0][1]
        except Exception as e:
            print(f"基于评估结果选择动作出错: {e}")
            # 如果出错，返回第一个动作
            return top_actions[0] if top_actions else None
    
    def update_q_value(self, state, action, reward, next_state, next_actions):
        """
        更新Q值
        """
        # 获取当前Q值
        current_q = self.get_q_value(state, action)
        
        # 计算最大未来Q值（使用目标Q-table）
        max_future_q = 0
        if next_actions:
            future_q_values = [self.get_q_value(next_state, next_action, use_target=True) for next_action in next_actions]
            max_future_q = max(future_q_values)
        
        # 更新Q值
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_future_q - current_q)
        self.q_table[state][action] = new_q
        
        # 增加更新计数
        self.update_count += 1
        
        # 定期更新目标Q-table
        if self.update_count % self.target_update_frequency == 0:
            self.update_target_q_table()
        
        # 衰减学习率
        self.learning_rate = max(self.min_learning_rate, self.learning_rate * self.learning_rate_decay)
    
    def update_target_q_table(self):
        """
        更新目标Q-table
        """
        # 深拷贝当前Q-table到目标Q-table
        import copy
        self.target_q_table = copy.deepcopy(self.q_table)
        print(f"目标Q-table已更新，当前更新计数: {self.update_count}")
    
    def store_experience(self, state, action, reward, next_state, next_actions, done):
        """
        存储经验到回放缓冲区，支持优先经验回放
        """
        experience = (state, action, reward, next_state, next_actions, done)
        self.replay_buffer.append(experience)
        
        # 存储优先级，新经验的优先级设为最高
        if self.use_prioritized_replay and self.priorities:
            max_priority = max(self.priorities)
        else:
            max_priority = 1.0
        self.priorities.append(max_priority)
        
        # 保持缓冲区大小
        if len(self.replay_buffer) > self.buffer_size:
            self.replay_buffer.pop(0)
            if self.use_prioritized_replay:
                self.priorities.pop(0)
    
    def store_expert_experience(self, state, action, reward, next_state, next_actions, done):
        """
        存储用户手动操作的经验到专家经验池，以高优先级存储
        """
        experience = (state, action, reward, next_state, next_actions, done)
        self.expert_buffer.append(experience)
        
        # 以极高优先级存储专家经验，确保用户的摆法能够优先影响AI的决策
        high_priority = 50.0  # 专家经验的优先级设为极高值
        self.expert_priorities.append(high_priority)
        
        # 保持专家经验池大小
        if len(self.expert_buffer) > self.expert_buffer_size:
            self.expert_buffer.pop(0)
            self.expert_priorities.pop(0)
        
        # 增加专家经验的权重，确保用户的摆法能够更明显地影响AI
        print(f"[学习系统] 存储用户专家经验，优先级: {high_priority}")
    
    def record_error_decision(self, state, wrong_action, correct_action, game, player):
        """
        记录AI的错误决策，并提供正确的动作建议
        """
        # 计算错误动作的奖励（惩罚）
        wrong_reward = -50  # 错误决策的惩罚
        
        # 计算正确动作的奖励
        # 模拟执行正确动作
        temp_cards = player.hand.get('temp', [])
        if correct_action:
            card_index, area_index = correct_action
            if card_index < len(temp_cards):
                card = temp_cards[card_index]
                areas = ['top', 'middle', 'bottom']
                area = areas[area_index]
                # 临时执行动作
                player.hand[area].append(card)
                player.hand['temp'].pop(card_index)
                
                # 计算新状态
                new_state = self.get_state(game, player)
                
                # 计算正确动作的奖励
                correct_reward = self.calculate_reward(game, player, state, correct_action, new_state)
                
                # 恢复原始状态
                player.hand['temp'].append(card)
                player.hand[area].pop()
            else:
                correct_reward = 0
        else:
            correct_reward = 0
        
        # 存储错误决策经验
        wrong_experience = (state, wrong_action, wrong_reward, state, self.get_actions(player), True)
        self.error_buffer.append(wrong_experience)
        
        # 以极高优先级存储错误决策
        very_high_priority = 20.0  # 错误决策的优先级设为极高值
        self.error_priorities.append(very_high_priority)
        
        # 存储正确动作经验
        if correct_action:
            correct_experience = (state, correct_action, correct_reward, state, self.get_actions(player), True)
            self.error_buffer.append(correct_experience)
            self.error_priorities.append(very_high_priority)
        
        # 保持错误记录缓冲区大小
        while len(self.error_buffer) > self.error_buffer_size:
            self.error_buffer.pop(0)
            self.error_priorities.pop(0)
        
        print(f"已记录错误决策，状态: {state}, 错误动作: {wrong_action}, 正确动作: {correct_action}")
    
    def train_from_replay(self, batch_size=150):
        """
        从经验回放中训练，支持Dueling DQN和优先经验回放
        强制抽取60%的专家经验和30%的错误记录，确保用户的摆法能够优先影响AI
        """
        # 计算各类型经验的采样数量
        expert_batch_size = int(batch_size * 0.6)  # 增加专家经验的比例到60%
        error_batch_size = int(batch_size * 0.3)  # 增加错误记录的比例到30%
        regular_batch_size = batch_size - expert_batch_size - error_batch_size
        
        # 检查是否有足够的经验
        if len(self.replay_buffer) < regular_batch_size:
            return
        
        # 初始化批次数据
        batch = []
        indices = []
        weights = []
        
        # 从错误记录缓冲区中采样
        if error_batch_size > 0 and len(self.error_buffer) > 0:
            error_sample_size = min(error_batch_size, len(self.error_buffer))
            error_indices, error_batch, error_weights = self._sample_error_replay(error_sample_size)
            batch.extend(error_batch)
            weights.extend(error_weights)
        else:
            # 如果错误记录不足，从普通经验池中补充
            regular_batch_size += error_batch_size
        
        # 从专家经验池中采样
        if expert_batch_size > 0 and len(self.expert_buffer) > 0:
            expert_sample_size = min(expert_batch_size, len(self.expert_buffer))
            expert_indices, expert_batch, expert_weights = self._sample_expert_replay(expert_sample_size)
            batch.extend(expert_batch)
            weights.extend(expert_weights)
        else:
            # 如果专家经验不足，从普通经验池中补充
            regular_batch_size += expert_batch_size
        
        # 从普通经验池中采样
        if self.use_prioritized_replay and self.use_dueling_dqn:
            # 使用优先经验回放
            regular_indices, regular_batch, regular_weights = self._sample_prioritized_replay(regular_batch_size)
            batch.extend(regular_batch)
            indices.extend(regular_indices)
            weights.extend(regular_weights)
        else:
            # 随机采样批次
            # 修复：确保采样大小不超过缓冲区大小
            sample_size = min(regular_batch_size, len(self.replay_buffer))
            if sample_size > 0:
                regular_batch = random.sample(self.replay_buffer, sample_size)
                batch.extend(regular_batch)

        # 检查批次是否为空
        if not batch:
            return
        
        # 转换权重为张量
        if weights:
            weights = torch.tensor(weights, dtype=torch.float32)
        
        # 训练
        if self.use_dueling_dqn:
            # 使用Dueling DQN训练
            self._train_dueling_dqn(batch, None, weights)
        else:
            # 使用传统Q-learning训练
            for experience in batch:
                state, action, reward, next_state, next_actions, done = experience
                self.update_q_value(state, action, reward, next_state, next_actions)
    
    def _sample_expert_replay(self, batch_size):
        """
        从专家经验池中采样批次
        """
        if len(self.expert_buffer) == 0:
            return [], [], []
        
        # 计算采样概率
        expert_priorities = np.array(self.expert_priorities, dtype=np.float32)
        probabilities = expert_priorities ** self.alpha
        probabilities /= probabilities.sum()
        
        # 采样
        sample_size = min(batch_size, len(self.expert_buffer))
        indices = np.random.choice(len(self.expert_buffer), sample_size, p=probabilities)
        batch = [self.expert_buffer[i] for i in indices]
        
        # 计算重要性采样权重
        weights = (len(self.expert_buffer) * probabilities[indices]) ** (-self.beta)
        weights /= weights.max()  # 归一化权重
        weights = weights.tolist()
        
        return indices, batch, weights
    
    def _sample_error_replay(self, batch_size):
        """
        从错误记录缓冲区中采样批次
        """
        if len(self.error_buffer) == 0:
            return [], [], []
        
        # 计算采样概率
        error_priorities = np.array(self.error_priorities, dtype=np.float32)
        probabilities = error_priorities ** self.alpha
        probabilities /= probabilities.sum()
        
        # 采样
        sample_size = min(batch_size, len(self.error_buffer))
        indices = np.random.choice(len(self.error_buffer), sample_size, p=probabilities)
        batch = [self.error_buffer[i] for i in indices]
        
        # 计算重要性采样权重
        weights = (len(self.error_buffer) * probabilities[indices]) ** (-self.beta)
        weights /= weights.max()  # 归一化权重
        weights = weights.tolist()
        
        return indices, batch, weights
    
    def _sample_prioritized_replay(self, batch_size):
        """
        从优先经验回放中采样批次
        """
        if not self.use_prioritized_replay or len(self.priorities) == 0:
            # 修复：确保采样大小不超过缓冲区大小
            sample_size = min(batch_size, len(self.replay_buffer))
            if sample_size == 0:
                return [], [], []
            indices = random.sample(range(len(self.replay_buffer)), sample_size)
            batch = [self.replay_buffer[i] for i in indices]
            weights = [1.0] * sample_size
            return indices, batch, weights
        
        # 计算采样概率
        priorities = np.array(self.priorities, dtype=np.float32)
        probabilities = priorities ** self.alpha
        probabilities /= probabilities.sum()
        
        # 采样
        indices = np.random.choice(len(self.replay_buffer), batch_size, p=probabilities)
        batch = [self.replay_buffer[i] for i in indices]
        
        # 计算重要性采样权重
        weights = (len(self.replay_buffer) * probabilities[indices]) ** (-self.beta)
        weights /= weights.max()  # 归一化权重
        weights = torch.tensor(weights, dtype=torch.float32)
        
        # 增加beta
        self.beta = min(1.0, self.beta + self.beta_increment)
        
        return indices, batch, weights
    
    def _train_dueling_dqn(self, batch, indices=None, weights=None):
        """
        使用Dueling DQN从批次中训练，支持优先经验回放
        """
        if not self.use_dueling_dqn:
            return
        
        # 准备批次数据
        states = []
        actions = []
        rewards = []
        next_states = []
        dones = []
        
        for experience in batch:
            state, action, reward, next_state, next_actions, done = experience
            states.append(state)
            actions.append(action)
            rewards.append(reward)
            next_states.append(next_state)
            dones.append(done)
        
        # 转换为张量
        state_tensors = torch.cat([self.state_to_tensor(s) for s in states])
        reward_tensors = torch.tensor(rewards, dtype=torch.float32)
        next_state_tensors = torch.cat([self.state_to_tensor(s) for s in next_states])
        done_tensors = torch.tensor(dones, dtype=torch.bool)
        
        # 计算当前Q值
        current_q_values = self.model(state_tensors)
        
        # 计算目标Q值，使用Double DQN避免过度估计
        with torch.no_grad():
            # 使用主网络选择动作
            next_q_values_main = self.model(next_state_tensors)
            next_actions = next_q_values_main.argmax(dim=1, keepdim=True)
            
            # 使用目标网络评估动作价值
            next_q_values_target = self.target_model(next_state_tensors)
            max_next_q_values = next_q_values_target.gather(1, next_actions).squeeze(1)
            
            # 计算目标Q值
            target_q_values = reward_tensors + self.discount_factor * max_next_q_values * (~done_tensors)
        
        # 选择对应的动作Q值
        action_indices = []
        for i, action in enumerate(actions):
            # 简单的动作编码，实际应用中可能需要更复杂的编码
            action_idx = action[0] * 3 + action[1]  # 假设action是(card_index, area_index)
            action_idx = min(action_idx, self.action_dim - 1)
            action_indices.append(action_idx)
        
        action_indices = torch.tensor(action_indices, dtype=torch.long)
        selected_q_values = current_q_values.gather(1, action_indices.unsqueeze(1)).squeeze(1)
        
        # 计算TD误差
        td_errors = selected_q_values - target_q_values
        
        # 计算损失，支持优先经验回放的权重
        if weights is not None:
            # 使用重要性采样权重
            loss = (td_errors ** 2) * weights
            loss = loss.mean()
        else:
            # 标准MSE损失
            loss = self.loss_fn(selected_q_values, target_q_values)
        
        # 反向传播
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # 定期输出loss值，用于监控训练过程
        if self.update_count % 100 == 0:
            print(f"[训练监控] 更新次数: {self.update_count}, Loss: {loss.item():.4f}, 学习率: {self.learning_rate:.6f}")
        
        # 更新优先经验回放的优先级
        if self.use_prioritized_replay and indices is not None:
            td_error_clipped = td_errors.detach().abs().cpu().numpy() + self.epsilon
            for i, idx in enumerate(indices):
                self.priorities[idx] = td_error_clipped[i]
        
        # 更新计数
        self.update_count += 1
        
        # 定期更新目标网络
        if self.update_count % self.target_update_frequency == 0:
            self.update_target_network()
        
        # 衰减学习率
        self.learning_rate = max(self.min_learning_rate, self.learning_rate * self.learning_rate_decay)
        for param_group in self.optimizer.param_groups:
            param_group['lr'] = self.learning_rate
    
    def calculate_card_potential(self, cards):
        """
        计算牌组的潜在发展潜力
        """
        if not cards:
            return 0
        
        # 计算牌型潜力
        rank_counts = {}
        for card in cards:
            rank_counts[card.value] = rank_counts.get(card.value, 0) + 1
        
        # 计算对子、三条、四条的潜力
        pairs = len([r for r, c in rank_counts.items() if c >= 2])
        triples = len([r for r, c in rank_counts.items() if c >= 3])
        quadruples = len([r for r, c in rank_counts.items() if c >= 4])
        
        # 计算顺子潜力，正确处理A的位置
        sorted_ranks = sorted([card.value for card in cards])
        straight_potential = 0
        
        # 处理A的特殊情况
        has_ace = 14 in sorted_ranks
        
        # 标准顺子潜力计算（不考虑A作为中间牌）
        for i in range(len(sorted_ranks) - 1):
            if sorted_ranks[i+1] == sorted_ranks[i] + 1:
                straight_potential += 1
        
        # 检查是否有A-2-3-4-5的潜力
        if has_ace:
            low_ranks = [r if r != 14 else 1 for r in sorted_ranks]
            low_ranks.sort()
            low_straight_potential = 0
            for i in range(len(low_ranks) - 1):
                if low_ranks[i+1] == low_ranks[i] + 1:
                    low_straight_potential += 1
            
            # 取最大值
            straight_potential = max(straight_potential, low_straight_potential)
        
        # 计算同花潜力
        suit_counts = {}
        for card in cards:
            suit_counts[card.suit] = suit_counts.get(card.suit, 0) + 1
        flush_potential = max(suit_counts.values()) if suit_counts else 0
        
        # 计算总潜力
        potential = pairs * 2 + triples * 5 + quadruples * 10 + straight_potential * 1.5 + flush_potential * 1
        
        return potential
    
    def predict_opponent_hand_strength(self, game, player):
        """
        预测对手的可能牌型强度
        基于已看到的公共牌和对手的行为模式
        """
        # 简单的对手模型：假设对手的牌型强度分布
        # 实际应用中可以基于历史数据和对手行为进行更复杂的预测
        import random
        
        # 预测对手各区域的牌型强度
        # 顶部区域（3张牌）：可能的强度范围 0-4
        opponent_top_strength = random.uniform(0, 4)
        # 中部区域（5张牌）：可能的强度范围 0-9
        opponent_middle_strength = random.uniform(0, 9)
        # 底部区域（5张牌）：可能的强度范围 0-9
        opponent_bottom_strength = random.uniform(0, 9)
        
        # 确保牌型顺序合理
        if opponent_top_strength > opponent_middle_strength:
            opponent_top_strength = opponent_middle_strength * 0.8
        if opponent_middle_strength > opponent_bottom_strength:
            opponent_middle_strength = opponent_bottom_strength * 0.8
        
        return opponent_top_strength, opponent_middle_strength, opponent_bottom_strength
    
    def calculate_relative_strength(self, player_strengths, opponent_strengths):
        """
        计算相对于对手的牌型强度
        """
        top_relative = player_strengths[0] - opponent_strengths[0]
        middle_relative = player_strengths[1] - opponent_strengths[1]
        bottom_relative = player_strengths[2] - opponent_strengths[2]
        
        # 计算总相对强度
        total_relative = top_relative * 0.3 + middle_relative * 0.4 + bottom_relative * 0.3
        
        return total_relative
    
    def calculate_card_potential_enhanced(self, cards, remaining_cards=0):
        """
        增强的牌型潜力计算
        考虑更多潜在发展可能性
        """
        if not cards:
            return 0
        
        # 基础潜力计算
        base_potential = self.calculate_card_potential(cards)
        
        # 增强的潜力因素
        enhanced_potential = base_potential
        
        # 1. 考虑顺子潜力的连续性
        sorted_ranks = sorted([card.value for card in cards])
        consecutive_count = 1
        max_consecutive = 1
        
        for i in range(1, len(sorted_ranks)):
            if sorted_ranks[i] == sorted_ranks[i-1] + 1:
                consecutive_count += 1
                max_consecutive = max(max_consecutive, consecutive_count)
            else:
                consecutive_count = 1
        
        # 连续牌的额外奖励
        if max_consecutive >= 3:
            enhanced_potential += max_consecutive * 0.8
        
        # 2. 考虑花色分布的均匀性
        suit_counts = {}
        for card in cards:
            suit_counts[card.suit] = suit_counts.get(card.suit, 0) + 1
        
        # 同花潜力的额外奖励
        max_suit = max(suit_counts.values()) if suit_counts else 0
        if max_suit >= 3:
            enhanced_potential += max_suit * 0.6
        
        # 3. 考虑高牌的价值
        high_cards = [card.value for card in cards if card.value >= 10]
        enhanced_potential += len(high_cards) * 0.3
        
        # 4. 考虑剩余牌数的影响
        if remaining_cards > 0:
            # 剩余牌越多，潜力越大
            enhanced_potential *= (1 + remaining_cards * 0.1)
        
        return enhanced_potential
    
    def calculate_win_probability(self, game, player, action, state):
        """
        计算当前摆法的获胜概率，考虑潜在的牌型发展
        """
        # 模拟摆牌后的手牌状态
        temp_hand = {
            'top': player.hand.get('top', []).copy(),
            'middle': player.hand.get('middle', []).copy(),
            'bottom': player.hand.get('bottom', []).copy(),
            'temp': sorted(player.hand.get('temp', []).copy(), key=lambda x: (x.value, x.suit))
        }
        
        # 执行动作
        if action:
            card_index, area_index = action
            if card_index < len(temp_hand['temp']):
                card = temp_hand['temp'][card_index]
                areas = ['top', 'middle', 'bottom']
                area = areas[area_index]
                temp_hand[area].append(card)
                temp_hand['temp'].pop(card_index)
        
        # 计算总牌数，判断游戏阶段
        total_cards = len(temp_hand['top']) + len(temp_hand['middle']) + len(temp_hand['bottom'])
        remaining_cards = len(temp_hand['temp'])
        
        # 游戏阶段判断
        is_first_round = total_cards <= 5  # 第一轮：摆放前5张牌
        is_early_stage = total_cards < 8  # 早期阶段：总牌数少于8张
        is_mid_stage = 8 <= total_cards < 12  # 中期阶段
        is_late_stage = total_cards >= 12  # 后期阶段
        is_final_stage = remaining_cards == 0  # 最终阶段：所有牌都已摆放
        
        # 计算牌型强度
        top_strength = game.evaluate_hand(temp_hand['top'])
        middle_strength = game.evaluate_hand(temp_hand['middle'])
        bottom_strength = game.evaluate_hand(temp_hand['bottom'])
        player_strengths = (top_strength, middle_strength, bottom_strength)
        
        # 计算总强度
        total_strength = top_strength + middle_strength + bottom_strength
        
        # 检查是否爆牌
        is_busted = False
        if len(temp_hand['top']) >= 3 and len(temp_hand['middle']) >= 5 and len(temp_hand['bottom']) >= 5:
            if not (top_strength <= middle_strength <= bottom_strength):
                is_busted = True
        
        # 计算各区域的潜在发展潜力（增强版）
        top_potential = self.calculate_card_potential_enhanced(temp_hand['top'], remaining_cards)
        middle_potential = self.calculate_card_potential_enhanced(temp_hand['middle'], remaining_cards)
        bottom_potential = self.calculate_card_potential_enhanced(temp_hand['bottom'], remaining_cards)
        total_potential = top_potential + middle_potential + bottom_potential
        
        # 区域牌数调整
        # 顶部区域需要3张牌
        top_count_adj = 0
        if len(temp_hand['top']) == 3:
            if is_early_stage:
                top_count_adj = -0.1  # 早期阶段填满顶道给予惩罚
            else:
                top_count_adj = 0.1
        elif len(temp_hand['top']) > 3:
            top_count_adj = -0.2
        
        # 中部区域需要5张牌
        middle_count_adj = 0
        if len(temp_hand['middle']) == 5:
            middle_count_adj = 0.1
        elif len(temp_hand['middle']) > 5:
            middle_count_adj = -0.2
        
        # 底部区域需要5张牌
        bottom_count_adj = 0
        if len(temp_hand['bottom']) == 5:
            bottom_count_adj = 0.2  # 增加底道填满的奖励
        elif len(temp_hand['bottom']) > 5:
            bottom_count_adj = -0.2
        
        # 牌型顺序调整
        order_adj = 0
        if len(temp_hand['top']) >= 3 and len(temp_hand['middle']) >= 5 and len(temp_hand['bottom']) >= 5:
            if top_strength <= middle_strength <= bottom_strength:
                order_adj = 0.2
            else:
                order_adj = -0.3
        
        # 预测对手的牌型强度
        opponent_strengths = self.predict_opponent_hand_strength(game, player)
        
        # 计算相对强度
        relative_strength = self.calculate_relative_strength(player_strengths, opponent_strengths)
        
        # 基础获胜概率
        base_prob = 0.5
        
        # 根据游戏阶段和轮次设计不同的评估逻辑
        if is_first_round:
            # 第一轮评估逻辑：更注重牌型潜力和灵活性
            # 1. 牌型强度权重较低
            prob_adjustment = (top_strength * 0.01 + middle_strength * 0.02 + bottom_strength * 0.03)
            # 2. 牌型潜力权重较高
            prob_adjustment += total_potential * 0.06
            # 3. 区域分布平衡奖励
            if len(temp_hand['top']) <= 1 and len(temp_hand['middle']) <= 2 and len(temp_hand['bottom']) <= 2:
                prob_adjustment += 0.1
            # 4. 避免过早填满区域
            if len(temp_hand['top']) == 3:
                prob_adjustment -= 0.15
            if len(temp_hand['middle']) >= 4 or len(temp_hand['bottom']) >= 4:
                prob_adjustment -= 0.1
        elif is_early_stage:
            # 早期阶段评估逻辑：平衡潜力和当前强度
            # 降低顶道强度的权重，增加底道权重
            prob_adjustment = (top_strength * 0.02 + middle_strength * 0.03 + bottom_strength * 0.06)
            # 中等潜力权重
            prob_adjustment += total_potential * 0.04
        elif is_mid_stage:
            # 中期阶段评估逻辑：平衡权重
            prob_adjustment = total_strength * 0.04
            # 中等潜力权重
            prob_adjustment += total_potential * 0.03
        else:
            # 后期阶段评估逻辑：更注重当前强度
            prob_adjustment = total_strength * 0.05
            # 较低潜力权重
            prob_adjustment += total_potential * 0.02
        
        # 增加对两对牌型的额外奖励
        if middle_strength == 2:  # 中部区域两对
            prob_adjustment += 0.08
        if bottom_strength == 2:  # 底部区域两对
            prob_adjustment += 0.06
        
        # 根据相对强度调整概率
        prob_adjustment += relative_strength * 0.05
        
        # 根据区域牌数调整概率
        prob_adjustment += top_count_adj + middle_count_adj + bottom_count_adj
        
        # 根据牌型顺序调整概率
        prob_adjustment += order_adj
        
        # 根据是否爆牌调整概率
        if is_busted:
            prob_adjustment -= 0.4
        
        # 最终阶段的额外调整
        if is_final_stage:
            # 所有牌都已摆放，更注重最终牌型强度
            if top_strength <= middle_strength <= bottom_strength:
                prob_adjustment += 0.1
            # 对强牌型给予额外奖励
            if bottom_strength >= 7:  # 葫芦及以上
                prob_adjustment += 0.15
            if middle_strength >= 5:  # 顺子及以上
                prob_adjustment += 0.1
        
        # 计算最终概率
        win_prob = min(0.99, max(0.01, base_prob + prob_adjustment))
        
        return win_prob
    
    def get_final_score(self, game, player):
        """
        获取玩家的最终得分
        基于游戏的calculate_score方法
        """
        # 检查是否爆牌
        if game.check_busted(player):
            return 0
        
        # 计算牌型分
        top_score = game.calculate_hand_score(player.hand.get('top', []), 'top')
        middle_score = game.calculate_hand_score(player.hand.get('middle', []), 'middle')
        bottom_score = game.calculate_hand_score(player.hand.get('bottom', []), 'bottom')
        
        total_score = top_score + middle_score + bottom_score
        return total_score
    
    def check_fantasy_land(self, game, player):
        """
        检查玩家是否进入了Fantasy Land
        """
        # 检查玩家是否处于fantasy_mode
        if hasattr(player, 'fantasy_mode') and player.fantasy_mode:
            return True
        
        # 检查是否满足进入范特西模式的条件
        # 基于check_fantasy_mode方法的逻辑
        top_cards = player.hand.get('top', [])
        if len(top_cards) == 3:
            # 检查是否有对子
            rank_counts = {}
            for card in top_cards:
                rank_counts[card.value] = rank_counts.get(card.value, 0) + 1
            pairs = [r for r, c in rank_counts.items() if c >= 2]
            
            if pairs:
                # 检查是否有三条或以上
                trips = [r for r, c in rank_counts.items() if c >= 3]
                if trips:
                    return True
                else:
                    high_pair = max(pairs)
                    # AA、KK、QQ都可以进入范特西模式
                    if high_pair >= 12:  # QQ及以上
                        return True
        
        return False
    
    def calculate_reward(self, game, player, old_state, action, new_state):
        """
        计算奖励 - 新的奖励机制
        """
        reward = 0
        
        # 1. 完成摆牌奖励
        if not player.hand.get('temp', []):
            reward += 50  # 完成摆牌奖励
            
            # 2. 爆牌惩罚：大幅增加惩罚值（只在所有牌都摆完后检查）
            if game.check_busted(player):
                reward -= 1500  # 大幅增加惩罚值，从-300分改为-1500分
                print(f"[{self.name}] 爆牌，惩罚1500分！")
        
        # 3. 取消区域强度顺序正确的奖励
        
        # 4. FL模式的高额奖励
        if not player.hand.get('temp', []):
            # 检查玩家是否进入了Fantasy Land
            if self.check_fantasy_land(game, player):
                # 检查进入FL的条件
                top_cards = player.hand.get('top', [])
                if len(top_cards) == 3:
                    # 检查顶部区域的牌型
                    rank_counts = {}
                    for card in top_cards:
                        rank_counts[card.value] = rank_counts.get(card.value, 0) + 1
                    
                    # 检查是否有对子
                    pairs = []
                    for rank, count in rank_counts.items():
                        if count >= 2:
                            pairs.append(rank)
                    
                    # 检查是否有三条或以上
                    three_of_a_kind = []
                    for rank, count in rank_counts.items():
                        if count >= 3:
                            three_of_a_kind.append(rank)
                    
                    # 根据进入FL的条件给予不同的奖励
                    if three_of_a_kind:
                        # 以三条或更强进入FL
                        reward += 6000
                        print(f"[{self.name}] 以三条或更强进入FL阶段，奖励6000分！")
                    elif pairs:
                        high_pair = max(pairs)
                        if high_pair == 14:  # AA
                            reward += 3500
                            print(f"[{self.name}] 以AA进入FL阶段，奖励3500分！")
                        elif high_pair == 13:  # KK
                            reward += 2500
                            print(f"[{self.name}] 以KK进入FL阶段，奖励2500分！")
                        elif high_pair == 12:  # QQ
                            reward += 2000
                            print(f"[{self.name}] 以QQ进入FL阶段，奖励2000分！")
        
        return reward
    
    def step(self, game, player, action):
        """
        执行一步操作，处理爆牌情况
        """
        # 获取当前状态
        old_state = self.get_state(game, player)
        
        # 执行动作
        card_index, area_index = action
        temp_cards = player.hand.get('temp', [])
        if card_index < len(temp_cards):
            card = temp_cards[card_index]
            areas = ['top', 'middle', 'bottom']
            area = areas[area_index]
            player.hand[area].append(card)
            player.hand['temp'].pop(card_index)
        
        # 获取新状态
        new_state = self.get_state(game, player)
        
        # 检查是否所有牌都已摆放完成
        is_completed = not player.hand.get('temp', [])
        
        # 计算奖励
        reward = self.calculate_reward(game, player, old_state, action, new_state)
        
        # 只有在摆牌完成或爆牌时才结束回合
        is_busted = game.check_busted(player)
        done = is_completed or is_busted
        
        # 获取下一个状态的可用动作
        next_actions = self.get_actions(player)
        
        # 存储经验
        self.store_experience(old_state, action, reward, new_state, next_actions, done)
        
        # 从经验中学习
        self.train_from_replay()
        
        # 衰减探索率
        self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)
        
        return new_state, reward, done
    
    def learn(self, game, player, action, old_state, new_state, done):
        """
        学习过程
        """
        # 计算奖励
        reward = self.calculate_reward(game, player, old_state, action, new_state)
        
        # 获取下一个状态的可用动作
        next_actions = self.get_actions(player)
        
        # 存储经验
        self.store_experience(old_state, action, reward, new_state, next_actions, done)
        
        # 从经验中学习
        self.train_from_replay()
        
        # 衰减探索率
        self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)
    
    def save_learning_data(self):
        """
        保存学习数据
        """
        data_file = f"ai_learning_{self.name.replace(' ', '_').lower()}.json"
        data = {
            'q_table': {str(state): {str(action): value for action, value in actions.items()} 
                        for state, actions in self.q_table.items()},
            'exploration_rate': self.exploration_rate,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"学习数据已保存到: {data_file}")
        except Exception as e:
            print(f"保存学习数据失败: {e}")
    
    def load_learning_data(self):
        """
        加载学习数据
        """
        data_file = f"ai_learning_{self.name.replace(' ', '_').lower()}.json"
        if os.path.exists(data_file):
            try:
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 恢复Q-table
                    for state_str, actions in data.get('q_table', {}).items():
                        # 这里需要将字符串转换回原始状态表示
                        # 为了简化，暂时跳过
                        pass
                    # 恢复探索率
                    self.exploration_rate = data.get('exploration_rate', 1.0)
                    print(f"加载了学习数据，当前探索率: {self.exploration_rate}")
            except Exception as e:
                print(f"加载学习数据失败: {e}")
