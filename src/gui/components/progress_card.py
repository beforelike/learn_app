#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
进度卡片组件
显示学习进度的可视化界面
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional
import math

from ...core.app_manager import AppManager
from ...utils.logger import get_logger

class ProgressCard(ctk.CTkFrame):
    """学习进度卡片组件"""
    
    def __init__(self, parent, app_manager: AppManager):
        super().__init__(parent)
        
        self.app_manager = app_manager
        self.logger = get_logger(__name__)
        
        # 配置网格
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self._setup_ui()
        self.refresh()
    
    def _setup_ui(self):
        """设置用户界面"""
        # 标题
        self.title_label = ctk.CTkLabel(
            self,
            text="📊 学习进度",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, pady=20)
        
        # 主要内容区域
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.content_frame.grid_columnconfigure((0, 1), weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)
        
        # 总体进度区域
        self._create_overall_progress()
        
        # 阶段进度区域
        self._create_stage_progress()
        
        # 详细进度列表
        self._create_detailed_progress()
    
    def _create_overall_progress(self):
        """创建总体进度区域"""
        self.overall_frame = ctk.CTkFrame(self.content_frame)
        self.overall_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.overall_frame.grid_columnconfigure(0, weight=1)
        
        # 总体进度标题
        overall_title = ctk.CTkLabel(
            self.overall_frame,
            text="总体进度",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        overall_title.grid(row=0, column=0, pady=10)
        
        # 进度条容器
        progress_container = ctk.CTkFrame(self.overall_frame)
        progress_container.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        progress_container.grid_columnconfigure(0, weight=1)
        
        # 总体进度条
        self.overall_progress = ctk.CTkProgressBar(
            progress_container,
            height=20,
            progress_color="#4CAF50"
        )
        self.overall_progress.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # 进度文本
        self.overall_text = ctk.CTkLabel(
            progress_container,
            text="0/140 (0.0%)",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.overall_text.grid(row=1, column=0, pady=5)
        
        # 统计信息
        self.stats_frame = ctk.CTkFrame(self.overall_frame)
        self.stats_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # 统计标签
        self.completed_label = ctk.CTkLabel(self.stats_frame, text="已完成: 0天")
        self.completed_label.grid(row=0, column=0, padx=10, pady=5)
        
        self.remaining_label = ctk.CTkLabel(self.stats_frame, text="剩余: 140天")
        self.remaining_label.grid(row=0, column=1, padx=10, pady=5)
        
        self.streak_label = ctk.CTkLabel(self.stats_frame, text="连续: 0天")
        self.streak_label.grid(row=0, column=2, padx=10, pady=5)
    
    def _create_stage_progress(self):
        """创建阶段进度区域"""
        self.stage_frame = ctk.CTkFrame(self.content_frame)
        self.stage_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.stage_frame.grid_columnconfigure(0, weight=1)
        
        # 阶段进度标题
        stage_title = ctk.CTkLabel(
            self.stage_frame,
            text="阶段进度",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        stage_title.grid(row=0, column=0, pady=10)
        
        # 阶段进度容器
        self.stage_container = ctk.CTkScrollableFrame(self.stage_frame)
        self.stage_container.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.stage_container.grid_columnconfigure(0, weight=1)
        
        self.stage_frame.grid_rowconfigure(1, weight=1)
    
    def _create_detailed_progress(self):
        """创建详细进度列表"""
        self.detail_frame = ctk.CTkFrame(self.content_frame)
        self.detail_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.detail_frame.grid_columnconfigure(0, weight=1)
        self.detail_frame.grid_rowconfigure(1, weight=1)
        
        # 详细进度标题
        detail_title = ctk.CTkLabel(
            self.detail_frame,
            text="详细进度",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        detail_title.grid(row=0, column=0, pady=10)
        
        # 创建Treeview用于显示详细进度
        self.tree_frame = ctk.CTkFrame(self.detail_frame)
        self.tree_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.tree_frame.grid_columnconfigure(0, weight=1)
        self.tree_frame.grid_rowconfigure(0, weight=1)
        
        # 创建Treeview
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("day", "title", "status", "difficulty", "time", "completed_date"),
            show="headings",
            height=15
        )
        
        # 设置列标题
        self.tree.heading("day", text="天数")
        self.tree.heading("title", text="任务标题")
        self.tree.heading("status", text="状态")
        self.tree.heading("difficulty", text="难度")
        self.tree.heading("time", text="预计时间")
        self.tree.heading("completed_date", text="完成日期")
        
        # 设置列宽
        self.tree.column("day", width=60, anchor="center")
        self.tree.column("title", width=300, anchor="w")
        self.tree.column("status", width=80, anchor="center")
        self.tree.column("difficulty", width=80, anchor="center")
        self.tree.column("time", width=100, anchor="center")
        self.tree.column("completed_date", width=120, anchor="center")
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 布局
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # 绑定双击事件
        self.tree.bind("<Double-1>", self._on_task_double_click)
    
    def refresh(self):
        """刷新进度显示"""
        try:
            self._update_overall_progress()
            self._update_stage_progress()
            self._update_detailed_progress()
            self.logger.info("进度卡片刷新完成")
        except Exception as e:
            self.logger.error(f"刷新进度卡片失败: {e}")
    
    def _update_overall_progress(self):
        """更新总体进度"""
        stats = self.app_manager.get_learning_stats()
        
        completed = stats.get('completed_days', 0)
        total = stats.get('total_days', 140)
        completion_rate = stats.get('completion_rate', 0)
        
        # 更新进度条
        self.overall_progress.set(completion_rate / 100)
        
        # 更新进度文本
        self.overall_text.configure(text=f"{completed}/{total} ({completion_rate:.1f}%)")
        
        # 更新统计信息
        remaining = total - completed
        streak = stats.get('current_streak', 0)
        
        self.completed_label.configure(text=f"已完成: {completed}天")
        self.remaining_label.configure(text=f"剩余: {remaining}天")
        self.streak_label.configure(text=f"连续: {streak}天")
    
    def _update_stage_progress(self):
        """更新阶段进度"""
        # 清空现有内容
        for widget in self.stage_container.winfo_children():
            widget.destroy()
        
        # 获取阶段信息
        stages = self.app_manager.learning_data.get_all_stages()
        progress_data = self.app_manager.get_progress_data()
        
        for i, stage in enumerate(stages):
            stage_frame = ctk.CTkFrame(self.stage_container)
            stage_frame.grid(row=i, column=0, padx=5, pady=5, sticky="ew")
            stage_frame.grid_columnconfigure(1, weight=1)
            
            # 阶段标题
            stage_title = ctk.CTkLabel(
                stage_frame,
                text=f"阶段 {stage['stage']}",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            stage_title.grid(row=0, column=0, padx=10, pady=5, sticky="w")
            
            # 阶段描述
            stage_desc = ctk.CTkLabel(
                stage_frame,
                text=stage['description'],
                font=ctk.CTkFont(size=12),
                wraplength=200
            )
            stage_desc.grid(row=1, column=0, columnspan=2, padx=10, pady=2, sticky="w")
            
            # 计算阶段进度
            stage_tasks = self.app_manager.learning_data.get_tasks_by_stage(stage['stage'])
            completed_in_stage = sum(1 for task in stage_tasks 
                                   if progress_data.get('completed_tasks', {}).get(str(task['day']), False))
            total_in_stage = len(stage_tasks)
            stage_progress = completed_in_stage / total_in_stage if total_in_stage > 0 else 0
            
            # 阶段进度条
            progress_bar = ctk.CTkProgressBar(
                stage_frame,
                height=15,
                progress_color="#2196F3" if stage_progress < 1 else "#4CAF50"
            )
            progress_bar.set(stage_progress)
            progress_bar.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
            
            # 阶段进度文本
            progress_text = ctk.CTkLabel(
                stage_frame,
                text=f"{completed_in_stage}/{total_in_stage} ({stage_progress*100:.1f}%)",
                font=ctk.CTkFont(size=11)
            )
            progress_text.grid(row=3, column=0, columnspan=2, padx=10, pady=2)
    
    def _update_detailed_progress(self):
        """更新详细进度列表"""
        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 获取所有任务和进度数据
        all_tasks = self.app_manager.learning_data.get_all_tasks()
        progress_data = self.app_manager.get_progress_data()
        completed_tasks = progress_data.get('completed_tasks', {})
        
        # 添加任务到树形视图
        for task in all_tasks:
            day = task['day']
            is_completed = completed_tasks.get(str(day), False)
            
            # 状态
            status = "✅ 已完成" if is_completed else "⏳ 待完成"
            
            # 完成日期
            completed_date = ""
            if is_completed and 'completion_dates' in progress_data:
                completed_date = progress_data['completion_dates'].get(str(day), "")
            
            # 插入数据
            item = self.tree.insert("", "end", values=(
                day,
                task['title'],
                status,
                task['difficulty'],
                task['estimated_time'],
                completed_date
            ))
            
            # 设置行颜色
            if is_completed:
                self.tree.set(item, "status", "✅ 已完成")
            else:
                self.tree.set(item, "status", "⏳ 待完成")
    
    def _on_task_double_click(self, event):
        """处理任务双击事件"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.tree.item(item, 'values')
        
        if values:
            day = int(values[0])
            task = self.app_manager.learning_data.get_task_by_day(day)
            
            if task:
                self._show_task_detail(task)
    
    def _show_task_detail(self, task: Dict):
        """显示任务详情对话框"""
        detail_window = ctk.CTkToplevel(self)
        detail_window.title(f"任务详情 - 第{task['day']}天")
        detail_window.geometry("600x400")
        detail_window.transient(self)
        detail_window.grab_set()
        
        # 任务标题
        title_label = ctk.CTkLabel(
            detail_window,
            text=task['title'],
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        # 任务信息框架
        info_frame = ctk.CTkFrame(detail_window)
        info_frame.pack(padx=20, pady=10, fill="x")
        
        # 任务信息
        info_items = [
            ("天数", f"第{task['day']}天"),
            ("阶段", f"第{task['stage']}阶段"),
            ("难度", task['difficulty']),
            ("预计时间", task['estimated_time'])
        ]
        
        for i, (label, value) in enumerate(info_items):
            row_frame = ctk.CTkFrame(info_frame)
            row_frame.pack(fill="x", padx=10, pady=5)
            
            label_widget = ctk.CTkLabel(row_frame, text=f"{label}:", font=ctk.CTkFont(weight="bold"))
            label_widget.pack(side="left", padx=10)
            
            value_widget = ctk.CTkLabel(row_frame, text=value)
            value_widget.pack(side="left", padx=10)
        
        # 任务内容
        content_frame = ctk.CTkFrame(detail_window)
        content_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        content_label = ctk.CTkLabel(
            content_frame,
            text="任务内容:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        content_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        content_text = ctk.CTkTextbox(content_frame, height=150)
        content_text.pack(padx=10, pady=(0, 10), fill="both", expand=True)
        content_text.insert("1.0", task['content'])
        content_text.configure(state="disabled")
        
        # 关闭按钮
        close_btn = ctk.CTkButton(
            detail_window,
            text="关闭",
            command=detail_window.destroy
        )
        close_btn.pack(pady=20)