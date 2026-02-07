from core import Player, Deck
from game_logic import OFCGame
from main import OFCGameManager

# 测试游戏初始化和启动
def test_game_initialization():
    """测试游戏是否能正常初始化和启动"""
    print("开始测试游戏初始化...")
    
    try:
        # 创建游戏管理器
        game_manager = OFCGameManager()
        print("✓ 游戏管理器创建成功")
        
        # 设置游戏
        game_manager.setup_game()
        print("✓ 游戏设置成功")
        
        # 检查玩家
        print(f"✓ 玩家数量: {len(game_manager.game.players)}")
        for player in game_manager.game.players:
            print(f"  - {player.name}")
        
        # 测试游戏逻辑
        game = OFCGame()
        print("✓ 游戏逻辑创建成功")
        
        # 测试发牌
        deck = Deck()
        print(f"✓ 牌组初始化成功，共{len(deck.cards)}张牌")
        
        # 测试范特西模式检查
        print("✓ 测试范特西模式检查...")
        game.check_fantasy_mode()
        print(f"  范特西模式: {game.table.fantasy_mode}")
        
        print("\n🎉 游戏初始化测试通过！")
        print("游戏已经准备就绪，可以开始玩了。")
        print("\n启动游戏命令:")
        print("python main.py")
        
    except Exception as e:
        print(f"✗ 游戏初始化失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_game_initialization()
