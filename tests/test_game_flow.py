"""
测试游戏流程
"""

import unittest
from game.ofc_game import OFCGame
from game.player import Player
from game.deck import Card

class TestGameFlow(unittest.TestCase):
    """
    测试游戏流程
    """
    
    def setUp(self):
        """
        设置测试环境
        """
        self.game = OFCGame()
        self.player1 = Player("Player1")
        self.player2 = Player("Player2")
        self.game.add_player(self.player1)
        self.game.add_player(self.player2)
    
    def test_start_game(self):
        """
        测试开始游戏
        """
        self.game.start_game()
        self.assertEqual(self.game.current_round, 1)
        
        # 检查玩家是否收到了牌
        self.assertGreater(len(self.player1.hand.get('temp', [])), 0)
        self.assertGreater(len(self.player2.hand.get('temp', [])), 0)
    
    def test_deal_first_round(self):
        """
        测试第一轮发牌
        """
        self.game.deal_first_round()
        self.assertEqual(self.game.current_round, 1)
        
        # 检查玩家是否收到了13张牌
        self.assertEqual(len(self.player1.hand.get('temp', [])), 13)
        self.assertEqual(len(self.player2.hand.get('temp', [])), 13)
    
    def test_next_round(self):
        """
        测试进入下一轮
        """
        self.game.deal_first_round()
        self.assertEqual(self.game.current_round, 1)
        
        # 进入第二轮
        result = self.game.next_round()
        self.assertTrue(result)
        self.assertEqual(self.game.current_round, 2)
        
        # 继续进入下一轮
        for i in range(3, 6):
            result = self.game.next_round()
            if i < 6:
                self.assertTrue(result)
                self.assertEqual(self.game.current_round, i)
        
        # 游戏结束
        result = self.game.next_round()
        self.assertFalse(result)
    
    def test_calculate_total_score(self):
        """
        测试计算总得分
        """
        # 为玩家1设置一个有效的手牌
        self.player1.hand['top'] = [Card(2, '♠'), Card(2, '♥'), Card(3, '♦')]  # 一对2
        self.player1.hand['middle'] = [Card(4, '♠'), Card(4, '♥'), Card(5, '♦'), Card(5, '♣'), Card(6, '♠')]  # 两对
        self.player1.hand['bottom'] = [Card(7, '♠'), Card(7, '♥'), Card(7, '♦'), Card(8, '♣'), Card(8, '♠')]  # 葫芦
        
        # 计算得分
        score = self.game.calculate_total_score(self.player1)
        self.assertGreater(score, 0)
        
        # 为玩家2设置一个爆牌的手牌
        self.player2.hand['top'] = [Card(14, '♠'), Card(13, '♥'), Card(12, '♦')]  # AAA
        self.player2.hand['middle'] = [Card(11, '♠'), Card(10, '♥'), Card(9, '♦'), Card(8, '♣'), Card(7, '♠')]  # 顺子
        self.player2.hand['bottom'] = [Card(6, '♠'), Card(5, '♥'), Card(4, '♦'), Card(3, '♣'), Card(2, '♠')]  # 高牌
        
        # 计算得分（应该为0，因为爆牌）
        busted_score = self.game.calculate_total_score(self.player2)
        self.assertEqual(busted_score, 0)
    
    def test_determine_winner(self):
        """
        测试确定获胜者
        """
        # 为玩家1设置一个有效的手牌
        self.player1.hand['top'] = [Card(2, '♠'), Card(2, '♥'), Card(3, '♦')]  # 一对2
        self.player1.hand['middle'] = [Card(4, '♠'), Card(4, '♥'), Card(5, '♦'), Card(5, '♣'), Card(6, '♠')]  # 两对
        self.player1.hand['bottom'] = [Card(7, '♠'), Card(7, '♥'), Card(7, '♦'), Card(8, '♣'), Card(8, '♠')]  # 葫芦
        
        # 为玩家2设置一个较弱的手牌
        self.player2.hand['top'] = [Card(2, '♠'), Card(3, '♥'), Card(4, '♦')]  # 高牌
        self.player2.hand['middle'] = [Card(5, '♠'), Card(6, '♥'), Card(7, '♦'), Card(8, '♣'), Card(9, '♠')]  # 高牌
        self.player2.hand['bottom'] = [Card(10, '♠'), Card(11, '♥'), Card(12, '♦'), Card(13, '♣'), Card(14, '♠')]  # 高牌
        
        # 确定获胜者
        winner = self.game.determine_winner()
        self.assertEqual(winner, self.player1)

if __name__ == '__main__':
    unittest.main()
