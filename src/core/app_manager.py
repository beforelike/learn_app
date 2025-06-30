#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用核心管理器
负责数据管理、学习进度跟踪、统计分析等核心功能
"""

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ..data.learning_data import LearningData
from ..utils.logger import get_logger

class AppManager:
    """应用核心管理器"""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.learning_data = LearningData()
        
        # 学习进度数据
        self.progress = {
            'current_day': 1,
            'completed_tasks': [],
            'task_notes': {},
            'statistics': {
                'total_study_time': 0,
                'completion_rate': 0.0,
                'current_streak': 0
            }
        }
        
        # 初始化数据
        self._initialize_data()
        
        self.logger.info("应用管理器初始化完成")
    
    def _initialize_data(self):
        """初始化数据"""
        try:
            # 加载学习进度
            self.load_progress()
            
        except Exception as e:
            self.logger.error(f"数据初始化失败: {e}")
            # 使用默认数据继续运行
            pass
    
    def load_progress(self):
        """加载学习进度"""
        try:
            # 尝试从文件加载进度数据
            import os
            import json
            progress_file = 'data/progress.json'
            
            if os.path.exists(progress_file):
                with open(progress_file, 'r', encoding='utf-8') as f:
                    saved_progress = json.load(f)
                    self.progress.update(saved_progress)
                    self.logger.info("学习进度加载成功")
            else:
                self.logger.info("未找到进度文件，使用默认进度")
                
        except Exception as e:
            self.logger.error(f"加载学习进度失败: {e}")
            # 使用默认进度继续
    
    def save_progress(self):
        """保存学习进度"""
        try:
            import os
            import json
            
            # 确保数据目录存在
            os.makedirs('data', exist_ok=True)
            
            # 保存进度到文件
            progress_file = 'data/progress.json'
            with open(progress_file, 'w', encoding='utf-8') as f:
                json.dump(self.progress, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"学习进度已保存: 第{self.progress['current_day']}天")
        except Exception as e:
            self.logger.error(f"保存学习进度失败: {e}")
            raise
    
    def get_current_task(self) -> Optional[Dict]:
        """获取当前学习任务"""
        try:
            return self.learning_data.get_task_by_day(self.progress['current_day'])
        except Exception as e:
            self.logger.error(f"获取当前任务失败: {e}")
            return None
    
    def complete_current_task(self) -> bool:
        """完成当前任务"""
        try:
            current_task = self.get_current_task()
            if not current_task:
                return False
            
            # 标记任务为完成
            task_id = f"day_{self.progress['current_day']}"
            if task_id not in self.progress['completed_tasks']:
                self.progress['completed_tasks'].append(task_id)
                
                # 更新统计信息
                self._update_statistics()
                
                # 保存进度
                self.save_progress()
                
                self.logger.info(f"任务完成: {current_task.get('title', '未知任务')}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"完成任务失败: {e}")
            return False
    
    def _update_statistics(self):
        """更新统计信息"""
        total_tasks = self.learning_data.get_total_days()
        completed_count = len(self.progress['completed_tasks'])
        
        self.progress['statistics']['completion_rate'] = completed_count / total_tasks if total_tasks > 0 else 0.0
        
        # 更新连续学习天数（简化实现）
        self.progress['statistics']['current_streak'] = completed_count
    
    def get_learning_stats(self) -> Dict:
        """获取学习统计信息"""
        try:
            total_days = self.learning_data.get_total_days()
            completed_count = len(self.progress['completed_tasks'])
            completion_rate = self.progress['statistics']['completion_rate'] * 100
            
            # 计算当前阶段和周
            current_day = self.progress['current_day']
            current_week = ((current_day - 1) // 7) + 1
            current_stage = ((current_day - 1) // 35) + 1  # 每5周一个阶段
            
            return {
                'total_days': total_days,
                'completed_days': completed_count,
                'completion_rate': completion_rate,
                'current_day': current_day,
                'current_stage': current_stage,
                'current_week': current_week,
                'current_streak': self.progress['statistics']['current_streak'],
                'total_study_time': self.progress['statistics']['total_study_time']
            }
        except Exception as e:
            self.logger.error(f"获取学习统计失败: {e}")
            return {}
    
    def get_task_history(self, limit: int = 10) -> List[Dict]:
        """获取任务历史记录"""
        try:
            # 获取已完成的任务
            completed_tasks = []
            for task_id in self.progress['completed_tasks'][-limit:]:
                day = int(task_id.split('_')[1])
                task = self.learning_data.get_task_by_day(day)
                if task:
                    task['completed'] = True
                    task['day'] = day
                    completed_tasks.append(task)
            return completed_tasks
        except Exception as e:
            self.logger.error(f"获取任务历史失败: {e}")
            return []
    
    def search_tasks(self, keyword: str) -> List[Dict]:
        """搜索任务"""
        try:
            return self.learning_data.search_tasks(keyword)
        except Exception as e:
            self.logger.error(f"搜索任务失败: {e}")
            return []
    
    def export_progress(self, file_path: str) -> bool:
        """导出学习进度"""
        try:
            import json
            from datetime import datetime
            
            data = {
                'progress': self.progress,
                'stats': self.get_learning_stats(),
                'history': self.get_task_history(100),
                'export_date': datetime.now().isoformat()
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"学习进度已导出到: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"导出学习进度失败: {e}")
            return False
    
    def import_progress(self, file_path: str) -> bool:
        """导入学习进度"""
        try:
            import json
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 恢复进度数据
            progress_data = data.get('progress', {})
            if progress_data:
                self.progress.update(progress_data)
                self.save_progress()
            
            self.logger.info(f"学习进度已从 {file_path} 导入")
            return True
            
        except Exception as e:
            self.logger.error(f"导入学习进度失败: {e}")
            return False
    
    def save_all_data(self):
        """保存所有数据"""
        try:
            self.save_progress()
            self.logger.info("所有数据已保存")
        except Exception as e:
            self.logger.error(f"保存数据失败: {e}")
    
    def set_task_note(self, day: int, note: str):
        """设置任务笔记"""
        task_id = f"day_{day}"
        self.progress['task_notes'][task_id] = note
        self.save_progress()
    
    def get_task_note(self, day: int) -> str:
        """获取任务笔记"""
        task_id = f"day_{day}"
        return self.progress['task_notes'].get(task_id, "")
    
    def is_task_completed(self, day: int) -> bool:
        """检查任务是否已完成"""
        task_id = f"day_{day}"
        return task_id in self.progress['completed_tasks']
    
    def next_day(self):
        """进入下一天"""
        self.progress['current_day'] += 1
        self.save_progress()