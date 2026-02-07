#!/usr/bin/env python3
"""
运行游戏并将所有输出重定向到日志文件
"""

import subprocess
import time

# 运行main.py并将输出重定向到文件
print("=======================================")
print("          启动OFC扑克游戏          ")
print("=======================================")
print("正在启动游戏...")
print("游戏输出将保存到 game_log.txt")
print("=======================================")

# 打开日志文件
with open('game_log.txt', 'w', encoding='utf-8') as f:
    # 启动游戏进程
    process = subprocess.Popen(
        ['python', 'main.py'],
        stdout=f,
        stderr=subprocess.STDOUT,
        text=True,
        shell=False
    )
    
    # 显示启动信息
    print("游戏进程已启动，PID:", process.pid)
    print("游戏正在运行中...")
    print("按Ctrl+C停止监控")
    print("=======================================")
    
    # 监控进程状态
    try:
        while process.poll() is None:
            time.sleep(1)
            print(f"游戏运行中... (PID: {process.pid})")
    except KeyboardInterrupt:
        print("\n正在停止游戏进程...")
        process.terminate()
        process.wait(timeout=5)
        print("游戏进程已停止")
    else:
        exit_code = process.poll()
        print(f"游戏进程已退出，退出码: {exit_code}")

print("=======================================")
print("游戏运行结束")
print("详细输出已保存到 game_log.txt")
print("=======================================")
