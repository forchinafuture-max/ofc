#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跳过学习阶段，直接开始游戏
"""

import sys
import os

# 添加当前目录到模块搜索路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from main import OFCGameManager
    print("[成功] 导入模块成功")
except Exception as e:
    print(f"[错误] 导入模块失败: {e}")
    sys.exit(1)

if __name__ == "__main__":
    print("=" * 50)
    print("        快速启动OFC扑克游戏        ")
    print("=" * 50)
    print("跳过学习阶段，直接进入游戏...")
    print("=" * 50)
    
    # 创建游戏管理器实例
    game_manager = OFCGameManager()
    
    # 直接运行游戏，跳过学习
    game_manager.run(skip_learning=True)
