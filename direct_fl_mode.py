from core import Player, Card, Deck
from game_logic import OFCGame
from ui import GameUI
from ai_strategy import AIStrategy

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

# 直接设置玩家为FL模式
player.fantasy_mode = True
player.fantasy_cards = 15  # KK触发，发15张牌

# 设置AI为普通模式
ai_player.fantasy_mode = False

# 重新初始化牌堆
game.deck = Deck()
print("重新洗牌，确保有足够的牌进行范特西模式游戏")

# 处理进入范特西模式的玩家（一次性发牌和摆牌）
print(f"\n{player.name}进入范特西模式:")
print(f"一次性发{player.fantasy_cards}张牌")

# 清空所有手牌区域
player.hand['temp'] = []
player.hand['top'] = []
player.hand['middle'] = []
player.hand['bottom'] = []

# 发Fantasy Land模式的牌
for _ in range(player.fantasy_cards):
    if game.deck.cards:
        player.hand['temp'].append(game.deck.deal(1)[0])

# 显示手牌
print(f"{player.name}的手牌:")
print(f"待摆放: {player.hand['temp']}")
print(f"顶部区域: {player.hand['top']}")
print(f"中部区域: {player.hand['middle']}")
print(f"底部区域: {player.hand['bottom']}")

# 玩家开始摆牌
print(f"\n{player.name}开始摆牌...")
print("\n=== 范特西模式摆牌 ===")
print("请将牌分配到三个区域:")
print("顶部区域：3张牌")
print("中部区域：5张牌")
print("底部区域：5张牌")

# 按照牌型排列显示
print("\n========================================")
print("           牌型排列显示")
print("========================================")
temp_cards = player.hand['temp']
# 按牌型分组
rank_groups = {}
for card in temp_cards:
    if card.rank not in rank_groups:
        rank_groups[card.rank] = []
    rank_groups[card.rank].append(card)
# 按牌型长度排序（四条 > 三条 > 对子 > 单牌）
sorted_groups = sorted(rank_groups.items(), key=lambda x: len(x[1]), reverse=True)
for rank, cards in sorted_groups:
    card_count = len(cards)
    if card_count == 4:
        print(f"四条: {cards}")
    elif card_count == 3:
        print(f"三条: {cards}")
    elif card_count == 2:
        print(f"对子: {cards}")
    else:
        print(f"单牌: {cards}")

# 按照花色排列显示
print("\n========================================")
print("           花色排列显示")
print("========================================")
# 按花色分组
suit_groups = {'♠': [], '♥': [], '♦': [], '♣': []}
for card in temp_cards:
    if card.suit in suit_groups:
        suit_groups[card.suit].append(card)
# 按花色显示
for suit, cards in suit_groups.items():
    if cards:
        # 按点数排序
        sorted_cards = sorted(cards, key=lambda x: x.value, reverse=True)
        print(f"{suit}: {sorted_cards}")

# 一张一张地选择牌并分配到区域
while temp_cards:
    print("\n当前牌型状态:")
    print(f"顶部区域: {len(player.hand['top'])}张牌 (最多3张)")
    print(f"中部区域: {len(player.hand['middle'])}张牌 (需要5张)")
    print(f"底部区域: {len(player.hand['bottom'])}张牌 (需要5张)")
    
    # 检查是否所有区域都已满
    if (len(player.hand['top']) >= 3 and 
        len(player.hand['middle']) >= 5 and 
        len(player.hand['bottom']) >= 5):
        print("\n========================================")
        print("           所有区域都已满！")
        print("========================================")
        print("摆牌完成，剩余牌将被丢弃。")
        print("========================================")
        break
    
    # 选择要摆放的牌
    print("\n待选择的牌:")
    for i, card in enumerate(temp_cards):
        print(f"{i+1}. {card}")
    
    # 选择要使用的牌
    while True:
        card_choice = input(f"请选择要使用的牌 (1-{len(temp_cards)}): ")
        if card_choice.isdigit():
            card_idx = int(card_choice) - 1
            if 0 <= card_idx < len(temp_cards):
                break
        print("无效选择，请重新输入")
    
    # 选择摆放区域
    while True:
        area_choice = input("请选择摆放区域 (1-顶部, 2-中部, 3-底部): ")
        if area_choice in ['1', '2', '3']:
            break
        print("无效选择，请重新输入")
    
    # 确定区域
    area_map = {'1': 'top', '2': 'middle', '3': 'bottom'}
    area = area_map[area_choice]
    
    # 检查区域牌数限制
    if area == 'top' and len(player.hand['top']) >= 3:
        print("顶部区域最多只能放3张牌！")
        input("按回车键继续...")
        continue
    elif area == 'middle' and len(player.hand['middle']) >= 5:
        print("中部区域最多只能放5张牌！")
        input("按回车键继续...")
        continue
    elif area == 'bottom' and len(player.hand['bottom']) >= 5:
        print("底部区域最多只能放5张牌！")
        input("按回车键继续...")
        continue
    
    # 摆放牌
    selected_card = temp_cards.pop(card_idx)
    player.hand[area].append(selected_card)
    print(f"已将 {selected_card} 放到 {area_map[area_choice]} 区域")
    
    # 显示当前已摆好的牌
    print("\n当前已摆好的牌:")
    print(f"顶部区域: {player.hand['top']}")
    print(f"中部区域: {player.hand['middle']}")
    print(f"底部区域: {player.hand['bottom']}")
    
    input("按回车键继续...")

# 摆牌完成后显示结果
print("\n========================================")
print("           摆牌完成！")
print("========================================")
print(f"顶部区域: {player.hand['top']}")
print(f"中部区域: {player.hand['middle']}")
print(f"底部区域: {player.hand['bottom']}")
print("========================================")

# 处理AI摆牌
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

# 游戏结束，判定胜负
print("\n========================================")
print("           范特西模式结束！")
print("========================================")

# 确定获胜者
winner = game.determine_winner()
print(f"获胜者: {winner.name}")

# 显示得分
print("\n详细得分:")
player_score = game.calculate_score(player, ai_player)
ai_score = game.calculate_score(ai_player, player)
print(f"{player.name}: {player_score} 分")
print(f"{ai_player.name}: {ai_score} 分")

print("\n========================================")
print("           游戏结束！")
print("========================================")
