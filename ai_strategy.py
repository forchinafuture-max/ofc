import random
from core import Player
from game_logic import OFCGame

class AIPlayer(Player):
    def __init__(self, name, chips=1000, difficulty='medium'):
        super().__init__(name, chips)
        self.difficulty = difficulty
        self.opponent_model = {}
        self.history = []  # 历史对战记录
        self.learning_rate = 0.1  # 学习率
        self.load_learning_data()
    
    def evaluate_hand_strength(self, game, cards):
        # 评估手牌强度
        return game.evaluate_hand(cards)
    
    def place_cards_strategy(self, game):
        # AI摆牌策略
        temp_cards = self.hand['temp'].copy()
        
        if self.difficulty == 'easy':
            return self.easy_place_strategy(temp_cards)
        elif self.difficulty == 'medium':
            return self.medium_place_strategy(temp_cards)
        else:  # hard
            return self.hard_place_strategy(temp_cards, game)
    
    def easy_place_strategy(self, cards):
        # 简单AI摆牌策略：按牌力排序，最弱的放顶部，中间的放中部，最强的放底部
        cards.sort(key=lambda x: x.value)
        
        # 确保不超过可用牌数
        top_cards = []
        middle_cards = []
        bottom_cards = []
        
        # 顶部放最弱的牌
        if len(cards) >= 3:
            top_cards = cards[:3]
        elif len(cards) > 0:
            top_cards = cards[:len(cards)]
        
        # 中部放中间的牌
        if len(cards) >= 5:
            middle_cards = cards[3:5]
        elif len(cards) > 3:
            middle_cards = cards[3:len(cards)]
        
        # 底部放最强的牌
        if len(cards) > 5:
            bottom_cards = cards[5:]
        
        return {
            'top': top_cards,
            'middle': middle_cards,
            'bottom': bottom_cards
        }
    
    def medium_place_strategy(self, cards):
        # 中等AI摆牌策略：考虑牌型组合
        cards.sort(key=lambda x: x.value, reverse=True)
        
        # 尝试构建牌型
        top_cards = []
        middle_cards = []
        bottom_cards = []
        
        # 确保不重复使用牌
        used_cards = set()
        
        # 顶部放3张较弱的牌
        if len(cards) >= 3:
            top_cards = cards[-3:]
            used_cards.update(top_cards)
        
        # 中部放中间强度的牌
        if len(cards) >= 5:
            # 选择未使用的中间强度牌
            for card in cards[1:3]:
                if card not in used_cards and len(middle_cards) < 2:
                    middle_cards.append(card)
                    used_cards.add(card)
        
        # 底部放最强的牌
        if len(cards) >= 2:
            # 选择未使用的最强牌
            for card in cards[:2]:
                if card not in used_cards and len(bottom_cards) < 2:
                    bottom_cards.append(card)
                    used_cards.add(card)
        
        # 确保总数不超过5张
        total_cards = len(top_cards) + len(middle_cards) + len(bottom_cards)
        if total_cards > len(cards):
            # 调整牌数
            while total_cards > len(cards):
                if len(top_cards) > 0:
                    card = top_cards.pop()
                    used_cards.remove(card)
                elif len(middle_cards) > 0:
                    card = middle_cards.pop()
                    used_cards.remove(card)
                elif len(bottom_cards) > 0:
                    card = bottom_cards.pop()
                    used_cards.remove(card)
                total_cards -= 1
        
        return {
            'top': top_cards,
            'middle': middle_cards,
            'bottom': bottom_cards
        }
    
    def hard_place_strategy(self, cards, game):
        # 高级AI摆牌策略：模拟不同摆法并选择最佳方案
        best_score = -float('inf')
        best_placement = None
        
        # 生成可能的摆法（简化处理）
        # 实际游戏中可能需要更复杂的排列组合
        cards.sort(key=lambda x: x.value, reverse=True)
        
        # 尝试几种常见的摆法
        placements = []
        
        # 摆法1：最弱的放顶部
        if len(cards) >= 5:
            # 确保不重复使用牌
            top_cards = cards[2:5]
            middle_cards = [c for c in cards[0:2] if c not in top_cards]
            placements.append({'top': top_cards, 'middle': middle_cards[:2], 'bottom': []})
        
        # 摆法2：平均分配
        if len(cards) >= 5:
            top_cards = cards[3:5]
            middle_cards = [c for c in cards[1:3] if c not in top_cards]
            bottom_cards = [c for c in cards[0:1] if c not in top_cards and c not in middle_cards]
            placements.append({'top': top_cards, 'middle': middle_cards[:2], 'bottom': bottom_cards[:1]})
        
        # 摆法3：强牌集中
        if len(cards) >= 4:
            top_cards = cards[-3:] if len(cards) >= 3 else cards
            middle_cards = [c for c in cards[2:4] if c not in top_cards]
            bottom_cards = [c for c in cards[0:2] if c not in top_cards and c not in middle_cards]
            placements.append({'top': top_cards, 'middle': middle_cards[:2], 'bottom': bottom_cards[:2]})
        
        # 确保至少有一个摆法
        if not placements:
            placements.append(self.medium_place_strategy(cards))
        
        for placement in placements:
            # 计算这种摆法的得分
            score = self.calculate_placement_score(placement, game)
            if score > best_score:
                best_score = score
                best_placement = placement
        
        return best_placement if best_placement else self.medium_place_strategy(cards)
    
    def calculate_placement_score(self, placement, game):
        # 计算摆法的得分
        top_score = game.evaluate_hand(placement['top'])
        middle_score = game.evaluate_hand(placement['middle'])
        bottom_score = game.evaluate_hand(placement['bottom'])
        
        # 检查是否爆牌
        if not (top_score <= middle_score <= bottom_score):
            return -100
        
        # 计算总分
        total_score = top_score + middle_score + bottom_score
        return total_score
    
    def evaluate_overall_strength(self, game):
        # 评估整体手牌强度
        top_strength = self.evaluate_hand_strength(game, self.hand['top'])
        middle_strength = self.evaluate_hand_strength(game, self.hand['middle'])
        bottom_strength = self.evaluate_hand_strength(game, self.hand['bottom'])
        
        return top_strength + middle_strength + bottom_strength
    
    def load_learning_data(self):
        """加载学习数据"""
        import os
        import json
        
        data_file = f"ai_learning_{self.name.replace(' ', '_').lower()}.json"
        if os.path.exists(data_file):
            try:
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.opponent_model = data.get('opponent_model', {})
                    self.history = data.get('history', [])
                    print(f"加载了 {len(self.history)} 条历史对战记录")
            except Exception as e:
                print(f"加载学习数据失败: {e}")
    
    def save_learning_data(self):
        """保存学习数据"""
        import os
        import json
        
        data_file = f"ai_learning_{self.name.replace(' ', '_').lower()}.json"
        data = {
            'opponent_model': self.opponent_model,
            'history': self.history[-100:],  # 只保存最近100条记录
            'timestamp': self.history[-1]['timestamp'] if self.history else None
        }
        
        try:
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"学习数据已保存到: {data_file}")
        except Exception as e:
            print(f"保存学习数据失败: {e}")
    
    def learn_from_game(self, game, opponent):
        """从游戏中学习"""
        from datetime import datetime
        
        # 记录本次游戏
        game_record = {
            'timestamp': datetime.now().isoformat(),
            'opponent': opponent.name,
            'own_hand': {
                'top': [str(card) for card in self.hand['top']],
                'middle': [str(card) for card in self.hand['middle']],
                'bottom': [str(card) for card in self.hand['bottom']]
            },
            'opponent_hand': {
                'top': [str(card) for card in opponent.hand['top']],
                'middle': [str(card) for card in opponent.hand['middle']],
                'bottom': [str(card) for card in opponent.hand['bottom']]
            },
            'result': 'win' if self.total_score > opponent.total_score else 'loss' if self.total_score < opponent.total_score else 'draw'
        }
        
        self.history.append(game_record)
        
        # 更新对手模型
        self._update_opponent_model(opponent)
        
        # 保存学习数据
        if len(self.history) % 5 == 0:  # 每5局保存一次
            self.save_learning_data()
    
    def _update_opponent_model(self, opponent):
        """更新对手模型"""
        opponent_name = opponent.name
        
        if opponent_name not in self.opponent_model:
            self.opponent_model[opponent_name] = {
                'play_style': 'unknown',  # 未知、保守、激进、平衡
                'hand_strength_estimation': {},
                'game_count': 0,
                'win_count': 0
            }
        
        model = self.opponent_model[opponent_name]
        model['game_count'] += 1
        
        # 分析对手的手牌强度
        import game_logic
        game = game_logic.OFCGame()
        
        # 计算对手的手牌强度
        top_strength = game.evaluate_hand(opponent.hand['top'])
        middle_strength = game.evaluate_hand(opponent.hand['middle'])
        bottom_strength = game.evaluate_hand(opponent.hand['bottom'])
        
        # 更新对手的手牌强度估计
        model['hand_strength_estimation'] = {
            'top': (model['hand_strength_estimation'].get('top', 0) * (model['game_count'] - 1) + top_strength) / model['game_count'],
            'middle': (model['hand_strength_estimation'].get('middle', 0) * (model['game_count'] - 1) + middle_strength) / model['game_count'],
            'bottom': (model['hand_strength_estimation'].get('bottom', 0) * (model['game_count'] - 1) + bottom_strength) / model['game_count']
        }
        
        # 基于历史数据调整策略
        if model['game_count'] >= 5:
            # 根据对手的平均手牌强度调整自己的策略
            avg_strength = (model['hand_strength_estimation']['top'] + 
                           model['hand_strength_estimation']['middle'] + 
                           model['hand_strength_estimation']['bottom']) / 3
            
            # 根据对手强度调整自己的难度
            if avg_strength > 3.0:
                # 对手较强，提高自己的难度
                if self.difficulty == 'easy':
                    self.difficulty = 'medium'
            elif avg_strength < 1.5:
                # 对手较弱，降低自己的难度
                if self.difficulty == 'hard':
                    self.difficulty = 'medium'

class AIStrategy:
    def __init__(self):
        pass
    
    def suggest_placement(self, game, player):
        # 为AI玩家提供摆牌建议
        if isinstance(player, AIPlayer):
            return player.place_cards_strategy(game)
        return {'top': [], 'middle': [], 'bottom': []}

# 导入RLAIPlayer
try:
    from rl_ai import RLAIPlayer
except ImportError:
    # 如果导入失败，定义一个占位类
    class RLAIPlayer(AIPlayer):
        def __init__(self, name, chips=1000, difficulty='medium'):
            super().__init__(name, chips, difficulty)
            print(f"RLAIPlayer 导入失败，使用普通AIPlayer")
