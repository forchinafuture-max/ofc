from core import Player, Table, Card
from game_logic import OFCGame
from ai_strategy import AIPlayer

# 创建测试脚本，模拟玩家a拿到AA后进入Fantasy Land模式并摆牌
def test_fantasy_play():
    print("========================================")
    print("    Fantasy Land模式摆牌测试")
    print("========================================")
    
    # 创建测试玩家
    player = Player("玩家a")
    ai_player = AIPlayer("AI", difficulty="medium")
    
    # 创建桌子和游戏
    table = Table()
    game = OFCGame()
    game.add_player(player)
    game.add_player(ai_player)
    
    # 假设玩家a拿了AA
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
        
        # 模拟发牌
        print("\n发牌中...")
        # 生成测试牌
        test_cards = [
            Card('A', '♣'), Card('K', '♠'), Card('Q', '♥'), Card('J', '♦'),
            Card('10', '♠'), Card('9', '♥'), Card('8', '♦'), Card('7', '♣'),
            Card('6', '♠'), Card('5', '♥'), Card('4', '♦'), Card('3', '♣'),
            Card('2', '♠'), Card('A', '♦'), Card('K', '♥'), Card('Q', '♦')
        ]
        
        # 分配牌给玩家和AI
        player.hand['temp'] = test_cards[:fantasy_cards]
        ai_player.hand['temp'] = test_cards[:fantasy_cards]  # AI也拿相同的牌作为测试
        
        # 显示玩家的手牌
        print("\n玩家a的手牌:")
        print(f"待摆放: {player.hand['temp']}")
        print("顶部区域: []")
        print("中部区域: []")
        print("底部区域: []")
        
        # 模拟玩家摆牌
        print("\n玩家a开始摆牌...")
        print("选择顶部区域的3张牌: 1 2 3")
        print("选择中部区域的5张牌: 4 5 6 7 8")
        print("选择底部区域的5张牌: 9 10 11 12 13")
        
        # 分配牌
        top_cards = player.hand['temp'][:3]
        middle_cards = player.hand['temp'][3:8]
        bottom_cards = player.hand['temp'][8:13]
        
        player.hand['top'] = top_cards
        player.hand['middle'] = middle_cards
        player.hand['bottom'] = bottom_cards
        player.hand['temp'] = []
        
        print("\n玩家a摆牌完成!")
        print(f"顶部区域: {player.hand['top']}")
        print(f"中部区域: {player.hand['middle']}")
        print(f"底部区域: {player.hand['bottom']}")
        
        # 模拟AI摆牌
        print("\nAI开始摆牌...")
        # AI摆牌策略：按点数排序，顶部放最弱的3张，中间放中等的5张，底部放最强的5张
        ai_cards = ai_player.hand['temp']
        ai_cards.sort(key=lambda x: x.value)
        
        ai_top = ai_cards[:3]
        ai_middle = ai_cards[3:8]
        ai_bottom = ai_cards[8:13]
        
        ai_player.hand['top'] = ai_top
        ai_player.hand['middle'] = ai_middle
        ai_player.hand['bottom'] = ai_bottom
        ai_player.hand['temp'] = []
        
        print("AI摆牌完成!")
        print(f"顶部区域: {ai_player.hand['top']}")
        print(f"中部区域: {ai_player.hand['middle']}")
        print(f"底部区域: {ai_player.hand['bottom']}")
        
        # 模拟判定胜负
        print("\n========================================")
        print("           范特西模式结束！")
        print("========================================")
        print("游戏结束，判定胜负...")
        
        # 显示最终结果
        print("\n最终手牌:")
        print(f"玩家a的顶部: {player.hand['top']}")
        print(f"玩家a的中部: {player.hand['middle']}")
        print(f"玩家a的底部: {player.hand['bottom']}")
        print(f"AI的顶部: {ai_player.hand['top']}")
        print(f"AI的中部: {ai_player.hand['middle']}")
        print(f"AI的底部: {ai_player.hand['bottom']}")
        
        print("\n========================================")
        print("        测试完成")
        print("========================================")
    else:
        print("✗ 未能进入Fantasy Land模式")

if __name__ == "__main__":
    test_fantasy_play()