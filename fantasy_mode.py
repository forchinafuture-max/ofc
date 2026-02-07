from core import Player, Deck
from ui import GameUI

class FantasyModeManager:
    def __init__(self, game, ui, ai_strategy):
        self.game = game
        self.ui = ui
        self.ai_strategy = ai_strategy
    
    def handle_fantasy_mode(self):
        """处理范特西模式"""
        # 检查是否有玩家进入范特西模式
        fantasy_players = [player for player in self.game.players if player.fantasy_mode]
        if not fantasy_players:
            return False
        
        print("\n========================================")
        print("           进入范特西模式！")
        print("========================================")
        
        # 重新初始化牌堆，确保有足够的牌
        self.game.deck = Deck()
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
        
        # 保存游戏记录
        self.game.save_game_record()
        
        # 询问是否再玩一局
        if not self.ui.ask_play_again():
            return False
        return True
    
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
                player.hand['temp'].append(self.game.deck.deal(1)[0])
        
        # 显示手牌
        print(f"{player.name}的手牌:")
        print(f"待摆放: {player.hand['temp']}")
        print(f"顶部区域: {player.hand['top']}")
        print(f"中部区域: {player.hand['middle']}")
        print(f"底部区域: {player.hand['bottom']}")
        
        # 玩家摆牌
        # 检查玩家是否为AI玩家
        if hasattr(player, 'difficulty'):
            # AI玩家，使用自动摆牌逻辑
            print(f"\n{player.name}开始摆牌...")
            print(f"AI (中等)在FL阶段自动摆牌...")
            self.ui.ai_place_cards_fantasy(player, self.game, self.ai_strategy)
        else:
            # 人类玩家，使用手动摆牌逻辑
            print(f"\n{player.name}开始摆牌...")
            self.ui.place_cards_fantasy(player, self.game)
    
    def _handle_normal_player(self, player):
        """处理未进入范特西模式的玩家，按照普通游戏模式规则进行"""
        print(f"\n{player.name}按普通模式进行游戏:")
        print("========================================")
        
        # 清空所有手牌区域
        player.hand['temp'] = []
        player.hand['top'] = []
        player.hand['middle'] = []
        player.hand['bottom'] = []
        
        # 第1轮：发5张牌
        print("第1轮：发5张牌")
        player.hand['temp'] = []
        for _ in range(5):
            if self.game.deck.cards:
                player.hand['temp'].append(self.game.deck.deal(1)[0])
        print(f"待摆放: {player.hand['temp']}")
        
        # 摆牌
        print(f"{player.name}开始摆牌...")
        if hasattr(player, 'difficulty'):
            # AI玩家，使用自动摆牌逻辑
            print(f"AI (中等)在第1轮自动摆牌...")
            self.ui.ai_place_cards(player, self.game, self.ai_strategy)
        else:
            # 人类玩家，使用手动摆牌逻辑
            self.ui.place_cards(player, self.game)
        
        # 第2-5轮：各发3张牌
        for round_num in range(2, 6):
            print(f"\n第{round_num}轮：发3张牌")
            player.hand['temp'] = []
            for _ in range(3):
                if self.game.deck.cards:
                    player.hand['temp'].append(self.game.deck.deal(1)[0])
            print(f"待摆放: {player.hand['temp']}")
            
            # 摆牌（摆两张丢一张）
            print(f"{player.name}开始摆牌...")
            if hasattr(player, 'difficulty'):
                # AI玩家，使用自动摆牌逻辑（后续轮次）
                print(f"AI (中等)在第{round_num}轮自动摆牌...")
                self.ui.ai_place_cards_round(player, self.game, self.ai_strategy)
            else:
                # 人类玩家，使用手动摆牌逻辑（后续轮次）
                self.ui.place_cards_round(player, self.game)
        
        # 显示最终摆牌结果
        print(f"\n{player.name}完成摆牌:")
        print(f"顶部区域: {player.hand['top']}")
        print(f"中部区域: {player.hand['middle']}")
        print(f"底部区域: {player.hand['bottom']}")
    
    def _end_fantasy_mode(self):
        """结束范特西模式，进行结算"""
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
                    # 设置发牌数量为14张
                    player.fantasy_cards = 14
                else:
                    # 重置范特西模式
                    player.fantasy_mode = False
        
        # 结算画面停留，按回车继续
        print("\n========================================")
        print("按回车键进入下一局...")
        print("========================================")
        input()
