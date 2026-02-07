#!/usr/bin/env python3
"""
日志记录模块
记录每轮AI决策、手牌状态、得分
可用于策略优化和bug定位
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from game.deck import Card
from game.player import Player
from game.ofc_game import OFCGame

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ofc_game.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('OFCGameLogger')

class GameLogger:
    """游戏日志记录器"""
    
    def __init__(self, log_dir: str = 'logs'):
        """初始化日志记录器
        
        Args:
            log_dir: 日志文件保存目录
        """
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.game_logs = []
        self.current_game_id = None
    
    def start_game(self, game: OFCGame):
        """开始记录新游戏
        
        Args:
            game: OFCGame对象
        """
        self.current_game_id = f"game_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        game_log = {
            'game_id': self.current_game_id,
            'start_time': datetime.now().isoformat(),
            'players': [player.name for player in game.players],
            'rounds': []
        }
        self.game_logs.append(game_log)
        logger.info(f"开始新游戏: {self.current_game_id}")
    
    def record_round(self, game: OFCGame, round_num: int, actions: Dict[str, Dict]):
        """记录每轮游戏
        
        Args:
            game: OFCGame对象
            round_num: 轮次
            actions: 玩家动作记录
        """
        round_log = {
            'round_num': round_num,
            'timestamp': datetime.now().isoformat(),
            'actions': actions,
            'player_states': []
        }
        
        # 记录每个玩家的状态
        for player in game.players:
            player_state = {
                'player_name': player.name,
                'hand_state': {
                    'top': self._cards_to_dict(player.hand['top']),
                    'middle': self._cards_to_dict(player.hand['middle']),
                    'bottom': self._cards_to_dict(player.hand['bottom']),
                    'temp': self._cards_to_dict(player.hand['temp'])
                },
                'score': game.calculate_total_score(player),
                'is_busted': game.check_busted(player),
                'fantasy_mode': getattr(player, 'fantasy_mode', False)
            }
            round_log['player_states'].append(player_state)
        
        # 找到当前游戏日志并添加轮次记录
        for game_log in self.game_logs:
            if game_log['game_id'] == self.current_game_id:
                game_log['rounds'].append(round_log)
                break
        
        logger.info(f"记录轮次 {round_num} 的游戏状态")
    
    def record_ai_decision(self, player_name: str, decision: Dict, hand_state: Dict, score: int):
        """记录AI决策
        
        Args:
            player_name: 玩家名称
            decision: 决策内容
            hand_state: 手牌状态
            score: 得分
        """
        ai_log = {
            'timestamp': datetime.now().isoformat(),
            'player_name': player_name,
            'decision': decision,
            'hand_state': hand_state,
            'score': score
        }
        
        # 找到当前游戏日志并添加AI决策记录
        for game_log in self.game_logs:
            if game_log['game_id'] == self.current_game_id:
                if 'ai_decisions' not in game_log:
                    game_log['ai_decisions'] = []
                game_log['ai_decisions'].append(ai_log)
                break
        
        logger.info(f"记录AI决策: {player_name} - {decision}")
    
    def end_game(self, game: OFCGame, winner: Optional[Player]):
        """结束游戏并记录结果
        
        Args:
            game: OFCGame对象
            winner: 获胜玩家
        """
        # 找到当前游戏日志并添加结束信息
        for game_log in self.game_logs:
            if game_log['game_id'] == self.current_game_id:
                game_log['end_time'] = datetime.now().isoformat()
                game_log['winner'] = winner.name if winner else None
                
                # 记录最终得分
                final_scores = {}
                for player in game.players:
                    final_scores[player.name] = game.calculate_total_score(player)
                game_log['final_scores'] = final_scores
                
                # 保存日志到文件
                self._save_game_log(game_log)
                break
        
        logger.info(f"结束游戏: {self.current_game_id}, 获胜者: {winner.name if winner else '无'}")
    
    def _cards_to_dict(self, cards: List[Card]) -> List[Dict]:
        """将卡牌列表转换为字典列表
        
        Args:
            cards: Card对象列表
        
        Returns:
            字典列表
        """
        return [{'value': card.value, 'suit': card.suit} for card in cards]
    
    def _save_game_log(self, game_log: Dict):
        """保存游戏日志到文件
        
        Args:
            game_log: 游戏日志字典
        """
        log_file = os.path.join(self.log_dir, f"{game_log['game_id']}.json")
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(game_log, f, ensure_ascii=False, indent=2)
        logger.info(f"保存游戏日志到文件: {log_file}")
    
    def get_game_logs(self) -> List[Dict]:
        """获取所有游戏日志
        
        Returns:
            游戏日志列表
        """
        return self.game_logs
    
    def analyze_game(self, game_id: str) -> Dict:
        """分析游戏日志
        
        Args:
            game_id: 游戏ID
        
        Returns:
            游戏分析结果
        """
        # 查找游戏日志
        game_log = None
        for log in self.game_logs:
            if log['game_id'] == game_id:
                game_log = log
                break
        
        if not game_log:
            # 尝试从文件加载
            log_file = os.path.join(self.log_dir, f"{game_id}.json")
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    game_log = json.load(f)
            else:
                logger.error(f"游戏日志不存在: {game_id}")
                return {}
        
        # 分析游戏数据
        analysis = {
            'game_id': game_id,
            'total_rounds': len(game_log.get('rounds', [])),
            'player_performance': {},
            'ai_decisions': game_log.get('ai_decisions', []),
            'final_scores': game_log.get('final_scores', {})
        }
        
        # 分析每个玩家的表现
        for player_name in game_log.get('players', []):
            player_rounds = []
            for round_log in game_log.get('rounds', []):
                for player_state in round_log.get('player_states', []):
                    if player_state['player_name'] == player_name:
                        player_rounds.append({
                            'round': round_log['round_num'],
                            'score': player_state['score'],
                            'is_busted': player_state['is_busted']
                        })
                        break
            
            analysis['player_performance'][player_name] = {
                'rounds': player_rounds,
                'final_score': game_log.get('final_scores', {}).get(player_name, 0)
            }
        
        return analysis

# 全局日志记录器实例
game_logger = GameLogger()

# 辅助函数
def log_ai_decision(player: Player, decision: Dict, game: OFCGame):
    """记录AI决策的辅助函数
    
    Args:
        player: 玩家对象
        decision: 决策内容
        game: 游戏对象
    """
    hand_state = {
        'top': game_logger._cards_to_dict(player.hand['top']),
        'middle': game_logger._cards_to_dict(player.hand['middle']),
        'bottom': game_logger._cards_to_dict(player.hand['bottom']),
        'temp': game_logger._cards_to_dict(player.hand['temp'])
    }
    score = game.calculate_total_score(player)
    game_logger.record_ai_decision(player.name, decision, hand_state, score)
