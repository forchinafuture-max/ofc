"""
调试脚本：从范特西模式（FL）阶段开始游戏
"""

from game.ofc_game import OFCGame
from game.player import Player
from ai.ai_player import AIPlayer
from ui import GameUI
from fantasy_mode import FantasyModeManager

class DebugFLGameManager:
    def __init__(self):
        self.game = OFCGame()
        self.ui = GameUI()
        self.ai_strategy = None  # 暂时设为None
        self.fantasy_manager = FantasyModeManager(self.game, self.ui, self.ai_strategy)
        self.player = None
        self.ai_player = None
    
    def setup_fl_game(self):
        """设置范特西模式游戏"""
        self.ui.clear_screen()
        self.ui.display_title()
        
        print("=== 从范特西模式（FL）阶段开始游戏 ===")
        print("====================================")
        
        # 清空游戏中的玩家列表
        self.game.players = []
        
        # 创建玩家
        self.player = Player("玩家a")
        self.ai_player = AIPlayer(f"AI (中等)", strategy_type="heuristic")
        
        # 设置玩家进入范特西模式
        self.player.fantasy_mode = True
        self.player.fantasy_cards = 17  # 范特西模式下一次性发17张牌
        
        # 重置累计积分
        self.player.total_score = 0
        self.ai_player.total_score = 0
        
        # 添加玩家到游戏
        self.game.add_player(self.player)
        self.game.add_player(self.ai_player)
        
        print(f"已设置 {self.player.name} 进入范特西模式")
        print(f"一次性发{self.player.fantasy_cards}张牌")
        print("====================================")
    
    def start_fl_game(self):
        """开始范特西模式游戏"""
        # 开始游戏
        self.game.start_game()
        
        print("\n=== 范特西模式游戏开始 ===")
        print("====================================")
        
        # 显示玩家手牌
        self.ui.display_player_hand(self.player)
        
        # 处理范特西模式
        self.handle_fantasy_mode()
    
    def handle_fantasy_mode(self):
        """处理范特西模式"""
        print("\n====================================")
        print("           进入范特西模式！")
        print("====================================")
        
        # 重新初始化牌堆，确保有足够的牌
        self.game.deck.reset()
        print("重新洗牌，确保有足够的牌进行范特西模式游戏")
        
        # 先处理进入范特西模式的玩家（一次性发牌和摆牌）
        for player in self.game.players:
            if player.fantasy_mode:
                self._handle_fantasy_player(player)
        
        # 处理未进入范特西模式的玩家（一次性发牌和摆牌）
        for player in self.game.players:
            if not player.fantasy_mode:
                self._handle_normal_player(player)
        
        # 游戏结束，判定胜负
        self._end_fantasy_mode()
    
    def _handle_fantasy_player(self, player):
        """处理进入范特西模式的玩家"""
        print(f"\n{player.name}进入范特西模式:")
        # 确定发牌数量
        fantasy_cards = getattr(player, 'fantasy_cards', 14)
        print(f"一次性发{fantasy_cards}张牌")
        
        # 清空所有手牌区域
        player.hand['temp'] = []
        player.hand['top'] = []
        player.hand['middle'] = []
        player.hand['bottom'] = []
        
        # 发Fantasy Land模式的牌
        for _ in range(fantasy_cards):
            if self.game.deck.cards:
                player.add_card(self.game.deck.deal(1)[0], 'temp')
        
        # 显示手牌
        print(f"{player.name}的手牌:")
        print(f"待摆放: {player.hand['temp']}")
        print(f"顶部区域: {player.hand['top']}")
        print(f"中部区域: {player.hand['middle']}")
        print(f"底部区域: {player.hand['bottom']}")
        
        # 玩家摆牌
        self.ui.place_cards_fantasy(player, self.game)
    
    def _handle_normal_player(self, player):
        """处理未进入范特西模式的玩家"""
        print(f"\n{player.name}按普通模式进行游戏:")
        print("====================================")
        
        # 清空所有手牌区域
        player.hand['temp'] = []
        player.hand['top'] = []
        player.hand['middle'] = []
        player.hand['bottom'] = []
        
        # 第1轮：发5张牌
        print("第1轮：发5张牌")
        for _ in range(5):
            if self.game.deck.cards:
                player.add_card(self.game.deck.deal(1)[0], 'temp')
        print(f"待摆放: {player.hand['temp']}")
        
        # 摆牌
        print(f"{player.name}开始摆牌...")
        self.ui.ai_place_cards(player, self.game, self.ai_strategy)
        
        # 第2-5轮：各发3张牌
        for round_num in range(2, 6):
            print(f"\n第{round_num}轮：发3张牌")
            player.hand['temp'] = []
            for _ in range(3):
                if self.game.deck.cards:
                    player.add_card(self.game.deck.deal(1)[0], 'temp')
            print(f"待摆放: {player.hand['temp']}")
            
            # 摆牌（摆两张丢一张）
            print(f"{player.name}开始摆牌...")
            self.ui.ai_place_cards_round(player, self.game, self.ai_strategy)
        
        # 显示最终摆牌结果
        print(f"\n{player.name}完成摆牌:")
        print(f"顶部区域: {player.hand['top']}")
        print(f"中部区域: {player.hand['middle']}")
        print(f"底部区域: {player.hand['bottom']}")
    
    def _end_fantasy_mode(self):
        """结束范特西模式，进行结算"""
        print("\n====================================")
        print("           范特西模式结束！")
        print("====================================")
        
        # 确定获胜者
        winner = self.game.determine_winner()
        self.ui.display_winner(winner, self.game)
        
        # 保存玩家的顶部手牌
        for player in self.game.players:
            if len(player.hand['top']) >= 3:
                player.last_top_hand = player.hand['top']
        
        # 检查是否满足留在范特西模式的条件
        for player in self.game.players:
            if player.fantasy_mode:
                if self.game.check_fantasy_stay_condition(player):
                    print(f"\n====================================")
                    print(f"           {player.name}满足留在范特西模式条件！")
                    print("====================================")
                    print("底部拿到4条以上或顶部拿到222+以上，继续留在范特西模式！")
                    print("下一局将继续以范特西模式进行，一次性发14张牌。")
                    print("====================================")
                    # 保持范特西模式为True
                    player.fantasy_mode = True
                    # 设置发牌数量为14张
                    player.fantasy_cards = 14
                else:
                    # 重置范特西模式
                    player.fantasy_mode = False
        
        # 结算画面停留，按回车继续
        print("\n====================================")
        print("按回车键结束游戏...")
        print("====================================")
        input()

def main():
    """主函数"""
    game_manager = DebugFLGameManager()
    game_manager.setup_fl_game()
    
    # 循环进行游戏，直到玩家不满足留在范特西模式的条件
    while game_manager.player.fantasy_mode:
        game_manager.start_fl_game()
        
        # 检查是否满足留在范特西模式的条件
        if game_manager.player.fantasy_mode:
            print("\n====================================")
            print("玩家满足留在范特西模式的条件")
            print("下一局将继续以范特西模式进行")
            print("====================================")
            input("按回车键开始下一局...")
            # 重置游戏状态，但保持玩家的fantasy_mode状态
            game_manager.game.players = []
            game_manager.game.add_player(game_manager.player)
            game_manager.game.add_player(game_manager.ai_player)
        else:
            print("\n====================================")
            print("玩家不满足留在范特西模式的条件")
            print("范特西模式结束")
            print("====================================")

if __name__ == "__main__":
    main()
