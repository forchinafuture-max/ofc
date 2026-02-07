"""
测试AI功能
"""

import unittest
from game.ofc_game import OFCGame
from game.player import Player
from ai.ai_player import AIPlayer
from ai.strategy import HeuristicStrategy
from ai.mcts import MCTS

class TestAI(unittest.TestCase):
    """
    测试AI功能
    """
    
    def setUp(self):
        """
        设置测试环境
        """
        self.game = OFCGame()
        self.ai_player = AIPlayer("AIPlayer", strategy_type='heuristic')
        self.game.add_player(self.ai_player)
    
    def test_ai_player_creation(self):
        """
        测试AI玩家创建
        """
        self.assertEqual(self.ai_player.name, "AIPlayer")
        self.assertEqual(self.ai_player.strategy_type, 'heuristic')
        self.assertIsNotNone(self.ai_player.strategy)
    
    def test_heuristic_strategy(self):
        """
        测试启发式策略
        """
        strategy = HeuristicStrategy()
        
        # 测试选择行动
        self.game.start_game()
        action = strategy.choose_action(self.ai_player, self.game)
        # 行动应该是一个元组 (card_index, area_index)
        self.assertIsInstance(action, tuple)
        self.assertEqual(len(action), 2)
        self.assertIsInstance(action[0], int)
        self.assertIsInstance(action[1], int)
        
        # 测试评估状态
        value = strategy.evaluate_state(self.ai_player, self.game)
        self.assertIsInstance(value, (int, float))
    
    def test_mcts_strategy(self):
        """
        测试MCTS策略
        """
        # 创建一个使用MCTS策略的AI玩家
        mcts_ai = AIPlayer("MCTSAI", strategy_type='mcts')
        self.game.add_player(mcts_ai)
        
        # 测试选择行动
        self.game.start_game()
        action = mcts_ai.choose_action(self.game)
        # 行动应该是一个元组 (card_index, area_index) 或者 None
        if action is not None:
            self.assertIsInstance(action, tuple)
            self.assertEqual(len(action), 2)
            self.assertIsInstance(action[0], int)
            self.assertIsInstance(action[1], int)
    
    def test_ai_place_cards(self):
        """
        测试AI摆放卡牌
        """
        self.game.start_game()
        temp_cards_before = len(self.ai_player.hand.get('temp', []))
        
        # 让AI摆放卡牌
        self.ai_player.place_cards(self.game)
        temp_cards_after = len(self.ai_player.hand.get('temp', []))
        
        # 检查是否有卡牌被摆放
        self.assertLess(temp_cards_after, temp_cards_before)
        
        # 检查区域长度限制
        self.assertLessEqual(len(self.ai_player.hand.get('top', [])), 3)
        self.assertLessEqual(len(self.ai_player.hand.get('middle', [])), 5)
        self.assertLessEqual(len(self.ai_player.hand.get('bottom', [])), 5)
    
    def test_mcts_search(self):
        """
        测试MCTS搜索
        """
        mcts = MCTS(iterations=100)  # 使用较少的迭代次数以加快测试速度
        
        # 测试搜索
        self.game.start_game()
        state = (self.ai_player, self.game)
        action = mcts.search(state)
        
        # 行动应该是一个元组 (card_index, area_index) 或者 None
        if action is not None:
            self.assertIsInstance(action, tuple)
            self.assertEqual(len(action), 2)
            self.assertIsInstance(action[0], int)
            self.assertIsInstance(action[1], int)

if __name__ == '__main__':
    unittest.main()
