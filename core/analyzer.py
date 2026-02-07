#!/usr/bin/env python3
"""
统计分析模块
用于策略优化和bug定位
"""

import os
import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from typing import List, Dict, Optional

class GameAnalyzer:
    """游戏分析器"""
    
    def __init__(self, log_dir: str = 'logs'):
        """初始化游戏分析器
        
        Args:
            log_dir: 日志文件保存目录
        """
        self.log_dir = log_dir
        self.analysis_results = {}
    
    def load_game_logs(self) -> List[Dict]:
        """加载所有游戏日志
        
        Returns:
            游戏日志列表
        """
        game_logs = []
        
        # 遍历日志目录
        if not os.path.exists(self.log_dir):
            return game_logs
        
        for filename in os.listdir(self.log_dir):
            if filename.endswith('.json'):
                log_file = os.path.join(self.log_dir, filename)
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        game_log = json.load(f)
                        game_logs.append(game_log)
                except Exception as e:
                    print(f"加载日志文件 {filename} 失败: {e}")
        
        return game_logs
    
    def analyze_ai_decisions(self, game_logs: List[Dict]) -> Dict:
        """分析AI决策模式
        
        Args:
            game_logs: 游戏日志列表
        
        Returns:
            AI决策分析结果
        """
        analysis = {
            'total_decisions': 0,
            'player_decisions': {},
            'area_distribution': {
                'top': 0,
                'middle': 0,
                'bottom': 0
            },
            'decision_scores': []
        }
        
        for game_log in game_logs:
            ai_decisions = game_log.get('ai_decisions', [])
            analysis['total_decisions'] += len(ai_decisions)
            
            for decision in ai_decisions:
                player_name = decision.get('player_name', 'Unknown')
                area_name = decision.get('decision', {}).get('area_name', 'Unknown')
                score = decision.get('decision', {}).get('score', 0)
                
                # 按玩家统计决策
                if player_name not in analysis['player_decisions']:
                    analysis['player_decisions'][player_name] = {
                        'total_decisions': 0,
                        'area_distribution': {
                            'top': 0,
                            'middle': 0,
                            'bottom': 0
                        },
                        'decision_scores': []
                    }
                
                analysis['player_decisions'][player_name]['total_decisions'] += 1
                if area_name in analysis['player_decisions'][player_name]['area_distribution']:
                    analysis['player_decisions'][player_name]['area_distribution'][area_name] += 1
                analysis['player_decisions'][player_name]['decision_scores'].append(score)
                
                # 总体区域分布
                if area_name in analysis['area_distribution']:
                    analysis['area_distribution'][area_name] += 1
                analysis['decision_scores'].append(score)
        
        # 计算统计信息
        if analysis['decision_scores']:
            analysis['average_score'] = np.mean(analysis['decision_scores'])
            analysis['median_score'] = np.median(analysis['decision_scores'])
            analysis['score_std'] = np.std(analysis['decision_scores'])
        
        for player_name, player_analysis in analysis['player_decisions'].items():
            if player_analysis['decision_scores']:
                player_analysis['average_score'] = np.mean(player_analysis['decision_scores'])
                player_analysis['median_score'] = np.median(player_analysis['decision_scores'])
                player_analysis['score_std'] = np.std(player_analysis['decision_scores'])
        
        return analysis
    
    def analyze_hand_states(self, game_logs: List[Dict]) -> Dict:
        """分析手牌状态分布
        
        Args:
            game_logs: 游戏日志列表
        
        Returns:
            手牌状态分析结果
        """
        analysis = {
            'total_states': 0,
            'area_card_counts': {
                'top': [],
                'middle': [],
                'bottom': [],
                'temp': []
            },
            'bust_count': 0,
            'fantasy_mode_count': 0
        }
        
        for game_log in game_logs:
            rounds = game_log.get('rounds', [])
            
            for round_log in rounds:
                player_states = round_log.get('player_states', [])
                analysis['total_states'] += len(player_states)
                
                for player_state in player_states:
                    hand_state = player_state.get('hand_state', {})
                    
                    # 统计各区域牌数
                    for area, cards in hand_state.items():
                        if area in analysis['area_card_counts']:
                            analysis['area_card_counts'][area].append(len(cards))
                    
                    # 统计爆牌情况
                    if player_state.get('is_busted', False):
                        analysis['bust_count'] += 1
                    
                    # 统计幻想模式情况
                    if player_state.get('fantasy_mode', False):
                        analysis['fantasy_mode_count'] += 1
        
        # 计算统计信息
        for area, counts in analysis['area_card_counts'].items():
            if counts:
                analysis['area_card_counts'][area] = {
                    'average': np.mean(counts),
                    'median': np.median(counts),
                    'std': np.std(counts),
                    'min': np.min(counts),
                    'max': np.max(counts)
                }
        
        # 计算爆牌率和幻想模式率
        if analysis['total_states'] > 0:
            analysis['bust_rate'] = analysis['bust_count'] / analysis['total_states']
            analysis['fantasy_mode_rate'] = analysis['fantasy_mode_count'] / analysis['total_states']
        
        return analysis
    
    def analyze_score_trends(self, game_logs: List[Dict]) -> Dict:
        """分析得分变化趋势
        
        Args:
            game_logs: 游戏日志列表
        
        Returns:
            得分趋势分析结果
        """
        analysis = {
            'total_games': len(game_logs),
            'player_score_trends': {},
            'final_scores': [],
            'average_final_score': 0,
            'score_distribution': []
        }
        
        for game_log in game_logs:
            players = game_log.get('players', [])
            rounds = game_log.get('rounds', [])
            final_scores = game_log.get('final_scores', {})
            
            # 统计最终得分
            for player_name, score in final_scores.items():
                analysis['final_scores'].append(score)
                analysis['score_distribution'].append(score)
                
                # 统计得分趋势
                if player_name not in analysis['player_score_trends']:
                    analysis['player_score_trends'][player_name] = []
                
                # 提取每轮得分
                round_scores = []
                for round_log in rounds:
                    for player_state in round_log.get('player_states', []):
                        if player_state.get('player_name') == player_name:
                            round_scores.append(player_state.get('score', 0))
                            break
                
                analysis['player_score_trends'][player_name].append(round_scores)
        
        # 计算统计信息
        if analysis['final_scores']:
            analysis['average_final_score'] = np.mean(analysis['final_scores'])
            analysis['median_final_score'] = np.median(analysis['final_scores'])
            analysis['final_score_std'] = np.std(analysis['final_scores'])
        
        return analysis
    
    def generate_statistics_report(self, output_dir: str = 'analysis') -> str:
        """生成统计报告
        
        Args:
            output_dir: 报告输出目录
        
        Returns:
            报告文件路径
        """
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 加载游戏日志
        game_logs = self.load_game_logs()
        if not game_logs:
            print("没有找到游戏日志文件")
            return None
        
        # 分析数据
        ai_analysis = self.analyze_ai_decisions(game_logs)
        hand_analysis = self.analyze_hand_states(game_logs)
        score_analysis = self.analyze_score_trends(game_logs)
        
        # 生成报告
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_games': len(game_logs),
            'ai_decisions': ai_analysis,
            'hand_states': hand_analysis,
            'score_trends': score_analysis
        }
        
        # 保存报告到文件
        report_file = os.path.join(output_dir, f"statistics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # 生成可视化图表
        self.generate_visualizations(report, output_dir)
        
        return report_file
    
    def generate_visualizations(self, report: Dict, output_dir: str):
        """生成可视化图表
        
        Args:
            report: 分析报告
            output_dir: 图表输出目录
        """
        # 生成AI决策区域分布图
        self._plot_area_distribution(report, output_dir)
        
        # 生成得分趋势图
        self._plot_score_trends(report, output_dir)
        
        # 生成爆牌率饼图
        self._plot_bust_rate(report, output_dir)
    
    def _plot_area_distribution(self, report: Dict, output_dir: str):
        """生成AI决策区域分布图
        
        Args:
            report: 分析报告
            output_dir: 图表输出目录
        """
        try:
            area_distribution = report.get('ai_decisions', {}).get('area_distribution', {})
            
            if not area_distribution:
                return
            
            labels = list(area_distribution.keys())
            sizes = list(area_distribution.values())
            colors = ['#ff9999', '#66b3ff', '#99ff99']
            
            plt.figure(figsize=(10, 6))
            plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')
            plt.title('AI决策区域分布')
            
            output_file = os.path.join(output_dir, 'area_distribution.png')
            plt.savefig(output_file)
            plt.close()
        except Exception as e:
            print(f"生成区域分布图失败: {e}")
    
    def _plot_score_trends(self, report: Dict, output_dir: str):
        """生成得分趋势图
        
        Args:
            report: 分析报告
            output_dir: 图表输出目录
        """
        try:
            player_trends = report.get('score_trends', {}).get('player_score_trends', {})
            
            if not player_trends:
                return
            
            plt.figure(figsize=(12, 8))
            
            for player_name, trends in player_trends.items():
                if trends:
                    # 取第一个游戏的得分趋势作为示例
                    trend = trends[0]
                    rounds = list(range(1, len(trend) + 1))
                    plt.plot(rounds, trend, label=player_name)
            
            plt.xlabel('轮次')
            plt.ylabel('得分')
            plt.title('得分变化趋势')
            plt.legend()
            plt.grid(True)
            
            output_file = os.path.join(output_dir, 'score_trends.png')
            plt.savefig(output_file)
            plt.close()
        except Exception as e:
            print(f"生成得分趋势图失败: {e}")
    
    def _plot_bust_rate(self, report: Dict, output_dir: str):
        """生成爆牌率饼图
        
        Args:
            report: 分析报告
            output_dir: 图表输出目录
        """
        try:
            bust_count = report.get('hand_states', {}).get('bust_count', 0)
            total_states = report.get('hand_states', {}).get('total_states', 1)
            
            sizes = [bust_count, total_states - bust_count]
            labels = ['爆牌', '非爆牌']
            colors = ['#ff9999', '#99ff99']
            
            plt.figure(figsize=(10, 6))
            plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')
            plt.title('爆牌率统计')
            
            output_file = os.path.join(output_dir, 'bust_rate.png')
            plt.savefig(output_file)
            plt.close()
        except Exception as e:
            print(f"生成爆牌率饼图失败: {e}")
    
    def find_bugs(self, game_logs: List[Dict]) -> List[Dict]:
        """查找潜在的bug
        
        Args:
            game_logs: 游戏日志列表
        
        Returns:
            潜在bug列表
        """
        bugs = []
        
        for game_log in game_logs:
            game_id = game_log.get('game_id', 'Unknown')
            rounds = game_log.get('rounds', [])
            
            for round_idx, round_log in enumerate(rounds):
                round_num = round_log.get('round_num', round_idx + 1)
                player_states = round_log.get('player_states', [])
                
                for player_state in player_states:
                    player_name = player_state.get('player_name', 'Unknown')
                    hand_state = player_state.get('hand_state', {})
                    
                    # 检查区域牌数是否合法
                    for area, cards in hand_state.items():
                        if area == 'top' and len(cards) > 3:
                            bugs.append({
                                'game_id': game_id,
                                'round': round_num,
                                'player': player_name,
                                'type': '区域牌数错误',
                                'description': f"顶部区域牌数超过限制: {len(cards)} > 3"
                            })
                        elif area in ['middle', 'bottom'] and len(cards) > 5:
                            bugs.append({
                                'game_id': game_id,
                                'round': round_num,
                                'player': player_name,
                                'type': '区域牌数错误',
                                'description': f"{area}区域牌数超过限制: {len(cards)} > 5"
                            })
                    
                    # 检查得分是否异常
                    score = player_state.get('score', 0)
                    if score < 0:
                        bugs.append({
                            'game_id': game_id,
                            'round': round_num,
                            'player': player_name,
                            'type': '得分异常',
                            'description': f"得分小于0: {score}"
                        })
        
        return bugs

# 全局分析器实例
game_analyzer = GameAnalyzer()

# 辅助函数
def generate_statistics_report():
    """生成统计报告的辅助函数
    
    Returns:
        报告文件路径
    """
    return game_analyzer.generate_statistics_report()

def find_bugs():
    """查找潜在bug的辅助函数
    
    Returns:
        潜在bug列表
    """
    game_logs = game_analyzer.load_game_logs()
    return game_analyzer.find_bugs(game_logs)
