from core import Player, Card, Deck
from game_logic import OFCGame
from ui import GameUI
from ai_strategy import AIStrategy
from fantasy_mode import FantasyModeManager

# 创建游戏实例
game = OFCGame()
ui = GameUI()
ai_strategy = AIStrategy()

# 创建玩家和AI
player = Player("玩家a", 1000)
ai_player = Player("AI (中等)", 1000)

# 添加玩家到游戏
game.add_player(player)
game.add_player(ai_player)

# 设置玩家的上一局手牌，顶部为KK，确保触发FL阶段
player.last_hand = {
    'top': [Card('K', '♦'), Card('K', '♠'), Card('A', '♣')],
    'middle': [Card('5', '♥'), Card('2', '♠'), Card('2', '♥'), Card('5', '♣'), Card('6', '♠')],
    'bottom': [Card('10', '♠'), Card('9', '♣'), Card('8', '♣'), Card('J', '♣'), Card('7', '♥')]
}
player.last_top_hand = player.last_hand['top']

# 设置AI的上一局手牌，不触发FL阶段
ai_player.last_hand = {
    'top': [Card('5', '♠'), Card('4', '♠'), Card('4', '♥')],
    'middle': [Card('10', '♥'), Card('10', '♦'), Card('6', '♥'), Card('A', '♦'), Card('7', '♠')],
    'bottom': [Card('J', '♠'), Card('Q', '♠'), Card('9', '♠'), Card('A', '♠'), Card('J', '♥')]
}
ai_player.last_top_hand = ai_player.last_hand['top']

# 检查范特西模式
game.check_fantasy_mode()

# 创建FantasyModeManager实例
fantasy_manager = FantasyModeManager(game, ui, ai_strategy)

# 触发范特西模式
print("\n========================================")
print("           测试范特西模式")
print("========================================")
print(f"玩家a是否进入FL模式: {player.fantasy_mode}")
print(f"AI是否进入FL模式: {ai_player.fantasy_mode}")

# 处理范特西模式
if player.fantasy_mode:
    print("\n========================================")
    print("           进入范特西模式！")
    print("========================================")
    # 重新初始化牌堆
    game.deck = Deck()
    print("重新洗牌，确保有足够的牌进行范特西模式游戏")
    
    # 处理进入范特西模式的玩家（一次性发牌和摆牌）
    print(f"\n{player.name}进入范特西模式:")
    # 确定发牌数量
    fantasy_cards = getattr(player, 'fantasy_cards', 14)
    print(f"一次性发{fantasy_cards}张牌")
    
    # 清空所有手牌区域
    player.hand['temp'] = []
    player.hand['top'] = []
    player.hand['middle'] = []
    player.hand['bottom'] = []
    
    # 发Fantasy Land模式的牌
    for _ in range(fantasy_cards):
        if game.deck.cards:
            player.hand['temp'].append(game.deck.deal(1)[0])
    
    # 显示手牌
    print(f"{player.name}的手牌:")
    print(f"待摆放: {player.hand['temp']}")
    print(f"顶部区域: {player.hand['top']}")
    print(f"中部区域: {player.hand['middle']}")
    print(f"底部区域: {player.hand['bottom']}")
    
    # 处理未进入范特西模式的玩家（一次性发牌和摆牌）
    print(f"\n{ai_player.name}按普通模式进行游戏:")
    print("========================================")
    
    # 清空所有手牌区域
    ai_player.hand['temp'] = []
    ai_player.hand['top'] = []
    ai_player.hand['middle'] = []
    ai_player.hand['bottom'] = []
    
    # 一次性发足够的牌（模拟完整的普通模式）
    total_cards = 13  # 顶部3张 + 中部5张 + 底部5张
    print(f"一次性发{total_cards}张牌（模拟完整的普通模式）:")
    
    for _ in range(total_cards):
        if game.deck.cards:
            ai_player.hand['temp'].append(game.deck.deal(1)[0])
    
    # 显示手牌
    print(f"{ai_player.name}的手牌:")
    print(f"待摆放: {ai_player.hand['temp']}")
    print(f"顶部区域: {ai_player.hand['top']}")
    print(f"中部区域: {ai_player.hand['middle']}")
    print(f"底部区域: {ai_player.hand['bottom']}")
    
    # AI自动摆牌
    print(f"\n{ai_player.name}开始摆牌...")
    print(f"AI (中等)在FL阶段自动摆牌...")
    # 简单的AI摆牌策略
    if ai_player.hand['temp']:
        # 简单的AI摆牌策略
        temp_cards = ai_player.hand['temp']
        
        # 按点数排序
        temp_cards.sort(key=lambda x: x.value, reverse=True)
        
        # 分配牌
        top_cards = temp_cards[:3]  # 顶部放最弱的3张
        middle_cards = temp_cards[3:8]  # 中间放中等强度的5张
        bottom_cards = temp_cards[8:13]  # 底部放最强的5张
        
        # 放置牌
        ai_player.hand['top'] = top_cards
        ai_player.hand['middle'] = middle_cards
        ai_player.hand['bottom'] = bottom_cards
        ai_player.hand['temp'] = []
        
        print(f"AI已完成摆牌")
        print(f"顶部区域: {ai_player.hand['top']}")
        print(f"中部区域: {ai_player.hand['middle']}")
        print(f"底部区域: {ai_player.hand['bottom']}")

print("\n========================================")
print("           测试完成！")
print("========================================")
