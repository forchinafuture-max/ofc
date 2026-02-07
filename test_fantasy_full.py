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
print("          范特西模式完整测试")
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
    
    # 自动摆牌（简化测试）
    print("\n========================================")
    print("           自动摆牌")
    print("========================================")
    
    # 简化摆牌：按点数排序，最弱的放顶部，中等的放中部，最强的放底部
    temp_cards = player.hand['temp'].copy()
    temp_cards.sort(key=lambda x: x.value, reverse=True)
    
    # 底部放5张最强的牌
    player.hand['bottom'] = temp_cards[:5]
    # 中部放5张中等的牌
    player.hand['middle'] = temp_cards[5:10]
    # 顶部放3张最弱的牌
    player.hand['top'] = temp_cards[10:13]
    # 清空临时区域
    player.hand['temp'] = []
    
    # 显示摆牌结果
    print(f"顶部区域: {player.hand['top']}")
    print(f"中部区域: {player.hand['middle']}")
    print(f"底部区域: {player.hand['bottom']}")
    
    # AI普通模式发牌和摆牌
    print("\n========================================")
    print("           AI普通模式")
    print("========================================")
    
    # 给AI发5张牌
    ai_player.hand['temp'] = []
    for _ in range(5):
        if game.deck.cards:
            ai_player.hand['temp'].append(game.deck.deal(1)[0])
    
    print(f"AI手牌: {ai_player.hand['temp']}")
    
    # AI自动摆牌
    ai_cards = ai_player.hand['temp'].copy()
    ai_cards.sort(key=lambda x: x.value, reverse=True)
    
    ai_player.hand['top'] = ai_cards[:3]
    ai_player.hand['middle'] = ai_cards[3:5]
    ai_player.hand['bottom'] = ai_cards[3:8]  # 简化处理，重复使用牌
    ai_player.hand['temp'] = []
    
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
    
    player_stay = game.check_fantasy_stay_condition(player)
    print(f"玩家是否满足留在范特西模式条件: {player_stay}")
    
    if player_stay:
        print("底部拿到4条以上或顶部拿到222+以上，继续留在范特西模式！")
        print("下一局将继续以范特西模式进行，一次性发14张牌。")
    else:
        print("不满足留在范特西模式条件，下一局将返回普通模式。")
    
    print("\n========================================")
    print("           测试完成！")
    print("========================================")
else:
    print("未进入范特西模式，测试结束。")
