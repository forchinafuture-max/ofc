from ofc_poker import OFCPoker, Player
from ai_strategy import AIPlayer, AIStrategy
import os

class GameInterface:
    def __init__(self):
        self.game = OFCPoker()
        self.ai_strategy = AIStrategy()
        self.player_name = "Player"
        self.ai_difficulty = "medium"
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_title(self):
        print("========================================")
        print("             OFC 扑克游戏              ")
        print("========================================")
    
    def display_game_state(self):
        print(f"\n锅底: {self.game.pot}")
        print(f"当前下注: {self.game.current_bet}")
        print("----------------------------------------")
        
        for player in self.game.players:
            status = "(行动中)" if self.game.players.index(player) == self.game.action_player else ""
            folded = "[已弃牌]" if player.folded else ""
            print(f"{player.name}: {player.chips} 筹码 {status} {folded}")
        
        print("----------------------------------------")
    
    def display_player_hand(self, player):
        print(f"\n{player.name}的手牌:")
        print("待摆放:", player.hand['temp'] if 'temp' in player.hand else "无")
        print("顶部区域:", player.hand['top'])
        print("中部区域:", player.hand['middle'])
        print("底部区域:", player.hand['bottom'])
    
    def get_player_action(self):
        print("\n请选择行动:")
        print("1. 跟注")
        print("2. 加注")
        print("3. 弃牌")
        
        while True:
            choice = input("请输入选择 (1-3): ")
            if choice in ['1', '2', '3']:
                break
            print("无效选择，请重新输入")
        
        if choice == '1':
            # 跟注
            amount = self.game.current_bet - self.game.players[0].bet
            return ('call', amount)
        elif choice == '2':
            # 加注
            while True:
                try:
                    amount = int(input(f"请输入加注金额 (至少 {self.game.current_bet * 2}): "))
                    if amount >= self.game.current_bet * 2 and amount <= self.game.players[0].chips:
                        break
                    print(f"无效金额，请输入至少 {self.game.current_bet * 2} 且不超过 {self.game.players[0].chips}")
                except ValueError:
                    print("请输入有效的数字")
            return ('raise', amount)
        else:
            # 弃牌
            return ('fold', 0)
    
    def place_cards(self, player):
        # 玩家摆牌功能
        print(f"\n{player.name}开始摆牌:")
        print("请将5张牌分别摆放到三个区域:")
        print("顶部区域(3张) ≤ 中部区域(5张) ≤ 底部区域(5张)")
        
        temp_cards = player.hand['temp'].copy()
        
        while temp_cards:
            self.clear_screen()
            self.display_title()
            self.display_player_hand(player)
            
            print("\n待摆放的牌:")
            for i, card in enumerate(temp_cards):
                print(f"{i+1}. {card}")
            
            # 选择要摆放的牌
            while True:
                card_choice = input("请选择要摆放的牌 (1-{}): ".format(len(temp_cards)))
                if card_choice.isdigit():
                    card_idx = int(card_choice) - 1
                    if 0 <= card_idx < len(temp_cards):
                        break
                print("无效选择，请重新输入")
            
            # 选择摆放区域
            while True:
                area_choice = input("请选择摆放区域 (1-顶部, 2-中部, 3-底部): ")
                if area_choice in ['1', '2', '3']:
                    break
                print("无效选择，请重新输入")
            
            # 确定区域
            area_map = {'1': 'top', '2': 'middle', '3': 'bottom'}
            area = area_map[area_choice]
            
            # 检查区域牌数限制
            if area == 'top' and len(player.hand['top']) >= 3:
                print("顶部区域最多只能放3张牌！")
                input("按回车键继续...")
                continue
            elif (area == 'middle' or area == 'bottom') and len(player.hand[area]) >= 5:
                print("中部和底部区域最多只能放5张牌！")
                input("按回车键继续...")
                continue
            
            # 摆放牌
            selected_card = temp_cards.pop(card_idx)
            player.hand[area].append(selected_card)
            print(f"已将 {selected_card} 放到 {area_map[area_choice]} 区域")
            input("按回车键继续...")
        
        # 摆牌完成后清空临时区域
        player.hand['temp'] = []
        print("\n摆牌完成！")
        self.display_player_hand(player)
        input("按回车键继续...")
    
    def ai_place_cards(self, player):
        # AI摆牌逻辑
        print(f"\n{player.name}正在摆牌...")
        temp_cards = player.hand['temp'].copy()
        
        # 简化的AI摆牌策略
        # 按牌力排序
        temp_cards.sort(key=lambda x: x.value, reverse=True)
        
        # 顶部区域放3张最弱的牌
        player.hand['top'] = temp_cards[:3]
        # 中部区域放中间强度的牌
        player.hand['middle'] = temp_cards[3:8] if len(temp_cards) >= 8 else temp_cards[3:]
        # 底部区域放最强的牌
        player.hand['bottom'] = temp_cards[8:] if len(temp_cards) >= 8 else []
        
        # 确保每个区域都有足够的牌
        while len(player.hand['top']) < 3 and temp_cards:
            player.hand['top'].append(temp_cards.pop())
        while len(player.hand['middle']) < 5 and temp_cards:
            player.hand['middle'].append(temp_cards.pop())
        while len(player.hand['bottom']) < 5 and temp_cards:
            player.hand['bottom'].append(temp_cards.pop())
        
        # 摆牌完成后清空临时区域
        player.hand['temp'] = []
        print(f"{player.name}摆牌完成！")
        self.display_player_hand(player)
        input("按回车键继续...")
    
    def process_action(self, player, action, amount):
        if action == 'call':
            if player.place_bet(amount):
                self.game.pot += amount
                print(f"{player.name} 跟注 {amount}")
        elif action == 'raise':
            if player.place_bet(amount):
                self.game.pot += amount
                self.game.current_bet = amount
                print(f"{player.name} 加注 {amount}")
        elif action == 'fold':
            player.folded = True
            print(f"{player.name} 弃牌")
    
    def play_round(self):
        self.clear_screen()
        self.display_title()
        self.display_game_state()
        
        # 显示当前轮次
        print(f"\n第 {self.game.round} 轮")
        
        # 显示范特西模式状态
        if self.game.fantasy_mode:
            print("[范特西模式] - 头道牌型为QQ或更大！")
        
        # 显示玩家手牌
        self.display_player_hand(self.game.players[0])
        
        # 检查是否爆牌
        if self.game.check_busted(self.game.players[0]):
            print("[警告] 你的手牌爆牌了！")
        
        # 下注阶段
        print("\n========================================")
        print("              下注阶段              ")
        print("========================================")
        
        # 处理玩家行动
        if not self.game.players[0].folded:
            action, amount = self.get_player_action()
            self.process_action(self.game.players[0], action, amount)
        
        # 处理AI行动
        for i, player in enumerate(self.game.players[1:]):
            if not player.folded:
                self.clear_screen()
                self.display_title()
                self.display_game_state()
                print(f"\n{player.name} 正在思考...")
                
                # AI决策
                action, amount = self.ai_strategy.suggest_action(self.game, player)
                self.process_action(player, action, amount)
                
                input("按回车键继续...")
        
        # 发牌（第二至第五轮）
        if self.game.round >= 2 and self.game.round <= 5:
            print("\n----------------------------------------")
            print("              发牌阶段              ")
            print("----------------------------------------")
            self.game.deal_round()
            print("发牌完成！")
            input("按回车键继续...")
    
    def determine_winner(self):
        winner = self.game.determine_winner()
        
        # 计算得分
        scores = {}
        if len(self.game.players) == 2:
            p1, p2 = self.game.players
            score1 = self.game.calculate_score(p1, p2)
            score2 = self.game.calculate_score(p2, p1)
            scores[p1.name] = score1
            scores[p2.name] = score2
        
        winner.chips += self.game.pot
        print(f"\n========================================")
        print(f"            游戏结束!            ")
        print(f"========================================")
        print(f"获胜者: {winner.name}")
        print(f"赢得锅底: {self.game.pot} 筹码")
        
        # 显示得分
        if scores:
            print("\n详细得分:")
            for name, score in scores.items():
                print(f"{name}: {score} 分")
        
        print(f"========================================")
        
        # 显示最终手牌
        for player in self.game.players:
            if not player.folded:
                print(f"\n{player.name}的最终手牌:")
                print("顶部区域:", player.hand['top'])
                print("中部区域:", player.hand['middle'])
                print("底部区域:", player.hand['bottom'])
                
                # 检查是否爆牌
                if self.game.check_busted(player):
                    print(f"[爆牌] {player.name}的手牌不符合规则！")
    
    def play_game(self):
        # 初始化游戏
        self.clear_screen()
        self.display_title()
        
        # 获取玩家名称
        self.player_name = input("请输入你的名字: ")
        
        # 获取AI难度
        print("\n请选择AI难度:")
        print("1. 简单")
        print("2. 中等")
        print("3. 困难")
        
        while True:
            difficulty_choice = input("请输入选择 (1-3): ")
            if difficulty_choice in ['1', '2', '3']:
                break
            print("无效选择，请重新输入")
        
        if difficulty_choice == '1':
            self.ai_difficulty = 'easy'
        elif difficulty_choice == '2':
            self.ai_difficulty = 'medium'
        else:
            self.ai_difficulty = 'hard'
        
        # 创建玩家
        human_player = Player(self.player_name, 1000)
        ai_player = AIPlayer(f"AI ({self.ai_difficulty})")
        
        self.game.add_player(human_player)
        self.game.add_player(ai_player)
        
        while True:
            # 开始新游戏
            self.game.start_game()
            
            # 摆牌阶段
            print("\n========================================")
            print("              摆牌阶段              ")
            print("========================================")
            
            # 玩家摆牌
            self.place_cards(self.game.players[0])
            
            # AI摆牌
            self.ai_place_cards(self.game.players[1])
            
            # 第一轮下注
            self.game.round = 1
            self.game.action_player = 0
            
            # 初始下注
            small_blind = 10
            big_blind = 20
            
            self.game.players[0].place_bet(small_blind)
            self.game.players[1].place_bet(big_blind)
            self.game.pot = small_blind + big_blind
            self.game.current_bet = big_blind
            
            # 游戏主循环
            for _ in range(4):  # 四轮下注
                self.play_round()
                
                # 检查是否只有一个玩家未弃牌
                active_players = [p for p in self.game.players if not p.folded]
                if len(active_players) == 1:
                    break
            
            # 确定获胜者
            self.determine_winner()
            
            # 询问是否继续游戏
            play_again = input("\n是否再玩一局? (y/n): ")
            if play_again.lower() != 'y':
                break
    
    def run(self):
        try:
            self.play_game()
        except KeyboardInterrupt:
            print("\n游戏已终止")
        except Exception as e:
            print(f"\n游戏出错: {e}")

if __name__ == "__main__":
    interface = GameInterface()
    interface.run()
