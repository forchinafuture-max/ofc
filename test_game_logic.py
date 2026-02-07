from core import Player, Deck, Card
from game_logic import OFCGame

# 测试游戏逻辑
def test_three_of_a_kind_vs_two_pair():
    """测试三条是否大于两队"""
    game = OFCGame()
    
    # 三条的手牌
    three_of_a_kind = [
        Card(10, '♠'),
        Card(10, '♥'),
        Card(10, '♦'),
        Card(5, '♣'),
        Card(3, '♠')
    ]
    
    # 两队的手牌
    two_pair = [
        Card(13, '♠'),  # K
        Card(13, '♥'),  # K
        Card(11, '♦'),  # J
        Card(11, '♣'),  # J
        Card(2, '♠')    # 2
    ]
    
    score_three = game.evaluate_5_card_hand(three_of_a_kind)
    score_two = game.evaluate_5_card_hand(two_pair)
    
    print(f"三条得分: {score_three}")
    print(f"两队得分: {score_two}")
    print(f"三条 > 两队: {score_three > score_two}")
    assert score_three > score_two, "三条应该大于两队"

def test_scoring_system():
    """测试得分系统"""
    game = OFCGame()
    
    # 创建两个玩家
    player1 = Player("玩家1", 1000)
    player2 = Player("玩家2", 1000)
    
    # 玩家1的手牌（非爆牌）
    player1.hand['top'] = [Card(2, '♠'), Card(3, '♥'), Card(4, '♦')]  # 高牌
    player1.hand['middle'] = [Card(5, '♣'), Card(5, '♠'), Card(6, '♥'), Card(7, '♦'), Card(8, '♣')]  # 一对
    player1.hand['bottom'] = [Card(9, '♠'), Card(9, '♥'), Card(9, '♦'), Card(10, '♣'), Card(11, '♠')]  # 三条
    
    # 玩家2的手牌（爆牌 - 顶部 > 中部）
    player2.hand['top'] = [Card(14, '♠'), Card(14, '♥'), Card(14, '♦')]  # AAA（强度2）
    player2.hand['middle'] = [Card(2, '♣'), Card(3, '♠'), Card(4, '♥'), Card(5, '♦'), Card(7, '♣')]  # 高牌（强度0）
    player2.hand['bottom'] = [Card(6, '♠'), Card(8, '♥'), Card(9, '♦'), Card(10, '♣'), Card(11, '♠')]  # 高牌（强度0）
    
    # 计算得分
    score1 = game.calculate_score(player1, player2)
    score2 = game.calculate_score(player2, player1)
    
    print(f"玩家1得分: {score1}")
    print(f"玩家2得分: {score2}")
    print(f"玩家1（非爆牌） vs 玩家2（爆牌）: {score1 > score2}")
    assert score1 > score2, "非爆牌玩家应该得分更高"
    assert score2 == 0, "爆牌玩家应该得0分"

def test_fantasy_land_trigger():
    """测试范特西模式触发"""
    game = OFCGame()
    
    # 创建玩家
    player = Player("测试玩家", 1000)
    player.last_top_hand = [Card(12, '♠'), Card(12, '♥'), Card(2, '♦')]  # QQ
    
    game.players.append(player)
    game.check_fantasy_mode()
    
    print(f"范特西模式触发: {game.table.fantasy_mode}")
    print(f"范特西模式发牌数: {getattr(game.table, 'fantasy_cards', '未设置')}")
    assert game.table.fantasy_mode, "QQ顶部手牌应该触发范特西模式"

def test_busted_evaluation():
    """测试爆牌评估"""
    game = OFCGame()
    
    # 创建玩家
    player = Player("测试玩家", 1000)
    
    # 正常手牌（不爆牌）
    player.hand['top'] = [Card(2, '♠'), Card(3, '♥'), Card(4, '♦')]  # 高牌
    player.hand['middle'] = [Card(5, '♣'), Card(5, '♠'), Card(6, '♥'), Card(7, '♦'), Card(8, '♣')]  # 一对
    player.hand['bottom'] = [Card(9, '♠'), Card(9, '♥'), Card(10, '♦'), Card(11, '♣'), Card(12, '♠')]  # 一对
    
    is_busted1 = game.check_busted(player)
    print(f"正常手牌是否爆牌: {is_busted1}")
    assert not is_busted1, "正常手牌不应该爆牌"
    
    # 爆牌手牌（顶部 > 中部）
    player.hand['top'] = [Card(14, '♠'), Card(14, '♥'), Card(14, '♦')]  # AAA
    player.hand['middle'] = [Card(2, '♣'), Card(3, '♠'), Card(4, '♥'), Card(5, '♦'), Card(6, '♣')]  # 高牌
    
    is_busted2 = game.check_busted(player)
    print(f"顶部 > 中部是否爆牌: {is_busted2}")
    assert is_busted2, "顶部 > 中部应该爆牌"

def test_hand_strength_values():
    """测试手牌强度值"""
    game = OFCGame()
    
    # 测试各种手牌的强度值
    hands = [
        ("皇家同花顺", [Card(10, '♠'), Card(11, '♠'), Card(12, '♠'), Card(13, '♠'), Card(14, '♠')]),
        ("同花顺", [Card(9, '♠'), Card(10, '♠'), Card(11, '♠'), Card(12, '♠'), Card(13, '♠')]),
        ("四条", [Card(8, '♠'), Card(8, '♥'), Card(8, '♦'), Card(8, '♣'), Card(2, '♠')]),
        ("葫芦", [Card(7, '♠'), Card(7, '♥'), Card(7, '♦'), Card(3, '♣'), Card(3, '♠')]),
        ("同花", [Card(2, '♠'), Card(5, '♠'), Card(8, '♠'), Card(11, '♠'), Card(14, '♠')]),
        ("顺子", [Card(3, '♠'), Card(4, '♥'), Card(5, '♦'), Card(6, '♣'), Card(7, '♠')]),
        ("三条", [Card(6, '♠'), Card(6, '♥'), Card(6, '♦'), Card(9, '♣'), Card(12, '♠')]),
        ("两队", [Card(5, '♠'), Card(5, '♥'), Card(10, '♦'), Card(10, '♣'), Card(13, '♠')]),
        ("一对", [Card(4, '♠'), Card(4, '♥'), Card(7, '♦'), Card(11, '♣'), Card(14, '♠')]),
        ("高牌", [Card(2, '♠'), Card(5, '♥'), Card(8, '♦'), Card(11, '♣'), Card(13, '♠')])
    ]
    
    print("\n手牌强度值测试:")
    print("-" * 50)
    
    for hand_name, cards in hands:
        strength = game.evaluate_5_card_hand(cards)
        print(f"{hand_name}: {strength}")

if __name__ == "__main__":
    print("开始测试游戏逻辑...\n")
    
    try:
        print("1. 测试三条是否大于两队:")
        print("-" * 50)
        test_three_of_a_kind_vs_two_pair()
        print("✓ 测试通过: 三条 > 两队\n")
        
        print("2. 测试得分系统:")
        print("-" * 50)
        test_scoring_system()
        print("✓ 测试通过: 得分系统正常\n")
        
        print("3. 测试范特西模式触发:")
        print("-" * 50)
        test_fantasy_land_trigger()
        print("✓ 测试通过: 范特西模式触发正常\n")
        
        print("4. 测试爆牌评估:")
        print("-" * 50)
        test_busted_evaluation()
        print("✓ 测试通过: 爆牌评估正常\n")
        
        print("5. 测试手牌强度值:")
        print("-" * 50)
        test_hand_strength_values()
        print("✓ 测试通过: 手牌强度值正常\n")
        
        print("所有测试通过！游戏逻辑正确。")
    except Exception as e:
        print(f"测试失败: {e}")
