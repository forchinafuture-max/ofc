#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行游戏并将输出重定向到文件
"""

import sys
import os
import subprocess

if __name__ == "__main__":
    print("正在启动游戏，输出将保存到 game_output.txt...")
    print("=" * 50)
    
    # 运行游戏并将输出重定向到文件
    with open('game_output.txt', 'w', encoding='utf-8') as f:
        result = subprocess.run(
            [sys.executable, 'skip_learning_start_game.py'],
            stdout=f,
            stderr=f,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
    
    print(f"游戏运行完成，退出码: {result.returncode}")
    print("输出已保存到 game_output.txt")
    print("=" * 50)
    
    # 显示文件内容
    print("\n游戏输出:")
    print("=" * 50)
    try:
        with open('game_output.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
    except Exception as e:
        print(f"读取文件失败: {e}")
