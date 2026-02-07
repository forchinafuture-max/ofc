import os
import random

class GameUI:
    def __init__(self):
        pass
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_title(self):
        print("=======================================")
        print("             OFC 扑克游戏              ")
        print("=======================================")
    
    def display_game_state(self, game):
        print(f"\n游戏状态:")
        print("---------------------------------------")
        
        for player in game.players:
            status = "(行动中)" if game.players.index(player) == game.table.action_player else ""
            print(f"{player.name}: {status}")
        
        print("---------------------------------------")
    
    def display_player_hand(self, player):
        print(f"\n{player.name}的手牌:")
        print("待摆放:", player.hand['temp'] if 'temp' in player.hand else "无")
        print("顶部区域:", player.hand['top'])
        print("中部区域:", player.hand['middle'])
        print("底部区域:", player.hand['bottom'])
    
    def get_ai_difficulty(self):
        print("\n请选择AI难度:")
        print("1. 简单")
        print("2. 中等")
        print("3. 困难")
        
        while True:
            choice = input("请输入选择 (1-3): ")
            if choice in ['1', '2', '3']:
                break
            print("无效选择，请重新输入")
        
        difficulty_map = {'1': 'easy', '2': 'medium', '3': 'hard'}
        return difficulty_map[choice]
    
    def place_cards(self, player, game):
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
                card_choice = input("请选择要摆放的牌 (1-{})".format(len(temp_cards)) + ": ")
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
            
            # 显示当前已摆好的牌
            print("\n当前已摆好的牌:")
            print(f"顶部区域: {player.hand['top']}")
            print(f"中部区域: {player.hand['middle']}")
            print(f"底部区域: {player.hand['bottom']}")
            
            input("按回车键继续...")
        
        # 摆牌完成后清空临时区域
        player.hand['temp'] = []
        print("\n摆牌完成！")
        self.display_player_hand(player)
        input("按回车键继续...")
    
    def ai_place_cards(self, player, game, ai_strategy):
        # AI摆牌
        print(f"\n{player.name}正在摆牌...")
        
        # 检查是否是RLAIPlayer，如果是，则使用其强化学习策略
        if hasattr(player, 'place_cards_strategy'):
            player.place_cards_strategy(game)
        else:
            # 获取AI摆牌建议
            placement = ai_strategy.suggest_placement(game, player)
            
            # 执行摆牌
            player.hand['top'] = placement['top']
            player.hand['middle'] = placement['middle']
            player.hand['bottom'] = placement['bottom']
            player.hand['temp'] = []
            
            print(f"{player.name}摆牌完成！")
            self.display_player_hand(player)
        
        input("按回车键继续...")
    
    def place_cards_round(self, player, game):
        # 后续轮次的摆牌功能（从3张牌中选择2张）
        print(f"\n{player.name}开始选择牌:")
        print("请从3张牌中选择2张放入牌型:")
        print("注意：顶部区域最多3张，中部和底部区域必须5张")
        
        temp_cards = player.hand['temp'].copy()
        selected_cards = []
        
        # 选择2张牌
        while len(selected_cards) < 2 and temp_cards:
            self.clear_screen()
            self.display_title()
            self.display_player_hand(player)
            
            print("\n待选择的牌:")
            for i, card in enumerate(temp_cards):
                print(f"{i+1}. {card}")
            
            # 选择要使用的牌
            while True:
                card_choice = input(f"请选择要使用的牌 (1-{len(temp_cards)}): ")
                if card_choice.isdigit():
                    card_idx = int(card_choice) - 1
                    if 0 <= card_idx < len(temp_cards):
                        break
                print("无效选择，请重新输入")
            
            # 添加到选择列表
            selected_card = temp_cards.pop(card_idx)
            selected_cards.append(selected_card)
            print(f"已选择: {selected_card}")
        
        # 分配选择的牌到三个区域
        print("\n请将选择的牌分配到三个区域:")
        print("当前牌型状态:")
        print(f"顶部区域: {len(player.hand['top'])}张牌 (最多3张)")
        print(f"中部区域: {len(player.hand['middle'])}张牌 (需要5张)")
        print(f"底部区域: {len(player.hand['bottom'])}张牌 (需要5张)")
        
        for i, card in enumerate(selected_cards):
            while True:
                self.clear_screen()
                self.display_title()
                self.display_player_hand(player)
                print(f"\n正在分配第 {i+1} 张牌: {card}")
                print("当前牌型状态:")
                print(f"顶部区域: {len(player.hand['top'])}张牌 (最多3张)")
                print(f"中部区域: {len(player.hand['middle'])}张牌 (需要5张)")
                print(f"底部区域: {len(player.hand['bottom'])}张牌 (需要5张)")
                
                # 选择摆放区域
                area_choice = input("请选择摆放区域 (1-顶部, 2-中部, 3-底部): ")
                if area_choice in ['1', '2', '3']:
                    # 检查区域牌数限制
                    area_map = {'1': 'top', '2': 'middle', '3': 'bottom'}
                    area = area_map[area_choice]
                    
                    if area == 'top' and len(player.hand['top']) >= 3:
                        print("顶部区域最多只能有3张牌！")
                        input("按回车键继续...")
                        continue
                    elif area == 'middle' and len(player.hand['middle']) >= 5:
                        print("中部区域已经有5张牌了！")
                        input("按回车键继续...")
                        continue
                    elif area == 'bottom' and len(player.hand['bottom']) >= 5:
                        print("底部区域已经有5张牌了！")
                        input("按回车键继续...")
                        continue
                    break
                print("无效选择，请重新输入")
            
            # 确定区域
            area_map = {'1': 'top', '2': 'middle', '3': 'bottom'}
            area = area_map[area_choice]
            
            # 摆放牌
            player.hand[area].append(card)
            print(f"已将 {card} 放到 {area_map[area_choice]} 区域")
        
        # 摆牌完成后清空临时区域
        player.hand['temp'] = []
        print("\n选择完成！")
        self.display_player_hand(player)
        input("按回车键继续...")
    
    def ai_place_cards_round(self, player, game, ai_strategy):
        # AI后续轮次摆牌
        print(f"\n{player.name}正在选择牌...")
        
        # 显示拿到的牌
        temp_cards = player.hand['temp'].copy()
        print(f"\n拿到的牌:")
        for i, card in enumerate(temp_cards, 1):
            print(f"{i}. {card}")
        
        # 简化处理：选择两张最大的牌
        temp_cards.sort(key=lambda x: x.value, reverse=True)
        selected_cards = temp_cards[:2]
        discarded_cards = temp_cards[2:]  # 丢弃的牌
        
        # 分配到三个区域，遵守牌数限制
        print(f"当前牌型状态:")
        print(f"顶部区域: {len(player.hand['top'])}张牌 (最多3张)")
        print(f"中部区域: {len(player.hand['middle'])}张牌 (需要5张)")
        print(f"底部区域: {len(player.hand['bottom'])}张牌 (需要5张)")
        
        # 记录摆牌顺序
        placement_order = []
        
        for card in selected_cards:
            # 智能选择区域：优先填满需要5张的区域，然后再考虑顶部
            if len(player.hand['middle']) < 5:
                area = 'middle'
            elif len(player.hand['bottom']) < 5:
                area = 'bottom'
            elif len(player.hand['top']) < 3:
                area = 'top'
            else:
                # 所有区域都满了，随便选一个
                area = 'middle'
            
            player.hand[area].append(card)
            print(f"已将 {card} 放到 {area} 区域")
            placement_order.append((card, area))
        
        # 显示丢弃的牌
        print(f"\n丢弃的牌:")
        for card in discarded_cards:
            print(f"- {card}")
        
        player.hand['temp'] = []
        print(f"{player.name}选择完成！")
        print("\nAI的摆牌结果:")
        print(f"顶部区域: {[str(card) for card in player.hand.get('top', [])]}")
        print(f"中部区域: {[str(card) for card in player.hand.get('middle', [])]}")
        print(f"底部区域: {[str(card) for card in player.hand.get('bottom', [])]}")
        
        # 显示摆牌顺序
        print("\n摆牌顺序:")
        for i, (card, area) in enumerate(placement_order, 1):
            area_name = '顶部' if area == 'top' else '中部' if area == 'middle' else '底部'
            print(f"{i}. 将 {card} 放到 {area_name} 区域")
        
        # 询问用户是否要纠正错误
        print("\n是否要纠正AI的摆牌？ (y/n): ")
        user_input = input().strip().lower()
        if user_input == 'y':
            print("\n请输入正确的摆法:")
            print("格式: 牌索引 区域索引 (例如: 0 1 表示将第1张牌放到中部区域)")
            print("区域索引: 0=顶部, 1=中部, 2=底部")
            print("输入多张牌时用空格分隔，例如: 0 1 1 2 2 2")
            print("输入 'cancel' 取消纠正")
            
            # 获取用户输入
            correction_input = input("请输入正确的摆法: ").strip()
            if correction_input.lower() != 'cancel':
                print("错误纠正已记录，AI将在后续训练中学习正确的摆法")
                # 这里可以添加代码来处理错误纠正，例如存储正确的摆法
            else:
                print("取消纠正")
        
        # 询问是否要暂停查看
        print("\n是否要暂停查看？ (y/n): ")
        user_input = input().strip().lower()
        if user_input == 'y':
            print("游戏暂停，按回车键继续...")
            input()
        else:
            print("按回车键继续...")
            input()
    
    def display_round_info(self, game):
        print(f"\n第 {game.table.round} 轮")
        
        if game.table.fantasy_mode:
            print("[范特西模式] - 头道牌型为QQ或更大！")
    
    def display_busted_warning(self, game, player):
        if game.check_busted(player):
            print("[警告] 你的手牌爆牌了！")
    
    def display_deal_info(self):
        print("\n---------------------------------------")
        print("              发牌阶段              ")
        print("---------------------------------------")
    
    def display_winner(self, winner, game):
        # 显示获胜者和得分
        # 注意：不调用calculate_score，因为determine_winner已经调用过了
        # 避免累计积分被重复更新
        
        print(f"\n=======================================")
        print(f"            游戏结束!            ")
        print(f"=======================================")
        
        # 处理winner为None的情况
        if winner:
            print(f"获胜者: {winner.name}")
        else:
            print("没有获胜者")
        
        # 显示本局的得分
        print("\n详细得分:")
        if len(game.players) == 2:
            p1, p2 = game.players
            # 检查爆牌情况
            p1_busted = game.check_busted(p1)
            p2_busted = game.check_busted(p2)
            
            # 计算双方的牌型分
            p1_top_score = game.calculate_hand_score(p1.hand['top'], 'top')
            p1_middle_score = game.calculate_hand_score(p1.hand['middle'], 'middle')
            p1_bottom_score = game.calculate_hand_score(p1.hand['bottom'], 'bottom')
            p1_hand_score = p1_top_score + p1_middle_score + p1_bottom_score
            
            p2_top_score = game.calculate_hand_score(p2.hand['top'], 'top')
            p2_middle_score = game.calculate_hand_score(p2.hand['middle'], 'middle')
            p2_bottom_score = game.calculate_hand_score(p2.hand['bottom'], 'bottom')
            p2_hand_score = p2_top_score + p2_middle_score + p2_bottom_score
            
            # 计算本局得分
            if p1_busted and p2_busted:
                p1_round_score = 0
                p2_round_score = 0
            elif p1_busted:
                p1_round_score = 0
                p2_round_score = 6 + p2_hand_score  # 爆牌规则：获胜者得6分 + 牌型分
            elif p2_busted:
                p1_round_score = 6 + p1_hand_score  # 爆牌规则：获胜者得6分 + 牌型分
                p2_round_score = 0
            else:
                # 计算区域得分
                top_result = game.compare_hands(p1.hand['top'], p2.hand['top'])
                middle_result = game.compare_hands(p1.hand['middle'], p2.hand['middle'])
                bottom_result = game.compare_hands(p1.hand['bottom'], p2.hand['bottom'])
                area_score = top_result + middle_result + bottom_result
                
                # 计算得分
                score_difference = p1_hand_score - p2_hand_score
                if top_result == 1 and middle_result == 1 and bottom_result == 1:
                    # 三道全赢
                    p1_round_score = max(0, score_difference + 6)
                    p2_round_score = 0
                elif top_result == -1 and middle_result == -1 and bottom_result == -1:
                    # 三道全输
                    p1_round_score = 0
                    p2_round_score = max(0, -score_difference + 6)
                elif p1_hand_score > p2_hand_score:
                    # 玩家1赢
                    p1_round_score = max(0, score_difference + area_score)
                    p2_round_score = 0
                elif p2_hand_score > p1_hand_score:
                    # 玩家2赢
                    p1_round_score = 0
                    p2_round_score = max(0, -score_difference - area_score)
                else:
                    # 平局
                    p1_round_score = 0
                    p2_round_score = 0
            
            # 显示本局得分
            print(f"{p1.name}: {p1_round_score} 分")
            print(f"{p2.name}: {p2_round_score} 分")
            
            # 显示爆牌情况
            if p1_busted:
                print(f"[爆牌] {p1.name}的手牌不符合规则！")
            if p2_busted:
                print(f"[爆牌] {p2.name}的手牌不符合规则！")
        else:
            # 多玩家情况
            for player in game.players:
                # 检查爆牌情况
                busted = game.check_busted(player)
                # 计算本局得分
                if busted:
                    round_score = 0
                    print(f"{player.name}: {round_score} 分")
                    print(f"[爆牌] {player.name}的手牌不符合规则！")
                else:
                    # 计算牌型分
                    top_score = game.calculate_hand_score(player.hand['top'], 'top')
                    middle_score = game.calculate_hand_score(player.hand['middle'], 'middle')
                    bottom_score = game.calculate_hand_score(player.hand['bottom'], 'bottom')
                    hand_score = top_score + middle_score + bottom_score
                    print(f"{player.name}: {hand_score} 分")
        
        # 显示累计积分
        print("\n累计积分:")
        for player in game.players:
            print(f"{player.name}: {player.total_score} 分")
        
        # 显示最终手牌
        print(f"\n=======================================")
        for player in game.players:
            print(f"\n{player.name}的最终手牌:")
            print("顶部区域:", player.hand['top'])
            print("中部区域:", player.hand['middle'])
            print("底部区域:", player.hand['bottom'])
            
            # 检查是否爆牌
            if game.check_busted(player):
                print(f"[爆牌] {player.name}的手牌不符合规则！")
        
        print(f"=======================================")
    
    def place_cards_fantasy(self, player, game):
        # 玩家在Fantasy Land模式下摆牌
        print("\n=== 范特西模式摆牌 ===")
        print("请将牌分配到三个区域:")
        print("顶部区域：3张牌")
        print("中部区域：5张牌")
        print("底部区域：5张牌")
        
        # 显示待摆放的牌
        temp_cards = player.hand['temp'].copy()
        print("\n待摆放的牌:")
        for i, card in enumerate(temp_cards, 1):
            print(f"{i}. {card}")
        
        # 按照牌型排列显示
        print("\n=======================================")
        print("           牌型排列显示")
        print("=======================================")
        # 按牌型分组
        rank_groups = {}
        for card in temp_cards:
            if card.rank not in rank_groups:
                rank_groups[card.rank] = []
            rank_groups[card.rank].append(card)
        # 按牌型长度排序（四条 > 三条 > 对子 > 单牌）
        sorted_groups = sorted(rank_groups.items(), key=lambda x: len(x[1]), reverse=True)
        for rank, cards in sorted_groups:
            card_count = len(cards)
            if card_count == 4:
                print(f"四条: {cards}")
            elif card_count == 3:
                print(f"三条: {cards}")
            elif card_count == 2:
                print(f"对子: {cards}")
            else:
                print(f"单牌: {cards}")
        
        # 按照花色排列显示
        print("\n=======================================")
        print("           花色排列显示")
        print("=======================================")
        # 按花色分组
        suit_map = {'S': 'S', 'H': 'H', 'D': 'D', 'C': 'C'}
        suit_groups = {'S': [], 'H': [], 'D': [], 'C': []}
        for card in temp_cards:
            ascii_suit = suit_map.get(card.suit, '?')
            suit_groups[ascii_suit].append(card)
        # 按花色显示
        for suit, cards in suit_groups.items():
            if cards:
                # 按点数排序
                sorted_cards = sorted(cards, key=lambda x: x.value, reverse=True)
                print(f"{suit}: {sorted_cards}")
        
        # 一张一张地选择牌并分配到区域
        while temp_cards:
            print("\n当前牌型状态:")
            print(f"顶部区域: {len(player.hand['top'])}张牌 (最多3张)")
            print(f"中部区域: {len(player.hand['middle'])}张牌 (需要5张)")
            print(f"底部区域: {len(player.hand['bottom'])}张牌 (需要5张)")
            
            # 检查是否所有区域都已满
            if (len(player.hand['top']) >= 3 and 
                len(player.hand['middle']) >= 5 and 
                len(player.hand['bottom']) >= 5):
                print("\n=======================================")
                print("           所有区域都已满！")
                print("=======================================")
                print("摆牌完成，剩余牌将被丢弃。")
                print("=======================================")
                break
            
            # 选择要摆放的牌
            print("\n待选择的牌:")
            for i, card in enumerate(temp_cards):
                print(f"{i+1}. {card}")
            
            # 选择要使用的牌
            while True:
                card_choice = input(f"请选择要使用的牌 (1-{len(temp_cards)}): ")
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
            elif area == 'middle' and len(player.hand['middle']) >= 5:
                print("中部区域最多只能放5张牌！")
                input("按回车键继续...")
                continue
            elif area == 'bottom' and len(player.hand['bottom']) >= 5:
                print("底部区域最多只能放5张牌！")
                input("按回车键继续...")
                continue
            
            # 摆放牌
            selected_card = temp_cards.pop(card_idx)
            player.hand[area].append(selected_card)
            print(f"已将 {selected_card} 放到 {area_map[area_choice]} 区域")
            
            # 显示当前已摆好的牌
            print("\n当前已摆好的牌:")
            print(f"顶部区域: {player.hand['top']}")
            print(f"中部区域: {player.hand['middle']}")
            print(f"底部区域: {player.hand['bottom']}")
            
            input("按回车键继续...")
        
        # 摆牌完成后显示结果
        print("\n=======================================")
        print("           摆牌完成！")
        print("=======================================")
        print(f"顶部区域: {player.hand['top']}")
        print(f"中部区域: {player.hand['middle']}")
        print(f"底部区域: {player.hand['bottom']}")
        print("=======================================")
        
        # 清空临时区域，确保不会再次要求摆牌
        player.hand['temp'] = []
    
    def ai_place_cards_fantasy(self, ai_player, game, ai_strategy):
        # AI在Fantasy Land模式下摆牌
        if ai_player.hand['temp']:
            # 检查是否是RLAIPlayer，如果是，则使用其强化学习策略
            if hasattr(ai_player, 'place_cards_strategy'):
                print(f"{ai_player.name}正在使用强化学习策略摆牌...")
                ai_player.place_cards_strategy(game)
            else:
                # 简单的AI摆牌策略
                temp_cards = ai_player.hand['temp']
                
                # 按点数排序
                temp_cards.sort(key=lambda x: x.value, reverse=True)
                
                # 分配牌
                top_cards = temp_cards[:3]  # 顶部放最弱的3张
                middle_cards = temp_cards[3:8]  # 中间放中等强度的5张
                bottom_cards = temp_cards[8:13]  # 底部放最强的5张
                
                # 放置牌
                ai_player.hand['top'] = top_cards
                ai_player.hand['middle'] = middle_cards
                ai_player.hand['bottom'] = bottom_cards
                ai_player.hand['temp'] = []
                
                print(f"AI已完成摆牌")
                print(f"顶部区域: {ai_player.hand['top']}")
                print(f"中部区域: {ai_player.hand['middle']}")
                print(f"底部区域: {ai_player.hand['bottom']}")
    
    def ask_play_again(self):
        while True:
            choice = input("\n是否再玩一局? (y/n): ")
            if choice.lower() in ['y', 'n']:
                return choice.lower() == 'y'
            print("无效选择，请重新输入")