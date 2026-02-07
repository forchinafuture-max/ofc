#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
筛选game_records目录中玩家a得分超过7分的json文件，并标记为优先级高的文件
"""

import os
import json
import glob
import shutil

if __name__ == "__main__":
    print("正在筛选玩家a得分超过7分的json文件...")
    print("=" * 60)
    
    # 定义游戏记录目录
    game_records_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "game_records")
    # 定义优先级高的文件目录
    priority_dir = os.path.join(game_records_dir, "priority")
    
    # 检查目录是否存在
    if not os.path.exists(game_records_dir):
        print(f"错误：目录 {game_records_dir} 不存在")
        exit(1)
    
    # 创建优先级目录
    if not os.path.exists(priority_dir):
        os.makedirs(priority_dir)
        print(f"创建优先级目录: {priority_dir}")
    else:
        # 清空优先级目录
        for file in os.listdir(priority_dir):
            file_path = os.path.join(priority_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"清空优先级目录: {priority_dir}")
    
    # 查找所有json文件
    json_files = glob.glob(os.path.join(game_records_dir, "*.json"))
    print(f"找到 {len(json_files)} 个json文件")
    print("=" * 60)
    
    # 筛选玩家a得分超过7分的文件
    high_score_files = []
    total_score = 0
    copied_files = 0
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # 检查是否处于Fantasy Land模式
                is_fl_mode = False
                if 'fantasy_mode' in data and data['fantasy_mode']:
                    is_fl_mode = True
                elif 'game_details' in data and 'fantasy_mode' in data['game_details'] and data['game_details']['fantasy_mode']:
                    is_fl_mode = True
                elif 'players' in data:
                    for player in data['players']:
                        if 'fantasy_mode' in player and player['fantasy_mode']:
                            is_fl_mode = True
                            break
                
                # 跳过FL阶段的文件
                if is_fl_mode:
                    continue
                
                # 检查玩家a的得分
                if 'players' in data:
                    for player in data['players']:
                        if 'name' in player and player['name'] == '玩家a' and 'total_score' in player:
                            score = player['total_score']
                            if score > 7:
                                filename = os.path.basename(json_file)
                                high_score_files.append((filename, score))
                                total_score += score
                                
                                # 复制到优先级目录
                                dest_path = os.path.join(priority_dir, filename)
                                shutil.copy2(json_file, dest_path)
                                copied_files += 1
                                break
        except Exception as e:
            print(f"读取文件 {os.path.basename(json_file)} 失败: {e}")
    
    # 按得分排序
    high_score_files.sort(key=lambda x: x[1], reverse=True)
    
    # 输出结果
    print("\n玩家a得分超过7分的文件：")
    print("=" * 60)
    print(f"共找到 {len(high_score_files)} 个文件")
    print(f"已复制 {copied_files} 个文件到优先级目录")
    print("=" * 60)
    
    if high_score_files:
        for filename, score in high_score_files:
            print(f"{filename}: {score}分")
        
        avg_score = total_score / len(high_score_files)
        print("=" * 60)
        print(f"平均得分: {avg_score:.2f}分")
        print(f"最高得分: {high_score_files[0][1]}分")
        print(f"最低得分: {high_score_files[-1][1]}分")
    else:
        print("没有找到玩家a得分超过7分的文件")
    
    print("=" * 60)
    print("筛选完成！")
