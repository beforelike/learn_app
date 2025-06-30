#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用程序设置管理
处理配置的存储、读取和管理
"""

import json
import os
import time
from typing import Any, Dict, Optional
from pathlib import Path

from ..utils.logger import get_logger

class AppSettings:
    """应用程序设置管理类"""
    
    def __init__(self, config_file: str = "config.json"):
        self.logger = get_logger(__name__)
        
        # 设置配置文件路径
        self.config_dir = Path.home() / ".mathmodeling"
        self.config_file = self.config_dir / config_file
        
        # 确保配置目录存在
        self.config_dir.mkdir(exist_ok=True)
        
        # 默认设置
        self.default_settings = {
            # 外观设置
            "appearance": {
                "theme": "系统",
                "font_size": "中等",
                "opacity": 1.0,
                "window_size": "1200x800",
                "window_position": "center",
                "color_scheme": "default"
            },
            
            # 行为设置
            "behavior": {
                "auto_save": True,
                "save_interval": 5,
                "check_updates": True,
                "minimize_to_tray": False,
                "auto_start": False,
                "confirm_exit": True,
                "remember_window_state": True
            },
            
            # 通知设置
            "notifications": {
                "enabled": True,
                "task_completion": True,
                "study_reminder": False,
                "reminder_time": "09:00",
                "sound_enabled": True,
                "popup_duration": 5
            },
            
            # 数据设置
            "data": {
                "storage_path": "./data",
                "auto_backup": True,
                "backup_retention_days": 30,
                "backup_interval": 24,
                "export_format": "json",
                "compression_enabled": False
            },
            
            # 学习设置
            "learning": {
                "daily_goal_minutes": 60,
                "break_reminder": True,
                "break_interval": 25,
                "auto_advance": False,
                "difficulty_adjustment": True,
                "show_progress_details": True
            },
            
            # 高级设置
            "advanced": {
                "debug_mode": False,
                "log_level": "INFO",
                "performance_monitor": False,
                "experimental_features": False,
                "cache_enabled": True,
                "max_cache_size": 100
            },
            
            # 界面设置
            "ui": {
                "show_sidebar": True,
                "show_status_bar": True,
                "show_toolbar": True,
                "compact_mode": False,
                "animation_enabled": True,
                "smooth_scrolling": True
            },
            
            # 快捷键设置
            "shortcuts": {
                "complete_task": "Ctrl+Return",
                "skip_task": "Ctrl+S",
                "save_notes": "Ctrl+S",
                "open_settings": "Ctrl+Comma",
                "toggle_sidebar": "Ctrl+B",
                "search": "Ctrl+F"
            },
            
            # 统计设置
            "statistics": {
                "track_time": True,
                "detailed_analytics": True,
                "export_stats": True,
                "chart_type": "line",
                "time_range": "30_days",
                "show_predictions": False
            }
        }
        
        # 当前设置
        self.settings = {}
        
        # 加载设置
        self.load()
    
    def load(self) -> bool:
        """加载设置"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                
                # 合并默认设置和加载的设置
                self.settings = self._merge_settings(self.default_settings, loaded_settings)
                
                self.logger.info(f"设置已从 {self.config_file} 加载")
                return True
            else:
                # 使用默认设置
                self.settings = self.default_settings.copy()
                self.save()  # 保存默认设置
                self.logger.info("使用默认设置并保存")
                return True
                
        except Exception as e:
            self.logger.error(f"加载设置失败: {e}")
            # 使用默认设置
            self.settings = self.default_settings.copy()
            return False
    
    def save(self) -> bool:
        """保存设置"""
        try:
            # 确保配置目录存在
            self.config_dir.mkdir(exist_ok=True)
            
            # 保存设置到文件
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"设置已保存到 {self.config_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"保存设置失败: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取设置值
        
        Args:
            key: 设置键，支持点号分隔的嵌套键（如 'appearance.theme'）
            default: 默认值
            
        Returns:
            设置值
        """
        try:
            keys = key.split('.')
            value = self.settings
            
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return default
            
            return value
            
        except Exception as e:
            self.logger.error(f"获取设置 {key} 失败: {e}")
            return default
    
    def set(self, key: str, value: Any) -> bool:
        """设置值
        
        Args:
            key: 设置键，支持点号分隔的嵌套键（如 'appearance.theme'）
            value: 设置值
            
        Returns:
            是否设置成功
        """
        try:
            keys = key.split('.')
            current = self.settings
            
            # 导航到目标位置
            for k in keys[:-1]:
                if k not in current:
                    current[k] = {}
                current = current[k]
            
            # 设置值
            current[keys[-1]] = value
            
            self.logger.debug(f"设置 {key} = {value}")
            return True
            
        except Exception as e:
            self.logger.error(f"设置 {key} 失败: {e}")
            return False
    
    def has(self, key: str) -> bool:
        """检查设置是否存在
        
        Args:
            key: 设置键
            
        Returns:
            是否存在
        """
        try:
            keys = key.split('.')
            current = self.settings
            
            for k in keys:
                if isinstance(current, dict) and k in current:
                    current = current[k]
                else:
                    return False
            
            return True
            
        except Exception:
            return False
    
    def remove(self, key: str) -> bool:
        """删除设置
        
        Args:
            key: 设置键
            
        Returns:
            是否删除成功
        """
        try:
            keys = key.split('.')
            current = self.settings
            
            # 导航到父级
            for k in keys[:-1]:
                if isinstance(current, dict) and k in current:
                    current = current[k]
                else:
                    return False
            
            # 删除键
            if isinstance(current, dict) and keys[-1] in current:
                del current[keys[-1]]
                self.logger.debug(f"删除设置 {key}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"删除设置 {key} 失败: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """重置到默认设置
        
        Returns:
            是否重置成功
        """
        try:
            self.settings = self.default_settings.copy()
            self.save()
            self.logger.info("设置已重置到默认值")
            return True
            
        except Exception as e:
            self.logger.error(f"重置设置失败: {e}")
            return False
    
    def reset_section(self, section: str) -> bool:
        """重置指定部分到默认设置
        
        Args:
            section: 设置部分名称（如 'appearance'）
            
        Returns:
            是否重置成功
        """
        try:
            if section in self.default_settings:
                self.settings[section] = self.default_settings[section].copy()
                self.logger.info(f"设置部分 {section} 已重置到默认值")
                return True
            else:
                self.logger.warning(f"未找到设置部分: {section}")
                return False
                
        except Exception as e:
            self.logger.error(f"重置设置部分 {section} 失败: {e}")
            return False
    
    def export_settings(self, file_path: str) -> bool:
        """导出设置到文件
        
        Args:
            file_path: 导出文件路径
            
        Returns:
            是否导出成功
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"设置已导出到 {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"导出设置失败: {e}")
            return False
    
    def import_settings(self, file_path: str) -> bool:
        """从文件导入设置
        
        Args:
            file_path: 导入文件路径
            
        Returns:
            是否导入成功
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_settings = json.load(f)
            
            # 合并导入的设置
            self.settings = self._merge_settings(self.default_settings, imported_settings)
            self.save()
            
            self.logger.info(f"设置已从 {file_path} 导入")
            return True
            
        except Exception as e:
            self.logger.error(f"导入设置失败: {e}")
            return False
    
    def get_all_settings(self) -> Dict[str, Any]:
        """获取所有设置
        
        Returns:
            所有设置的字典
        """
        return self.settings.copy()
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """获取设置部分
        
        Args:
            section: 设置部分名称
            
        Returns:
            设置部分的字典
        """
        return self.settings.get(section, {}).copy()
    
    def update_section(self, section: str, values: Dict[str, Any]) -> bool:
        """更新设置部分
        
        Args:
            section: 设置部分名称
            values: 要更新的值
            
        Returns:
            是否更新成功
        """
        try:
            if section not in self.settings:
                self.settings[section] = {}
            
            self.settings[section].update(values)
            self.logger.debug(f"更新设置部分 {section}")
            return True
            
        except Exception as e:
            self.logger.error(f"更新设置部分 {section} 失败: {e}")
            return False
    
    def _merge_settings(self, default: Dict[str, Any], loaded: Dict[str, Any]) -> Dict[str, Any]:
        """合并默认设置和加载的设置
        
        Args:
            default: 默认设置
            loaded: 加载的设置
            
        Returns:
            合并后的设置
        """
        result = default.copy()
        
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_settings(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def validate_settings(self) -> bool:
        """验证设置的有效性
        
        Returns:
            设置是否有效
        """
        try:
            # 检查必要的设置部分
            required_sections = ['appearance', 'behavior', 'notifications', 'data']
            for section in required_sections:
                if section not in self.settings:
                    self.logger.warning(f"缺少必要的设置部分: {section}")
                    return False
            
            # 检查数据类型
            if not isinstance(self.get('appearance.opacity'), (int, float)):
                self.logger.warning("透明度设置类型错误")
                return False
            
            if not isinstance(self.get('behavior.save_interval'), int):
                self.logger.warning("保存间隔设置类型错误")
                return False
            
            # 检查值范围
            opacity = self.get('appearance.opacity')
            if not (0.1 <= opacity <= 1.0):
                self.logger.warning(f"透明度值超出范围: {opacity}")
                return False
            
            save_interval = self.get('behavior.save_interval')
            if not (1 <= save_interval <= 60):
                self.logger.warning(f"保存间隔值超出范围: {save_interval}")
                return False
            
            self.logger.debug("设置验证通过")
            return True
            
        except Exception as e:
            self.logger.error(f"设置验证失败: {e}")
            return False
    
    def get_config_file_path(self) -> str:
        """获取配置文件路径
        
        Returns:
            配置文件路径
        """
        return str(self.config_file)
    
    def backup_settings(self, backup_path: Optional[str] = None) -> bool:
        """备份设置
        
        Args:
            backup_path: 备份文件路径，如果为None则使用默认路径
            
        Returns:
            是否备份成功
        """
        try:
            if backup_path is None:
                backup_path = str(self.config_dir / f"config_backup_{int(time.time())}.json")
            
            return self.export_settings(backup_path)
            
        except Exception as e:
            self.logger.error(f"备份设置失败: {e}")
            return False

# 全局设置实例
_settings_instance = None

def get_settings() -> AppSettings:
    """获取全局设置实例
    
    Returns:
        设置实例
    """
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = AppSettings()
    return _settings_instance

def setup_settings(config_file: str = "config.json") -> AppSettings:
    """设置全局设置实例
    
    Args:
        config_file: 配置文件名
        
    Returns:
        设置实例
    """
    global _settings_instance
    _settings_instance = AppSettings(config_file)
    return _settings_instance