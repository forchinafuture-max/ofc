from core import Player, Deck
from game_logic import OFCGame

# 测试游戏初始化
print("测试游戏初始化...")
game = OFCGame()

# 创建玩家
player1 = Player("玩家a")
player2 = Player("玩家b")

game.add_player(player1)
game.add_player(player2)

# 测试发牌
print("测试发牌...")
game.start_game()
game.deal_round()

print("玩家1手牌:", player1.hand)
print("玩家2手牌:", player2.hand)

print("测试完成，游戏组件正常工作！")