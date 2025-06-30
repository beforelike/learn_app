#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
历史面板组件
显示学习历史记录和已完成任务的详细信息
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Optional
from datetime import datetime

from ...core.app_manager import AppManager
from ...utils.logger import get_logger

class HistoryPanel(ctk.CTkFrame):
    """学习历史面板组件"""
    
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
        # 标题和控制区域
        self._create_header()
        
        # 主要内容区域
        self._create_content_area()
    
    def _create_header(self):
        """创建标题和控制区域"""
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.header_frame.grid_columnconfigure(1, weight=1)
        
        # 标题
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="📝 学习历史",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        # 控制按钮区域
        self.control_frame = ctk.CTkFrame(self.header_frame)
        self.control_frame.grid(row=0, column=1, padx=20, pady=10, sticky="e")
        
        # 筛选选项
        self.filter_label = ctk.CTkLabel(self.control_frame, text="筛选:")
        self.filter_label.grid(row=0, column=0, padx=5)
        
        self.filter_var = ctk.StringVar(value="全部")
        self.filter_combo = ctk.CTkComboBox(
            self.control_frame,
            values=["全部", "已完成", "未完成", "本周", "本月"],
            variable=self.filter_var,
            command=self._on_filter_changed,
            width=120
        )
        self.filter_combo.grid(row=0, column=1, padx=5)
        
        # 搜索框
        self.search_label = ctk.CTkLabel(self.control_frame, text="搜索:")
        self.search_label.grid(row=0, column=2, padx=(20, 5))
        
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            self.control_frame,
            textvariable=self.search_var,
            width=200
        )
        self.search_entry.grid(row=0, column=3, padx=5)
        self.search_entry.bind('<KeyRelease>', self._on_search_changed)
        
        # 刷新按钮
        self.refresh_btn = ctk.CTkButton(
            self.control_frame,
            text="🔄 刷新",
            command=self.refresh,
            width=80,
            height=30
        )
        self.refresh_btn.grid(row=0, column=4, padx=10)
    
    def _create_content_area(self):
        """创建主要内容区域"""
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # 创建分栏布局
        self.paned_window = ttk.PanedWindow(self.content_frame, orient=tk.HORIZONTAL)
        self.paned_window.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # 左侧：任务列表
        self._create_task_list()
        
        # 右侧：任务详情
        self._create_task_detail()
        
        # 添加到分栏窗口
        self.paned_window.add(self.list_frame, weight=2)
        self.paned_window.add(self.detail_frame, weight=1)
    
    def _create_task_list(self):
        """创建任务列表"""
        self.list_frame = ctk.CTkFrame(self.content_frame)
        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_rowconfigure(1, weight=1)
        
        # 列表标题
        list_title = ctk.CTkLabel(
            self.list_frame,
            text="任务列表",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        list_title.grid(row=0, column=0, pady=10)
        
        # 创建Treeview容器
        self.tree_container = ctk.CTkFrame(self.list_frame)
        self.tree_container.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
        self.tree_container.grid_columnconfigure(0, weight=1)
        self.tree_container.grid_rowconfigure(0, weight=1)
        
        # 创建Treeview
        self.tree = ttk.Treeview(
            self.tree_container,
            columns=("day", "title", "status", "difficulty", "stage", "completed_date"),
            show="headings",
            height=20
        )
        
        # 设置列标题
        self.tree.heading("day", text="天数")
        self.tree.heading("title", text="任务标题")
        self.tree.heading("status", text="状态")
        self.tree.heading("difficulty", text="难度")
        self.tree.heading("stage", text="阶段")
        self.tree.heading("completed_date", text="完成日期")
        
        # 设置列宽
        self.tree.column("day", width=60, anchor="center")
        self.tree.column("title", width=250, anchor="w")
        self.tree.column("status", width=80, anchor="center")
        self.tree.column("difficulty", width=80, anchor="center")
        self.tree.column("stage", width=80, anchor="center")
        self.tree.column("completed_date", width=120, anchor="center")
        
        # 添加滚动条
        v_scrollbar = ttk.Scrollbar(self.tree_container, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(self.tree_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # 布局
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # 绑定选择事件
        self.tree.bind("<<TreeviewSelect>>", self._on_task_selected)
        self.tree.bind("<Double-1>", self._on_task_double_click)
        
        # 右键菜单
        self._create_context_menu()
    
    def _create_task_detail(self):
        """创建任务详情区域"""
        self.detail_frame = ctk.CTkFrame(self.content_frame)
        self.detail_frame.grid_columnconfigure(0, weight=1)
        self.detail_frame.grid_rowconfigure(2, weight=1)
        
        # 详情标题
        detail_title = ctk.CTkLabel(
            self.detail_frame,
            text="任务详情",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        detail_title.grid(row=0, column=0, pady=10)
        
        # 任务信息区域
        self.info_frame = ctk.CTkFrame(self.detail_frame)
        self.info_frame.grid(row=1, column=0, padx=15, pady=10, sticky="ew")
        self.info_frame.grid_columnconfigure(1, weight=1)
        
        # 任务信息标签
        self.detail_day_label = ctk.CTkLabel(self.info_frame, text="天数: --")
        self.detail_day_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        self.detail_title_label = ctk.CTkLabel(self.info_frame, text="标题: --", wraplength=300)
        self.detail_title_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        self.detail_stage_label = ctk.CTkLabel(self.info_frame, text="阶段: --")
        self.detail_stage_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        self.detail_difficulty_label = ctk.CTkLabel(self.info_frame, text="难度: --")
        self.detail_difficulty_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        self.detail_time_label = ctk.CTkLabel(self.info_frame, text="预计时间: --")
        self.detail_time_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        
        self.detail_status_label = ctk.CTkLabel(self.info_frame, text="状态: --")
        self.detail_status_label.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        
        self.detail_completed_label = ctk.CTkLabel(self.info_frame, text="完成日期: --")
        self.detail_completed_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        # 任务内容区域
        content_label = ctk.CTkLabel(
            self.detail_frame,
            text="任务内容:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        content_label.grid(row=2, column=0, padx=15, pady=(10, 5), sticky="w")
        
        self.detail_content = ctk.CTkTextbox(
            self.detail_frame,
            height=200,
            font=ctk.CTkFont(size=12),
            wrap="word"
        )
        self.detail_content.grid(row=3, column=0, padx=15, pady=(0, 10), sticky="nsew")
        
        # 学习笔记区域
        notes_label = ctk.CTkLabel(
            self.detail_frame,
            text="学习笔记:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        notes_label.grid(row=4, column=0, padx=15, pady=(10, 5), sticky="w")
        
        self.detail_notes = ctk.CTkTextbox(
            self.detail_frame,
            height=150,
            font=ctk.CTkFont(size=12),
            wrap="word"
        )
        self.detail_notes.grid(row=5, column=0, padx=15, pady=(0, 15), sticky="nsew")
        
        self.detail_frame.grid_rowconfigure(5, weight=1)
        
        # 操作按钮
        self.action_frame = ctk.CTkFrame(self.detail_frame)
        self.action_frame.grid(row=6, column=0, padx=15, pady=10, sticky="ew")
        
        self.mark_complete_btn = ctk.CTkButton(
            self.action_frame,
            text="标记为完成",
            command=self._mark_as_completed,
            height=35,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.mark_complete_btn.grid(row=0, column=0, padx=5, pady=5)
        
        self.mark_incomplete_btn = ctk.CTkButton(
            self.action_frame,
            text="标记为未完成",
            command=self._mark_as_incomplete,
            height=35,
            fg_color="#f44336",
            hover_color="#d32f2f"
        )
        self.mark_incomplete_btn.grid(row=0, column=1, padx=5, pady=5)
        
        self.save_notes_btn = ctk.CTkButton(
            self.action_frame,
            text="保存笔记",
            command=self._save_notes,
            height=35
        )
        self.save_notes_btn.grid(row=0, column=2, padx=5, pady=5)
    
    def _create_context_menu(self):
        """创建右键菜单"""
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="查看详情", command=self._view_task_detail)
        self.context_menu.add_command(label="标记为完成", command=self._mark_as_completed)
        self.context_menu.add_command(label="标记为未完成", command=self._mark_as_incomplete)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="复制任务标题", command=self._copy_task_title)
        
        self.tree.bind("<Button-3>", self._show_context_menu)
    
    def refresh(self):
        """刷新历史显示"""
        try:
            self._load_task_list()
            self._clear_task_detail()
            self.logger.info("历史面板刷新完成")
        except Exception as e:
            self.logger.error(f"刷新历史面板失败: {e}")
    
    def _load_task_list(self):
        """加载任务列表"""
        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 获取所有任务和进度数据
        all_tasks = self.app_manager.learning_data.get_all_tasks()
        progress_data = self.app_manager.get_progress_data()
        completed_tasks = progress_data.get('completed_tasks', {})
        completion_dates = progress_data.get('completion_dates', {})
        
        # 应用筛选和搜索
        filtered_tasks = self._filter_tasks(all_tasks, completed_tasks, completion_dates)
        
        # 添加任务到树形视图
        for task in filtered_tasks:
            day = task['day']
            is_completed = completed_tasks.get(str(day), False)
            
            # 状态
            status = "✅ 已完成" if is_completed else "⏳ 待完成"
            
            # 完成日期
            completed_date = completion_dates.get(str(day), "") if is_completed else ""
            
            # 插入数据
            item = self.tree.insert("", "end", values=(
                day,
                task['title'],
                status,
                task['difficulty'],
                f"第{task['stage']}阶段",
                completed_date
            ))
            
            # 设置行颜色
            if is_completed:
                self.tree.set(item, "status", "✅ 已完成")
            else:
                self.tree.set(item, "status", "⏳ 待完成")
    
    def _filter_tasks(self, all_tasks: List[Dict], completed_tasks: Dict, completion_dates: Dict) -> List[Dict]:
        """筛选任务"""
        filtered_tasks = []
        filter_value = self.filter_var.get()
        search_text = self.search_var.get().lower()
        
        for task in all_tasks:
            day = task['day']
            is_completed = completed_tasks.get(str(day), False)
            
            # 应用筛选
            if filter_value == "已完成" and not is_completed:
                continue
            elif filter_value == "未完成" and is_completed:
                continue
            elif filter_value in ["本周", "本月"]:
                if not is_completed:
                    continue
                
                completed_date_str = completion_dates.get(str(day), "")
                if not completed_date_str:
                    continue
                
                try:
                    completed_date = datetime.strptime(completed_date_str, "%Y-%m-%d").date()
                    now = datetime.now().date()
                    
                    if filter_value == "本周":
                        # 计算本周的开始日期（周一）
                        days_since_monday = now.weekday()
                        week_start = now - timedelta(days=days_since_monday)
                        if completed_date < week_start:
                            continue
                    elif filter_value == "本月":
                        if completed_date.year != now.year or completed_date.month != now.month:
                            continue
                except:
                    continue
            
            # 应用搜索
            if search_text and search_text not in task['title'].lower():
                continue
            
            filtered_tasks.append(task)
        
        return filtered_tasks
    
    def _on_filter_changed(self, value):
        """筛选条件改变时的处理"""
        self._load_task_list()
    
    def _on_search_changed(self, event):
        """搜索条件改变时的处理"""
        self._load_task_list()
    
    def _on_task_selected(self, event):
        """任务选择时的处理"""
        selection = self.tree.selection()
        if not selection:
            self._clear_task_detail()
            return
        
        item = selection[0]
        values = self.tree.item(item, 'values')
        
        if values:
            day = int(values[0])
            self._show_task_detail(day)
    
    def _on_task_double_click(self, event):
        """任务双击时的处理"""
        self._view_task_detail()
    
    def _show_task_detail(self, day: int):
        """显示任务详情"""
        task = self.app_manager.learning_data.get_task_by_day(day)
        if not task:
            self._clear_task_detail()
            return
        
        progress_data = self.app_manager.get_progress_data()
        completed_tasks = progress_data.get('completed_tasks', {})
        completion_dates = progress_data.get('completion_dates', {})
        
        is_completed = completed_tasks.get(str(day), False)
        completed_date = completion_dates.get(str(day), "") if is_completed else ""
        
        # 更新任务信息
        self.detail_day_label.configure(text=f"天数: 第{task['day']}天")
        self.detail_title_label.configure(text=f"标题: {task['title']}")
        self.detail_stage_label.configure(text=f"阶段: 第{task['stage']}阶段")
        self.detail_difficulty_label.configure(text=f"难度: {task['difficulty']}")
        self.detail_time_label.configure(text=f"预计时间: {task['estimated_time']}")
        self.detail_status_label.configure(text=f"状态: {'✅ 已完成' if is_completed else '⏳ 待完成'}")
        self.detail_completed_label.configure(text=f"完成日期: {completed_date}")
        
        # 更新任务内容
        self.detail_content.configure(state="normal")
        self.detail_content.delete("1.0", "end")
        self.detail_content.insert("1.0", task['content'])
        self.detail_content.configure(state="disabled")
        
        # 加载学习笔记
        notes = self.app_manager.get_task_notes(day)
        self.detail_notes.delete("1.0", "end")
        if notes:
            self.detail_notes.insert("1.0", notes)
        
        # 更新按钮状态
        if is_completed:
            self.mark_complete_btn.configure(state="disabled")
            self.mark_incomplete_btn.configure(state="normal")
        else:
            self.mark_complete_btn.configure(state="normal")
            self.mark_incomplete_btn.configure(state="disabled")
        
        # 保存当前选中的任务
        self.selected_task_day = day
    
    def _clear_task_detail(self):
        """清空任务详情"""
        self.detail_day_label.configure(text="天数: --")
        self.detail_title_label.configure(text="标题: --")
        self.detail_stage_label.configure(text="阶段: --")
        self.detail_difficulty_label.configure(text="难度: --")
        self.detail_time_label.configure(text="预计时间: --")
        self.detail_status_label.configure(text="状态: --")
        self.detail_completed_label.configure(text="完成日期: --")
        
        self.detail_content.configure(state="normal")
        self.detail_content.delete("1.0", "end")
        self.detail_content.configure(state="disabled")
        
        self.detail_notes.delete("1.0", "end")
        
        self.mark_complete_btn.configure(state="disabled")
        self.mark_incomplete_btn.configure(state="disabled")
        
        self.selected_task_day = None
    
    def _show_context_menu(self, event):
        """显示右键菜单"""
        # 选择右键点击的项目
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def _view_task_detail(self):
        """查看任务详情（弹窗）"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.tree.item(item, 'values')
        
        if values:
            day = int(values[0])
            task = self.app_manager.learning_data.get_task_by_day(day)
            
            if task:
                self._show_task_detail_dialog(task)
    
    def _show_task_detail_dialog(self, task: Dict):
        """显示任务详情对话框"""
        detail_window = ctk.CTkToplevel(self)
        detail_window.title(f"任务详情 - 第{task['day']}天")
        detail_window.geometry("700x500")
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
        progress_data = self.app_manager.get_progress_data()
        completed_tasks = progress_data.get('completed_tasks', {})
        completion_dates = progress_data.get('completion_dates', {})
        
        is_completed = completed_tasks.get(str(task['day']), False)
        completed_date = completion_dates.get(str(task['day']), "") if is_completed else "未完成"
        
        info_items = [
            ("天数", f"第{task['day']}天"),
            ("阶段", f"第{task['stage']}阶段"),
            ("难度", task['difficulty']),
            ("预计时间", task['estimated_time']),
            ("状态", "✅ 已完成" if is_completed else "⏳ 待完成"),
            ("完成日期", completed_date)
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
        
        content_text = ctk.CTkTextbox(content_frame, height=200)
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
    
    def _mark_as_completed(self):
        """标记为已完成"""
        if not hasattr(self, 'selected_task_day') or self.selected_task_day is None:
            messagebox.showwarning("警告", "请先选择一个任务")
            return
        
        try:
            success = self.app_manager.mark_task_completed(self.selected_task_day)
            if success:
                messagebox.showinfo("成功", "任务已标记为完成")
                self.refresh()
            else:
                messagebox.showerror("错误", "标记任务失败")
        except Exception as e:
            self.logger.error(f"标记任务完成失败: {e}")
            messagebox.showerror("错误", f"标记任务失败: {e}")
    
    def _mark_as_incomplete(self):
        """标记为未完成"""
        if not hasattr(self, 'selected_task_day') or self.selected_task_day is None:
            messagebox.showwarning("警告", "请先选择一个任务")
            return
        
        try:
            success = self.app_manager.mark_task_incomplete(self.selected_task_day)
            if success:
                messagebox.showinfo("成功", "任务已标记为未完成")
                self.refresh()
            else:
                messagebox.showerror("错误", "标记任务失败")
        except Exception as e:
            self.logger.error(f"标记任务未完成失败: {e}")
            messagebox.showerror("错误", f"标记任务失败: {e}")
    
    def _save_notes(self):
        """保存学习笔记"""
        if not hasattr(self, 'selected_task_day') or self.selected_task_day is None:
            messagebox.showwarning("警告", "请先选择一个任务")
            return
        
        try:
            notes = self.detail_notes.get("1.0", "end-1c")
            success = self.app_manager.save_task_notes(self.selected_task_day, notes)
            
            if success:
                messagebox.showinfo("成功", "学习笔记已保存")
            else:
                messagebox.showerror("错误", "保存笔记失败")
        except Exception as e:
            self.logger.error(f"保存笔记失败: {e}")
            messagebox.showerror("错误", f"保存笔记失败: {e}")
    
    def _copy_task_title(self):
        """复制任务标题"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.tree.item(item, 'values')
        
        if values:
            title = values[1]  # 任务标题在第二列
            self.clipboard_clear()
            self.clipboard_append(title)
            messagebox.showinfo("成功", "任务标题已复制到剪贴板")