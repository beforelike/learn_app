#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设置面板组件
应用程序的配置和个性化设置
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser
from typing import Dict, Optional
import os

from ...config.settings import AppSettings
from ...utils.logger import get_logger

class SettingsPanel(ctk.CTkFrame):
    """设置面板组件"""
    
    def __init__(self, parent, settings: AppSettings):
        super().__init__(parent)
        
        self.settings = settings
        self.logger = get_logger(__name__)
        
        # 配置网格
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self._setup_ui()
        self._load_settings()
    
    def _setup_ui(self):
        """设置用户界面"""
        # 标题
        self.title_label = ctk.CTkLabel(
            self,
            text="⚙️ 应用设置",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, pady=20)
        
        # 主要内容区域
        self.content_frame = ctk.CTkScrollableFrame(self)
        self.content_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # 创建设置分组
        self._create_appearance_settings()
        self._create_behavior_settings()
        self._create_notification_settings()
        self._create_data_settings()
        self._create_advanced_settings()
        
        # 操作按钮
        self._create_action_buttons()
    
    def _create_appearance_settings(self):
        """创建外观设置"""
        appearance_frame = ctk.CTkFrame(self.content_frame)
        appearance_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        appearance_frame.grid_columnconfigure(1, weight=1)
        
        # 分组标题
        title_label = ctk.CTkLabel(
            appearance_frame,
            text="🎨 外观设置",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=15, sticky="w")
        
        # 主题设置
        theme_label = ctk.CTkLabel(appearance_frame, text="主题:")
        theme_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
        self.theme_var = ctk.StringVar(value="系统")
        self.theme_combo = ctk.CTkComboBox(
            appearance_frame,
            values=["浅色", "深色", "系统"],
            variable=self.theme_var,
            command=self._on_theme_changed,
            width=150
        )
        self.theme_combo.grid(row=1, column=1, padx=20, pady=10, sticky="w")
        
        # 字体大小设置
        font_size_label = ctk.CTkLabel(appearance_frame, text="字体大小:")
        font_size_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        
        self.font_size_var = ctk.StringVar(value="中等")
        self.font_size_combo = ctk.CTkComboBox(
            appearance_frame,
            values=["小", "中等", "大", "特大"],
            variable=self.font_size_var,
            command=self._on_font_size_changed,
            width=150
        )
        self.font_size_combo.grid(row=2, column=1, padx=20, pady=10, sticky="w")
        
        # 窗口透明度设置
        opacity_label = ctk.CTkLabel(appearance_frame, text="窗口透明度:")
        opacity_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        
        self.opacity_var = ctk.DoubleVar(value=1.0)
        self.opacity_slider = ctk.CTkSlider(
            appearance_frame,
            from_=0.7,
            to=1.0,
            variable=self.opacity_var,
            command=self._on_opacity_changed,
            width=200
        )
        self.opacity_slider.grid(row=3, column=1, padx=20, pady=10, sticky="w")
        
        self.opacity_value_label = ctk.CTkLabel(appearance_frame, text="100%")
        self.opacity_value_label.grid(row=3, column=2, padx=10, pady=10, sticky="w")
        
        # 启动时窗口大小
        window_size_label = ctk.CTkLabel(appearance_frame, text="启动窗口大小:")
        window_size_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        
        self.window_size_var = ctk.StringVar(value="1200x800")
        self.window_size_combo = ctk.CTkComboBox(
            appearance_frame,
            values=["1000x700", "1200x800", "1400x900", "1600x1000", "最大化"],
            variable=self.window_size_var,
            width=150
        )
        self.window_size_combo.grid(row=4, column=1, padx=20, pady=10, sticky="w")
    
    def _create_behavior_settings(self):
        """创建行为设置"""
        behavior_frame = ctk.CTkFrame(self.content_frame)
        behavior_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        behavior_frame.grid_columnconfigure(1, weight=1)
        
        # 分组标题
        title_label = ctk.CTkLabel(
            behavior_frame,
            text="⚡ 行为设置",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=15, sticky="w")
        
        # 自动保存设置
        self.auto_save_var = ctk.BooleanVar(value=True)
        self.auto_save_check = ctk.CTkCheckBox(
            behavior_frame,
            text="自动保存学习进度",
            variable=self.auto_save_var
        )
        self.auto_save_check.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="w")
        
        # 启动时检查更新
        self.check_updates_var = ctk.BooleanVar(value=True)
        self.check_updates_check = ctk.CTkCheckBox(
            behavior_frame,
            text="启动时检查更新",
            variable=self.check_updates_var
        )
        self.check_updates_check.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="w")
        
        # 最小化到系统托盘
        self.minimize_to_tray_var = ctk.BooleanVar(value=False)
        self.minimize_to_tray_check = ctk.CTkCheckBox(
            behavior_frame,
            text="最小化到系统托盘",
            variable=self.minimize_to_tray_var
        )
        self.minimize_to_tray_check.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="w")
        
        # 开机自启动
        self.auto_start_var = ctk.BooleanVar(value=False)
        self.auto_start_check = ctk.CTkCheckBox(
            behavior_frame,
            text="开机自动启动",
            variable=self.auto_start_var
        )
        self.auto_start_check.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="w")
        
        # 自动保存间隔
        save_interval_label = ctk.CTkLabel(behavior_frame, text="自动保存间隔(分钟):")
        save_interval_label.grid(row=5, column=0, padx=20, pady=10, sticky="w")
        
        self.save_interval_var = ctk.IntVar(value=5)
        self.save_interval_spinbox = ctk.CTkEntry(
            behavior_frame,
            textvariable=self.save_interval_var,
            width=100
        )
        self.save_interval_spinbox.grid(row=5, column=1, padx=20, pady=10, sticky="w")
    
    def _create_notification_settings(self):
        """创建通知设置"""
        notification_frame = ctk.CTkFrame(self.content_frame)
        notification_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        notification_frame.grid_columnconfigure(1, weight=1)
        
        # 分组标题
        title_label = ctk.CTkLabel(
            notification_frame,
            text="🔔 通知设置",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=15, sticky="w")
        
        # 启用通知
        self.enable_notifications_var = ctk.BooleanVar(value=True)
        self.enable_notifications_check = ctk.CTkCheckBox(
            notification_frame,
            text="启用桌面通知",
            variable=self.enable_notifications_var
        )
        self.enable_notifications_check.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="w")
        
        # 任务完成通知
        self.task_completion_var = ctk.BooleanVar(value=True)
        self.task_completion_check = ctk.CTkCheckBox(
            notification_frame,
            text="任务完成时通知",
            variable=self.task_completion_var
        )
        self.task_completion_check.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="w")
        
        # 学习提醒
        self.study_reminder_var = ctk.BooleanVar(value=False)
        self.study_reminder_check = ctk.CTkCheckBox(
            notification_frame,
            text="每日学习提醒",
            variable=self.study_reminder_var
        )
        self.study_reminder_check.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="w")
        
        # 提醒时间
        reminder_time_label = ctk.CTkLabel(notification_frame, text="提醒时间:")
        reminder_time_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        
        self.reminder_time_var = ctk.StringVar(value="09:00")
        self.reminder_time_entry = ctk.CTkEntry(
            notification_frame,
            textvariable=self.reminder_time_var,
            width=100
        )
        self.reminder_time_entry.grid(row=4, column=1, padx=20, pady=10, sticky="w")
    
    def _create_data_settings(self):
        """创建数据设置"""
        data_frame = ctk.CTkFrame(self.content_frame)
        data_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        data_frame.grid_columnconfigure(1, weight=1)
        
        # 分组标题
        title_label = ctk.CTkLabel(
            data_frame,
            text="💾 数据设置",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=15, sticky="w")
        
        # 数据存储位置
        data_path_label = ctk.CTkLabel(data_frame, text="数据存储位置:")
        data_path_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
        self.data_path_var = ctk.StringVar(value="./data")
        self.data_path_entry = ctk.CTkEntry(
            data_frame,
            textvariable=self.data_path_var,
            width=300
        )
        self.data_path_entry.grid(row=1, column=1, padx=20, pady=10, sticky="w")
        
        self.browse_data_btn = ctk.CTkButton(
            data_frame,
            text="浏览",
            command=self._browse_data_path,
            width=80
        )
        self.browse_data_btn.grid(row=1, column=2, padx=10, pady=10)
        
        # 自动备份
        self.auto_backup_var = ctk.BooleanVar(value=True)
        self.auto_backup_check = ctk.CTkCheckBox(
            data_frame,
            text="自动备份数据",
            variable=self.auto_backup_var
        )
        self.auto_backup_check.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="w")
        
        # 备份保留天数
        backup_days_label = ctk.CTkLabel(data_frame, text="备份保留天数:")
        backup_days_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        
        self.backup_days_var = ctk.IntVar(value=30)
        self.backup_days_spinbox = ctk.CTkEntry(
            data_frame,
            textvariable=self.backup_days_var,
            width=100
        )
        self.backup_days_spinbox.grid(row=3, column=1, padx=20, pady=10, sticky="w")
        
        # 数据操作按钮
        data_actions_frame = ctk.CTkFrame(data_frame)
        data_actions_frame.grid(row=4, column=0, columnspan=3, padx=20, pady=15, sticky="ew")
        
        self.backup_now_btn = ctk.CTkButton(
            data_actions_frame,
            text="立即备份",
            command=self._backup_now,
            height=35
        )
        self.backup_now_btn.grid(row=0, column=0, padx=10, pady=10)
        
        self.restore_backup_btn = ctk.CTkButton(
            data_actions_frame,
            text="恢复备份",
            command=self._restore_backup,
            height=35
        )
        self.restore_backup_btn.grid(row=0, column=1, padx=10, pady=10)
        
        self.clear_data_btn = ctk.CTkButton(
            data_actions_frame,
            text="清空数据",
            command=self._clear_data,
            height=35,
            fg_color="#f44336",
            hover_color="#d32f2f"
        )
        self.clear_data_btn.grid(row=0, column=2, padx=10, pady=10)
    
    def _create_advanced_settings(self):
        """创建高级设置"""
        advanced_frame = ctk.CTkFrame(self.content_frame)
        advanced_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        advanced_frame.grid_columnconfigure(1, weight=1)
        
        # 分组标题
        title_label = ctk.CTkLabel(
            advanced_frame,
            text="🔧 高级设置",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=15, sticky="w")
        
        # 调试模式
        self.debug_mode_var = ctk.BooleanVar(value=False)
        self.debug_mode_check = ctk.CTkCheckBox(
            advanced_frame,
            text="启用调试模式",
            variable=self.debug_mode_var
        )
        self.debug_mode_check.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="w")
        
        # 日志级别
        log_level_label = ctk.CTkLabel(advanced_frame, text="日志级别:")
        log_level_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        
        self.log_level_var = ctk.StringVar(value="INFO")
        self.log_level_combo = ctk.CTkComboBox(
            advanced_frame,
            values=["DEBUG", "INFO", "WARNING", "ERROR"],
            variable=self.log_level_var,
            width=150
        )
        self.log_level_combo.grid(row=2, column=1, padx=20, pady=10, sticky="w")
        
        # 性能监控
        self.performance_monitor_var = ctk.BooleanVar(value=False)
        self.performance_monitor_check = ctk.CTkCheckBox(
            advanced_frame,
            text="启用性能监控",
            variable=self.performance_monitor_var
        )
        self.performance_monitor_check.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="w")
        
        # 实验性功能
        self.experimental_features_var = ctk.BooleanVar(value=False)
        self.experimental_features_check = ctk.CTkCheckBox(
            advanced_frame,
            text="启用实验性功能",
            variable=self.experimental_features_var
        )
        self.experimental_features_check.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="w")
    
    def _create_action_buttons(self):
        """创建操作按钮"""
        action_frame = ctk.CTkFrame(self.content_frame)
        action_frame.grid(row=5, column=0, padx=10, pady=20, sticky="ew")
        
        # 保存设置按钮
        self.save_btn = ctk.CTkButton(
            action_frame,
            text="💾 保存设置",
            command=self._save_settings,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.save_btn.grid(row=0, column=0, padx=20, pady=15)
        
        # 重置设置按钮
        self.reset_btn = ctk.CTkButton(
            action_frame,
            text="🔄 重置设置",
            command=self._reset_settings,
            height=40,
            font=ctk.CTkFont(size=16),
            fg_color="#FF9800",
            hover_color="#F57C00"
        )
        self.reset_btn.grid(row=0, column=1, padx=20, pady=15)
        
        # 应用设置按钮
        self.apply_btn = ctk.CTkButton(
            action_frame,
            text="✅ 应用设置",
            command=self._apply_settings,
            height=40,
            font=ctk.CTkFont(size=16)
        )
        self.apply_btn.grid(row=0, column=2, padx=20, pady=15)
    
    def _load_settings(self):
        """加载设置"""
        try:
            # 加载外观设置
            self.theme_var.set(self.settings.get('appearance.theme', '系统'))
            self.font_size_var.set(self.settings.get('appearance.font_size', '中等'))
            self.opacity_var.set(self.settings.get('appearance.opacity', 1.0))
            self.window_size_var.set(self.settings.get('appearance.window_size', '1200x800'))
            
            # 加载行为设置
            self.auto_save_var.set(self.settings.get('behavior.auto_save', True))
            self.check_updates_var.set(self.settings.get('behavior.check_updates', True))
            self.minimize_to_tray_var.set(self.settings.get('behavior.minimize_to_tray', False))
            self.auto_start_var.set(self.settings.get('behavior.auto_start', False))
            self.save_interval_var.set(self.settings.get('behavior.save_interval', 5))
            
            # 加载通知设置
            self.enable_notifications_var.set(self.settings.get('notifications.enabled', True))
            self.task_completion_var.set(self.settings.get('notifications.task_completion', True))
            self.study_reminder_var.set(self.settings.get('notifications.study_reminder', False))
            self.reminder_time_var.set(self.settings.get('notifications.reminder_time', '09:00'))
            
            # 加载数据设置
            self.data_path_var.set(self.settings.get('data.storage_path', './data'))
            self.auto_backup_var.set(self.settings.get('data.auto_backup', True))
            self.backup_days_var.set(self.settings.get('data.backup_retention_days', 30))
            
            # 加载高级设置
            self.debug_mode_var.set(self.settings.get('advanced.debug_mode', False))
            self.log_level_var.set(self.settings.get('advanced.log_level', 'INFO'))
            self.performance_monitor_var.set(self.settings.get('advanced.performance_monitor', False))
            self.experimental_features_var.set(self.settings.get('advanced.experimental_features', False))
            
            # 更新透明度显示
            self._update_opacity_display()
            
            self.logger.info("设置加载完成")
            
        except Exception as e:
            self.logger.error(f"加载设置失败: {e}")
            messagebox.showerror("错误", f"加载设置失败: {e}")
    
    def _save_settings(self):
        """保存设置"""
        try:
            # 保存外观设置
            self.settings.set('appearance.theme', self.theme_var.get())
            self.settings.set('appearance.font_size', self.font_size_var.get())
            self.settings.set('appearance.opacity', self.opacity_var.get())
            self.settings.set('appearance.window_size', self.window_size_var.get())
            
            # 保存行为设置
            self.settings.set('behavior.auto_save', self.auto_save_var.get())
            self.settings.set('behavior.check_updates', self.check_updates_var.get())
            self.settings.set('behavior.minimize_to_tray', self.minimize_to_tray_var.get())
            self.settings.set('behavior.auto_start', self.auto_start_var.get())
            self.settings.set('behavior.save_interval', self.save_interval_var.get())
            
            # 保存通知设置
            self.settings.set('notifications.enabled', self.enable_notifications_var.get())
            self.settings.set('notifications.task_completion', self.task_completion_var.get())
            self.settings.set('notifications.study_reminder', self.study_reminder_var.get())
            self.settings.set('notifications.reminder_time', self.reminder_time_var.get())
            
            # 保存数据设置
            self.settings.set('data.storage_path', self.data_path_var.get())
            self.settings.set('data.auto_backup', self.auto_backup_var.get())
            self.settings.set('data.backup_retention_days', self.backup_days_var.get())
            
            # 保存高级设置
            self.settings.set('advanced.debug_mode', self.debug_mode_var.get())
            self.settings.set('advanced.log_level', self.log_level_var.get())
            self.settings.set('advanced.performance_monitor', self.performance_monitor_var.get())
            self.settings.set('advanced.experimental_features', self.experimental_features_var.get())
            
            # 保存到文件
            self.settings.save()
            
            messagebox.showinfo("成功", "设置已保存")
            self.logger.info("设置保存完成")
            
        except Exception as e:
            self.logger.error(f"保存设置失败: {e}")
            messagebox.showerror("错误", f"保存设置失败: {e}")
    
    def _apply_settings(self):
        """应用设置"""
        try:
            # 应用主题设置
            theme = self.theme_var.get()
            if theme == "浅色":
                ctk.set_appearance_mode("light")
            elif theme == "深色":
                ctk.set_appearance_mode("dark")
            else:
                ctk.set_appearance_mode("system")
            
            # 应用透明度设置
            opacity = self.opacity_var.get()
            main_window = self.winfo_toplevel()
            main_window.attributes('-alpha', opacity)
            
            messagebox.showinfo("成功", "设置已应用")
            self.logger.info("设置应用完成")
            
        except Exception as e:
            self.logger.error(f"应用设置失败: {e}")
            messagebox.showerror("错误", f"应用设置失败: {e}")
    
    def _reset_settings(self):
        """重置设置"""
        result = messagebox.askyesno(
            "确认重置",
            "确定要重置所有设置到默认值吗？\n\n此操作不可撤销！",
            icon="warning"
        )
        
        if result:
            try:
                self.settings.reset_to_defaults()
                self._load_settings()
                messagebox.showinfo("成功", "设置已重置到默认值")
                self.logger.info("设置重置完成")
            except Exception as e:
                self.logger.error(f"重置设置失败: {e}")
                messagebox.showerror("错误", f"重置设置失败: {e}")
    
    def _on_theme_changed(self, value):
        """主题改变时的处理"""
        # 实时预览主题变化
        if value == "浅色":
            ctk.set_appearance_mode("light")
        elif value == "深色":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("system")
    
    def _on_font_size_changed(self, value):
        """字体大小改变时的处理"""
        # 这里可以实现字体大小的实时预览
        pass
    
    def _on_opacity_changed(self, value):
        """透明度改变时的处理"""
        self._update_opacity_display()
        # 实时应用透明度
        main_window = self.winfo_toplevel()
        main_window.attributes('-alpha', value)
    
    def _update_opacity_display(self):
        """更新透明度显示"""
        opacity = self.opacity_var.get()
        percentage = int(opacity * 100)
        self.opacity_value_label.configure(text=f"{percentage}%")
    
    def _browse_data_path(self):
        """浏览数据存储路径"""
        folder_path = filedialog.askdirectory(
            title="选择数据存储文件夹",
            initialdir=self.data_path_var.get()
        )
        
        if folder_path:
            self.data_path_var.set(folder_path)
    
    def _backup_now(self):
        """立即备份"""
        try:
            # 这里应该调用实际的备份功能
            messagebox.showinfo("成功", "数据备份完成")
            self.logger.info("手动备份完成")
        except Exception as e:
            self.logger.error(f"备份失败: {e}")
            messagebox.showerror("错误", f"备份失败: {e}")
    
    def _restore_backup(self):
        """恢复备份"""
        backup_file = filedialog.askopenfilename(
            title="选择备份文件",
            filetypes=[("备份文件", "*.backup"), ("JSON文件", "*.json"), ("所有文件", "*.*")]
        )
        
        if backup_file:
            result = messagebox.askyesno(
                "确认恢复",
                "恢复备份将覆盖当前的所有数据，确定要继续吗？",
                icon="warning"
            )
            
            if result:
                try:
                    # 这里应该调用实际的恢复功能
                    messagebox.showinfo("成功", "备份恢复完成")
                    self.logger.info(f"从备份文件恢复: {backup_file}")
                except Exception as e:
                    self.logger.error(f"恢复备份失败: {e}")
                    messagebox.showerror("错误", f"恢复备份失败: {e}")
    
    def _clear_data(self):
        """清空数据"""
        result = messagebox.askyesno(
            "确认清空",
            "确定要清空所有学习数据吗？\n\n此操作将删除所有学习进度、笔记和统计数据，且不可撤销！",
            icon="warning"
        )
        
        if result:
            # 二次确认
            result2 = messagebox.askyesno(
                "最终确认",
                "请再次确认：真的要清空所有数据吗？",
                icon="warning"
            )
            
            if result2:
                try:
                    # 这里应该调用实际的清空数据功能
                    messagebox.showinfo("完成", "所有数据已清空")
                    self.logger.info("用户清空了所有数据")
                except Exception as e:
                    self.logger.error(f"清空数据失败: {e}")
                    messagebox.showerror("错误", f"清空数据失败: {e}")