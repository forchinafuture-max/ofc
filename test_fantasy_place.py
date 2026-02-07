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
    
    # 交互式摆牌
    print("\n========================================")
    print("           开始摆牌")
    print("========================================")
    print("请将14张牌摆放到三个区域:")
    print("- 顶部区域: 3张牌")
    print("- 中部区域: 5张牌")
    print("- 底部区域: 5张牌")
    print("规则: 底部强度 ≥ 中部强度 ≥ 顶部强度")
    
    # 按照牌型排列显示
    print("\n========================================")
    print("           牌型排列显示")
    print("========================================")
    # 按牌型分组
    rank_groups = {}
    for card in player.hand['temp']:
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
    for card in player.hand['temp']:
        if card.suit in suit_groups:
            suit_groups[card.suit].append(card)
    # 按花色显示
    for suit, cards in suit_groups.items():
        if cards:
            # 按点数排序
            sorted_cards = sorted(cards, key=lambda x: x.value, reverse=True)
            print(f"{suit}: {sorted_cards}")
    
    print("\n========================================")
    
    while len(player.hand['temp']) > 0:
        # 检查所有区域是否已满
        if len(player.hand['top']) >= 3 and len(player.hand['middle']) >= 5 and len(player.hand['bottom']) >= 5:
            print("\n========================================")
            print("           所有区域都已满！")
            print("========================================")
            print("摆牌完成，剩余牌将被丢弃。")
            print("========================================")
            break
        
        print("\n待摆放的牌:")
        for i, card in enumerate(player.hand['temp'], 1):
            print(f"{i}. {card}")
        
        # 显示当前区域状态
        print("\n当前区域状态:")
        print(f"顶部区域 ({len(player.hand['top'])}/3): {player.hand['top']}")
        print(f"中部区域 ({len(player.hand['middle'])}/5): {player.hand['middle']}")
        print(f"底部区域 ({len(player.hand['bottom'])}/5): {player.hand['bottom']}")
        
        # 选择牌
        try:
            card_idx = int(input("\n请选择要摆放的牌 (输入编号): ")) - 1
            if card_idx < 0 or card_idx >= len(player.hand['temp']):
                print("无效的选择，请重新输入！")
                continue
        except ValueError:
            print("请输入数字！")
            continue
        
        # 选择区域
        print("\n选择要摆放到的区域:")
        print("1. 顶部区域")
        print("2. 中部区域")
        print("3. 底部区域")
        
        try:
            region_idx = int(input("请选择区域 (输入编号): "))
            if region_idx < 1 or region_idx > 3:
                print("无效的选择，请重新输入！")
                continue
        except ValueError:
            print("请输入数字！")
            continue
        
        # 确定区域
        region_map = {1: 'top', 2: 'middle', 3: 'bottom'}
        region = region_map[region_idx]
        
        # 检查区域是否已满
        if region == 'top' and len(player.hand['top']) >= 3:
            print("顶部区域已满！")
            continue
        elif region == 'middle' and len(player.hand['middle']) >= 5:
            print("中部区域已满！")
            continue
        elif region == 'bottom' and len(player.hand['bottom']) >= 5:
            print("底部区域已满！")
            continue
        
        # 摆放牌
        selected_card = player.hand['temp'].pop(card_idx)
        player.hand[region].append(selected_card)
        
        print(f"\n成功将 {selected_card} 摆放到 {region} 区域！")
    
    # 摆牌完成
    print("\n========================================")
    print("           摆牌完成")
    print("========================================")
    print(f"顶部区域: {player.hand['top']}")
    print(f"中部区域: {player.hand['middle']}")
    print(f"底部区域: {player.hand['bottom']}")
    
    # 检查是否爆牌
    is_busted = game.check_busted(player)
    print(f"\n是否爆牌: {is_busted}")
    
    # 检查是否满足留在范特西模式的条件
    stay_condition = game.check_fantasy_stay_condition(player)
    print(f"是否满足留在范特西模式条件: {stay_condition}")
    
    if stay_condition:
        print("底部拿到4条以上或顶部拿到222+以上，继续留在范特西模式！")
    else:
        print("不满足留在范特西模式条件，下一局将返回普通模式。")
    
    print("\n测试完成！")
else:
    print("未进入范特西模式，测试结束。")
