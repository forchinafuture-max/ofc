"""
AIStrategy 抽象类 + 启发式策略实现
"""

from abc import ABC, abstractmethod
from core.hand_state import HandState

class AIStrategy(ABC):
    """
    AI策略抽象类
    定义AI决策的接口
    """
    
    @abstractmethod
    def decide_placement(self, hand_state: HandState) -> HandState:
        """
        决定卡牌摆放
        
        Args:
            hand_state: 手牌状态
            
        Returns:
            摆放后的手牌状态
        """
        pass
    
    @abstractmethod
    def choose_action(self, player, game):
        """
        选择行动
        
        Args:
            player: 玩家对象
            game: 游戏对象
            
        Returns:
            行动元组 (card_index, area_index)
        """
        pass
    
    @abstractmethod
    def evaluate_state(self, player, game):
        """
        评估状态
        
        Args:
            player: 玩家对象
            game: 游戏对象
            
        Returns:
            状态价值
        """
        pass

class HeuristicStrategy(AIStrategy):
    """
    启发式策略实现
    基于简单规则和启发式评估
    """
    
    def decide_placement(self, hand_state: HandState) -> HandState:
        """
        决定卡牌摆放
        
        Args:
            hand_state: 手牌状态
            
        Returns:
            摆放后的手牌状态
        """
        # 这里实现一个简单的摆放策略
        # 实际实现可以根据具体需求进行扩展
        import copy
        result_state = copy.deepcopy(hand_state)
        
        # 获取待摆放的牌
        temp_cards = result_state.get('temp', [])
        
        # 简单策略：将牌按价值排序，然后依次放入各个区域
        temp_cards.sort(key=lambda card: card.value, reverse=True)
        
        # 先放顶部区域（最多3张）
        while temp_cards and len(result_state.get('top', [])) < 3:
            card = temp_cards.pop(0)
            top_cards = result_state.get('top', [])
            top_cards.append(card)
            result_state['top'] = top_cards
        
        # 再放中部区域（最多5张）
        while temp_cards and len(result_state.get('middle', [])) < 5:
            card = temp_cards.pop(0)
            middle_cards = result_state.get('middle', [])
            middle_cards.append(card)
            result_state['middle'] = middle_cards
        
        # 最后放底部区域（最多5张）
        while temp_cards and len(result_state.get('bottom', [])) < 5:
            card = temp_cards.pop(0)
            bottom_cards = result_state.get('bottom', [])
            bottom_cards.append(card)
            result_state['bottom'] = bottom_cards
        
        return result_state
    
    def choose_action(self, player, game):
        """
        选择行动
        
        Args:
            player: 玩家对象
            game: 游戏对象
            
        Returns:
            行动元组 (card_index, area_index)
        """
        # 获取当前待摆放的牌
        temp_cards = player.hand.get('temp', [])
        if not temp_cards:
            return None
        
        # 生成所有合法动作
        legal_actions = []
        for i, card in enumerate(temp_cards):
            # 检查顶部区域
            if len(player.hand.get('top', [])) < 3:
                legal_actions.append((i, 0))  # 0表示顶部区域
            
            # 检查中部区域
            if len(player.hand.get('middle', [])) < 5:
                legal_actions.append((i, 1))  # 1表示中部区域
            
            # 检查底部区域
            if len(player.hand.get('bottom', [])) < 5:
                legal_actions.append((i, 2))  # 2表示底部区域
        
        if not legal_actions:
            return None
        
        # 评估每个合法动作
        best_action = None
        best_score = -float('inf')
        
        for action in legal_actions:
            score = self.evaluate_action(player, game, action)
            if score > best_score:
                best_score = score
                best_action = action
        
        # 记录AI决策
        if best_action:
            from core.logger import log_ai_decision
            card_index, area_index = best_action
            areas = ['top', 'middle', 'bottom']
            area_name = areas[area_index]
            decision = {
                'action': 'choose_action',
                'card_index': card_index,
                'area_index': area_index,
                'area_name': area_name,
                'score': best_score
            }
            log_ai_decision(player, decision, game)
        
        return best_action
    
    def evaluate_action(self, player, game, action):
        """
        评估动作
        
        Args:
            player: 玩家对象
            game: 游戏对象
            action: 动作元组 (card_index, area_index)
            
        Returns:
            动作得分
        """
        import copy
        
        # 创建玩家的深拷贝，避免修改原始状态
        sim_player = copy.deepcopy(player)
        
        # 模拟执行动作
        card_index, area_index = action
        temp_cards = sim_player.hand.get('temp', [])
        if card_index >= len(temp_cards):
            return 0
        
        card = temp_cards[card_index]
        areas = ['top', 'middle', 'bottom']
        area = areas[area_index]
        
        # 检查区域是否已满
        if len(sim_player.hand.get(area, [])) >= (3 if area == 'top' else 5):
            return 0
        
        # 执行动作
        sim_player.add_card(card, area)
        sim_player.hand['temp'].pop(card_index)
        
        # 评估执行后的状态
        return self.evaluate_state(sim_player, game)
    
    def evaluate_state(self, player, game):
        """
        评估状态
        
        Args:
            player: 玩家对象
            game: 游戏对象
            
        Returns:
            状态价值
        """
        value = 0
        
        # 评估各区域的牌型强度
        top_cards = player.hand.get('top', [])
        middle_cards = player.hand.get('middle', [])
        bottom_cards = player.hand.get('bottom', [])
        
        try:
            # 计算各区域的牌型强度
            top_strength = game.evaluate_hand(top_cards)
            middle_strength = game.evaluate_hand(middle_cards)
            bottom_strength = game.evaluate_hand(bottom_cards)
            
            # 区域强度顺序奖励
            if top_strength <= middle_strength <= bottom_strength:
                value += 10
            else:
                value -= 5
            
            # 各区域牌型强度奖励
            value += top_strength * 2
            value += middle_strength * 3
            value += bottom_strength * 4
            
            # 检查爆牌风险
            is_busted = game.check_busted(player)
            if is_busted:
                value -= 50
            
            # 检查幻想模式潜力
            if len(top_cards) >= 2:
                # 检查顶部区域是否有对子
                rank_counts = {}
                for card in top_cards:
                    rank_counts[card.value] = rank_counts.get(card.value, 0) + 1
                pairs = [r for r, c in rank_counts.items() if c >= 2]
                if pairs:
                    high_pair = max(pairs)
                    if high_pair >= 12:  # QQ及以上
                        value += 15
        except:
            pass
        
        return value

class MCTSStrategy(AIStrategy):
    """
    MCTS策略实现
    基于蒙特卡洛树搜索
    """
    
    def __init__(self, iterations=None):
        """
        初始化MCTS策略
        
        Args:
            iterations: 搜索迭代次数
        """
        from .mcts import MCTS
        self.mcts = MCTS(iterations)
    
    def decide_placement(self, hand_state):
        """
        决定卡牌摆放
        
        Args:
            hand_state: 手牌状态
            
        Returns:
            摆放后的手牌状态
        """
        # 这里需要实现一个完整的摆放策略
        # 由于MCTS是基于单次动作的，我们需要迭代调用它来完成整个摆放过程
        import copy
        result_state = copy.deepcopy(hand_state)
        
        # 这里可以实现一个基于MCTS的完整摆放策略
        # 暂时返回原始状态
        return result_state
    
    def choose_action(self, player, game):
        """
        选择行动
        
        Args:
            player: 玩家对象
            game: 游戏对象
            
        Returns:
            行动元组 (card_index, area_index)
        """
        state = (player, game)
        return self.mcts.search(state)
    
    def evaluate_state(self, player, game):
        """
        评估状态
        
        Args:
            player: 玩家对象
            game: 游戏对象
            
        Returns:
            状态价值
        """
        # 这里可以实现一个基于MCTS的状态评估
        # 暂时返回一个简单的评估值
        value = 0
        
        # 评估各区域的牌型强度
        top_cards = player.hand.get('top', [])
        middle_cards = player.hand.get('middle', [])
        bottom_cards = player.hand.get('bottom', [])
        
        try:
            # 计算各区域的牌型强度
            top_strength = game.evaluate_hand(top_cards)
            middle_strength = game.evaluate_hand(middle_cards)
            bottom_strength = game.evaluate_hand(bottom_cards)
            
            # 区域强度顺序奖励
            if top_strength <= middle_strength <= bottom_strength:
                value += 10
            else:
                value -= 5
            
            # 各区域牌型强度奖励
            value += top_strength * 2
            value += middle_strength * 3
            value += bottom_strength * 4
            
            # 检查爆牌风险
            is_busted = game.check_busted(player)
            if is_busted:
                value -= 50
        except:
            pass
        
        return value
