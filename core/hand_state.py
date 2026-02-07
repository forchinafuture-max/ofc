"""
手牌状态管理类
负责集中管理玩家手牌，确保区域长度不变式
"""

class HandState:
    """
    手牌状态类，负责管理玩家的手牌状态
    确保top/middle/bottom的长度不变式
    """
    
    def __init__(self):
        """
        初始化手牌状态
        """
        self._hand = {
            'temp': [],
            'top': [],
            'middle': [],
            'bottom': []
        }
    
    def __getitem__(self, key):
        """
        支持通过索引访问手牌区域
        """
        return self._hand.get(key, [])
    
    def __setitem__(self, key, value):
        """
        支持通过索引设置手牌区域
        确保区域长度不变式
        """
        if key == 'top':
            if len(value) > 3:
                raise ValueError("顶部区域最多只能有3张牌")
        elif key == 'middle' or key == 'bottom':
            if len(value) > 5:
                raise ValueError(f"{key}区域最多只能有5张牌")
        self._hand[key] = value
    
    def __contains__(self, key):
        """
        支持in操作符检查区域是否存在
        """
        return key in self._hand
    
    def get(self, key, default=None):
        """
        支持字典风格的get方法
        """
        return self._hand.get(key, default)
    
    def copy(self):
        """
        创建手牌状态的深拷贝
        """
        import copy
        new_hand_state = HandState()
        new_hand_state._hand = copy.deepcopy(self._hand)
        return new_hand_state
    
    def clear(self):
        """
        清空所有手牌区域
        """
        for key in self._hand:
            self._hand[key] = []
    
    def is_valid(self):
        """
        检查手牌状态是否有效
        
        Returns:
            bool: 是否有效
        """
        if len(self._hand['top']) > 3:
            return False
        if len(self._hand['middle']) > 5:
            return False
        if len(self._hand['bottom']) > 5:
            return False
        return True
