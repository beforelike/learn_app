#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主窗口GUI界面
使用CustomTkinter构建现代化的用户界面
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Dict, Optional
from datetime import datetime
import threading

from ..core.app_manager import AppManager
from ..config.settings import AppSettings
from ..utils.logger import get_logger
from .components.progress_card import ProgressCard
from .components.task_detail import TaskDetailFrame
from .components.stats_panel import StatsPanel
from .components.history_panel import HistoryPanel
from .components.settings_panel import SettingsPanel

class MainWindow(ctk.CTk):
    """主窗口类"""
    
    def __init__(self, app_manager: AppManager, settings: AppSettings):
        super().__init__()
        
        self.app_manager = app_manager
        self.settings = settings
        self.logger = get_logger(__name__)
        
        # 窗口配置
        self.title("数学建模学习进度追踪 - Python版")
        self.geometry("1200x800")
        self.minsize(800, 600)
        
        # 设置窗口图标（如果有的话）
        try:
            self.iconbitmap("assets/icon.ico")
        except:
            pass
        
        # 初始化UI
        self._setup_ui()
        self._load_initial_data()
        
        # 绑定窗口关闭事件
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        self.logger.info("主窗口初始化完成")
    
    def _setup_ui(self):
        """设置用户界面"""
        # 创建主框架
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # 侧边栏
        self._create_sidebar()
        
        # 主内容区域
        self._create_main_content()
        
        # 状态栏
        self._create_status_bar()
    
    def _create_sidebar(self):
        """创建侧边栏"""
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        # 应用标题
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="数学建模学习",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # 导航按钮
        self.nav_buttons = {}
        nav_items = [
            ("home", "📚 学习首页", self._show_home),
            ("progress", "📊 学习进度", self._show_progress),
            ("history", "📝 学习历史", self._show_history),
            ("stats", "📈 统计分析", self._show_stats),
            ("settings", "⚙️ 设置", self._show_settings)
        ]
        
        for i, (key, text, command) in enumerate(nav_items, 1):
            btn = ctk.CTkButton(
                self.sidebar_frame,
                text=text,
                command=command,
                height=40,
                font=ctk.CTkFont(size=14)
            )
            btn.grid(row=i, column=0, padx=20, pady=10, sticky="ew")
            self.nav_buttons[key] = btn
        
        # 快速操作区域
        self.quick_actions_frame = ctk.CTkFrame(self.sidebar_frame)
        self.quick_actions_frame.grid(row=6, column=0, padx=20, pady=20, sticky="ew")
        
        # 完成当前任务按钮
        self.complete_btn = ctk.CTkButton(
            self.quick_actions_frame,
            text="✅ 完成当前任务",
            command=self._complete_current_task,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.complete_btn.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # 导出数据按钮
        self.export_btn = ctk.CTkButton(
            self.quick_actions_frame,
            text="💾 导出数据",
            command=self._export_data,
            height=35
        )
        self.export_btn.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        # 导入数据按钮
        self.import_btn = ctk.CTkButton(
            self.quick_actions_frame,
            text="📁 导入数据",
            command=self._import_data,
            height=35
        )
        self.import_btn.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
    
    def _create_main_content(self):
        """创建主内容区域"""
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # 创建内容容器
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # 初始化各个面板
        self._init_panels()
        
        # 默认显示首页
        self._show_home()
    
    def _init_panels(self):
        """初始化各个面板"""
        # 首页面板
        self.home_panel = self._create_home_panel()
        
        # 进度面板
        self.progress_panel = ProgressCard(self.content_frame, self.app_manager)
        
        # 历史面板
        self.history_panel = HistoryPanel(self.content_frame, self.app_manager)
        
        # 统计面板
        self.stats_panel = StatsPanel(self.content_frame, self.app_manager)
        
        # 设置面板
        self.settings_panel = SettingsPanel(self.content_frame, self.settings)
        
        # 隐藏所有面板
        for panel in [self.home_panel, self.progress_panel, self.history_panel, 
                     self.stats_panel, self.settings_panel]:
            panel.grid_remove()
    
    def _create_home_panel(self):
        """创建首页面板"""
        panel = ctk.CTkFrame(self.content_frame)
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(1, weight=1)
        
        # 欢迎标题
        welcome_label = ctk.CTkLabel(
            panel,
            text="欢迎使用数学建模学习系统",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        welcome_label.grid(row=0, column=0, pady=20)
        
        # 主要内容区域
        content_container = ctk.CTkFrame(panel)
        content_container.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        content_container.grid_columnconfigure((0, 1), weight=1)
        content_container.grid_rowconfigure(1, weight=1)
        
        # 当前任务卡片
        self.current_task_frame = ctk.CTkFrame(content_container)
        self.current_task_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # 学习统计卡片
        self.stats_summary_frame = ctk.CTkFrame(content_container)
        self.stats_summary_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # 任务详情区域
        self.task_detail_frame = TaskDetailFrame(content_container, self.app_manager)
        self.task_detail_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        return panel
    
    def _create_status_bar(self):
        """创建状态栏"""
        self.status_frame = ctk.CTkFrame(self, height=30)
        self.status_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.status_frame.grid_columnconfigure(1, weight=1)
        
        # 状态标签
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="就绪",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=0, column=0, padx=10, pady=5)
        
        # 时间标签
        self.time_label = ctk.CTkLabel(
            self.status_frame,
            text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            font=ctk.CTkFont(size=12)
        )
        self.time_label.grid(row=0, column=2, padx=10, pady=5)
        
        # 定时更新时间
        self._update_time()
    
    def _update_time(self):
        """更新时间显示"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.configure(text=current_time)
        self.after(1000, self._update_time)
    
    def _load_initial_data(self):
        """加载初始数据"""
        try:
            self._update_current_task_display()
            self._update_stats_summary()
            self.set_status("数据加载完成")
        except Exception as e:
            self.logger.error(f"加载初始数据失败: {e}")
            self.set_status(f"加载数据失败: {e}")
    
    def _update_current_task_display(self):
        """更新当前任务显示"""
        current_task = self.app_manager.get_current_task()
        
        # 清空当前任务框架
        for widget in self.current_task_frame.winfo_children():
            widget.destroy()
        
        if current_task:
            # 任务标题
            title_label = ctk.CTkLabel(
                self.current_task_frame,
                text=f"第{current_task.get('day', 0)}天: {current_task.get('title', '未知任务')}",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            title_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
            
            # 任务描述
            desc_label = ctk.CTkLabel(
                self.current_task_frame,
                text=current_task.get('content', ''),
                font=ctk.CTkFont(size=14),
                wraplength=400
            )
            desc_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")
            
            # 难度和时间
            info_label = ctk.CTkLabel(
                self.current_task_frame,
                text=f"难度: {current_task.get('difficulty', '未知')} | 预计时间: {current_task.get('estimated_time', '未知')}",
                font=ctk.CTkFont(size=12)
            )
            info_label.grid(row=2, column=0, padx=20, pady=5, sticky="w")
        else:
            # 没有当前任务
            no_task_label = ctk.CTkLabel(
                self.current_task_frame,
                text="🎉 恭喜！所有任务已完成！",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            no_task_label.grid(row=0, column=0, padx=20, pady=20)
    
    def _update_stats_summary(self):
        """更新统计摘要"""
        stats = self.app_manager.get_learning_stats()
        
        # 清空统计框架
        for widget in self.stats_summary_frame.winfo_children():
            widget.destroy()
        
        # 标题
        title_label = ctk.CTkLabel(
            self.stats_summary_frame,
            text="学习统计",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=10)
        
        # 统计信息
        stats_info = [
            ("总进度", f"{stats.get('completed_days', 0)}/{stats.get('total_days', 140)}天"),
            ("完成率", f"{stats.get('completion_rate', 0):.1f}%"),
            ("当前阶段", f"第{stats.get('current_stage', 1)}阶段"),
            ("学习天数", f"{stats.get('days_since_start', 0)}天")
        ]
        
        for i, (label, value) in enumerate(stats_info, 1):
            info_frame = ctk.CTkFrame(self.stats_summary_frame)
            info_frame.grid(row=i, column=0, padx=20, pady=5, sticky="ew")
            
            label_widget = ctk.CTkLabel(info_frame, text=label, font=ctk.CTkFont(size=12))
            label_widget.grid(row=0, column=0, padx=10, pady=5, sticky="w")
            
            value_widget = ctk.CTkLabel(info_frame, text=value, font=ctk.CTkFont(size=12, weight="bold"))
            value_widget.grid(row=0, column=1, padx=10, pady=5, sticky="e")
            
            info_frame.grid_columnconfigure(1, weight=1)
    
    def _show_home(self):
        """显示首页"""
        self._hide_all_panels()
        self.home_panel.grid(row=0, column=0, sticky="nsew")
        self._update_current_task_display()
        self._update_stats_summary()
        self.task_detail_frame.refresh()
        self.set_status("显示首页")
    
    def _show_progress(self):
        """显示进度页面"""
        self._hide_all_panels()
        self.progress_panel.grid(row=0, column=0, sticky="nsew")
        self.progress_panel.refresh()
        self.set_status("显示学习进度")
    
    def _show_history(self):
        """显示历史页面"""
        self._hide_all_panels()
        self.history_panel.grid(row=0, column=0, sticky="nsew")
        self.history_panel.refresh()
        self.set_status("显示学习历史")
    
    def _show_stats(self):
        """显示统计页面"""
        self._hide_all_panels()
        self.stats_panel.grid(row=0, column=0, sticky="nsew")
        self.stats_panel.refresh()
        self.set_status("显示统计分析")
    
    def _show_settings(self):
        """显示设置页面"""
        self._hide_all_panels()
        self.settings_panel.grid(row=0, column=0, sticky="nsew")
        self.set_status("显示设置")
    
    def _hide_all_panels(self):
        """隐藏所有面板"""
        for panel in [self.home_panel, self.progress_panel, self.history_panel, 
                     self.stats_panel, self.settings_panel]:
            panel.grid_remove()
    
    def _complete_current_task(self):
        """完成当前任务"""
        try:
            current_task = self.app_manager.get_current_task()
            if not current_task:
                messagebox.showinfo("提示", "没有待完成的任务！")
                return
            
            # 确认对话框
            result = messagebox.askyesno(
                "确认完成",
                f"确定要完成任务：{current_task.get('title', '')}？"
            )
            
            if result:
                # 在后台线程中完成任务
                def complete_task():
                    success = self.app_manager.complete_current_task()
                    
                    # 在主线程中更新UI
                    self.after(0, lambda: self._on_task_completed(success, current_task))
                
                threading.Thread(target=complete_task, daemon=True).start()
                self.set_status("正在完成任务...")
                
        except Exception as e:
            self.logger.error(f"完成任务失败: {e}")
            messagebox.showerror("错误", f"完成任务失败: {e}")
    
    def _on_task_completed(self, success: bool, task: Dict):
        """任务完成后的回调"""
        if success:
            messagebox.showinfo("恭喜", f"任务 '{task.get('title', '')}' 已完成！")
            self._update_current_task_display()
            self._update_stats_summary()
            self.set_status("任务完成")
        else:
            messagebox.showerror("错误", "完成任务失败，请重试")
            self.set_status("任务完成失败")
    
    def _export_data(self):
        """导出数据"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="导出学习数据",
                defaultextension=".json",
                filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
            )
            
            if file_path:
                success = self.app_manager.export_progress(file_path)
                if success:
                    messagebox.showinfo("成功", f"数据已导出到: {file_path}")
                    self.set_status(f"数据已导出: {file_path}")
                else:
                    messagebox.showerror("错误", "导出数据失败")
                    self.set_status("导出失败")
        except Exception as e:
            self.logger.error(f"导出数据失败: {e}")
            messagebox.showerror("错误", f"导出数据失败: {e}")
    
    def _import_data(self):
        """导入数据"""
        try:
            file_path = filedialog.askopenfilename(
                title="导入学习数据",
                filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
            )
            
            if file_path:
                result = messagebox.askyesno(
                    "确认导入",
                    "导入数据将覆盖当前的学习进度，确定要继续吗？"
                )
                
                if result:
                    success = self.app_manager.import_progress(file_path)
                    if success:
                        messagebox.showinfo("成功", "数据导入成功")
                        self._load_initial_data()  # 重新加载数据
                        self.set_status(f"数据已导入: {file_path}")
                    else:
                        messagebox.showerror("错误", "导入数据失败")
                        self.set_status("导入失败")
        except Exception as e:
            self.logger.error(f"导入数据失败: {e}")
            messagebox.showerror("错误", f"导入数据失败: {e}")
    
    def set_status(self, message: str):
        """设置状态栏消息"""
        self.status_label.configure(text=message)
        self.logger.info(f"状态: {message}")
    
    def _on_closing(self):
        """窗口关闭事件处理"""
        try:
            result = messagebox.askyesno("确认退出", "确定要退出应用吗？")
            if result:
                self.app_manager.save_all_data()
                self.destroy()
        except Exception as e:
            self.logger.error(f"关闭窗口时出错: {e}")
            self.destroy()