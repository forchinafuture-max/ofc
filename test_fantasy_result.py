from core import Player, Deck, Card
from game_logic import OFCGame

# 创建游戏实例
game = OFCGame()

# 创建玩家
player = Player("玩家a")
ai_player = Player("AI")

# 添加玩家到游戏
game.add_player(player)
game.add_player(ai_player)

print("========================================")
print("          范特西模式结算测试")
print("========================================")

# 手动设置玩家和AI的手牌（模拟范特西模式后的情况）
print("\n设置玩家手牌（范特西模式）:")
# 玩家手牌：底部三条Q，中部对子J，顶部小牌
player.hand['top'] = [Card('4', '♦'), Card('3', '♦'), Card('2', '♦')]
player.hand['middle'] = [Card('J', '♥'), Card('J', '♠'), Card('10', '♦'), Card('8', '♦'), Card('6', '♣')]
player.hand['bottom'] = [Card('A', '♠'), Card('K', '♥'), Card('Q', '♦'), Card('Q', '♣'), Card('Q', '♠')]

print(f"玩家顶部区域: {player.hand['top']}")
print(f"玩家中部区域: {player.hand['middle']}")
print(f"玩家底部区域: {player.hand['bottom']}")

print("\n设置AI手牌（普通模式）:")
# AI手牌：简化处理，确保爆牌
ai_player.hand['top'] = [Card('8', '♣'), Card('6', '♦'), Card('5', '♥')]
ai_player.hand['middle'] = [Card('4', '♥'), Card('3', '♥')]
ai_player.hand['bottom'] = [Card('4', '♥'), Card('3', '♥')]

print(f"AI顶部区域: {ai_player.hand['top']}")
print(f"AI中部区域: {ai_player.hand['middle']}")
print(f"AI底部区域: {ai_player.hand['bottom']}")

# 结算阶段
print("\n========================================")
print("           结算阶段")
print("========================================")

# 检查是否爆牌
player_busted = game.check_busted(player)
ai_busted = game.check_busted(ai_player)

print(f"玩家是否爆牌: {player_busted}")
print(f"AI是否爆牌: {ai_busted}")

# 计算得分
player_score = game.calculate_score(player, ai_player)
ai_score = game.calculate_score(ai_player, player)

print(f"\n详细得分:")
print(f"玩家a: {player_score} 分")
print(f"AI: {ai_score} 分")

# 确定获胜者
winner = game.determine_winner()
print(f"\n获胜者: {winner.name}")

# 检查是否满足留在范特西模式的条件
print("\n========================================")
print("           范特西模式留存检查")
print("========================================")

# 模拟玩家进入过范特西模式
player.fantasy_mode = True

player_stay = game.check_fantasy_stay_condition(player)
print(f"玩家是否满足留在范特西模式条件: {player_stay}")

if player_stay:
    print("底部拿到4条以上或顶部拿到222+以上，继续留在范特西模式！")
    print("下一局将继续以范特西模式进行，一次性发14张牌。")
else:
    print("不满足留在范特西模式条件，下一局将返回普通模式。")

# 显示详细的手牌强度比较
print("\n========================================")
print("           手牌强度分析")
print("========================================")

print("玩家手牌强度:")
print(f"顶部: {game.evaluate_hand(player.hand['top'])}")
print(f"中部: {game.evaluate_hand(player.hand['middle'])}")
print(f"底部: {game.evaluate_hand(player.hand['bottom'])}")

print("\nAI手牌强度:")
print(f"顶部: {game.evaluate_hand(ai_player.hand['top'])}")
print(f"中部: {game.evaluate_hand(ai_player.hand['middle'])}")
print(f"底部: {game.evaluate_hand(ai_player.hand['bottom'])}")

print("\n========================================")
print("           测试完成！")
print("========================================")
