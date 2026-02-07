from core import Player, Deck, Card
from game_logic import OFCGame

# 创建游戏实例
game = OFCGame()

print("========================================")
print("          手牌比较测试")
print("========================================")

# 测试用例1：比较两个对子
print("\n测试用例1：比较两个对子")
hand1 = [Card('Q', '♦'), Card('Q', '♣'), Card('K', '♥'), Card('A', '♠'), Card('8', '♣')]  # 对子Q
hand2 = [Card('6', '♦'), Card('6', '♣'), Card('J', '♥'), Card('K', '♣'), Card('A', '♣')]  # 对子6

result = game.compare_hands(hand1, hand2)
print(f"对子Q vs 对子6: {result}")
print(f"预期结果: 1 (对子Q > 对子6)")

# 测试用例2：比较相同强度的高牌
print("\n测试用例2：比较相同强度的高牌")
hand3 = [Card('K', '♦'), Card('Q', '♣'), Card('J', '♥'), Card('10', '♠'), Card('9', '♣')]  # 高牌KQJT9
hand4 = [Card('Q', '♦'), Card('J', '♣'), Card('10', '♥'), Card('9', '♠'), Card('8', '♣')]  # 高牌QJT98

result = game.compare_hands(hand3, hand4)
print(f"高牌KQJT9 vs 高牌QJT98: {result}")
print(f"预期结果: 1 (KQJT9 > QJT98)")

# 测试用例3：测试爆牌检测
print("\n测试用例3：测试爆牌检测")
player = Player("测试玩家")

# 设置玩家手牌：底部对子Q，中部对子6，顶部小牌
player.hand['top'] = [Card('4', '♦'), Card('3', '♦'), Card('2', '♦')]  # 高牌
player.hand['middle'] = [Card('6', '♦'), Card('6', '♣'), Card('J', '♥'), Card('K', '♣'), Card('A', '♣')]  # 对子6
player.hand['bottom'] = [Card('Q', '♦'), Card('Q', '♣'), Card('K', '♥'), Card('A', '♠'), Card('8', '♣')]  # 对子Q

is_busted = game.check_busted(player)
print(f"底部对子Q，中部对子6，顶部小牌：是否爆牌？ {is_busted}")
print(f"预期结果: False (底部Q > 中部6 > 顶部小牌)")

# 测试用例4：测试错误的牌型顺序
print("\n测试用例4：测试错误的牌型顺序")
player2 = Player("测试玩家2")

# 设置玩家手牌：底部对子6，中部对子Q，顶部小牌（错误顺序）
player2.hand['top'] = [Card('4', '♦'), Card('3', '♦'), Card('2', '♦')]  # 高牌
player2.hand['middle'] = [Card('Q', '♦'), Card('Q', '♣'), Card('K', '♥'), Card('A', '♠'), Card('8', '♣')]  # 对子Q
player2.hand['bottom'] = [Card('6', '♦'), Card('6', '♣'), Card('J', '♥'), Card('K', '♣'), Card('A', '♣')]  # 对子6

is_busted2 = game.check_busted(player2)
print(f"底部对子6，中部对子Q，顶部小牌：是否爆牌？ {is_busted2}")
print(f"预期结果: True (底部6 < 中部Q，爆牌)")

print("\n========================================")
print("          测试完成！")
print("========================================")
