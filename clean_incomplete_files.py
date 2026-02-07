#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理未摆满牌的AI对弈文件
"""

import os
import json

class CleanIncompleteFiles:
    def __init__(self):
        self.records_dir = "game_records"
        self.deleted_files = []
    
    def is_hand_complete(self, hand):
        """
        检查手牌是否完整
        """
        top = len(hand.get('top', []))
        middle = len(hand.get('middle', []))
        bottom = len(hand.get('bottom', []))
        
        # 检查是否每个区域都达到了最大牌数
        return top == 3 and middle == 5 and bottom == 5
    
    def check_file(self, file_path):
        """
        检查文件是否包含完整的手牌
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 检查每个玩家的手牌
            for player in data.get('players', []):
                hand = player.get('hand', {})
                if not self.is_hand_complete(hand):
                    return False
            
            return True
        except Exception as e:
            print(f"检查文件 {file_path} 时出错: {e}")
            return False
    
    def clean_files(self):
        """
        清理未完成的文件
        """
        if not os.path.exists(self.records_dir):
            print(f"目录 {self.records_dir} 不存在")
            return
        
        # 遍历所有JSON文件
        for filename in os.listdir(self.records_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(self.records_dir, filename)
                
                # 检查文件是否完整
                if not self.check_file(file_path):
                    try:
                        os.remove(file_path)
                        self.deleted_files.append(filename)
                        print(f"已删除未完成的文件: {filename}")
                    except Exception as e:
                        print(f"删除文件 {filename} 失败: {e}")
        
        # 检查优先级目录
        priority_dir = os.path.join(self.records_dir, "priority")
        if os.path.exists(priority_dir):
            for filename in os.listdir(priority_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(priority_dir, filename)
                    
                    # 检查文件是否完整
                    if not self.check_file(file_path):
                        try:
                            os.remove(file_path)
                            self.deleted_files.append(f"priority/{filename}")
                            print(f"已删除优先级目录中未完成的文件: {filename}")
                        except Exception as e:
                            print(f"删除优先级目录中的文件 {filename} 失败: {e}")
    
    def run(self):
        """
        运行清理过程
        """
        print("开始清理未摆满牌的AI对弈文件...")
        print("=" * 80)
        
        self.clean_files()
        
        print("=" * 80)
        print(f"清理完成！")
        print(f"共删除了 {len(self.deleted_files)} 个未完成的文件")
        
        if self.deleted_files:
            print("\n删除的文件列表:")
            for file in self.deleted_files:
                print(f"- {file}")
        else:
            print("\n没有发现未完成的文件，所有文件都已摆满牌！")

if __name__ == "__main__":
    cleaner = CleanIncompleteFiles()
    cleaner.run()
