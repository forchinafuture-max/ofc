import time
import threading
from ai.learning import RLAgent

class ErrorCorrectionModule:
    """
    错误纠正模块，用于记录AI的错误决策并提供正确的动作建议
    """
    def __init__(self, rl_agent):
        self.rl_agent = rl_agent
        self.is_listening = False
        self.current_state = None
        self.current_action = None
        self.current_game = None
        self.current_player = None
        self.agent = None  # 存储RLAIPlayer实例
        print("错误纠正模块已初始化")
    
    def start_listening(self):
        """
        开始监听用户输入
        """
        if not self.is_listening:
            self.is_listening = True
            print("错误纠正模块已启动")
    
    def stop_listening(self):
        """
        停止监听用户输入
        """
        if self.is_listening:
            self.is_listening = False
            print("错误纠正模块已停止")
    
    def set_current_context(self, game, player, state, action):
        """
        设置当前游戏上下文
        """
        self.current_game = game
        self.current_player = player
        self.current_state = state
        self.current_action = action
    
    def record_error(self):
        """
        记录AI的错误决策
        """
        # 打印当前状态和动作
        print(f"当前状态: {self.current_state}")
        print(f"AI执行的动作: {self.current_action}")
        
        # 提示用户输入正确的动作
        print("\n请输入正确的动作:")
        print("格式: 卡牌索引 区域索引 (例如: 0 2 表示将第一张牌放到底部区域)")
        print("区域索引: 0=顶部, 1=中部, 2=底部")
        print("输入 'cancel' 取消记录")
        
        # 获取用户输入
        while True:
            try:
                user_input = input("请输入正确的动作: ").strip()
                if user_input.lower() == 'cancel':
                    print("取消记录错误决策")
                    return
                
                # 解析用户输入
                parts = user_input.split()
                if len(parts) != 2:
                    raise ValueError("输入格式错误")
                
                card_index = int(parts[0])
                area_index = int(parts[1])
                
                # 验证输入
                if area_index not in [0, 1, 2]:
                    raise ValueError("区域索引必须是 0, 1 或 2")
                
                temp_cards = self.current_player.hand.get('temp', [])
                if card_index < 0 or card_index >= len(temp_cards):
                    raise ValueError(f"卡牌索引超出范围，有效范围: 0-{len(temp_cards)-1}")
                
                correct_action = (card_index, area_index)
                break
            except ValueError as e:
                print(f"输入错误: {e}，请重新输入")
                continue
        
        # 记录错误决策
        self.rl_agent.record_error_decision(
            self.current_state,
            self.current_action,
            correct_action,
            self.current_game,
            self.current_player
        )
        
        print("错误决策已记录，AI将在后续训练中加强学习")
    
    def record_error_manual(self):
        """
        手动记录错误决策的简单界面
        """
        print("\n手动记录错误决策:")
        print("请输入AI的错误动作和正确动作")
        print("格式: 错误卡牌索引 错误区域索引 正确卡牌索引 正确区域索引")
        print("例如: 0 0 0 2 表示将错误地放在顶部的第一张牌改到底部")
        print("区域索引: 0=顶部, 1=中部, 2=底部")
        print("输入 'cancel' 取消记录")
        
        # 获取用户输入
        try:
            user_input = input("请输入错误和正确动作: ").strip()
            if user_input.lower() == 'cancel':
                print("取消记录错误决策")
                return
            
            # 解析用户输入
            parts = user_input.split()
            if len(parts) != 4:
                raise ValueError("输入格式错误")
            
            wrong_card_index = int(parts[0])
            wrong_area_index = int(parts[1])
            correct_card_index = int(parts[2])
            correct_area_index = int(parts[3])
            
            # 验证输入
            for area_index in [wrong_area_index, correct_area_index]:
                if area_index not in [0, 1, 2]:
                    raise ValueError("区域索引必须是 0, 1 或 2")
            
            # 创建错误动作和正确动作
            wrong_action = (wrong_card_index, wrong_area_index)
            correct_action = (correct_card_index, correct_area_index)
            
            # 假设当前玩家是AI，获取其手牌
            if hasattr(self, 'agent') and self.agent:
                player = self.agent
                if hasattr(player, 'hand'):
                    # 创建一个简单的状态
                    state = (tuple(), tuple(), tuple(), tuple(), 1, 1000, 0)
                    
                    # 计算奖励
                    wrong_reward = -50
                    correct_reward = 50
                    
                    # 存储经验
                    if hasattr(self, 'agent') and hasattr(self.agent, 'rl_agent'):
                        rl_agent = self.agent.rl_agent
                        if hasattr(rl_agent, 'store_experience'):
                            # 存储错误动作
                            rl_agent.store_experience(state, wrong_action, wrong_reward, state, [], True)
                            # 存储正确动作
                            rl_agent.store_experience(state, correct_action, correct_reward, state, [], True)
                            print("错误和正确动作已记录，AI将在后续训练中学习")
                        else:
                            print("RLAgent没有store_experience方法")
                    else:
                        print("无法访问RLAgent")
                else:
                    print("当前玩家没有手牌")
            else:
                print("无法访问当前玩家")
        except ValueError as e:
            print(f"输入错误: {e}，请重新输入")
        except Exception as e:
            print(f"记录错误: {e}")

# 测试函数
def test_error_correction():
    """
    测试错误纠正模块
    """
    print("测试错误纠正模块...")
    
    # 创建RLAgent实例
    agent = RLAgent("test_agent")
    
    # 创建错误纠正模块
    error_module = ErrorCorrectionModule(agent)
    
    # 开始监听
    error_module.start_listening()
    
    print("错误纠正模块测试启动")
    print("按回车键退出测试")
    
    # 等待用户输入
    try:
        input()
    except KeyboardInterrupt:
        pass
    finally:
        # 停止监听
        error_module.stop_listening()
        print("错误纠正模块测试结束")

if __name__ == "__main__":
    test_error_correction()
