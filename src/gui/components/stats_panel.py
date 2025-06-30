#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统计面板组件
显示学习数据的统计分析和图表
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

from ...core.app_manager import AppManager
from ...utils.logger import get_logger

class StatsPanel(ctk.CTkFrame):
    """统计分析面板组件"""
    
    def __init__(self, parent, app_manager: AppManager):
        super().__init__(parent)
        
        self.app_manager = app_manager
        self.logger = get_logger(__name__)
        
        # 配置网格
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # 设置matplotlib中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False
        
        self._setup_ui()
        self.refresh()
    
    def _setup_ui(self):
        """设置用户界面"""
        # 标题
        self.title_label = ctk.CTkLabel(
            self,
            text="📈 统计分析",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, pady=20)
        
        # 主要内容区域
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)
        
        # 统计摘要区域
        self._create_stats_summary()
        
        # 图表区域
        self._create_charts_area()
    
    def _create_stats_summary(self):
        """创建统计摘要区域"""
        self.summary_frame = ctk.CTkFrame(self.content_frame)
        self.summary_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.summary_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # 统计卡片
        self.stats_cards = {}
        
        # 总进度卡片
        self.stats_cards['progress'] = self._create_stat_card(
            self.summary_frame, "总进度", "0/140", "📊", 0
        )
        
        # 完成率卡片
        self.stats_cards['completion'] = self._create_stat_card(
            self.summary_frame, "完成率", "0.0%", "✅", 1
        )
        
        # 连续天数卡片
        self.stats_cards['streak'] = self._create_stat_card(
            self.summary_frame, "连续天数", "0天", "🔥", 2
        )
        
        # 平均难度卡片
        self.stats_cards['difficulty'] = self._create_stat_card(
            self.summary_frame, "平均难度", "--", "⭐", 3
        )
    
    def _create_stat_card(self, parent, title: str, value: str, icon: str, column: int):
        """创建统计卡片"""
        card_frame = ctk.CTkFrame(parent)
        card_frame.grid(row=0, column=column, padx=10, pady=10, sticky="nsew")
        card_frame.grid_columnconfigure(0, weight=1)
        
        # 图标
        icon_label = ctk.CTkLabel(
            card_frame,
            text=icon,
            font=ctk.CTkFont(size=24)
        )
        icon_label.grid(row=0, column=0, pady=(15, 5))
        
        # 数值
        value_label = ctk.CTkLabel(
            card_frame,
            text=value,
            font=ctk.CTkFont(size=20, weight="bold")
        )
        value_label.grid(row=1, column=0, pady=5)
        
        # 标题
        title_label = ctk.CTkLabel(
            card_frame,
            text=title,
            font=ctk.CTkFont(size=12)
        )
        title_label.grid(row=2, column=0, pady=(5, 15))
        
        return {
            'frame': card_frame,
            'value': value_label,
            'title': title_label
        }
    
    def _create_charts_area(self):
        """创建图表区域"""
        self.charts_frame = ctk.CTkFrame(self.content_frame)
        self.charts_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.charts_frame.grid_columnconfigure((0, 1), weight=1)
        self.charts_frame.grid_rowconfigure((0, 1), weight=1)
        
        # 进度趋势图
        self._create_progress_chart()
        
        # 难度分布图
        self._create_difficulty_chart()
        
        # 阶段完成情况图
        self._create_stage_chart()
        
        # 学习时间分析图
        self._create_time_analysis_chart()
    
    def _create_progress_chart(self):
        """创建进度趋势图"""
        self.progress_chart_frame = ctk.CTkFrame(self.charts_frame)
        self.progress_chart_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.progress_chart_frame.grid_columnconfigure(0, weight=1)
        self.progress_chart_frame.grid_rowconfigure(1, weight=1)
        
        # 图表标题
        chart_title = ctk.CTkLabel(
            self.progress_chart_frame,
            text="📈 学习进度趋势",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        chart_title.grid(row=0, column=0, pady=10)
        
        # 创建matplotlib图表
        self.progress_fig = Figure(figsize=(6, 4), dpi=100)
        self.progress_ax = self.progress_fig.add_subplot(111)
        
        self.progress_canvas = FigureCanvasTkAgg(self.progress_fig, self.progress_chart_frame)
        self.progress_canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    
    def _create_difficulty_chart(self):
        """创建难度分布图"""
        self.difficulty_chart_frame = ctk.CTkFrame(self.charts_frame)
        self.difficulty_chart_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.difficulty_chart_frame.grid_columnconfigure(0, weight=1)
        self.difficulty_chart_frame.grid_rowconfigure(1, weight=1)
        
        # 图表标题
        chart_title = ctk.CTkLabel(
            self.difficulty_chart_frame,
            text="⭐ 难度分布",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        chart_title.grid(row=0, column=0, pady=10)
        
        # 创建matplotlib图表
        self.difficulty_fig = Figure(figsize=(6, 4), dpi=100)
        self.difficulty_ax = self.difficulty_fig.add_subplot(111)
        
        self.difficulty_canvas = FigureCanvasTkAgg(self.difficulty_fig, self.difficulty_chart_frame)
        self.difficulty_canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    
    def _create_stage_chart(self):
        """创建阶段完成情况图"""
        self.stage_chart_frame = ctk.CTkFrame(self.charts_frame)
        self.stage_chart_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.stage_chart_frame.grid_columnconfigure(0, weight=1)
        self.stage_chart_frame.grid_rowconfigure(1, weight=1)
        
        # 图表标题
        chart_title = ctk.CTkLabel(
            self.stage_chart_frame,
            text="🎯 阶段完成情况",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        chart_title.grid(row=0, column=0, pady=10)
        
        # 创建matplotlib图表
        self.stage_fig = Figure(figsize=(6, 4), dpi=100)
        self.stage_ax = self.stage_fig.add_subplot(111)
        
        self.stage_canvas = FigureCanvasTkAgg(self.stage_fig, self.stage_chart_frame)
        self.stage_canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    
    def _create_time_analysis_chart(self):
        """创建学习时间分析图"""
        self.time_chart_frame = ctk.CTkFrame(self.charts_frame)
        self.time_chart_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.time_chart_frame.grid_columnconfigure(0, weight=1)
        self.time_chart_frame.grid_rowconfigure(1, weight=1)
        
        # 图表标题
        chart_title = ctk.CTkLabel(
            self.time_chart_frame,
            text="⏰ 学习时间分析",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        chart_title.grid(row=0, column=0, pady=10)
        
        # 创建matplotlib图表
        self.time_fig = Figure(figsize=(6, 4), dpi=100)
        self.time_ax = self.time_fig.add_subplot(111)
        
        self.time_canvas = FigureCanvasTkAgg(self.time_fig, self.time_chart_frame)
        self.time_canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    
    def refresh(self):
        """刷新统计显示"""
        try:
            self._update_stats_summary()
            self._update_progress_chart()
            self._update_difficulty_chart()
            self._update_stage_chart()
            self._update_time_analysis_chart()
            self.logger.info("统计面板刷新完成")
        except Exception as e:
            self.logger.error(f"刷新统计面板失败: {e}")
    
    def _update_stats_summary(self):
        """更新统计摘要"""
        stats = self.app_manager.get_learning_stats()
        
        # 更新总进度
        completed = stats.get('completed_days', 0)
        total = stats.get('total_days', 140)
        self.stats_cards['progress']['value'].configure(text=f"{completed}/{total}")
        
        # 更新完成率
        completion_rate = stats.get('completion_rate', 0)
        self.stats_cards['completion']['value'].configure(text=f"{completion_rate:.1f}%")
        
        # 更新连续天数
        streak = stats.get('current_streak', 0)
        self.stats_cards['streak']['value'].configure(text=f"{streak}天")
        
        # 更新平均难度
        avg_difficulty = self._calculate_average_difficulty()
        self.stats_cards['difficulty']['value'].configure(text=avg_difficulty)
    
    def _calculate_average_difficulty(self) -> str:
        """计算平均难度"""
        try:
            progress_data = self.app_manager.get_progress_data()
            completed_tasks = progress_data.get('completed_tasks', {})
            
            if not completed_tasks:
                return "--"
            
            difficulty_map = {'简单': 1, '中等': 2, '困难': 3}
            total_difficulty = 0
            count = 0
            
            for day_str in completed_tasks:
                if completed_tasks[day_str]:
                    task = self.app_manager.learning_data.get_task_by_day(int(day_str))
                    if task:
                        difficulty = task.get('difficulty', '中等')
                        total_difficulty += difficulty_map.get(difficulty, 2)
                        count += 1
            
            if count == 0:
                return "--"
            
            avg = total_difficulty / count
            if avg <= 1.3:
                return "简单"
            elif avg <= 2.3:
                return "中等"
            else:
                return "困难"
                
        except Exception as e:
            self.logger.error(f"计算平均难度失败: {e}")
            return "--"
    
    def _update_progress_chart(self):
        """更新进度趋势图"""
        try:
            self.progress_ax.clear()
            
            # 获取进度数据
            progress_data = self.app_manager.get_progress_data()
            completed_tasks = progress_data.get('completed_tasks', {})
            completion_dates = progress_data.get('completion_dates', {})
            
            if not completed_tasks:
                self.progress_ax.text(0.5, 0.5, '暂无数据', ha='center', va='center', transform=self.progress_ax.transAxes)
                self.progress_canvas.draw()
                return
            
            # 按日期统计完成情况
            date_progress = {}
            for day_str, is_completed in completed_tasks.items():
                if is_completed and day_str in completion_dates:
                    date_str = completion_dates[day_str]
                    try:
                        date = datetime.strptime(date_str, "%Y-%m-%d").date()
                        if date not in date_progress:
                            date_progress[date] = 0
                        date_progress[date] += 1
                    except:
                        continue
            
            if not date_progress:
                self.progress_ax.text(0.5, 0.5, '暂无完成记录', ha='center', va='center', transform=self.progress_ax.transAxes)
                self.progress_canvas.draw()
                return
            
            # 排序日期
            sorted_dates = sorted(date_progress.keys())
            
            # 计算累积进度
            cumulative_progress = []
            total = 0
            for date in sorted_dates:
                total += date_progress[date]
                cumulative_progress.append(total)
            
            # 绘制图表
            self.progress_ax.plot(sorted_dates, cumulative_progress, marker='o', linewidth=2, markersize=4)
            self.progress_ax.set_title('学习进度趋势')
            self.progress_ax.set_xlabel('日期')
            self.progress_ax.set_ylabel('累计完成任务数')
            self.progress_ax.grid(True, alpha=0.3)
            
            # 格式化x轴日期
            if len(sorted_dates) > 10:
                step = len(sorted_dates) // 10
                self.progress_ax.set_xticks(sorted_dates[::step])
            
            self.progress_fig.autofmt_xdate()
            self.progress_canvas.draw()
            
        except Exception as e:
            self.logger.error(f"更新进度趋势图失败: {e}")
            self.progress_ax.clear()
            self.progress_ax.text(0.5, 0.5, '图表加载失败', ha='center', va='center', transform=self.progress_ax.transAxes)
            self.progress_canvas.draw()
    
    def _update_difficulty_chart(self):
        """更新难度分布图"""
        try:
            self.difficulty_ax.clear()
            
            # 获取已完成任务的难度分布
            progress_data = self.app_manager.get_progress_data()
            completed_tasks = progress_data.get('completed_tasks', {})
            
            difficulty_count = {'简单': 0, '中等': 0, '困难': 0}
            
            for day_str, is_completed in completed_tasks.items():
                if is_completed:
                    task = self.app_manager.learning_data.get_task_by_day(int(day_str))
                    if task:
                        difficulty = task.get('difficulty', '中等')
                        if difficulty in difficulty_count:
                            difficulty_count[difficulty] += 1
            
            # 如果没有完成的任务，显示全部任务的难度分布
            if sum(difficulty_count.values()) == 0:
                all_tasks = self.app_manager.learning_data.get_all_tasks()
                for task in all_tasks:
                    difficulty = task.get('difficulty', '中等')
                    if difficulty in difficulty_count:
                        difficulty_count[difficulty] += 1
                
                title = '全部任务难度分布'
            else:
                title = '已完成任务难度分布'
            
            # 绘制饼图
            labels = list(difficulty_count.keys())
            sizes = list(difficulty_count.values())
            colors = ['#4CAF50', '#FF9800', '#f44336']
            
            if sum(sizes) > 0:
                wedges, texts, autotexts = self.difficulty_ax.pie(
                    sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                    startangle=90
                )
                
                # 设置文本样式
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
            else:
                self.difficulty_ax.text(0.5, 0.5, '暂无数据', ha='center', va='center', transform=self.difficulty_ax.transAxes)
            
            self.difficulty_ax.set_title(title)
            self.difficulty_canvas.draw()
            
        except Exception as e:
            self.logger.error(f"更新难度分布图失败: {e}")
            self.difficulty_ax.clear()
            self.difficulty_ax.text(0.5, 0.5, '图表加载失败', ha='center', va='center', transform=self.difficulty_ax.transAxes)
            self.difficulty_canvas.draw()
    
    def _update_stage_chart(self):
        """更新阶段完成情况图"""
        try:
            self.stage_ax.clear()
            
            # 获取阶段信息
            stages = self.app_manager.learning_data.get_all_stages()
            progress_data = self.app_manager.get_progress_data()
            completed_tasks = progress_data.get('completed_tasks', {})
            
            stage_names = []
            completion_rates = []
            
            for stage in stages:
                stage_num = stage['stage']
                stage_tasks = self.app_manager.learning_data.get_tasks_by_stage(stage_num)
                
                completed_in_stage = sum(1 for task in stage_tasks 
                                       if completed_tasks.get(str(task['day']), False))
                total_in_stage = len(stage_tasks)
                
                completion_rate = (completed_in_stage / total_in_stage * 100) if total_in_stage > 0 else 0
                
                stage_names.append(f"阶段{stage_num}")
                completion_rates.append(completion_rate)
            
            # 绘制柱状图
            bars = self.stage_ax.bar(stage_names, completion_rates, color='#2196F3', alpha=0.7)
            
            # 添加数值标签
            for bar, rate in zip(bars, completion_rates):
                height = bar.get_height()
                self.stage_ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                                 f'{rate:.1f}%', ha='center', va='bottom')
            
            self.stage_ax.set_title('各阶段完成情况')
            self.stage_ax.set_xlabel('学习阶段')
            self.stage_ax.set_ylabel('完成率 (%)')
            self.stage_ax.set_ylim(0, 105)
            self.stage_ax.grid(True, alpha=0.3, axis='y')
            
            self.stage_canvas.draw()
            
        except Exception as e:
            self.logger.error(f"更新阶段完成情况图失败: {e}")
            self.stage_ax.clear()
            self.stage_ax.text(0.5, 0.5, '图表加载失败', ha='center', va='center', transform=self.stage_ax.transAxes)
            self.stage_canvas.draw()
    
    def _update_time_analysis_chart(self):
        """更新学习时间分析图"""
        try:
            self.time_ax.clear()
            
            # 获取已完成任务的时间分布
            progress_data = self.app_manager.get_progress_data()
            completed_tasks = progress_data.get('completed_tasks', {})
            
            time_distribution = {}
            
            for day_str, is_completed in completed_tasks.items():
                if is_completed:
                    task = self.app_manager.learning_data.get_task_by_day(int(day_str))
                    if task:
                        estimated_time = task.get('estimated_time', '')
                        # 简化时间分类
                        if '30分钟' in estimated_time or '0.5小时' in estimated_time:
                            time_category = '30分钟'
                        elif '1小时' in estimated_time:
                            time_category = '1小时'
                        elif '1.5小时' in estimated_time:
                            time_category = '1.5小时'
                        elif '2小时' in estimated_time:
                            time_category = '2小时'
                        else:
                            time_category = '其他'
                        
                        if time_category not in time_distribution:
                            time_distribution[time_category] = 0
                        time_distribution[time_category] += 1
            
            if not time_distribution:
                self.time_ax.text(0.5, 0.5, '暂无完成记录', ha='center', va='center', transform=self.time_ax.transAxes)
                self.time_canvas.draw()
                return
            
            # 绘制水平柱状图
            categories = list(time_distribution.keys())
            counts = list(time_distribution.values())
            
            bars = self.time_ax.barh(categories, counts, color='#FF9800', alpha=0.7)
            
            # 添加数值标签
            for bar, count in zip(bars, counts):
                width = bar.get_width()
                self.time_ax.text(width + 0.1, bar.get_y() + bar.get_height()/2.,
                                f'{count}', ha='left', va='center')
            
            self.time_ax.set_title('学习时间分布')
            self.time_ax.set_xlabel('任务数量')
            self.time_ax.set_ylabel('预计学习时间')
            self.time_ax.grid(True, alpha=0.3, axis='x')
            
            self.time_canvas.draw()
            
        except Exception as e:
            self.logger.error(f"更新学习时间分析图失败: {e}")
            self.time_ax.clear()
            self.time_ax.text(0.5, 0.5, '图表加载失败', ha='center', va='center', transform=self.time_ax.transAxes)
            self.time_canvas.draw()