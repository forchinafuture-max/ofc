#!/usr/bin/env python3
"""
运行游戏并将所有输出重定向到文件
"""

import subprocess
import time

# 运行start_game_now.py并将输出重定向到文件
print("=======================================")
print("          启动OFC扑克游戏          ")
print("=======================================")
print("正在启动游戏...")
print("所有输出将保存到 game_final_output.txt")
print("=======================================")

# 打开日志文件
with open('game_final_output.txt', 'w', encoding='utf-8') as f:
    # 启动游戏进程
    process = subprocess.Popen(
        ['python', 'start_game_now.py'],
        stdout=f,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # 显示启动信息
    print(f"游戏进程已启动，PID: {process.pid}")
    print("正在等待游戏输出...")
    
    # 等待进程运行
    try:
        # 等待进程结束
        while process.poll() is None:
            time.sleep(1)
            print(f"游戏运行中... (PID: {process.pid})")
        
        exit_code = process.poll()
        print(f"游戏进程已退出，退出码: {exit_code}")
    except KeyboardInterrupt:
        print("\n正在停止游戏进程...")
        process.terminate()
        process.wait(timeout=5)
        print("游戏进程已停止")
    except Exception as e:
        print(f"发生错误: {e}")
        process.terminate()
        process.wait(timeout=5)

print("=======================================")
print("游戏运行结束")
print("详细输出已保存到 game_final_output.txt")
print("=======================================")

# 读取并显示日志文件
try:
    with open('game_final_output.txt', 'r', encoding='gbk') as f:
        content = f.read()
    
    print("\n游戏输出:")
    print("=======================================")
    print(content)
    print("=======================================")
except Exception as e:
    print(f"读取日志文件失败: {e}")
