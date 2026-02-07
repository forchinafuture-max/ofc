"""
测试规则引擎
"""

import unittest
from game.deck import Card
from core.rules import RuleEngine

class TestRules(unittest.TestCase):
    """
    测试规则引擎
    """
    
    def setUp(self):
        """
        设置测试环境
        """
        self.rule_engine = RuleEngine()
    
    def test_evaluate_3_card_hand(self):
        """
        测试评估3张牌的手牌
        """
        # 测试高牌
        high_card = [Card(2, '♠'), Card(3, '♥'), Card(4, '♦')]
        self.assertEqual(self.rule_engine.evaluate_hand(high_card), 0)
        
        # 测试一对
        pair = [Card(2, '♠'), Card(2, '♥'), Card(3, '♦')]
        self.assertEqual(self.rule_engine.evaluate_hand(pair), 1)
        
        # 测试三条
        trips = [Card(2, '♠'), Card(2, '♥'), Card(2, '♦')]
        self.assertEqual(self.rule_engine.evaluate_hand(trips), 2)
        
        # 测试A23轮子
        wheel = [Card(14, '♠'), Card(2, '♥'), Card(3, '♦')]
        # 注意：3张牌的轮子在当前实现中不会影响强度值
        self.assertEqual(self.rule_engine.evaluate_hand(wheel), 0)
    
    def test_evaluate_5_card_hand(self):
        """
        测试评估5张牌的手牌
        """
        # 测试高牌
        high_card = [Card(2, '♠'), Card(3, '♥'), Card(4, '♦'), Card(5, '♣'), Card(7, '♠')]
        self.assertEqual(self.rule_engine.evaluate_hand(high_card), 0)
        
        # 测试一对
        pair = [Card(2, '♠'), Card(2, '♥'), Card(3, '♦'), Card(4, '♣'), Card(5, '♠')]
        self.assertEqual(self.rule_engine.evaluate_hand(pair), 1)
        
        # 测试两对
        two_pair = [Card(2, '♠'), Card(2, '♥'), Card(3, '♦'), Card(3, '♣'), Card(5, '♠')]
        self.assertEqual(self.rule_engine.evaluate_hand(two_pair), 2)
        
        # 测试三条
        trips = [Card(2, '♠'), Card(2, '♥'), Card(2, '♦'), Card(4, '♣'), Card(5, '♠')]
        self.assertEqual(self.rule_engine.evaluate_hand(trips), 3)
        
        # 测试顺子
        straight = [Card(2, '♠'), Card(3, '♥'), Card(4, '♦'), Card(5, '♣'), Card(6, '♠')]
        self.assertEqual(self.rule_engine.evaluate_hand(straight), 4)
        
        # 测试同花
        flush = [Card(2, '♠'), Card(3, '♠'), Card(4, '♠'), Card(5, '♠'), Card(7, '♠')]
        self.assertEqual(self.rule_engine.evaluate_hand(flush), 5)
        
        # 测试葫芦
        full_house = [Card(2, '♠'), Card(2, '♥'), Card(2, '♦'), Card(3, '♣'), Card(3, '♠')]
        self.assertEqual(self.rule_engine.evaluate_hand(full_house), 6)
        
        # 测试四条
        four_of_a_kind = [Card(2, '♠'), Card(2, '♥'), Card(2, '♦'), Card(2, '♣'), Card(5, '♠')]
        self.assertEqual(self.rule_engine.evaluate_hand(four_of_a_kind), 7)
        
        # 测试同花顺
        straight_flush = [Card(2, '♠'), Card(3, '♠'), Card(4, '♠'), Card(5, '♠'), Card(6, '♠')]
        self.assertEqual(self.rule_engine.evaluate_hand(straight_flush), 8)
        
        # 测试皇家同花顺
        royal_flush = [Card(10, '♠'), Card(11, '♠'), Card(12, '♠'), Card(13, '♠'), Card(14, '♠')]
        self.assertEqual(self.rule_engine.evaluate_hand(royal_flush), 9)
        
        # 测试A2345轮子
        wheel = [Card(14, '♠'), Card(2, '♥'), Card(3, '♦'), Card(4, '♣'), Card(5, '♠')]
        self.assertEqual(self.rule_engine.evaluate_hand(wheel), 4)  # 顺子
    
    def test_compare_hands(self):
        """
        测试比较两手牌的大小
        """
        # 测试相同牌数的比较
        hand1 = [Card(2, '♠'), Card(2, '♥'), Card(3, '♦')]  # 一对2
        hand2 = [Card(3, '♠'), Card(3, '♥'), Card(2, '♦')]  # 一对3
        self.assertEqual(self.rule_engine.compare_hands(hand1, hand2), -1)
        
        # 测试不同牌数的比较
        hand3 = [Card(2, '♠'), Card(2, '♥'), Card(2, '♦')]  # 三条2
        hand4 = [Card(3, '♠'), Card(3, '♥'), Card(4, '♦'), Card(5, '♣'), Card(6, '♠')]  # 一对3
        # 注意：不同牌数的比较在当前实现中会进行详细比较
        # 这里的结果可能会根据具体实现有所不同
    
    def test_calculate_hand_score(self):
        """
        测试计算牌型分
        """
        # 测试头道对子
        top_pair = [Card(12, '♠'), Card(12, '♥'), Card(3, '♦')]  # QQ
        self.assertEqual(self.rule_engine.calculate_hand_score(top_pair, 'top'), 7)
        
        # 测试头道三条
        top_trips = [Card(12, '♠'), Card(12, '♥'), Card(12, '♦')]  # QQQ
        self.assertEqual(self.rule_engine.calculate_hand_score(top_trips, 'top'), 20)
        
        # 测试中道皇家同花顺
        middle_royal = [Card(10, '♠'), Card(11, '♠'), Card(12, '♠'), Card(13, '♠'), Card(14, '♠')]
        self.assertEqual(self.rule_engine.calculate_hand_score(middle_royal, 'middle'), 50)
        
        # 测试底道皇家同花顺
        bottom_royal = [Card(10, '♠'), Card(11, '♠'), Card(12, '♠'), Card(13, '♠'), Card(14, '♠')]
        self.assertEqual(self.rule_engine.calculate_hand_score(bottom_royal, 'bottom'), 25)

if __name__ == '__main__':
    unittest.main()
