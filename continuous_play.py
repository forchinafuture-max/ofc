#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
后台持续运行AI对战的脚本
"""

from rl_ai import RLAIPlayer
from game_logic import OFCGame
import time
import sys

class ContinuousPlay:
    def __init__(self):
        self.game = OFCGame()
        self.ai1 = None
        self.ai2 = None
        self.running = True
        self.game_count = 0
    
    def initialize_ais(self):
        """
        初始化两个AI玩家
        """
        print("初始化AI玩家...")
        # 创建两个AI玩家，设置skip_learning=True以跳过初始JSON学习
        self.ai1 = RLAIPlayer("AI Player 1", skip_learning=True)
        self.ai2 = RLAIPlayer("AI Player 2", skip_learning=True)
        
        # 添加玩家到游戏
        self.game.add_player(self.ai1)
        self.game.add_player(self.ai2)
        print("AI玩家初始化完成！")
    
    def reset_game(self):
        """
        重置游戏状态
        """
        # 清空游戏中的玩家列表
        self.game.players = []
        
        # 重置AI玩家的手牌和分数
        self.ai1.hand = {'temp': [], 'top': [], 'middle': [], 'bottom': []}
        self.ai2.hand = {'temp': [], 'top': [], 'middle': [], 'bottom': []}
        self.ai1.total_score = 0
        self.ai2.total_score = 0
        
        # 重新添加玩家到游戏
        self.game.add_player(self.ai1)
        self.game.add_player(self.ai2)
    
    def play_one_game(self):
        """
        玩一局完整的游戏（5轮），简化输出
        """
        try:
            # 重置游戏状态
            self.reset_game()
            
            # 开始游戏
            self.game.start_game()
            
            # 进行五轮游戏
            for round_num in range(1, 6):
                # 设置当前轮次
                self.game.table.round = round_num
                
                # 发牌
                self.game.deal_round()
                
                # 让两个AI玩家进行摆牌
                for player in self.game.players:
                    # 使用place_cards_strategy方法摆牌，auto_mode=True
                    player.place_cards_strategy(self.game, auto_mode=True)
            
            # 保存游戏记录
            self.game.save_game_record()
            
            # 两个AI都从游戏中学习
            self.ai1.learn_from_game(self.game, self.ai2, ask_for_stats=False)
            self.ai2.learn_from_game(self.game, self.ai1, ask_for_stats=False)
            
            self.game_count += 1
            return True
        except Exception as e:
            print(f"游戏过程中出错: {e}")
            return False
    
    def start_continuous_play(self):
        """
        开始持续运行游戏
        """
        print("开始后台持续运行AI对战...")
        print("=====================================")
        print("按 'r' 键并回车停止对战")
        print("=====================================")
        
        # 初始化AI玩家
        self.initialize_ais()
        
        # 记录开始时间
        start_time = time.time()
        
        try:
            while self.running:
                # 玩一局游戏
                self.play_one_game()
                
                # 每10局显示一次统计信息
                if self.game_count % 10 == 0:
                    print(f"\n已完成 {self.game_count} 局对战...")
                    
                    # 显示AI统计信息
                    print("\nAI Player 1 统计信息:")
                    self.ai1.show_stats()
                    
                    print("\nAI Player 2 统计信息:")
                    self.ai2.show_stats()
                    
                    print("=====================================")
                    print("按 'r' 键并回车停止对战")
                    print("=====================================")
                    
                    # 检查是否按了r键
                    import sys
                    
                    # 尝试不同的键盘输入检测方法
                    try:
                        # Windows系统的方法
                        import msvcrt
                        if msvcrt.kbhit():
                            key = msvcrt.getch().decode('utf-8')
                            if key.lower() == 'r':
                                print("检测到 'r' 键，正在停止对战...")
                                self.running = False
                    except ImportError:
                        try:
                            # Unix/Linux系统的方法
                            import select
                            import tty
                            import termios
                            
                            # 保存终端设置
                            old_settings = termios.tcgetattr(sys.stdin)
                            try:
                                # 设置终端为非阻塞模式
                                tty.setcbreak(sys.stdin.fileno())
                                
                                # 检查是否有输入
                                if select.select([sys.stdin], [], [], 0)[0]:
                                    key = sys.stdin.read(1)
                                    if key.lower() == 'r':
                                        print("检测到 'r' 键，正在停止对战...")
                                        self.running = False
                            finally:
                                # 恢复终端设置
                                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                        except ImportError:
                            # 如果都失败了，就跳过键盘检测
                            pass
                
                # 短暂暂停，避免CPU占用过高
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n检测到停止信号，正在停止...")
        finally:
            # 记录结束时间
            end_time = time.time()
            total_time = end_time - start_time
            
            # 显示最终统计信息
            print("\n" + "=" * 80)
            print(f"持续对战已停止！")
            print(f"总对战局数: {self.game_count}局")
            print(f"总耗时: {total_time:.2f}秒")
            print(f"平均每局耗时: {total_time / self.game_count:.2f}秒")
            
            print("\nAI Player 1 最终统计:")
            self.ai1.show_stats()
            
            print("\nAI Player 2 最终统计:")
            self.ai2.show_stats()
            
            print("=" * 80)

if __name__ == "__main__":
    # 创建并运行脚本
    continuous_play = ContinuousPlay()
    continuous_play.start_continuous_play()
