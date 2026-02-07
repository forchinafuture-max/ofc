#!/usr/bin/env python3
"""
运行main.py并将所有输出重定向到日志文件
"""

import subprocess
import time

# 运行main.py并将输出重定向到文件
print("=======================================")
print("          运行OFC扑克游戏          ")
print("=======================================")
print("正在启动游戏...")
print("所有输出将保存到 main_output.txt")
print("=======================================")

# 打开日志文件
with open('main_output.txt', 'w', encoding='utf-8') as f:
    # 启动main.py进程
    process = subprocess.Popen(
        ['python', 'main.py'],
        stdout=f,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # 显示启动信息
    print(f"游戏进程已启动，PID: {process.pid}")
    print("正在等待游戏输出...")
    
    # 等待进程运行一段时间
    try:
        # 等待10秒，让游戏有足够的时间初始化
        time.sleep(10)
        
        # 检查进程状态
        if process.poll() is None:
            print(f"游戏仍在运行中 (PID: {process.pid})")
            print("正在停止游戏进程以查看输出...")
            process.terminate()
            process.wait(timeout=5)
            print("游戏进程已停止")
        else:
            exit_code = process.poll()
            print(f"游戏进程已退出，退出码: {exit_code}")
    except Exception as e:
        print(f"发生错误: {e}")
        process.terminate()
        process.wait(timeout=5)

print("=======================================")
print("游戏运行完成")
print("详细输出已保存到 main_output.txt")
print("=======================================")

# 读取并显示日志文件的前100行
print("\n游戏输出预览 (前50行):")
print("=======================================")
try:
    with open('main_output.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines[:50], 1):
            print(f"{i:3d}: {line.rstrip()}")
        if len(lines) > 50:
            print(f"... 还有 {len(lines) - 50} 行未显示")
except Exception as e:
    print(f"读取日志文件失败: {e}")

print("=======================================")
