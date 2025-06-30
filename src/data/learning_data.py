#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学习数据模型
包含完整的数学建模学习路线数据
"""

from typing import Dict, List, Optional
from datetime import datetime

class LearningData:
    """学习数据管理类"""
    
    def __init__(self):
        self.learning_path = self._initialize_learning_path()
        self.total_days = 140  # 20周 * 7天
        self.total_weeks = 20
        self.total_stages = 6
    
    def _initialize_learning_path(self) -> Dict:
        """初始化学习路线数据"""
        return {
            "title": "数学建模完整学习路线",
            "description": "20周系统性数学建模学习计划",
            "total_weeks": 20,
            "total_days": 140,
            "stages": [
                {
                    "id": 1,
                    "name": "Python基础与数据科学环境",
                    "weeks": "第1-3周",
                    "description": "掌握Python编程基础和数据科学工具",
                    "color": "#4CAF50",
                    "weeks_detail": [
                        {
                            "week": 1,
                            "title": "Python编程基础",
                            "days": [
                                {
                                    "day": 1,
                                    "title": "Python环境搭建与基础语法",
                                    "content": "安装Python、IDE配置、变量类型、基本运算",
                                    "tasks": [
                                        "安装Python 3.8+和Anaconda",
                                        "配置Jupyter Notebook",
                                        "学习变量、数据类型、运算符",
                                        "练习基本输入输出"
                                    ],
                                    "estimated_time": "2-3小时",
                                    "difficulty": "入门",
                                    "code_examples": [
                                        {
                                            "title": "基础语法示例",
                                            "code": "# Python基础语法\nname = 'Python学习者'\nage = 25\nprint(f'你好，{name}！你今年{age}岁。')\n\n# 基本运算\na, b = 10, 3\nprint(f'加法: {a + b}')\nprint(f'除法: {a / b}')\nprint(f'整除: {a // b}')\nprint(f'取余: {a % b}')"
                                        }
                                    ]
                                },
                                {
                                    "day": 2,
                                    "title": "控制结构与函数",
                                    "content": "条件语句、循环结构、函数定义与调用",
                                    "tasks": [
                                        "掌握if-elif-else语句",
                                        "学习for和while循环",
                                        "函数定义、参数传递、返回值",
                                        "练习递归函数"
                                    ],
                                    "estimated_time": "2-3小时",
                                    "difficulty": "入门",
                                    "code_examples": [
                                        {
                                            "title": "函数和循环示例",
                                            "code": "# 函数定义\ndef fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\n\n# 循环应用\nfor i in range(10):\n    print(f'斐波那契数列第{i}项: {fibonacci(i)}')"
                                        }
                                    ]
                                },
                                {
                                    "day": 3,
                                    "title": "数据结构基础",
                                    "content": "列表、元组、字典、集合的使用",
                                    "tasks": [
                                        "列表操作和方法",
                                        "字典的创建和遍历",
                                        "集合运算",
                                        "数据结构选择原则"
                                    ],
                                    "estimated_time": "2-3小时",
                                    "difficulty": "入门"
                                },
                                {
                                    "day": 4,
                                    "title": "文件操作与异常处理",
                                    "content": "文件读写、异常捕获、模块导入",
                                    "tasks": [
                                        "文件的打开、读取、写入",
                                        "try-except异常处理",
                                        "模块导入和使用",
                                        "包的概念和创建"
                                    ],
                                    "estimated_time": "2-3小时",
                                    "difficulty": "入门"
                                },
                                {
                                    "day": 5,
                                    "title": "面向对象编程基础",
                                    "content": "类与对象、继承、封装",
                                    "tasks": [
                                        "类的定义和实例化",
                                        "属性和方法",
                                        "继承和多态",
                                        "特殊方法(__init__, __str__等)"
                                    ],
                                    "estimated_time": "3-4小时",
                                    "difficulty": "基础"
                                },
                                {
                                    "day": 6,
                                    "title": "Python标准库",
                                    "content": "常用标准库的使用",
                                    "tasks": [
                                        "math、random模块",
                                        "datetime时间处理",
                                        "os、sys系统操作",
                                        "json数据处理"
                                    ],
                                    "estimated_time": "2-3小时",
                                    "difficulty": "基础"
                                },
                                {
                                    "day": 7,
                                    "title": "Python基础综合练习",
                                    "content": "综合运用所学知识完成小项目",
                                    "tasks": [
                                        "设计一个简单的学生管理系统",
                                        "实现文件数据的读写",
                                        "添加异常处理机制",
                                        "代码重构和优化"
                                    ],
                                    "estimated_time": "3-4小时",
                                    "difficulty": "基础"
                                }
                            ]
                        },
                        {
                            "week": 2,
                            "title": "NumPy数值计算",
                            "days": [
                                {
                                    "day": 8,
                                    "title": "NumPy基础与数组操作",
                                    "content": "NumPy安装、数组创建、基本操作",
                                    "tasks": [
                                        "安装NumPy库",
                                        "创建不同类型的数组",
                                        "数组索引和切片",
                                        "数组形状操作"
                                    ],
                                    "estimated_time": "2-3小时",
                                    "difficulty": "基础"
                                },
                                {
                                    "day": 9,
                                    "title": "数组运算与函数",
                                    "content": "数学运算、统计函数、线性代数",
                                    "tasks": [
                                        "元素级运算",
                                        "统计函数应用",
                                        "矩阵运算",
                                        "广播机制理解"
                                    ],
                                    "estimated_time": "2-3小时",
                                    "difficulty": "基础"
                                },
                                {
                                    "day": 10,
                                    "title": "高级数组操作",
                                    "content": "条件筛选、排序、去重",
                                    "tasks": [
                                        "布尔索引",
                                        "数组排序方法",
                                        "唯一值处理",
                                        "数组合并和分割"
                                    ],
                                    "estimated_time": "2-3小时",
                                    "difficulty": "基础"
                                },
                                {
                                    "day": 11,
                                    "title": "随机数与概率分布",
                                    "content": "随机数生成、概率分布采样",
                                    "tasks": [
                                        "随机数生成器",
                                        "常见概率分布",
                                        "蒙特卡洛方法入门",
                                        "随机采样技术"
                                    ],
                                    "estimated_time": "2-3小时",
                                    "difficulty": "基础"
                                },
                                {
                                    "day": 12,
                                    "title": "文件I/O与数据格式",
                                    "content": "数据文件读写、格式转换",
                                    "tasks": [
                                        "CSV文件处理",
                                        "二进制文件操作",
                                        "数据格式转换",
                                        "大文件处理技巧"
                                    ],
                                    "estimated_time": "2-3小时",
                                    "difficulty": "基础"
                                },
                                {
                                    "day": 13,
                                    "title": "性能优化与内存管理",
                                    "content": "代码优化、内存使用",
                                    "tasks": [
                                        "向量化操作",
                                        "内存视图使用",
                                        "性能测试方法",
                                        "内存优化技巧"
                                    ],
                                    "estimated_time": "3-4小时",
                                    "difficulty": "中级"
                                },
                                {
                                    "day": 14,
                                    "title": "NumPy综合应用",
                                    "content": "实际问题解决、项目实践",
                                    "tasks": [
                                        "图像处理基础",
                                        "信号处理入门",
                                        "数值积分方法",
                                        "线性方程组求解"
                                    ],
                                    "estimated_time": "3-4小时",
                                    "difficulty": "中级"
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 2,
                    "name": "数据处理与分析",
                    "weeks": "第4-8周",
                    "description": "掌握Pandas数据处理和Matplotlib可视化",
                    "color": "#2196F3",
                    "weeks_detail": [
                        {
                            "week": 4,
                            "title": "Pandas数据处理基础",
                            "days": [
                                {
                                    "day": 22,
                                    "title": "Pandas入门与数据结构",
                                    "content": "Series和DataFrame基础操作",
                                    "tasks": [
                                        "安装Pandas库",
                                        "Series创建和操作",
                                        "DataFrame基础",
                                        "数据索引和选择"
                                    ],
                                    "estimated_time": "2-3小时",
                                    "difficulty": "基础"
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 3,
                    "name": "数学基础与优化",
                    "weeks": "第9-12周",
                    "description": "线性代数、微积分、优化理论",
                    "color": "#FF9800",
                    "weeks_detail": []
                },
                {
                    "id": 4,
                    "name": "机器学习基础",
                    "weeks": "第13-16周",
                    "description": "监督学习、无监督学习、模型评估",
                    "color": "#9C27B0",
                    "weeks_detail": []
                },
                {
                    "id": 5,
                    "name": "数学建模实战",
                    "weeks": "第17-19周",
                    "description": "经典建模问题、算法实现",
                    "color": "#F44336",
                    "weeks_detail": []
                },
                {
                    "id": 6,
                    "name": "项目实践与总结",
                    "weeks": "第20周",
                    "description": "综合项目、知识总结",
                    "color": "#607D8B",
                    "weeks_detail": []
                }
            ]
        }
    
    def get_task_by_day(self, day: int) -> Optional[Dict]:
        """根据天数获取任务"""
        if day < 1 or day > self.total_days:
            return None
        
        # 遍历所有阶段和周，找到对应的任务
        current_day = 1
        for stage in self.learning_path["stages"]:
            for week_detail in stage["weeks_detail"]:
                for day_data in week_detail["days"]:
                    if current_day == day:
                        return {
                            **day_data,
                            "stage_id": stage["id"],
                            "stage_name": stage["name"],
                            "week": week_detail["week"],
                            "week_title": week_detail["title"]
                        }
                    current_day += 1
        
        return None
    
    def get_stage_by_day(self, day: int) -> Optional[Dict]:
        """根据天数获取阶段信息"""
        task = self.get_task_by_day(day)
        if task:
            return {
                "stage_id": task["stage_id"],
                "stage_name": task["stage_name"],
                "week": task["week"]
            }
        return None
    
    def get_total_days(self) -> int:
        """获取总天数"""
        return self.total_days
    
    def get_stage_progress(self, stage_id: int, completed_days: int) -> Dict:
        """获取阶段进度"""
        stage = next((s for s in self.learning_path["stages"] if s["id"] == stage_id), None)
        if not stage:
            return {}
        
        # 计算该阶段的总天数和已完成天数
        stage_total_days = sum(len(week["days"]) for week in stage["weeks_detail"])
        
        # 计算该阶段开始的天数
        stage_start_day = 1
        for s in self.learning_path["stages"]:
            if s["id"] == stage_id:
                break
            stage_start_day += sum(len(week["days"]) for week in s["weeks_detail"])
        
        stage_completed = max(0, min(completed_days - stage_start_day + 1, stage_total_days))
        
        return {
            "stage_id": stage_id,
            "stage_name": stage["name"],
            "total_days": stage_total_days,
            "completed_days": stage_completed,
            "progress_rate": (stage_completed / stage_total_days) * 100 if stage_total_days > 0 else 0
        }
    
    def search_tasks(self, keyword: str) -> List[Dict]:
        """搜索任务"""
        results = []
        keyword_lower = keyword.lower()
        
        current_day = 1
        for stage in self.learning_path["stages"]:
            for week_detail in stage["weeks_detail"]:
                for day_data in week_detail["days"]:
                    # 在标题、内容、任务中搜索
                    if (keyword_lower in day_data["title"].lower() or
                        keyword_lower in day_data["content"].lower() or
                        any(keyword_lower in task.lower() for task in day_data["tasks"])):
                        
                        results.append({
                            **day_data,
                            "day": current_day,
                            "stage_id": stage["id"],
                            "stage_name": stage["name"],
                            "week": week_detail["week"],
                            "week_title": week_detail["title"]
                        })
                    current_day += 1
        
        return results
    
    def get_all_stages(self) -> List[Dict]:
        """获取所有阶段信息"""
        return self.learning_path["stages"]
    
    def get_week_tasks(self, week: int) -> List[Dict]:
        """获取指定周的所有任务"""
        tasks = []
        current_day = 1
        
        for stage in self.learning_path["stages"]:
            for week_detail in stage["weeks_detail"]:
                if week_detail["week"] == week:
                    for day_data in week_detail["days"]:
                        tasks.append({
                            **day_data,
                            "day": current_day,
                            "stage_id": stage["id"],
                            "stage_name": stage["name"],
                            "week": week_detail["week"],
                            "week_title": week_detail["title"]
                        })
                        current_day += 1
                else:
                    current_day += len(week_detail["days"])
        
        return tasks