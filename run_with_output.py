#!/usr/bin/env python3
"""
运行游戏并捕获完整的输出信息
"""

import subprocess
import sys

# 运行游戏并捕获输出
result = subprocess.run(
    [sys.executable, 'main.py'],
    cwd='.',
    capture_output=True,
    text=True,
    timeout=30  # 设置30秒超时，避免游戏无限等待
)

# 打印输出
print("游戏输出:")
print("=" * 80)
print(result.stdout)
print("=" * 80)

# 打印错误
if result.stderr:
    print("错误信息:")
    print("=" * 80)
    print(result.stderr)
    print("=" * 80)

print(f"退出码: {result.returncode}")
