from ai_strategy import AIPlayer
from ai.learning import RLAgent
from ai.test_module import ErrorCorrectionModule
from mcts import MCTS

class RLAIPlayer(AIPlayer):
    def __init__(self, name, chips=1000, difficulty='medium', skip_learning=False):
        super().__init__(name, chips, difficulty)
        # 初始化强化学习代理
        self.rl_agent = RLAgent(name)
        # 初始化错误纠正模块
        self.error_module = ErrorCorrectionModule(self.rl_agent)
        # 传递RLAIPlayer实例给错误纠正模块
        self.error_module.agent = self
        # 开始监听用户输入
        self.error_module.start_listening()
        # 记录上一个状态
        self.last_state = None
        
        # 初始化MCTS对象
        self.mcts = MCTS(iterations=500)  # 设置迭代次数为500，可根据需要调整
        
        # 统计数据
        self.stats = {
            'total_games': 0,  # 总游戏次数
            'high_pairs_attempt_fl': 0,  # 拿到AA/KK/QQ时尝试进FL的次数
            'high_pairs_count': 0,  # 拿到AA/KK/QQ的总次数
            'fl_attempts': 0,  # 尝试进FL的总次数
            'fl_successes': 0,  # 成功进FL的次数
            'busted_count': 0,  # 爆牌次数
            'ai_scores': [],  # AI的得分历史
            'expert_scores': [],  # 专家的得分历史
            'game_history': []  # 游戏历史记录
        }
        
        # 从JSON游戏记录中学习
        if not skip_learning:
            print("正在从JSON游戏记录中学习...")
            self.learn_from_json_records()
    
    def place_cards_strategy(self, game, auto_mode=False):
        """
        使用强化学习和MCTS进行摆牌决策
        """
        # 获取当前手牌（本轮新发的牌）
        temp_cards = self.hand['temp'].copy()
        
        # 统计当前各区域的牌数
        current_top = len(self.hand['top'])
        current_middle = len(self.hand['middle'])
        current_bottom = len(self.hand['bottom'])
        
        print(f"当前各区域牌数: 顶部 {current_top}张, 中部 {current_middle}张, 底部 {current_bottom}张")
        print(f"本轮需要摆放的牌: {temp_cards}")
        
        # 判断是否是第一轮摆牌
        total_cards_played = len(self.hand['top']) + len(self.hand['middle']) + len(self.hand['bottom'])
        is_first_round = total_cards_played == 0
        
        if is_first_round:
            print("\n=== 第一轮摆牌策略 ===")
            print("第一轮摆牌非常重要！")
            print("使用强化学习进行第一轮摆牌决策...")
        else:
            print("\n=== 非第一轮摆牌策略 ===")
            print("从第二轮开始使用MCTS进行深度搜索...")
        
        # 记录摆牌顺序
        placement_order = []
        
        # 处理第2-5轮的丢牌逻辑
        if not is_first_round and len(temp_cards) == 3:
            print("\n=== 丢牌决策 ===")
            print("需要从3张牌中选择丢弃1张")
            
            # 使用MCTS选择要丢弃的牌
            print("使用MCTS选择要丢弃的牌...")
            
            # 创建一个临时状态来评估丢弃不同牌的效果
            best_discard_index = 0
            best_score = -float('inf')
            
            # 评估每张牌作为丢弃牌的效果
            for discard_index in range(3):
                # 创建临时手牌
                temp_hand = {
                    'top': self.hand['top'].copy(),
                    'middle': self.hand['middle'].copy(),
                    'bottom': self.hand['bottom'].copy(),
                    'temp': [card for i, card in enumerate(temp_cards) if i != discard_index]
                }
                
                # 评估这个选择的效果
                # 这里可以使用更复杂的评估方法，比如模拟摆牌后的强度
                top_strength = game.evaluate_hand(temp_hand['top'])
                middle_strength = game.evaluate_hand(temp_hand['middle'])
                bottom_strength = game.evaluate_hand(temp_hand['bottom'])
                
                # 计算总分
                total_strength = top_strength + middle_strength + bottom_strength
                
                if total_strength > best_score:
                    best_score = total_strength
                    best_discard_index = discard_index
            
            # 执行丢牌
            discarded_card = temp_cards.pop(best_discard_index)
            print(f"已丢弃: {discarded_card}")
            print(f"保留: {temp_cards}")
        
        # 如果还有剩余的牌，按照规则分配
        while temp_cards:
            # 更新原始的temp_cards，确保get_actions方法基于正确的牌列表
            self.hand['temp'] = temp_cards.copy()
            
            # 获取当前状态
            current_state = self.rl_agent.get_state(game, self)
            
            # 选择动作 - 改回原来的工作流程
            try:
                if is_first_round:
                    # 第一轮使用强化学习选择动作
                    action = self.rl_agent.choose_action(game, self)
                else:
                    # 第二轮及以后使用MCTS选择动作
                    print("使用MCTS进行深度搜索...")
                    # 创建MCTS状态
                    mcts_state = (self, game)
                    # 使用MCTS搜索最佳动作
                    action = self.mcts.search(mcts_state)
                    print("MCTS搜索完成！")
            except Exception as e:
                print(f"选择动作出错: {e}")
                # 如果出错，使用简单的策略选择动作
                # 按照区域顺序选择第一个可用区域
                if len(self.hand['top']) < 3:
                    area = 'top'
                elif len(self.hand['middle']) < 5:
                    area = 'middle'
                elif len(self.hand['bottom']) < 5:
                    area = 'bottom'
                else:
                    break
                # 选择第一张牌
                card_index = 0
                action = (card_index, ['top', 'middle', 'bottom'].index(area))
            
            if not action:
                break
            
            # 设置当前上下文，用于错误纠正模块
            self.error_module.set_current_context(game, self, current_state, action)
            
            # 执行动作前，显示AI的选择
            print(f"AI选择的动作: 将第{action[0]+1}张牌放到{'顶部' if action[1]==0 else '中部' if action[1]==1 else '底部'}区域")
            
            # 执行动作
            card_index, area_index = action
            
            # 检查card_index是否有效
            if card_index < 0 or card_index >= len(temp_cards):
                break
            
            card = temp_cards[card_index]
            
            # 确定摆放区域
            areas = ['top', 'middle', 'bottom']
            area = areas[area_index]
            
            # 强制规则：检查区域是否已满
            # 头道只能3张牌，中道底道只能5张牌
            max_cards = 3 if area == 'top' else 5
            if len(self.hand[area]) >= max_cards:
                # 强制规则：区域已满，必须选择其他未满的区域
                print(f"强制规则: {area}区域已满({len(self.hand[area])}张)，必须选择其他区域")
                # 取消优先级顺序规则，随机选择可用区域
                available_areas = []
                if len(self.hand['top']) < 3:
                    available_areas.append('top')
                if len(self.hand['middle']) < 5:
                    available_areas.append('middle')
                if len(self.hand['bottom']) < 5:
                    available_areas.append('bottom')
                
                if available_areas:
                    import random
                    area = random.choice(available_areas)  # 随机选择可用区域
                    area_name = '顶部' if area == 'top' else '中部' if area == 'middle' else '底部'
                    print(f"强制规则: 随机选择{area_name}区域")
                else:
                    print("强制规则: 所有区域都已满，无法继续摆放牌")
                    break  # 所有区域都已满
            
            # 取消QQ+牌优先分配到顶部区域的规则
            
            # 记录摆牌顺序
            placement_order.append((card, area))
            
            # 执行摆牌
            if area in self.hand:
                self.hand[area].append(card)
                temp_cards.pop(card_index)
                print(f"已将 {card} 放到 {area} 区域")
            
            # 获取新状态
            new_state = self.rl_agent.get_state(game, self)
            
            # 学习
            done = not temp_cards
            self.rl_agent.learn(game, self, action, current_state, new_state, done)
            
            # 更新上一个状态
            self.last_state = new_state
        
        # 清空temp_cards，因为所有牌都已摆放
        self.hand['temp'] = []
        
        # 取消自动调整区域强度顺序的规则
        
        # 显示各区域强度
        
        
        # 显示最终各区域的牌数
        final_top = len(self.hand['top'])
        final_middle = len(self.hand['middle'])
        final_bottom = len(self.hand['bottom'])
        print(f"\n摆牌完成，最终各区域牌数: 顶部 {final_top}张, 中部 {final_middle}张, 底部 {final_bottom}张")
        
        # 显示摆牌结果和顺序
        print("\nAI摆牌完成，显示摆牌结果:")
        print(f"顶部区域: {[str(card) for card in self.hand.get('top', [])]}")
        print(f"中部区域: {[str(card) for card in self.hand.get('middle', [])]}")
        print(f"底部区域: {[str(card) for card in self.hand.get('bottom', [])]}")
        
        # 显示摆牌顺序
        print("\n摆牌顺序:")
        for i, (card, area) in enumerate(placement_order, 1):
            area_name = '顶部' if area == 'top' else '中部' if area == 'middle' else '底部'
            print(f"{i}. 将 {card} 放到 {area_name} 区域")
        
        # 自动模式，跳过用户输入
        if auto_mode:
            print("\n自动模式: 跳过用户输入")
        else:
            # 询问用户是否要纠正错误
            print("\n是否要纠正AI的摆牌？ (y/n): ")
            user_input = input().strip().lower()
            if user_input == 'y':
                print("\n请输入正确的摆法:")
                print("格式: 牌索引 区域索引 (例如: 0 1 表示将第1张牌放到中部区域)")
                print("区域索引: 0=顶部, 1=中部, 2=底部")
                print("输入多张牌时用空格分隔，例如: 0 1 1 2 2 2")
                print("输入 'cancel' 取消纠正")
                
                # 显示当前待摆放的牌，方便用户参考
                temp_cards = self.hand.get('temp', []).copy()
                if temp_cards:
                    print("\n当前待摆放的牌 (索引 0-4):")
                    for i, card in enumerate(temp_cards):
                        print(f"{i}: {card}")
                
                # 获取用户输入
                correction_input = input("请输入正确的摆法: ").strip()
                if correction_input.lower() != 'cancel':
                    try:
                        # 解析用户输入
                        parts = correction_input.split()
                        if len(parts) % 2 != 0:
                            print("输入格式错误，请确保每个牌都有对应的区域索引")
                        else:
                            # 解析正确的摆法
                            correct_actions = []
                            for i in range(0, len(parts), 2):
                                card_index = int(parts[i])
                                area_index = int(parts[i+1])
                                correct_actions.append((card_index, area_index))
                            
                            print(f"\n解析到 {len(correct_actions)} 个摆牌动作")
                            
                            # 验证动作的有效性
                            valid_actions = []
                            temp_cards_copy = temp_cards.copy()
                            for action in correct_actions:
                                card_index, area_index = action
                                if card_index >= 0 and card_index < len(temp_cards_copy):
                                    # 检查区域是否有效
                                    if area_index in [0, 1, 2]:
                                        # 检查区域是否已满
                                        area_name = ['top', 'middle', 'bottom'][area_index]
                                        if len(self.hand.get(area_name, [])) < (3 if area_name == 'top' else 5):
                                            valid_actions.append(action)
                                            # 从临时牌中移除已摆放的牌
                                            temp_cards_copy.pop(card_index)
                                        else:
                                            print(f"警告: {['顶部', '中部', '底部'][area_index]}区域已满")
                                    else:
                                        print(f"警告: 区域索引 {area_index} 无效，应为 0-2")
                                else:
                                    print(f"警告: 牌索引 {card_index} 无效")
                            
                            if valid_actions:
                                print(f"\n有效动作数: {len(valid_actions)}")
                                
                                # 存储用户的正确摆法作为专家经验
                                print("\n=== AI学习过程 ===")
                                print("1. 记录您的摆法作为专家经验")
                                
                                # 获取当前状态
                                current_state = self.rl_agent.get_state(game, self)
                                
                                # 模拟用户的正确摆法过程
                                temp_cards_learn = temp_cards.copy()
                                for i, action in enumerate(valid_actions):
                                    card_index, area_index = action
                                    if card_index < len(temp_cards_learn):
                                        # 获取牌
                                        card = temp_cards_learn[card_index]
                                        
                                        # 确定区域
                                        area_name = ['top', 'middle', 'bottom'][area_index]
                                        
                                        # 显示学习过程
                                        print(f"   学习动作 {i+1}: 将 {card} 放到 {['顶部', '中部', '底部'][area_index]} 区域")
                                        
                                        # 存储为专家经验
                                        if hasattr(self.rl_agent, 'store_expert_experience'):
                                            # 创建简化的下一个状态
                                            next_state = self.rl_agent.get_state(game, self)
                                            # 给予高奖励
                                            reward = 100.0  # 专家经验的高奖励
                                            # 存储经验
                                            self.rl_agent.store_expert_experience(current_state, action, reward, next_state, [], True)
                                        
                                        # 从临时牌中移除
                                        temp_cards_learn.pop(card_index)
                                
                                print("2. 增强训练过程")
                                print("   正在进行强化学习训练...")
                                
                                # 增加训练频率，立即进行多次训练
                                training_rounds = 15  # 每纠正一次训练15次
                                for i in range(training_rounds):
                                    self.rl_agent.train_from_replay()
                                    if (i+1) % 3 == 0:
                                        print(f"   训练进度: {i+1}/{training_rounds}")
                                
                                print("\n=== 学习完成 ===")
                                print("[成功] AI已成功学习您的摆牌策略！")
                                print("[成功] 专家经验已存储并优先用于训练")
                                print("[成功] 训练完成，AI的摆牌策略已更新")
                                print("\n下次摆牌时，AI将尝试使用您教的策略！")
                    except Exception as e:
                        print(f"处理纠正时出错: {e}")
            else:
                print("取消纠正")
            
            # 询问是否要暂停查看
            print("\n是否要暂停查看？ (y/n): ")
            user_input = input().strip().lower()
            if user_input == 'y':
                print("游戏暂停，按回车键继续...")
                input()
        
        # 返回最终的摆牌结果
        return {
            'top': self.hand.get('top', []),
            'middle': self.hand.get('middle', []),
            'bottom': self.hand.get('bottom', [])
        }
    
    def check_high_pairs(self, cards):
        """
        检查是否有AA/KK/QQ高对子
        """
        if not cards:
            return False
        
        # 统计每张牌的点数
        rank_counts = {}
        for card in cards:
            rank = card[0] if isinstance(card, tuple) else card.value
            rank_counts[rank] = rank_counts.get(rank, 0) + 1
        
        # 检查是否有AA/KK/QQ
        high_pairs = {14: 'AA', 13: 'KK', 12: 'QQ'}
        for rank, name in high_pairs.items():
            if rank_counts.get(rank, 0) >= 2:
                return True
        
        return False
    
    def update_stats(self, game, opponent, fl_attempt=False, fl_success=False, busted=False):
        """
        更新统计数据
        """
        # 增加总游戏次数
        self.stats['total_games'] += 1
        
        # 检查是否拿到高对子
        temp_cards = self.hand.get('temp', [])
        all_cards = temp_cards + self.hand.get('top', []) + self.hand.get('middle', []) + self.hand.get('bottom', [])
        has_high_pairs = self.check_high_pairs(all_cards)
        
        if has_high_pairs:
            self.stats['high_pairs_count'] += 1
            if fl_attempt:
                self.stats['high_pairs_attempt_fl'] += 1
        
        # 更新FL相关统计
        if fl_attempt:
            self.stats['fl_attempts'] += 1
            if fl_success:
                self.stats['fl_successes'] += 1
        
        # 更新爆牌统计
        if busted:
            self.stats['busted_count'] += 1
        
        # 计算得分
        ai_score = self.calculate_hand_score(game)
        self.stats['ai_scores'].append(ai_score)
        
        # 计算专家得分（假设对手是专家）
        if opponent:
            expert_score = self.calculate_opponent_score(game, opponent)
            self.stats['expert_scores'].append(expert_score)
        
        # 保持历史记录在100局以内
        max_history = 100
        if len(self.stats['ai_scores']) > max_history:
            self.stats['ai_scores'] = self.stats['ai_scores'][-max_history:]
        if len(self.stats['expert_scores']) > max_history:
            self.stats['expert_scores'] = self.stats['expert_scores'][-max_history:]
        
        # 计算专家得分
        expert_score = 0
        if opponent:
            expert_score = self.calculate_opponent_score(game, opponent)
        
        # 记录游戏历史
        game_record = {
            'game_id': self.stats['total_games'],
            'has_high_pairs': has_high_pairs,
            'fl_attempt': fl_attempt,
            'fl_success': fl_success,
            'busted': busted,
            'ai_score': ai_score,
            'expert_score': expert_score
        }
        self.stats['game_history'].append(game_record)
        
        # 保持游戏历史在100局以内
        if len(self.stats['game_history']) > max_history:
            self.stats['game_history'] = self.stats['game_history'][-max_history:]
    
    def calculate_hand_score(self, game):
        """
        计算当前手牌的得分
        """
        # 简单的得分计算：基于牌型强度
        top_strength = game.evaluate_hand(self.hand.get('top', []))
        middle_strength = game.evaluate_hand(self.hand.get('middle', []))
        bottom_strength = game.evaluate_hand(self.hand.get('bottom', []))
        
        # 计算总分
        total_score = top_strength + middle_strength + bottom_strength
        
        # 检查是否爆牌
        if top_strength > middle_strength or middle_strength > bottom_strength:
            total_score -= 50  # 爆牌惩罚
        
        return total_score
    
    def calculate_opponent_score(self, game, opponent):
        """
        计算对手的得分
        """
        # 简单的得分计算：基于牌型强度
        top_strength = game.evaluate_hand(opponent.hand.get('top', []))
        middle_strength = game.evaluate_hand(opponent.hand.get('middle', []))
        bottom_strength = game.evaluate_hand(opponent.hand.get('bottom', []))
        
        # 计算总分
        total_score = top_strength + middle_strength + bottom_strength
        
        # 检查是否爆牌
        if top_strength > middle_strength or middle_strength > bottom_strength:
            total_score -= 50  # 爆牌惩罚
        
        return total_score
    
    def get_top_actions(self, game, top_n=3):
        """
        获取排名最高的top_n个动作
        """
        # 获取当前状态
        current_state = self.rl_agent.get_state(game, self)
        # 获取所有可用动作
        actions = self.rl_agent.get_actions(self)
        
        if not actions:
            return []
        
        # 计算每个动作的得分
        action_scores = []
        for action in actions:
            try:
                # 使用强化学习计算动作得分
                q_value = self.rl_agent.get_q_value(current_state, action)
                win_prob = self.rl_agent.calculate_win_probability(game, self, action, current_state)
                
                # 模拟摆牌后的手牌状态，计算潜力
                temp_hand = {
                    'top': self.hand.get('top', []).copy(),
                    'middle': self.hand.get('middle', []).copy(),
                    'bottom': self.hand.get('bottom', []).copy(),
                    'temp': sorted(self.hand.get('temp', []).copy(), key=lambda x: (x.value, x.suit))
                }
                
                # 执行动作
                if action:
                    card_index, area_index = action
                    if card_index < len(temp_hand['temp']):
                        card = temp_hand['temp'][card_index]
                        areas = ['top', 'middle', 'bottom']
                        area = areas[area_index]
                        temp_hand[area].append(card)
                        temp_hand['temp'].pop(card_index)
                
                # 计算各区域的潜在发展潜力
                top_potential = self.rl_agent.calculate_card_potential(temp_hand['top'])
                middle_potential = self.rl_agent.calculate_card_potential(temp_hand['middle'])
                bottom_potential = self.rl_agent.calculate_card_potential(temp_hand['bottom'])
                total_potential = top_potential + middle_potential + bottom_potential
                
                # 综合得分
                score = q_value * 0.6 + win_prob * 12 + total_potential * 8
                action_scores.append((score, action))
            except Exception as e:
                print(f"计算动作得分出错: {e}")
                action_scores.append((0, action))
        
        # 按得分排序，返回前top_n个动作
        action_scores.sort(reverse=True, key=lambda x: x[0])
        return [action for _, action in action_scores[:top_n]]
    
    def evaluate_mcts_result(self, mcts_result, game):
        """
        评估MCTS结果的分数
        """
        try:
            # 简单评估：如果MCTS返回了有效动作，给予高分
            if mcts_result:
                # 检查动作是否有效
                card_index, area_index = mcts_result
                if card_index >= 0 and 0 <= area_index <= 2:
                    return 100.0  # MCTS验证通过
            return 0.0  # MCTS验证失败
        except Exception as e:
            print(f"评估MCTS结果出错: {e}")
            return 0.0
    
    def adjust_area_strength_order(self, game):
        """
        自动调整区域强度顺序，确保顶部 <= 中部 <= 底部 这个不需要
        """
        print("强制规则: 执行自动调整区域强度顺序...")
        
        # 获取当前各区域的牌和强度
        top_cards = self.hand['top'].copy()
        middle_cards = self.hand['middle'].copy()
        bottom_cards = self.hand['bottom'].copy()
        
        top_strength = game.evaluate_hand(top_cards)
        middle_strength = game.evaluate_hand(middle_cards)
        bottom_strength = game.evaluate_hand(bottom_cards)
        
        # 简单的调整策略：交换区域中最强和最弱的牌
        # 1. 首先确保底部区域是最强的
        if bottom_strength < middle_strength or bottom_strength < top_strength:
            print("强制规则: 底部区域不是最强的，需要调整...")
            
            # 找到所有区域中最强的牌
            all_cards = top_cards + middle_cards + bottom_cards
            strongest_card = max(all_cards, key=lambda x: x.value)
            
            # 找到最强牌所在的区域
            if strongest_card in top_cards:
                top_cards.remove(strongest_card)
                bottom_cards.append(strongest_card)
                print(f"强制规则: 将最强牌 {strongest_card} 从顶部移到底部")
            elif strongest_card in middle_cards:
                middle_cards.remove(strongest_card)
                bottom_cards.append(strongest_card)
                print(f"强制规则: 将最强牌 {strongest_card} 从中部移到底部")
            
            # 找到底部区域中最弱的牌
            if bottom_cards:
                weakest_in_bottom = min(bottom_cards, key=lambda x: x.value)
                # 将最弱的牌移到顶部
                bottom_cards.remove(weakest_in_bottom)
                if len(top_cards) < 3:
                    top_cards.append(weakest_in_bottom)
                    print(f"强制规则: 将最弱牌 {weakest_in_bottom} 从底部移到顶部")
                elif len(middle_cards) < 5:
                    middle_cards.append(weakest_in_bottom)
                    print(f"强制规则: 将最弱牌 {weakest_in_bottom} 从底部移到中部")
        
        # 2. 确保中部区域比顶部区域强
        if middle_strength < top_strength:
            print("强制规则: 中部区域弱于顶部区域，需要调整...")
            
            # 找到顶部区域中最强的牌
            if top_cards:
                strongest_in_top = max(top_cards, key=lambda x: x.value)
                top_cards.remove(strongest_in_top)
                middle_cards.append(strongest_in_top)
                print(f"强制规则: 将顶部最强牌 {strongest_in_top} 移到中部")
            
            # 找到中部区域中最弱的牌
            if middle_cards:
                weakest_in_middle = min(middle_cards, key=lambda x: x.value)
                middle_cards.remove(weakest_in_middle)
                top_cards.append(weakest_in_middle)
                print(f"强制规则: 将中部最弱牌 {weakest_in_middle} 移到顶部")
        
        # 3. 确保各区域牌数正确
        # 调整顶部区域牌数为3
        while len(top_cards) > 3:
            extra_card = top_cards.pop()
            if len(middle_cards) < 5:
                middle_cards.append(extra_card)
            elif len(bottom_cards) < 5:
                bottom_cards.append(extra_card)
        while len(top_cards) < 3 and (middle_cards or bottom_cards):
            if middle_cards:
                weakest_in_middle = min(middle_cards, key=lambda x: x.value)
                middle_cards.remove(weakest_in_middle)
                top_cards.append(weakest_in_middle)
            elif bottom_cards:
                weakest_in_bottom = min(bottom_cards, key=lambda x: x.value)
                bottom_cards.remove(weakest_in_bottom)
                top_cards.append(weakest_in_bottom)
        
        # 调整中部区域牌数为5
        while len(middle_cards) > 5:
            extra_card = middle_cards.pop()
            if len(bottom_cards) < 5:
                bottom_cards.append(extra_card)
        while len(middle_cards) < 5 and bottom_cards:
            weakest_in_bottom = min(bottom_cards, key=lambda x: x.value)
            bottom_cards.remove(weakest_in_bottom)
            middle_cards.append(weakest_in_bottom)
        
        # 调整底部区域牌数为5
        while len(bottom_cards) > 5:
            extra_card = bottom_cards.pop()
            if len(middle_cards) < 5:
                middle_cards.append(extra_card)
        while len(bottom_cards) < 5 and middle_cards:
            strongest_in_middle = max(middle_cards, key=lambda x: x.value)
            middle_cards.remove(strongest_in_middle)
            bottom_cards.append(strongest_in_middle)
        
        # 更新手牌
        self.hand['top'] = top_cards
        self.hand['middle'] = middle_cards
        self.hand['bottom'] = bottom_cards
        
        print("强制规则: 区域强度顺序调整完成")
    
    def show_stats(self):
        """
        显示统计面板
        """
        print("\n=====================================")
        print("             AI 统计面板            ")
        print("=====================================")
        
        # 计算最近100局的数据
        recent_games = min(self.stats['total_games'], 100)
        print(f"统计周期: 最近 {recent_games} 局")
        
        # 统计最近100局的高对子次数和爆牌次数
        recent_high_pairs = 0
        recent_busted = 0
        recent_fl_attempts = 0
        recent_fl_successes = 0
        
        # 从游戏历史中统计最近100局的数据
        if 'game_history' in self.stats:
            recent_history = self.stats['game_history'][-recent_games:]
            for game in recent_history:
                if game.get('has_high_pairs'):
                    recent_high_pairs += 1
                if game.get('busted'):
                    recent_busted += 1
                if game.get('fl_attempt'):
                    recent_fl_attempts += 1
                    if game.get('fl_success'):
                        recent_fl_successes += 1
        
        # 1. 高对子尝试进FL的统计
        high_pairs_count = recent_high_pairs
        high_pairs_attempt_fl = recent_fl_attempts
        if high_pairs_count > 0:
            high_pairs_fl_rate = (high_pairs_attempt_fl / high_pairs_count) * 100
        else:
            high_pairs_fl_rate = 0
        print(f"\n1. 高对子(AA/KK/QQ)统计:")
        print(f"   拿到高对子次数: {high_pairs_count}")
        print(f"   尝试进FL次数: {high_pairs_attempt_fl}")
        print(f"   尝试进FL比例: {high_pairs_fl_rate:.1f}%")
        
        # 2. FL成功率与爆牌率对比
        fl_attempts = recent_fl_attempts
        fl_successes = recent_fl_successes
        busted_count = recent_busted
        
        if fl_attempts > 0:
            fl_success_rate = (fl_successes / fl_attempts) * 100
        else:
            fl_success_rate = 0
        
        if recent_games > 0:
            busted_rate = (busted_count / recent_games) * 100
        else:
            busted_rate = 0
        
        print(f"\n2. FL成功率与爆牌率:")
        print(f"   尝试进FL次数: {fl_attempts}")
        print(f"   成功进FL次数: {fl_successes}")
        print(f"   FL成功率: {fl_success_rate:.1f}%")
        print(f"   爆牌次数: {busted_count}")
        print(f"   爆牌率: {busted_rate:.1f}%")
        
        # 3. 平均分差距
        ai_scores = self.stats['ai_scores']
        expert_scores = self.stats['expert_scores']
        
        if ai_scores:
            avg_ai_score = sum(ai_scores) / len(ai_scores)
        else:
            avg_ai_score = 0
        
        if expert_scores:
            avg_expert_score = sum(expert_scores) / len(expert_scores)
            score_gap = avg_expert_score - avg_ai_score
        else:
            avg_expert_score = 0
            score_gap = 0
        
        print(f"\n3. 平均分差距:")
        print(f"   AI平均分: {avg_ai_score:.2f}")
        print(f"   专家平均分: {avg_expert_score:.2f}")
        print(f"   分差: {score_gap:.2f}")
        
        # 4. 学习效果验证
        print(f"\n4. 学习效果验证:")
        
        # 计算最近10局和之前10局的对比
        if len(ai_scores) >= 20:
            recent_10_scores = ai_scores[-10:]
            previous_10_scores = ai_scores[-20:-10]
            
            avg_recent = sum(recent_10_scores) / 10
            avg_previous = sum(previous_10_scores) / 10
            improvement = avg_recent - avg_previous
            
            print(f"   最近10局平均分: {avg_recent:.2f}")
            print(f"   之前10局平均分: {avg_previous:.2f}")
            print(f"   平均分变化: {improvement:+.2f}")
            
            if improvement > 0:
                print(f"   [成功] AI正在进步！")
            elif improvement < 0:
                print(f"   [警告] AI需要更多学习")
            else:
                print(f"   [信息] AI表现稳定")
        
        # 5. 专家经验学习情况
        if hasattr(self.rl_agent, 'expert_buffer'):
            expert_experience_count = len(self.rl_agent.expert_buffer)
            print(f"\n5. 专家经验学习情况:")
            print(f"   已学习的专家经验数: {expert_experience_count}")
            if expert_experience_count > 0:
                print(f"   [成功] AI已从您的摆法中学习")
                print(f"   [成功] 专家经验优先级: 50.0")
                print(f"   [成功] 专家经验占训练比例: 60%")
        
        print("=====================================")
    
    def learn_from_game(self, game, opponent, ask_for_stats=False):
        """
        从游戏中学习
        ask_for_stats: 是否询问用户是否查看统计面板（默认False，用于AI自我博弈）
        """
        # 调用父类的学习方法
        super().learn_from_game(game, opponent)
        
        # 检查是否爆牌
        busted = game.check_busted(self)
        
        # 更新统计数据
        # 假设这里可以获取FL尝试和成功的信息
        # 实际应用中需要根据游戏逻辑调整
        self.update_stats(game, opponent, busted=busted)
        
        # 增加训练频率，每局游戏进行多次训练
        for _ in range(5):  # 每局游戏训练5次
            self.rl_agent.train_from_replay()
        
        # 询问用户是否要查看统计面板（仅在ask_for_stats=True时）
        if ask_for_stats:
            print("\n本局游戏结束，是否要查看统计面板？ (y/n): ")
            user_input = input().strip().lower()
            if user_input == 'y':
                self.show_stats()
        # 每5局自动显示一次统计面板
        if self.stats['total_games'] % 5 == 0:
            self.show_stats()
        
        # 保存强化学习数据
        self.rl_agent.save_learning_data()
    
    def save_learning_data(self):
        """
        保存学习数据
        """
        super().save_learning_data()
        self.rl_agent.save_learning_data()
    
    def learn_from_json_records(self):
        """
        从json文件中学习
        """
        import json
        import os
        
        records_dir = "game_records"
        if not os.path.exists(records_dir):
            print(f"目录 {records_dir} 不存在")
            return
        
        # 定义优先级目录
        priority_dir = os.path.join(records_dir, "priority")
        
        # 先从优先级目录学习
        if os.path.exists(priority_dir):
            priority_files = [f for f in os.listdir(priority_dir) if f.endswith('.json')]
            if priority_files:
                print(f"\n优先从优先级目录学习: 找到 {len(priority_files)} 个优先级文件")
                self._learn_from_files(priority_dir, priority_files, is_priority=True)
        
        # 再从主目录学习
        main_files = [f for f in os.listdir(records_dir) if f.endswith('.json')]
        print(f"\n从主目录学习: 找到 {len(main_files)} 个游戏记录文件")
        self._learn_from_files(records_dir, main_files, is_priority=False)
        
        print("从json文件中学习完成")
    
    def _learn_from_files(self, directory, files, is_priority=False):
        """
        从指定目录的文件中学习
        """
        import json
        import os
        
        # 遍历所有文件
        for i, json_file in enumerate(files):
            prefix = "[优先级] " if is_priority else ""
            print(f"{prefix}学习第 {i+1}/{len(files)} 个文件: {json_file}")
            
            # 读取文件
            file_path = os.path.join(directory, json_file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                print(f"读取文件 {json_file} 失败: {e}")
                continue
            
            # 提取玩家信息
            for player in data.get('players', []):
                if not player.get('is_ai'):  # 只学习人类玩家的摆法
                    hand = player.get('hand', {})
                    top = hand.get('top', [])
                    middle = hand.get('middle', [])
                    bottom = hand.get('bottom', [])
                    
                    # 转换为经验
                    print(f"学习人类玩家的摆法: 顶部 {len(top)}张, 中部 {len(middle)}张, 底部 {len(bottom)}张")
                    
                    # 提取所有牌
                    all_cards = top + middle + bottom
                    if len(all_cards) < 5:
                        continue  # 跳过牌数不足的情况
                    
                    # 创建一个简单的游戏状态
                    # 由于没有完整的游戏状态信息，我们使用简化的状态表示
                    state = (tuple(), tuple(), tuple(), tuple(), 1, 1000, 0)
                    
                    # 模拟摆牌过程，为每张牌创建一个动作
                    temp_cards = all_cards.copy()
                    for card in all_cards:
                        # 确定这张牌应该放在哪个区域
                        if card in top:
                            area_index = 0
                        elif card in middle:
                            area_index = 1
                        else:  # card in bottom
                            area_index = 2
                        
                        # 找到牌在temp_cards中的索引
                        try:
                            card_index = temp_cards.index(card)
                        except ValueError:
                            continue  # 跳过找不到的牌
                        
                        # 创建动作
                        action = (card_index, area_index)
                        
                        # 计算奖励
                        # 优先级文件给予更高的奖励
                        reward = 100 if is_priority else 50
                        
                        # 存储经验
                        if hasattr(self, 'rl_agent') and hasattr(self.rl_agent, 'store_experience'):
                            # 创建新状态（简化表示）
                            new_state = (tuple(), tuple(), tuple(), tuple(), 1, 1000, 0)
                            
                            # 存储经验，标记为专家经验
                            self.rl_agent.store_expert_experience(state, action, reward, new_state, [], True)
                            
                            # 从temp_cards中移除这张牌
                            temp_cards.pop(card_index)
                    
                    print(f"成功从人类玩家的摆法中学习到 {len(all_cards)} 个经验")
