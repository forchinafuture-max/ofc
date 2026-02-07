#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
捕获游戏的完整输出，包括交互式提示
"""

import sys
import os
import subprocess
import time

if __name__ == "__main__":
    print("正在启动游戏并捕获完整输出...")
    print("=" * 50)
    
    # 运行游戏并捕获输出
    process = subprocess.Popen(
        [sys.executable, 'skip_learning_start_game.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdin=subprocess.PIPE,
        text=True,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    # 读取输出
    output_lines = []
    
    try:
        # 给游戏一些时间启动
        time.sleep(2)
        
        # 读取输出，直到进程结束或超时
        start_time = time.time()
        timeout = 10  # 10秒超时
        
        while time.time() - start_time < timeout:
            if process.poll() is not None:
                break
            
            # 尝试读取一行输出
            try:
                line = process.stdout.readline()
                if line:
                    output_lines.append(line)
                    print(line, end='')
            except:
                pass
            
            time.sleep(0.1)
        
        # 终止进程
        process.terminate()
        try:
            process.wait(timeout=2)
        except:
            pass
            
    except Exception as e:
        print(f"捕获输出时出错: {e}")
    
    # 保存输出到文件
    with open('game_full_output.txt', 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    
    print("\n" + "=" * 50)
    print("游戏输出已保存到 game_full_output.txt")
    print(f"捕获到 {len(output_lines)} 行输出")
    print("=" * 50)
