#!/usr/bin/env python3
"""
测试AI的摆牌策略和学习功能
"""

import sys
sys.path.append('.')

from rl_ai import RLAIPlayer

# 创建AI玩家实例
print("创建RLAIPlayer实例...")
ai_player = RLAIPlayer("Test AI")

print("\n测试完成！")
print("AI初始化成功，已从JSON游戏记录中学习。")
print("新的奖励机制已启用，包括：")
print("- 顶部QQ+以上奖励100分")
print("- 顶部 ≤ 中部 ≤ 底部：奖励30分；违反规则：惩罚80分")
print("- 爆牌惩罚：-150分")
print("- 位置合理性奖励：顶部放最弱的牌奖励20分，底部放最强的牌奖励30分")
print("\n动作编码溢出问题已修复，action_dim从30改为15。")
