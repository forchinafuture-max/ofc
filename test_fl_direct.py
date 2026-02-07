from core import Player, Table, Card
from game_logic import OFCGame
from ai_strategy import AIPlayer

# 创建测试脚本，直接进入Fantasy Land模式并允许手动摆牌
def test_fl_direct():
    print("========================================")
    print("    直接进入Fantasy Land模式")
    print("========================================")
    
    # 创建测试玩家
    player = Player("玩家a")
    ai_player = AIPlayer("AI", difficulty="medium")
    
    # 创建桌子和游戏
    table = Table()
    game = OFCGame()
    game.add_player(player)
    game.add_player(ai_player)
    
    # 设置玩家a顶部拿了AA
    print("\n=== 玩家a顶部拿了AA ===")
    player.last_top_hand = [Card('A', '♠'), Card('A', '♥'), Card('J', '♦')]
    
    # 检查Fantasy Land模式
    print("检查是否进入Fantasy Land模式...")
    game.check_fantasy_mode()
    
    if game.table.fantasy_mode:
        print("✓ 成功进入Fantasy Land模式！")
        fantasy_cards = getattr(game.table, 'fantasy_cards', 16)
        print(f"根据顶部AA，一次性发{fantasy_cards}张牌")
        
        print("\n========================================")
        print("           进入范特西模式！")
        print("========================================")
        print(f"根据顶部牌型，一次性发{fantasy_cards}张牌")
        print("========================================")
        print("玩家自由摆牌到三个区域")
        print("顶部区域：3张牌")
        print("中部区域：5张牌")
        print("底部区域：5张牌")
        print("========================================")
        
        # 生成测试牌
        test_cards = [
            Card('A', '♣'), Card('K', '♠'), Card('Q', '♥'), Card('J', '♦'),
            Card('10', '♠'), Card('9', '♥'), Card('8', '♦'), Card('7', '♣'),
            Card('6', '♠'), Card('5', '♥'), Card('4', '♦'), Card('3', '♣'),
            Card('2', '♠'), Card('A', '♦'), Card('K', '♥'), Card('Q', '♦')
        ]
        
        # 分配牌给玩家
        player.hand['temp'] = test_cards[:fantasy_cards]
        
        # 显示待摆放的牌
        print("\n玩家a的手牌:")
        print(f"待摆放: {player.hand['temp']}")
        print("顶部区域: []")
        print("中部区域: []")
        print("底部区域: []")
        
        # 一张一张地选择牌并分配到区域
        while player.hand['temp']:
            print("\n当前牌型状态:")
            print(f"顶部区域: {len(player.hand['top'])}张牌 (最多3张)")
            print(f"中部区域: {len(player.hand['middle'])}张牌 (需要5张)")
            print(f"底部区域: {len(player.hand['bottom'])}张牌 (需要5张)")
            
            # 选择要摆放的牌
            print("\n待选择的牌:")
            for i, card in enumerate(player.hand['temp']):
                print(f"{i+1}. {card}")
            
            # 选择要使用的牌
            while True:
                card_choice = input(f"请选择要使用的牌 (1-{len(player.hand['temp'])}): ")
                if card_choice.isdigit():
                    card_idx = int(card_choice) - 1
                    if 0 <= card_idx < len(player.hand['temp']):
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
            selected_card = player.hand['temp'].pop(card_idx)
            player.hand[area].append(selected_card)
            print(f"已将 {selected_card} 放到 {area_map[area_choice]} 区域")
            
            # 显示当前已摆好的牌
            print("\n当前已摆好的牌:")
            print(f"顶部区域: {player.hand['top']}")
            print(f"中部区域: {player.hand['middle']}")
            print(f"底部区域: {player.hand['bottom']}")
            
            input("按回车键继续...")
        
        # 玩家摆牌完成
        print("\n========================================")
        print("           摆牌完成！")
        print("========================================")
        print(f"顶部区域: {player.hand['top']}")
        print(f"中部区域: {player.hand['middle']}")
        print(f"底部区域: {player.hand['bottom']}")
        print("========================================")
        
        # AI摆牌
        print("\n=== AI摆牌 ===")
        print("AI开始摆牌...")
        # 模拟AI摆牌
        ai_cards = [
            Card('A', '♣'), Card('K', '♠'), Card('Q', '♥'), Card('J', '♦'),
            Card('10', '♠'), Card('9', '♥'), Card('8', '♦'), Card('7', '♣'),
            Card('6', '♠'), Card('5', '♥'), Card('4', '♦'), Card('3', '♣'),
            Card('2', '♠'), Card('A', '♦'), Card('K', '♥'), Card('Q', '♦')
        ]
        # 按点数排序
        ai_cards.sort(key=lambda x: x.value)
        # 分配牌
        ai_player.hand['top'] = ai_cards[:3]  # 顶部放最弱的3张
        ai_player.hand['middle'] = ai_cards[3:8]  # 中间放中等强度的5张
        ai_player.hand['bottom'] = ai_cards[8:13]  # 底部放最强的5张
        
        print("AI摆牌完成！")
        print(f"AI顶部区域: {ai_player.hand['top']}")
        print(f"AI中部区域: {ai_player.hand['middle']}")
        print(f"AI底部区域: {ai_player.hand['bottom']}")
        
        # 判定胜负
        print("\n========================================")
        print("           判定胜负！")
        print("========================================")
        
        # 模拟判定胜负
        print("计算得分中...")
        # 简单的胜负判定
        player_score = 0
        ai_score = 0
        
        # 比较顶部
        print("\n比较顶部区域...")
        print(f"玩家a顶部: {player.hand['top']}")
        print(f"AI顶部: {ai_player.hand['top']}")
        print("玩家a顶部更强，+1分")
        player_score += 1
        
        # 比较中部
        print("\n比较中部区域...")
        print(f"玩家a中部: {player.hand['middle']}")
        print(f"AI中部: {ai_player.hand['middle']}")
        print("AI中部更强，+1分")
        ai_score += 1
        
        # 比较底部
        print("\n比较底部区域...")
        print(f"玩家a底部: {player.hand['bottom']}")
        print(f"AI底部: {ai_player.hand['bottom']}")
        print("AI底部更强，+1分")
        ai_score += 1
        
        # 显示得分
        print("\n========================================")
        print("           最终得分")
        print("========================================")
        print(f"玩家a: {player_score} 分")
        print(f"AI: {ai_score} 分")
        
        # 判定获胜者
        if player_score > ai_score:
            winner = "玩家a"
        else:
            winner = "AI"
        
        print(f"\n获胜者: {winner}")
        print("========================================")
        print("        测试完成")
        print("========================================")
    else:
        print("✗ 未能进入Fantasy Land模式")

if __name__ == "__main__":
    test_fl_direct()