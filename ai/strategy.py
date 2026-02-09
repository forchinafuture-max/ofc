"""
AIStrategy 抽象类 + 启发式策略实现
"""

from abc import ABC, abstractmethod
from core.hand_state import HandState
from ai.evaluation import evaluate_player_state
from core.rules import RuleEngine

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
        import copy

        result_state = copy.deepcopy(hand_state)
        rule_engine = RuleEngine()

        temp_cards = result_state.get('temp', [])
        temp_cards.sort(key=lambda card: card.value, reverse=True)

        def can_place(area):
            return len(result_state.get(area, [])) < (3 if area == 'top' else 5)

        for card in list(temp_cards):
            best_area = None
            best_score = -float('inf')
            for area in ['top', 'middle', 'bottom']:
                if not can_place(area):
                    continue
                simulated = copy.deepcopy(result_state)
                simulated[area].append(card)
                simulated['temp'] = [c for c in simulated.get('temp', []) if c != card]

                score = _evaluate_hand_state(simulated, rule_engine)
                if score > best_score:
                    best_score = score
                    best_area = area

            if best_area:
                result_state[best_area].append(card)
                result_state['temp'].remove(card)

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
        return evaluate_player_state(player, game)


def _evaluate_hand_state(hand_state, rule_engine):
    temp_player = _HandStateAdapter(hand_state)
    class _DummyGame:
        def __init__(self, engine):
            self.rule_engine = engine
        def check_busted(self, player):
            return self.rule_engine.check_busted(player)
        def calculate_total_score(self, player):
            return 0
        def check_fantasy_mode(self, player):
            return False
    dummy_game = _DummyGame(rule_engine)
    return evaluate_player_state(temp_player, dummy_game)


class _HandStateAdapter:
    def __init__(self, hand_state):
        self.hand = hand_state

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
        import copy

        result_state = copy.deepcopy(hand_state)
        rule_engine = RuleEngine()

        temp_cards = result_state.get('temp', [])
        while temp_cards:
            best_area = None
            best_score = -float('inf')
            card = temp_cards[0]
            for area in ['top', 'middle', 'bottom']:
                if len(result_state.get(area, [])) >= (3 if area == 'top' else 5):
                    continue
                simulated = copy.deepcopy(result_state)
                simulated[area].append(card)
                simulated['temp'] = simulated['temp'][1:]
                score = _evaluate_hand_state(simulated, rule_engine)
                if score > best_score:
                    best_score = score
                    best_area = area
            if best_area:
                result_state[best_area].append(card)
            result_state['temp'] = result_state['temp'][1:]
            temp_cards = result_state.get('temp', [])

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
        return evaluate_player_state(player, game)
