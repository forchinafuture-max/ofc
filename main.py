from game.player import Player
from game.ofc_game import OFCGame
from ai.ai_player import AIPlayer
from ui import GameUI
from fantasy_mode import FantasyModeManager

# 由于AIStrategy可能不存在，暂时注释掉
# from ai_strategy import AIStrategy

class OFCGameManager:
    def __init__(self):
        self.game = OFCGame()
        self.ui = GameUI()
        self.ai_strategy = None  # 暂时设为None
        self.fantasy_manager = FantasyModeManager(self.game, self.ui, self.ai_strategy)
        self.player = None
        self.ai_player = None
    
    def setup_game(self, skip_learning=False):
        # 设置游戏
        self.ui.clear_screen()
        self.ui.display_title()
        
        # 默认选择中等难度AI
        ai_difficulty = "medium"
        print(f"默认选择AI难度: 中等")
        
        # 清空游戏中的玩家列表
        self.game.players = []
        
        # 创建玩家
        self.player = Player("玩家a")
        self.ai_player = AIPlayer(f"AI (中等)", strategy_type="heuristic")
        
        # 重置累计积分
        self.player.total_score = 0
        self.ai_player.total_score = 0
        
        # 添加玩家到游戏
        self.game.add_player(self.player)
        self.game.add_player(self.ai_player)
    
    def handle_fantasy_mode(self):
        """处理范特西模式"""
        # 检查是否有玩家进入范特西模式
        fantasy_players = [player for player in self.game.players if player.fantasy_mode]
        if not fantasy_players:
            return False
        
        print("\n========================================")
        print("           进入范特西模式！")
        print("========================================")
        
        # 先处理进入范特西模式的玩家（一次性发牌和摆牌）
        for player in self.game.players:
            if player.fantasy_mode:
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
                        player.hand['temp'].append(self.game.deck.deal(1)[0])
                
                # 显示手牌
                print(f"{player.name}的手牌:")
                print(f"待摆放: {player.hand['temp']}")
                print(f"顶部区域: {player.hand['top']}")
                print(f"中部区域: {player.hand['middle']}")
                print(f"底部区域: {player.hand['bottom']}")
                
                # 玩家摆牌
                if isinstance(player, Player):
                    print(f"\n{player.name}开始摆牌...")
                    self.ui.place_cards_fantasy(player, self.game)
                else:
                    print(f"\n{player.name}开始摆牌...")
                    self.ui.ai_place_cards_fantasy(player, self.game, self.ai_strategy)
        
        # 处理未进入范特西模式的玩家（一次性发牌和摆牌）
        for player in self.game.players:
            if not player.fantasy_mode:
                print(f"\n========================================")
                print(f"{player.name}按普通模式进行游戏:")
                print("========================================")
                
                # 清空所有手牌区域
                player.hand['temp'] = []
                player.hand['top'] = []
                player.hand['middle'] = []
                player.hand['bottom'] = []
                
                # 一次性发足够的牌（模拟完整的普通模式）
                total_cards = 13  # 顶部3张 + 中部5张 + 底部5张
                print(f"一次性发{total_cards}张牌（模拟完整的普通模式）:")
                
                for _ in range(total_cards):
                    if self.game.deck.cards:
                        player.hand['temp'].append(self.game.deck.deal(1)[0])
                
                # 显示手牌
                print(f"{player.name}的手牌:")
                print(f"待摆放: {player.hand['temp']}")
                print(f"顶部区域: {player.hand['top']}")
                print(f"中部区域: {player.hand['middle']}")
                print(f"底部区域: {player.hand['bottom']}")
                
                # 一次性摆牌
                print(f"\n{player.name}开始摆牌...")
                if isinstance(player, Player):
                    # 使用范特西模式的摆牌逻辑，因为需要分配13张牌
                    self.ui.place_cards_fantasy(player, self.game)
                else:
                    # 使用范特西模式的AI摆牌逻辑
                    self.ui.ai_place_cards_fantasy(player, self.game, self.ai_strategy)
        
        # 游戏结束，判定胜负
        print("\n========================================")
        print("           范特西模式结束！")
        print("========================================")
        
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
                    print(f"\n========================================")
                    print(f"           {player.name}满足留在范特西模式条件！")
                    print("========================================")
                    print("底部拿到4条以上或顶部拿到222+以上，继续留在范特西模式！")
                    print("下一局将继续以范特西模式进行，一次性发14张牌。")
                    print("========================================")
                    # 保持范特西模式为True
                    player.fantasy_mode = True
                else:
                    # 重置范特西模式
                    player.fantasy_mode = False
        
        # 结算画面停留，按回车继续
        print("\n========================================")
        print("按回车键进入下一局...")
        print("========================================")
        input()
        
        # 询问是否再玩一局
        if not self.ui.ask_play_again():
            return False
        return True
    
    def play_round(self, round_num):
        # 一轮游戏
        self.ui.clear_screen()
        self.ui.display_title()
        self.ui.display_game_state(self.game)
        
        # 显示当前轮次和状态
        self.ui.display_round_info(self.game)
        
        # 显示玩家手牌
        self.ui.display_player_hand(self.player)
        
        # 显示AI手牌
        print(f"\n{self.ai_player.name}的手牌:")
        print("顶部区域:", self.ai_player.hand['top'])
        print("中部区域:", self.ai_player.hand['middle'])
        print("底部区域:", self.ai_player.hand['bottom'])
        
        # 发牌阶段
        print("\n========================================")
        print(f"              第 {round_num} 轮发牌              ")
        print("========================================")
        
        # 发牌
        print(f"当前轮次: {round_num}")
        if round_num >= 1 and round_num <= 5:
            self.ui.display_deal_info()
            print(f"准备发第 {round_num} 轮牌...")
            
            # 保存当前轮次
            self.game.current_round = round_num
            self.game.deal_round()
            print("发牌完成！")
            
            # 摆牌
            print(f"开始第 {round_num} 轮摆牌...")
            # 玩家选择牌
            if not self.player.folded and self.player.hand['temp']:
                print("玩家a开始选择牌...")
                self.ui.place_cards_round(self.player, self.game)
            
            # AI选择牌
            if not self.ai_player.folded and self.ai_player.hand['temp']:
                print("AI开始选择牌...")
                self.ui.ai_place_cards_round(self.ai_player, self.game, self.ai_strategy)
            
            input("按回车键继续...")
        else:
            print("本轮不需要发牌")
            input("按回车键继续...")
    
    def play_game(self):
        # 主游戏循环
        while True:
            # 开始新游戏
            self.game.start_game()
            
            # 检查范特西模式
            for player in self.game.players:
                self.game.check_fantasy_mode(player)
            
            # 检查是否有玩家进入范特西模式
            has_fantasy_players = any(player.fantasy_mode for player in self.game.players)
            
            if has_fantasy_players:
                # 处理范特西模式
                if not self.fantasy_manager.handle_fantasy_mode():
                    break
                continue
            
            # 第1轮：发5张牌并摆牌
            print("\n========================================")
            print("              第 1 轮              ")
            print("========================================")
            
            # 发第一轮牌
            print("\n发第一轮牌...")
            # 不需要再次发牌，因为start_game已经调用了deal_first_round方法
            # self.game.current_round = 1
            # self.game.deal_round()
            
            # 摆牌阶段
            print("\n摆牌阶段...")
            # 玩家摆牌
            if not self.player.folded and self.player.hand['temp']:
                self.ui.place_cards(self.player, self.game)
            
            # AI摆牌
            if not self.ai_player.folded and self.ai_player.hand['temp']:
                self.ui.ai_place_cards(self.ai_player, self.game, self.ai_strategy)
            
            # 游戏主循环 - 后续轮次
            print("\n开始后续轮次游戏...")
            
            # 第2轮
            print("\n=== 第 2 轮 ===")
            self.play_round(2)
            
            # 第3轮
            print("\n=== 第 3 轮 ===")
            self.play_round(3)
            
            # 第4轮
            print("\n=== 第 4 轮 ===")
            self.play_round(4)
            
            # 第5轮
            print("\n=== 第 5 轮 ===")
            self.play_round(5)
            
            print("\n五轮游戏结束，开始判定胜负")
            
            # 确定获胜者
            winner = self.game.determine_winner()
            # 显示获胜者和得分
            self.ui.display_winner(winner, self.game)
            
            # 保存游戏记录
            # 由于OFCGame类没有save_game_record方法，暂时注释掉
            # self.game.save_game_record()
            
            # AI从游戏中学习
            if hasattr(self.ai_player, 'learn_from_game'):
                self.ai_player.learn_from_game(self.game, self.player)
            
            # 保存玩家的完整手牌和顶部手牌，用于Fantasy Land模式检查
            for player in self.game.players:
                if len(player.hand['top']) >= 3 and len(player.hand['middle']) >= 5 and len(player.hand['bottom']) >= 5:
                    # 保存完整手牌，用于爆牌检查
                    player.last_hand = {
                        'top': player.hand['top'].copy(),
                        'middle': player.hand['middle'].copy(),
                        'bottom': player.hand['bottom'].copy()
                    }
                    # 保存顶部手牌，用于牌型检查
                    player.last_top_hand = player.hand['top']
            
            # 检查是否进入Fantasy Land模式
            for player in self.game.players:
                self.game.check_fantasy_mode(player)
            # 检查是否有玩家进入范特西模式
            has_fantasy_players = any(player.fantasy_mode for player in self.game.players)
            if has_fantasy_players:
                if not self.fantasy_manager.handle_fantasy_mode():
                    break
                continue
            
            # 询问是否再玩一局
            if not self.ui.ask_play_again():
                break
    
    def run(self, skip_learning=False):
        try:
            self.setup_game(skip_learning=skip_learning)
            self.play_game()
        except KeyboardInterrupt:
            print("\n游戏已终止")
        except Exception as e:
            print(f"\n游戏出错: {e}")

if __name__ == "__main__":
    game_manager = OFCGameManager()
    game_manager.run()
