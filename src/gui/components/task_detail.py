#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务详情组件
显示当前任务的详细信息和操作
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from typing import Dict, Optional
from datetime import datetime

from ...core.app_manager import AppManager
from ...utils.logger import get_logger

class TaskDetailFrame(ctk.CTkFrame):
    """任务详情框架组件"""
    
    def __init__(self, parent, app_manager: AppManager):
        super().__init__(parent)
        
        self.app_manager = app_manager
        self.logger = get_logger(__name__)
        self.current_task = None
        
        # 配置网格
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self._setup_ui()
        self.refresh()
    
    def _setup_ui(self):
        """设置用户界面"""
        # 标题区域
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.header_frame.grid_columnconfigure(1, weight=1)
        
        # 任务标题
        self.task_title = ctk.CTkLabel(
            self.header_frame,
            text="当前任务详情",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.task_title.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        # 操作按钮区域
        self.action_frame = ctk.CTkFrame(self.header_frame)
        self.action_frame.grid(row=0, column=1, padx=20, pady=10, sticky="e")
        
        # 完成任务按钮
        self.complete_btn = ctk.CTkButton(
            self.action_frame,
            text="✅ 完成任务",
            command=self._complete_task,
            height=35,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.complete_btn.grid(row=0, column=0, padx=5)
        
        # 跳过任务按钮
        self.skip_btn = ctk.CTkButton(
            self.action_frame,
            text="⏭️ 跳过任务",
            command=self._skip_task,
            height=35,
            font=ctk.CTkFont(size=14),
            fg_color="#FF9800",
            hover_color="#F57C00"
        )
        self.skip_btn.grid(row=0, column=1, padx=5)
        
        # 重置进度按钮
        self.reset_btn = ctk.CTkButton(
            self.action_frame,
            text="🔄 重置进度",
            command=self._reset_progress,
            height=35,
            font=ctk.CTkFont(size=14),
            fg_color="#f44336",
            hover_color="#d32f2f"
        )
        self.reset_btn.grid(row=0, column=2, padx=5)
        
        # 主要内容区域
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.content_frame.grid_columnconfigure((0, 1), weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)
        
        # 任务信息区域
        self._create_task_info_area()
        
        # 任务内容区域
        self._create_task_content_area()
        
        # 学习笔记区域
        self._create_notes_area()
    
    def _create_task_info_area(self):
        """创建任务信息区域"""
        self.info_frame = ctk.CTkFrame(self.content_frame)
        self.info_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.info_frame.grid_columnconfigure(0, weight=1)
        
        # 信息标题
        info_title = ctk.CTkLabel(
            self.info_frame,
            text="📋 任务信息",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        info_title.grid(row=0, column=0, pady=10)
        
        # 信息容器
        self.info_container = ctk.CTkFrame(self.info_frame)
        self.info_container.grid(row=1, column=0, padx=15, pady=10, sticky="ew")
        self.info_container.grid_columnconfigure(1, weight=1)
        
        # 任务信息标签
        self.day_label = ctk.CTkLabel(self.info_container, text="天数: --")
        self.day_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        self.stage_label = ctk.CTkLabel(self.info_container, text="阶段: --")
        self.stage_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        self.difficulty_label = ctk.CTkLabel(self.info_container, text="难度: --")
        self.difficulty_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        self.time_label = ctk.CTkLabel(self.info_container, text="预计时间: --")
        self.time_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        self.status_label = ctk.CTkLabel(self.info_container, text="状态: --")
        self.status_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        # 进度信息
        progress_frame = ctk.CTkFrame(self.info_frame)
        progress_frame.grid(row=2, column=0, padx=15, pady=10, sticky="ew")
        progress_frame.grid_columnconfigure(0, weight=1)
        
        progress_title = ctk.CTkLabel(
            progress_frame,
            text="📊 学习进度",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        progress_title.grid(row=0, column=0, pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            height=20,
            progress_color="#4CAF50"
        )
        self.progress_bar.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        self.progress_text = ctk.CTkLabel(
            progress_frame,
            text="0/140 (0.0%)",
            font=ctk.CTkFont(size=12)
        )
        self.progress_text.grid(row=2, column=0, pady=5)
    
    def _create_task_content_area(self):
        """创建任务内容区域"""
        self.task_content_frame = ctk.CTkFrame(self.content_frame)
        self.task_content_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.task_content_frame.grid_columnconfigure(0, weight=1)
        self.task_content_frame.grid_rowconfigure(1, weight=1)
        
        # 内容标题
        content_title = ctk.CTkLabel(
            self.task_content_frame,
            text="📖 任务内容",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        content_title.grid(row=0, column=0, pady=10)
        
        # 任务内容文本框
        self.content_textbox = ctk.CTkTextbox(
            self.task_content_frame,
            height=200,
            font=ctk.CTkFont(size=13),
            wrap="word"
        )
        self.content_textbox.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
    
    def _create_notes_area(self):
        """创建学习笔记区域"""
        self.notes_frame = ctk.CTkFrame(self.content_frame)
        self.notes_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.notes_frame.grid_columnconfigure(0, weight=1)
        self.notes_frame.grid_rowconfigure(1, weight=1)
        
        # 笔记标题和操作按钮
        notes_header = ctk.CTkFrame(self.notes_frame)
        notes_header.grid(row=0, column=0, padx=15, pady=10, sticky="ew")
        notes_header.grid_columnconfigure(1, weight=1)
        
        notes_title = ctk.CTkLabel(
            notes_header,
            text="📝 学习笔记",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        notes_title.grid(row=0, column=0, sticky="w")
        
        # 笔记操作按钮
        notes_actions = ctk.CTkFrame(notes_header)
        notes_actions.grid(row=0, column=1, sticky="e")
        
        self.save_notes_btn = ctk.CTkButton(
            notes_actions,
            text="💾 保存笔记",
            command=self._save_notes,
            height=30,
            width=100
        )
        self.save_notes_btn.grid(row=0, column=0, padx=5)
        
        self.clear_notes_btn = ctk.CTkButton(
            notes_actions,
            text="🗑️ 清空",
            command=self._clear_notes,
            height=30,
            width=80,
            fg_color="#f44336",
            hover_color="#d32f2f"
        )
        self.clear_notes_btn.grid(row=0, column=1, padx=5)
        
        # 笔记文本框
        self.notes_textbox = ctk.CTkTextbox(
            self.notes_frame,
            height=120,
            font=ctk.CTkFont(size=12),
            wrap="word"
        )
        self.notes_textbox.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
    
    def refresh(self):
        """刷新任务详情显示"""
        try:
            self.current_task = self.app_manager.get_current_task()
            self._update_task_display()
            self._update_progress_display()
            self._load_notes()
            self.logger.info("任务详情刷新完成")
        except Exception as e:
            self.logger.error(f"刷新任务详情失败: {e}")
    
    def _update_task_display(self):
        """更新任务显示"""
        if not self.current_task:
            # 没有当前任务
            self.task_title.configure(text="🎉 所有任务已完成！")
            self.day_label.configure(text="天数: 已完成全部140天")
            self.stage_label.configure(text="阶段: 全部阶段已完成")
            self.difficulty_label.configure(text="难度: --")
            self.time_label.configure(text="预计时间: --")
            self.status_label.configure(text="状态: ✅ 全部完成")
            
            self.content_textbox.delete("1.0", "end")
            self.content_textbox.insert("1.0", "恭喜你！已经完成了所有的数学建模学习任务。\n\n你可以：\n1. 复习之前的学习内容\n2. 导出学习数据作为备份\n3. 开始新的学习计划")
            self.content_textbox.configure(state="disabled")
            
            # 禁用操作按钮
            self.complete_btn.configure(state="disabled")
            self.skip_btn.configure(state="disabled")
            
            return
        
        # 更新任务信息
        task = self.current_task
        self.task_title.configure(text=f"第{task['day']}天: {task['title']}")
        self.day_label.configure(text=f"天数: 第{task['day']}天")
        self.stage_label.configure(text=f"阶段: 第{task['stage']}阶段")
        self.difficulty_label.configure(text=f"难度: {task['difficulty']}")
        self.time_label.configure(text=f"预计时间: {task['estimated_time']}")
        self.status_label.configure(text="状态: ⏳ 待完成")
        
        # 更新任务内容
        self.content_textbox.configure(state="normal")
        self.content_textbox.delete("1.0", "end")
        self.content_textbox.insert("1.0", task['content'])
        self.content_textbox.configure(state="disabled")
        
        # 启用操作按钮
        self.complete_btn.configure(state="normal")
        self.skip_btn.configure(state="normal")
    
    def _update_progress_display(self):
        """更新进度显示"""
        stats = self.app_manager.get_learning_stats()
        
        completed = stats.get('completed_days', 0)
        total = stats.get('total_days', 140)
        completion_rate = stats.get('completion_rate', 0)
        
        # 更新进度条
        self.progress_bar.set(completion_rate / 100)
        
        # 更新进度文本
        self.progress_text.configure(text=f"{completed}/{total} ({completion_rate:.1f}%)")
    
    def _load_notes(self):
        """加载学习笔记"""
        if not self.current_task:
            self.notes_textbox.delete("1.0", "end")
            return
        
        day = self.current_task['day']
        notes = self.app_manager.get_task_notes(day)
        
        self.notes_textbox.delete("1.0", "end")
        if notes:
            self.notes_textbox.insert("1.0", notes)
    
    def _complete_task(self):
        """完成当前任务"""
        if not self.current_task:
            messagebox.showinfo("提示", "没有待完成的任务！")
            return
        
        # 确认对话框
        result = messagebox.askyesno(
            "确认完成",
            f"确定要完成任务：{self.current_task['title']}？"
        )
        
        if result:
            try:
                # 保存当前笔记
                self._save_notes()
                
                # 完成任务
                success = self.app_manager.complete_current_task()
                
                if success:
                    messagebox.showinfo("恭喜", f"任务 '{self.current_task['title']}' 已完成！")
                    self.refresh()  # 刷新显示
                else:
                    messagebox.showerror("错误", "完成任务失败，请重试")
                    
            except Exception as e:
                self.logger.error(f"完成任务失败: {e}")
                messagebox.showerror("错误", f"完成任务失败: {e}")
    
    def _skip_task(self):
        """跳过当前任务"""
        if not self.current_task:
            messagebox.showinfo("提示", "没有待完成的任务！")
            return
        
        # 确认对话框
        result = messagebox.askyesno(
            "确认跳过",
            f"确定要跳过任务：{self.current_task['title']}？\n\n跳过的任务将标记为未完成，但会继续下一个任务。"
        )
        
        if result:
            try:
                # 保存当前笔记
                self._save_notes()
                
                # 跳过任务
                success = self.app_manager.skip_current_task()
                
                if success:
                    messagebox.showinfo("提示", f"已跳过任务：{self.current_task['title']}")
                    self.refresh()  # 刷新显示
                else:
                    messagebox.showerror("错误", "跳过任务失败，请重试")
                    
            except Exception as e:
                self.logger.error(f"跳过任务失败: {e}")
                messagebox.showerror("错误", f"跳过任务失败: {e}")
    
    def _reset_progress(self):
        """重置学习进度"""
        result = messagebox.askyesno(
            "确认重置",
            "确定要重置所有学习进度吗？\n\n这将清除所有已完成的任务记录和笔记，此操作不可撤销！",
            icon="warning"
        )
        
        if result:
            # 二次确认
            result2 = messagebox.askyesno(
                "最终确认",
                "请再次确认：真的要重置所有学习进度吗？",
                icon="warning"
            )
            
            if result2:
                try:
                    success = self.app_manager.reset_all_progress()
                    
                    if success:
                        messagebox.showinfo("完成", "学习进度已重置")
                        self.refresh()  # 刷新显示
                    else:
                        messagebox.showerror("错误", "重置进度失败，请重试")
                        
                except Exception as e:
                    self.logger.error(f"重置进度失败: {e}")
                    messagebox.showerror("错误", f"重置进度失败: {e}")
    
    def _save_notes(self):
        """保存学习笔记"""
        if not self.current_task:
            return
        
        try:
            day = self.current_task['day']
            notes = self.notes_textbox.get("1.0", "end-1c")
            
            success = self.app_manager.save_task_notes(day, notes)
            
            if success:
                # 不显示成功消息，避免打扰用户
                self.logger.info(f"第{day}天的笔记已保存")
            else:
                messagebox.showerror("错误", "保存笔记失败")
                
        except Exception as e:
            self.logger.error(f"保存笔记失败: {e}")
            messagebox.showerror("错误", f"保存笔记失败: {e}")
    
    def _clear_notes(self):
        """清空学习笔记"""
        result = messagebox.askyesno(
            "确认清空",
            "确定要清空当前的学习笔记吗？"
        )
        
        if result:
            self.notes_textbox.delete("1.0", "end")