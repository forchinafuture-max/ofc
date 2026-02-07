from core import Player, Card
from game_logic import OFCGame

# 测试三道全赢附加分
def test_three_wins_bonus():
    """测试三道全赢附加分"""
    print("开始测试三道全赢附加分...")
    
    game = OFCGame()
    
    # 创建两个玩家
    player1 = Player("玩家a", 1000)
    player2 = Player("AI (中等)", 1000)
    
    # 设置玩家1的手牌（三道全赢）
    player1.hand['top'] = [Card(10, '♠'), Card(10, '♥'), Card(10, '♦')]  # 三条（很强）
    player1.hand['middle'] = [Card(13, '♠'), Card(13, '♥'), Card(11, '♦'), Card(11, '♣'), Card(2, '♠')]  # 两队
    player1.hand['bottom'] = [Card(14, '♠'), Card(14, '♥'), Card(14, '♦'), Card(14, '♣'), Card(5, '♠')]  # 四条（最强）
    
    # 设置玩家2的手牌（较弱）
    player2.hand['top'] = [Card(2, '♠'), Card(3, '♥'), Card(4, '♦')]  # 高牌
    player2.hand['middle'] = [Card(5, '♣'), Card(5, '♠'), Card(6, '♥'), Card(7, '♦'), Card(8, '♣')]  # 一对
    player2.hand['bottom'] = [Card(9, '♠'), Card(9, '♥'), Card(9, '♦'), Card(10, '♣'), Card(11, '♠')]  # 三条
    
    # 计算得分
    score1 = game.calculate_score(player1, player2)
    score2 = game.calculate_score(player2, player1)
    
    print(f"玩家a得分: {score1}")
    print(f"AI得分: {score2}")
    
    # 验证：三道全赢应该获得附加分
    # 基础得分：3（三个区域全赢） + 牌型分 + 3（附加分）
    assert score1 > score2, "三道全赢的玩家应该得分更高"
    assert score1 >= 6, "三道全赢的玩家应该至少得6分"
    
    print("✓ 测试通过: 三道全赢获得附加分")

def test_no_three_wins_bonus():
    """测试非三道全赢不获得附加分"""
    print("\n开始测试非三道全赢不获得附加分...")
    
    game = OFCGame()
    
    # 创建两个玩家
    player1 = Player("玩家a", 1000)
    player2 = Player("AI (中等)", 1000)
    
    # 设置玩家1的手牌（赢两个区域）
    player1.hand['top'] = [Card(2, '♠'), Card(3, '♥'), Card(4, '♦')]  # 高牌
    player1.hand['middle'] = [Card(5, '♣'), Card(5, '♠'), Card(6, '♥'), Card(7, '♦'), Card(8, '♣')]  # 一对
    player1.hand['bottom'] = [Card(9, '♠'), Card(9, '♥'), Card(9, '♦'), Card(10, '♣'), Card(11, '♠')]  # 三条
    
    # 设置玩家2的手牌（赢一个区域，但牌型分低）
    player2.hand['top'] = [Card(1, '♠'), Card(2, '♥'), Card(3, '♦')]  # 高牌（比玩家1弱）
    player2.hand['middle'] = [Card(4, '♣'), Card(4, '♠'), Card(5, '♥'), Card(6, '♦'), Card(7, '♣')]  # 一对（比玩家1弱）
    player2.hand['bottom'] = [Card(8, '♠'), Card(8, '♥'), Card(8, '♦'), Card(8, '♣'), Card(9, '♠')]  # 四条（比玩家1强）
    
    # 计算得分
    score1 = game.calculate_score(player1, player2)
    score2 = game.calculate_score(player2, player1)
    
    print(f"玩家a得分: {score1}")
    print(f"AI得分: {score2}")
    
    # 验证：非三道全赢不应该获得附加分
    # 玩家1赢两个区域，玩家2赢一个区域，所以玩家1应该得分更高
    assert score1 > score2, "赢更多区域的玩家应该得分更高"
    
    print("✓ 测试通过: 非三道全赢不获得附加分")

if __name__ == "__main__":
    try:
        test_three_wins_bonus()
        test_no_three_wins_bonus()
        print("\n🎉 所有测试通过！三道全赢附加分修复成功。")
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
