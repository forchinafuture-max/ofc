print("Hello, World!")
print("Testing terminal output...")

# 测试游戏的基本功能
print("Testing game setup...")

# 导入必要的模块
try:
    from core import Player
    from game_logic import OFCGame
    from ai_strategy import AIPlayer, AIStrategy, RLAIPlayer
    from ui import GameUI
    from fantasy_mode import FantasyModeManager
    from main import OFCGameManager
    print("✅ All modules imported successfully")
except Exception as e:
    print(f"❌ Import failed: {e}")

print("Test completed!")