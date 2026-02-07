from core import Player, Card
from game_logic import OFCGame

# 测试爆牌玩家不能触发范特西模式
def test_busted_player_cannot_trigger_fantasy():
    """测试爆牌玩家不能触发范特西模式"""
    print("开始测试爆牌玩家不能触发范特西模式...")
    
    game = OFCGame()
    
    # 创建爆牌玩家
    busted_player = Player("爆牌玩家", 1000)
    
    # 设置爆牌手牌
    busted_player.hand['top'] = [Card(14, '♠'), Card(14, '♥'), Card(14, '♦')]  # AAA（很强）
    busted_player.hand['middle'] = [Card(2, '♣'), Card(3, '♠'), Card(4, '♥'), Card(5, '♦'), Card(7, '♣')]  # 高牌
    busted_player.hand['bottom'] = [Card(6, '♠'), Card(8, '♥'), Card(9, '♦'), Card(10, '♣'), Card(11, '♠')]  # 高牌
    
    # 保存顶部手牌（包含AA对子）
    busted_player.last_top_hand = busted_player.hand['top']
    
    # 检查是否爆牌
    is_busted = game.check_busted(busted_player)
    print(f"玩家是否爆牌: {is_busted}")
    assert is_busted, "玩家应该爆牌"
    
    game.players.append(busted_player)
    
    # 检查范特西模式
    game.check_fantasy_mode()
    
    print(f"范特西模式触发: {game.table.fantasy_mode}")
    print(f"范特西模式发牌数: {getattr(game.table, 'fantasy_cards', '未设置')}")
    
    # 验证：爆牌玩家不应该触发范特西模式
    assert not game.table.fantasy_mode, "爆牌玩家不应该触发范特西模式"
    print("✓ 测试通过: 爆牌玩家不能触发范特西模式")

def test_non_busted_player_can_trigger_fantasy():
    """测试非爆牌玩家可以触发范特西模式"""
    print("\n开始测试非爆牌玩家可以触发范特西模式...")
    
    game = OFCGame()
    
    # 创建非爆牌玩家
    non_busted_player = Player("非爆牌玩家", 1000)
    
    # 设置非爆牌手牌
    non_busted_player.hand['top'] = [Card(2, '♠'), Card(3, '♥'), Card(4, '♦')]  # 高牌（强度0）
    non_busted_player.hand['middle'] = [Card(5, '♣'), Card(5, '♠'), Card(6, '♥'), Card(7, '♦'), Card(8, '♣')]  # 一对（强度1）
    non_busted_player.hand['bottom'] = [Card(9, '♠'), Card(9, '♥'), Card(9, '♦'), Card(10, '♣'), Card(11, '♠')]  # 三条（强度3）
    
    # 保存顶部手牌（包含QQ对子）
    non_busted_player.last_top_hand = [Card(12, '♠'), Card(12, '♥'), Card(2, '♦')]  # QQ
    
    # 检查是否爆牌
    is_busted = game.check_busted(non_busted_player)
    print(f"玩家是否爆牌: {is_busted}")
    assert not is_busted, "玩家不应该爆牌"
    
    game.players.append(non_busted_player)
    
    # 检查范特西模式
    game.check_fantasy_mode()
    
    print(f"范特西模式触发: {game.table.fantasy_mode}")
    print(f"范特西模式发牌数: {getattr(game.table, 'fantasy_cards', '未设置')}")
    
    # 验证：非爆牌玩家可以触发范特西模式
    assert game.table.fantasy_mode, "非爆牌玩家应该能触发范特西模式"
    print("✓ 测试通过: 非爆牌玩家可以触发范特西模式")

if __name__ == "__main__":
    try:
        test_busted_player_cannot_trigger_fantasy()
        test_non_busted_player_can_trigger_fantasy()
        print("\n🎉 所有测试通过！")
        print("爆牌玩家不能触发范特西模式的修复成功。")
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
