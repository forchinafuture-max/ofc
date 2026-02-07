#!/usr/bin/env python3
"""
修复编码问题的游戏启动脚本
"""

import sys
import os

# 设置默认编码为UTF-8
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# 导入游戏管理器
from main import OFCGameManager

if __name__ == "__main__":
    print("启动OFC扑克游戏...")
    print("已修复编码问题，现在可以正常显示扑克牌符号。")
    print("AI已经从101个游戏记录文件中学习，具备了基本的摆牌策略。")
    print("新的奖励机制已启用，AI会避免过早填满头道和爆牌。")
    print("\n" + "="*50)
    
    # 创建游戏管理器实例并运行
    game_manager = OFCGameManager()
    game_manager.run()
