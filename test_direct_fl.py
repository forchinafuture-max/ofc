from core import Player, Table, Card
from game_logic import OFCGame
from ai_strategy import AIPlayer

# 创建测试脚本，直接进入Fantasy Land模式并允许手动摆牌
def test_direct_fl():
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
        
        # 显示手牌
        print("\n玩家a的手牌:")
        print(f"待摆放: {player.hand['temp']}")
        print("顶部区域: []")
        print("中部区域: []")
        print("底部区域: []")
        
        # 手动摆牌
        print("\n=== 开始手动摆牌 ===")
        print("请按照提示输入牌的序号，用空格分隔")
        
        # 选择顶部区域的牌
        while True:
            try:
                top_input = input("请选择顶部区域的3张牌 (输入卡号，用空格分隔): ")
                top_indices = list(map(int, top_input.split()))
                if len(top_indices) != 3:
                    print("请输入3张牌的序号")
                    continue
                if all(1 <= idx <= len(player.hand['temp']) for idx in top_indices):
                    break
                else:
                    print("输入的序号超出范围")
            except ValueError:
                print("请输入有效的数字")
        
        # 选择中部区域的牌
        while True:
            try:
                middle_input = input("请选择中部区域的5张牌 (输入卡号，用空格分隔): ")
                middle_indices = list(map(int, middle_input.split()))
                if len(middle_indices) != 5:
                    print("请输入5张牌的序号")
                    continue
                if all(1 <= idx <= len(player.hand['temp']) for idx in middle_indices):
                    break
                else:
                    print("输入的序号超出范围")
            except ValueError:
                print("请输入有效的数字")
        
        # 选择底部区域的牌
        while True:
            try:
                bottom_input = input("请选择底部区域的5张牌 (输入卡号，用空格分隔): ")
                bottom_indices = list(map(int, bottom_input.split()))
                if len(bottom_indices) != 5:
                    print("请输入5张牌的序号")
                    continue
                if all(1 <= idx <= len(player.hand['temp']) for idx in bottom_indices):
                    break
                else:
                    print("输入的序号超出范围")
            except ValueError:
                print("请输入有效的数字")
        
        # 验证所有牌都被选择，且没有重复
        all_indices = top_indices + middle_indices + bottom_indices
        if len(all_indices) != len(set(all_indices)):
            print("有重复的牌，测试结束")
            return
        
        # 分配牌
        top_cards = [player.hand['temp'][idx-1] for idx in top_indices]
        middle_cards = [player.hand['temp'][idx-1] for idx in middle_indices]
        bottom_cards = [player.hand['temp'][idx-1] for idx in bottom_indices]
        
        # 放置牌
        player.hand['top'] = top_cards
        player.hand['middle'] = middle_cards
        player.hand['bottom'] = bottom_cards
        player.hand['temp'] = []
        
        print("\n========================================")
        print("           摆牌完成！")
        print("========================================")
        print(f"顶部区域: {player.hand['top']}")
        print(f"中部区域: {player.hand['middle']}")
        print(f"底部区域: {player.hand['bottom']}")
        print("========================================")
        print("        测试完成")
        print("========================================")
    else:
        print("✗ 未能进入Fantasy Land模式")

if __name__ == "__main__":
    test_direct_fl()