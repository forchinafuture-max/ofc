from core import Player, Table, Card
from game_logic import OFCGame
from ai_strategy import AIPlayer

# 创建测试脚本，直接进入Fantasy Land模式测试
def test_fantasy_land():
    print("========================================")
    print("        Fantasy Land模式测试")
    print("========================================")
    
    # 创建测试玩家
    player = Player("测试玩家")
    ai_player = AIPlayer("测试AI", difficulty="medium")
    
    # 创建桌子和游戏
    table = Table()
    game = OFCGame()
    game.add_player(player)
    game.add_player(ai_player)
    
    # 测试1: QQ → 14张牌
    print("\n=== 测试1: 顶部QQ ===")
    player.last_top_hand = [Card('Q', '♠'), Card('Q', '♥'), Card('J', '♦')]
    game.check_fantasy_mode()
    if game.table.fantasy_mode:
        print("✓ 成功进入Fantasy Land模式")
        print(f"发牌数量: {getattr(game.table, 'fantasy_cards', 14)}")
    else:
        print("✗ 未能进入Fantasy Land模式")
    
    # 重置
    game.table.fantasy_mode = False
    
    # 测试2: KK → 15张牌
    print("\n=== 测试2: 顶部KK ===")
    player.last_top_hand = [Card('K', '♠'), Card('K', '♥'), Card('J', '♦')]
    game.check_fantasy_mode()
    if game.table.fantasy_mode:
        print("✓ 成功进入Fantasy Land模式")
        print(f"发牌数量: {getattr(game.table, 'fantasy_cards', 15)}")
    else:
        print("✗ 未能进入Fantasy Land模式")
    
    # 重置
    game.table.fantasy_mode = False
    
    # 测试3: AA → 16张牌
    print("\n=== 测试3: 顶部AA ===")
    player.last_top_hand = [Card('A', '♠'), Card('A', '♥'), Card('J', '♦')]
    game.check_fantasy_mode()
    if game.table.fantasy_mode:
        print("✓ 成功进入Fantasy Land模式")
        print(f"发牌数量: {getattr(game.table, 'fantasy_cards', 16)}")
    else:
        print("✗ 未能进入Fantasy Land模式")
    
    # 重置
    game.table.fantasy_mode = False
    
    # 测试4: 三条 → 17张牌
    print("\n=== 测试4: 顶部三条 ===")
    player.last_top_hand = [Card('2', '♠'), Card('2', '♥'), Card('2', '♦')]
    game.check_fantasy_mode()
    if game.table.fantasy_mode:
        print("✓ 成功进入Fantasy Land模式")
        print(f"发牌数量: {getattr(game.table, 'fantasy_cards', 17)}")
    else:
        print("✗ 未能进入Fantasy Land模式")
    
    print("\n========================================")
    print("        测试完成")
    print("========================================")

if __name__ == "__main__":
    test_fantasy_land()