"""
配置加载器
负责读取和解析YAML配置文件
"""

import yaml
import os

class ConfigLoader:
    """
    配置加载器类
    """
    
    def __init__(self, config_path=None):
        """
        初始化配置加载器
        
        Args:
            config_path: 配置文件路径
        """
        if config_path is None:
            # 默认配置文件路径
            config_path = os.path.join(os.path.dirname(__file__), 'game_rules.yaml')
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self):
        """
        加载配置文件
        
        Returns:
            配置字典
        """
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def get(self, key, default=None):
        """
        获取配置值
        
        Args:
            key: 配置键
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_region_length(self, region):
        """
        获取区域长度限制
        
        Args:
            region: 区域名称
            
        Returns:
            区域长度
        """
        return self.get(f'region_lengths.{region}', 0)
    
    def get_scoring(self, key):
        """
        获取计分规则
        
        Args:
            key: 计分规则键
            
        Returns:
            计分规则值
        """
        return self.get(f'scoring.{key}', 0)
    
    def get_top_pair_score(self, rank):
        """
        获取头道对子牌型分
        
        Args:
            rank: 牌面值
            
        Returns:
            牌型分
        """
        # 先获取整个top_pair_scores字典
        top_pair_scores = self.get('top_pair_scores', {})
        # 然后从字典中获取对应的值
        # 尝试直接使用整数键，如果不存在则尝试字符串键
        if rank in top_pair_scores:
            return top_pair_scores[rank]
        elif str(rank) in top_pair_scores:
            return top_pair_scores[str(rank)]
        else:
            return 0
    
    def get_top_trips_score(self, rank):
        """
        获取头道三条牌型分
        
        Args:
            rank: 牌面值
            
        Returns:
            牌型分
        """
        # 先获取整个top_trips_scores字典
        top_trips_scores = self.get('top_trips_scores', {})
        # 然后从字典中获取对应的值
        # 尝试直接使用整数键，如果不存在则尝试字符串键
        if rank in top_trips_scores:
            return top_trips_scores[rank]
        elif str(rank) in top_trips_scores:
            return top_trips_scores[str(rank)]
        else:
            return 0
    
    def get_hand_score(self, region, hand_type):
        """
        获取手牌牌型分
        
        Args:
            region: 区域名称
            hand_type: 牌型
            
        Returns:
            牌型分
        """
        return self.get(f'{region}_hand_scores.{hand_type}', 0)
    
    def get_fantasy_mode_config(self, key):
        """
        获取范特西模式配置
        
        Args:
            key: 配置键
            
        Returns:
            配置值
        """
        return self.get(f'fantasy_mode.{key}', {})
    
    def get_mcts_config(self, key):
        """
        获取MCTS配置
        
        Args:
            key: 配置键
            
        Returns:
            配置值
        """
        return self.get(f'mcts.{key}', 0)
    
    def get_reward_config(self, key):
        """
        获取奖励函数配置
        
        Args:
            key: 配置键
            
        Returns:
            配置值
        """
        return self.get(f'reward.{key}', 0)

# 全局配置实例
config_loader = ConfigLoader()
