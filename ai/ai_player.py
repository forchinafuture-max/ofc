"""
AIPlayer，调用策略接口
"""

from game.player import Player
from ai.strategy import HeuristicStrategy
from ai.mcts import MCTS

class AIPlayer(Player):
    """
    AI玩家类
    继承自Player类，使用策略接口进行决策
    """
    
    def __init__(self, name, strategy_type='heuristic'):
        """
        初始化AI玩家
        
        Args:
            name: 玩家名称
            strategy_type: 策略类型，可选 'heuristic' 或 'mcts'
        """
        super().__init__(name)
        self.strategy_type = strategy_type
        self.strategy = self._create_strategy(strategy_type)
        self.mcts = MCTS() if strategy_type == 'mcts' else None
    
    def _create_strategy(self, strategy_type):
        """
        创建策略实例
        
        Args:
            strategy_type: 策略类型
            
        Returns:
            策略实例
        """
        if strategy_type == 'heuristic':
            return HeuristicStrategy()
        elif strategy_type == 'mcts':
            # MCTS策略使用单独的实现
            return None
        else:
            raise ValueError(f"Unknown strategy type: {strategy_type}")
    
    def choose_action(self, game):
        """
        选择行动
        
        Args:
            game: 游戏对象
            
        Returns:
            行动元组 (card_index, area_index)
        """
        if self.strategy_type == 'heuristic':
            # 使用启发式策略
            return self.strategy.choose_action(self, game)
        elif self.strategy_type == 'mcts':
            # 使用MCTS策略
            state = (self, game)
            return self.mcts.search(state)
        else:
            return None
    
    def place_cards(self, game):
        """
        摆放卡牌
        
        Args:
            game: 游戏对象
        """
        # 获取待摆放的牌
        temp_cards = self.hand.get('temp', [])
        
        while temp_cards:
            # 选择行动
            action = self.choose_action(game)
            if not action:
                break
            
            # 执行行动
            card_index, area_index = action
            if card_index >= len(temp_cards):
                break
            
            card = temp_cards[card_index]
            areas = ['top', 'middle', 'bottom']
            area = areas[area_index]
            
            # 检查区域是否已满
            if len(self.hand.get(area, [])) >= (3 if area == 'top' else 5):
                continue
            
            # 摆放卡牌
            self.add_card(card, area)
            self.hand['temp'].pop(card_index)
            
            # 更新待摆放的牌
            temp_cards = self.hand.get('temp', [])
    
    def evaluate_state(self, game):
        """
        评估状态
        
        Args:
            game: 游戏对象
            
        Returns:
            状态价值
        """
        if self.strategy_type == 'heuristic' and self.strategy:
            return self.strategy.evaluate_state(self, game)
        else:
            # 简单的状态评估
            value = 0
            
            # 评估各区域的牌型强度
            top_cards = self.hand.get('top', [])
            middle_cards = self.hand.get('middle', [])
            bottom_cards = self.hand.get('bottom', [])
            
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
                is_busted = game.check_busted(self)
                if is_busted:
                    value -= 50
            except:
                pass
            
            return value
