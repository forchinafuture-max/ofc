from core import Player, Deck
from game_logic import OFCGame

# 创建游戏实例
game = OFCGame()

# 创建玩家
player = Player("玩家a")
ai_player = Player("AI")

# 添加玩家到游戏
game.add_player(player)
game.add_player(ai_player)

# 模拟前一局玩家拿到QQ的情况
# 创建QQ的牌型
from core import Card
# 先设置hand['top']，因为reset_hand会保存这个到last_top_hand
player.hand['top'] = [Card('Q', '♥'), Card('Q', '♦'), Card('K', '♠')]
ai_player.hand['top'] = [Card('K', '♥'), Card('J', '♦'), Card('10', '♠')]

print("========================================")
print("测试范特西模式流程")
print("========================================")
print(f"前一局玩家顶部手牌: {player.hand['top']}")
print(f"前一局AI顶部手牌: {ai_player.hand['top']}")

# 开始游戏
game.start_game()

# 检查范特西模式
game.check_fantasy_mode()

print(f"\n玩家范特西模式状态: {player.fantasy_mode}")
print(f"AI范特西模式状态: {ai_player.fantasy_mode}")

if hasattr(player, 'fantasy_cards'):
    print(f"玩家范特西模式发牌数量: {player.fantasy_cards}")

print("\n测试完成！")
print("========================================")
