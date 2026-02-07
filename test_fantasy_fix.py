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

# 模拟前一局玩家拿到QQ的情况
player.hand['top'] = [Card('Q', '♥'), Card('Q', '♦'), Card('K', '♠')]

print("========================================")
print("          范特西模式修复测试")
print("========================================")

# 开始游戏
game.start_game()

print(f"玩家范特西模式状态: {player.fantasy_mode}")
print(f"AI范特西模式状态: {ai_player.fantasy_mode}")

if player.fantasy_mode:
    print(f"玩家范特西模式发牌数量: {player.fantasy_cards}")
    
    # 执行范特西模式发牌
    print("\n========================================")
    print("           范特西模式发牌")
    print("========================================")
    
    # 清空所有手牌区域
    player.hand['temp'] = []
    player.hand['top'] = []
    player.hand['middle'] = []
    player.hand['bottom'] = []
    
    # 发Fantasy Land模式的牌
    fantasy_cards = getattr(player, 'fantasy_cards', 14)
    print(f"给{player.name}一次性发{fantasy_cards}张牌:")
    
    for _ in range(fantasy_cards):
        if game.deck.cards:
            player.hand['temp'].append(game.deck.deal(1)[0])
    
    print(f"{player.name}的手牌: {player.hand['temp']}")
    
    # 为AI发普通模式的牌（修复后）
    print("\n========================================")
    print("           AI普通模式发牌")
    print("========================================")
    
    # 清空所有手牌区域
    ai_player.hand['temp'] = []
    ai_player.hand['top'] = []
    ai_player.hand['middle'] = []
    ai_player.hand['bottom'] = []
    
    # 发足够的牌（模拟完整的普通模式发牌）
    total_cards = 13  # 顶部3张 + 中部5张 + 底部5张
    print(f"给{ai_player.name}一次性发{total_cards}张牌（模拟完整的普通模式）:")
    
    for _ in range(total_cards):
        if game.deck.cards:
            ai_player.hand['temp'].append(game.deck.deal(1)[0])
    
    print(f"{ai_player.name}的手牌: {ai_player.hand['temp']}")
    
    # 自动摆牌
    print("\n========================================")
    print("           自动摆牌")
    print("========================================")
    
    # 玩家自动摆牌
    temp_cards = player.hand['temp'].copy()
    temp_cards.sort(key=lambda x: x.value, reverse=True)
    player.hand['top'] = temp_cards[10:13]
    player.hand['middle'] = temp_cards[5:10]
    player.hand['bottom'] = temp_cards[:5]
    player.hand['temp'] = []
    
    print(f"玩家顶部区域: {player.hand['top']}")
    print(f"玩家中部区域: {player.hand['middle']}")
    print(f"玩家底部区域: {player.hand['bottom']}")
    
    # AI自动摆牌
    ai_temp_cards = ai_player.hand['temp'].copy()
    ai_temp_cards.sort(key=lambda x: x.value, reverse=True)
    ai_player.hand['top'] = ai_temp_cards[:3]
    ai_player.hand['middle'] = ai_temp_cards[3:8]
    ai_player.hand['bottom'] = ai_temp_cards[8:13]
    ai_player.hand['temp'] = []
    
    print(f"\nAI顶部区域: {ai_player.hand['top']}")
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
    
    print("\n========================================")
    print("          测试完成！")
    print("========================================")
else:
    print("未进入范特西模式，测试结束。")
