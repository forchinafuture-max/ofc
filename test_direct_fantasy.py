from core import Player, Table, Card
from game_logic import OFCGame
from ai_strategy import AIPlayer

# 创建测试脚本，直接模拟游戏结束并进入Fantasy Land模式
def test_direct_fantasy():
    print("========================================")
    print("    直接进入Fantasy Land模式测试")
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
    print("\n=== 假设玩家a顶部拿了AA ===")
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
        # 模拟玩家和AI摆牌
        print("玩家和AI摆牌中...")
        
        # 模拟游戏结束
        print("\n========================================")
        print("           范特西模式结束！")
        print("========================================")
        print("游戏结束，判定胜负...")
        
        # 重置范特西模式
        game.table.fantasy_mode = False
    else:
        print("✗ 未能进入Fantasy Land模式")
    
    print("\n========================================")
    print("        测试完成")
    print("========================================")

if __name__ == "__main__":
    test_direct_fantasy()