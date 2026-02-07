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
print("          范特西模式测试")
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
    print(f"顶部区域: {player.hand['top']}")
    print(f"中部区域: {player.hand['middle']}")
    print(f"底部区域: {player.hand['bottom']}")
    
    # 为AI发普通模式的牌
    print("\n========================================")
    print("           AI普通模式发牌")
    print("========================================")
    
    ai_player.hand['temp'] = []
    ai_player.hand['top'] = []
    ai_player.hand['middle'] = []
    ai_player.hand['bottom'] = []
    
    # 普通模式第一轮发5张牌
    print(f"给{ai_player.name}发5张牌:")
    for _ in range(5):
        if game.deck.cards:
            ai_player.hand['temp'].append(game.deck.deal(1)[0])
    
    print(f"{ai_player.name}的手牌: {ai_player.hand['temp']}")
    print(f"顶部区域: {ai_player.hand['top']}")
    print(f"中部区域: {ai_player.hand['middle']}")
    print(f"底部区域: {ai_player.hand['bottom']}")
    
    print("\n========================================")
    print("          发牌完成，准备摆牌")
    print("========================================")
    print("现在可以开始摆牌了！")
    print("玩家需要将14张牌摆放到三个区域:")
    print("- 顶部区域: 3张牌")
    print("- 中部区域: 5张牌")
    print("- 底部区域: 5张牌")
    print("规则: 底部强度 ≥ 中部强度 ≥ 顶部强度")
else:
    print("未进入范特西模式，测试结束。")

print("\n测试完成！")
