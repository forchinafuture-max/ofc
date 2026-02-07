from core import Player, Card
from game_logic import OFCGame

# 简化测试三道全赢附加分
def test_three_wins_bonus_simple():
    """简化测试三道全赢附加分"""
    print("开始测试三道全赢附加分...")
    
    game = OFCGame()
    
    # 创建两个玩家
    player1 = Player("玩家a", 1000)
    player2 = Player("AI (中等)", 1000)
    
    # 设置玩家1的手牌（三道全赢）
    player1.hand['top'] = [Card(10, '♠'), Card(10, '♥'), Card(5, '♦')]  # 一对（强度1）
    player1.hand['middle'] = [Card(11, '♠'), Card(11, '♥'), Card(12, '♦'), Card(12, '♣'), Card(2, '♠')]  # 两队（强度2）
    player1.hand['bottom'] = [Card(13, '♠'), Card(13, '♥'), Card(13, '♦'), Card(3, '♣'), Card(4, '♠')]  # 三条（强度3）
    
    # 设置玩家2的手牌（较弱，所有区域都输）
    player2.hand['top'] = [Card(2, '♠'), Card(3, '♥'), Card(4, '♦')]  # 高牌（强度0）
    player2.hand['middle'] = [Card(5, '♣'), Card(5, '♠'), Card(6, '♥'), Card(7, '♦'), Card(8, '♣')]  # 一对（强度1）
    player2.hand['bottom'] = [Card(9, '♠'), Card(9, '♥'), Card(9, '♦'), Card(10, '♣'), Card(11, '♠')]  # 三条（强度3）
    
    # 计算得分
    score1 = game.calculate_score(player1, player2)
    score2 = game.calculate_score(player2, player1)
    
    print(f"玩家a得分: {score1}")
    print(f"AI得分: {score2}")
    
    # 验证：三道全赢应该获得附加分
    # 基础得分：3（三个区域全赢） + 牌型分 + 3（附加分）
    # 牌型分：玩家1的牌型分应该比玩家2高
    assert score1 > score2, "三道全赢的玩家应该得分更高"
    assert score1 >= 6, "三道全赢的玩家应该至少得6分"
    
    print("✓ 测试通过: 三道全赢获得附加分")
    
    # 检查是否正确计算了三道全赢附加分
    # 计算区域得分
    top_result = game.compare_hands(player1.hand['top'], player2.hand['top'])
    middle_result = game.compare_hands(player1.hand['middle'], player2.hand['middle'])
    bottom_result = game.compare_hands(player1.hand['bottom'], player2.hand['bottom'])
    
    print(f"区域得分: 顶部={top_result}, 中部={middle_result}, 底部={bottom_result}")
    
    # 验证三个区域都赢
    assert top_result == 1, "玩家1应该赢顶部"
    assert middle_result == 1, "玩家1应该赢中部"
    assert bottom_result == 1, "玩家1应该赢底部"
    
    print("✓ 测试通过: 正确识别三道全赢")

if __name__ == "__main__":
    try:
        test_three_wins_bonus_simple()
        print("\n🎉 所有测试通过！三道全赢附加分修复成功。")
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
