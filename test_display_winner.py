from core import Player, Card
from game_logic import OFCGame
from ui import GameUI

# 创建游戏和UI
print("测试display_winner方法...")
game = OFCGame()
ui = GameUI()

# 创建玩家
player1 = Player("玩家a")
player2 = Player("玩家b")

# 添加玩家到游戏
game.add_player(player1)
game.add_player(player2)

# 创建测试用的Card对象
def create_test_cards(card_strings):
    """根据字符串创建Card对象列表"""
    cards = []
    for card_str in card_strings:
        # 简化处理，创建具有基本属性的对象
        class MockCard:
            def __init__(self, value, suit):
                self.value = value
                self.suit = suit
            def __str__(self):
                return f"{self.value}{self.suit}"
        
        # 解析牌值和花色
        if card_str[0] == 'A':
            value = 14
        elif card_str[0] == 'K':
            value = 13
        elif card_str[0] == 'Q':
            value = 12
        elif card_str[0] == 'J':
            value = 11
        elif card_str[0] == 'T':
            value = 10
        else:
            value = int(card_str[0])
        
        suit = card_str[1]
        cards.append(MockCard(value, suit))
    return cards

# 模拟游戏结束的情况
print("\n测试场景1: 玩家1获胜，双方都没有爆牌")
player1.total_score = 10
player2.total_score = 0

# 模拟手牌
player1.hand = {
    'top': create_test_cards(['A♣', 'K♦', 'Q♥']),
    'middle': create_test_cards(['A♦', 'K♥', 'Q♦', 'J♥', 'T♦']),
    'bottom': create_test_cards(['A♥', 'K♣', 'Q♣', 'J♦', 'T♥']),
    'temp': []
}

player2.hand = {
    'top': create_test_cards(['J♣', 'T♦', '9♥']),
    'middle': create_test_cards(['J♦', 'T♥', '9♦', '8♥', '7♦']),
    'bottom': create_test_cards(['J♥', 'T♣', '9♣', '8♦', '7♥']),
    'temp': []
}

# 测试display_winner方法
winner = player1
ui.display_winner(winner, game)

print("\n测试场景2: 玩家2爆牌，玩家1获胜")
player1.total_score = 6  # 爆牌规则：获胜者得6分
player2.total_score = 0

# 模拟玩家2爆牌的情况
player2.hand = {
    'top': create_test_cards(['A♣', 'K♦', 'Q♥']),  # 顶部太强
    'middle': create_test_cards(['J♦', 'T♥', '9♦', '8♥', '7♦']),  # 中部太弱
    'bottom': create_test_cards(['A♥', 'K♣', 'Q♣', 'J♦', 'T♥']),
    'temp': []
}

# 测试display_winner方法
winner = player1
ui.display_winner(winner, game)

print("\n测试场景3: 多玩家情况")
# 添加第三个玩家
player3 = Player("玩家c")
game.add_player(player3)
player3.total_score = 5

player3.hand = {
    'top': create_test_cards(['K♣', 'Q♦', 'J♥']),
    'middle': create_test_cards(['K♦', 'Q♥', 'J♦', 'T♥', '9♦']),
    'bottom': create_test_cards(['K♥', 'Q♣', 'J♣', 'T♦', '9♥']),
    'temp': []
}

# 测试display_winner方法
winner = player1
ui.display_winner(winner, game)

print("\n测试场景4: 没有获胜者")
# 测试winner为None的情况
winner = None
ui.display_winner(winner, game)

print("\n测试完成，display_winner方法正常工作！")