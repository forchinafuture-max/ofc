#!/usr/bin/env python3
"""
查看日志文件内容，处理编码问题
"""

import sys

def read_log_file(file_path):
    """读取日志文件，处理编码问题"""
    encodings = ['utf-8', 'gbk', 'latin-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            print(f"✅ 使用编码 {encoding} 成功读取文件")
            return content
        except Exception as e:
            print(f"❌ 使用编码 {encoding} 读取失败: {e}")
    
    return None

if __name__ == "__main__":
    print("=======================================")
    print("          查看游戏日志          ")
    print("=======================================")
    
    # 读取main_output.txt文件
    print("\n读取 main_output.txt 文件:")
    content = read_log_file('main_output.txt')
    
    if content:
        print("\n文件内容预览 (前100行):")
        print("=======================================")
        lines = content.split('\n')
        for i, line in enumerate(lines[:100], 1):
            print(f"{i:3d}: {line}")
        if len(lines) > 100:
            print(f"... 还有 {len(lines) - 100} 行未显示")
        print("=======================================")
    else:
        print("❌ 无法读取日志文件")
