#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志工具模块
提供统一的日志记录功能
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

class ColoredFormatter(logging.Formatter):
    """彩色日志格式化器"""
    
    # ANSI颜色代码
    COLORS = {
        'DEBUG': '\033[36m',     # 青色
        'INFO': '\033[32m',      # 绿色
        'WARNING': '\033[33m',   # 黄色
        'ERROR': '\033[31m',     # 红色
        'CRITICAL': '\033[35m',  # 紫色
        'RESET': '\033[0m'       # 重置
    }
    
    def format(self, record):
        # 获取原始格式化的消息
        formatted = super().format(record)
        
        # 如果支持颜色（通常是终端）
        if hasattr(sys.stderr, 'isatty') and sys.stderr.isatty():
            color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            reset = self.COLORS['RESET']
            
            # 只给级别名称添加颜色
            formatted = formatted.replace(
                record.levelname,
                f"{color}{record.levelname}{reset}"
            )
        
        return formatted

class LoggerManager:
    """日志管理器"""
    
    def __init__(self):
        self.loggers = {}
        self.log_dir = Path.home() / ".mathmodeling" / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 默认配置
        self.default_level = logging.INFO
        self.default_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        self.console_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        
        # 文件日志配置
        self.file_max_bytes = 10 * 1024 * 1024  # 10MB
        self.file_backup_count = 5
        
        # 是否已经设置过根日志器
        self._root_configured = False
    
    def setup_logger(
        self,
        name: str,
        level: Optional[int] = None,
        console_output: bool = True,
        file_output: bool = True,
        file_name: Optional[str] = None
    ) -> logging.Logger:
        """设置日志器
        
        Args:
            name: 日志器名称
            level: 日志级别
            console_output: 是否输出到控制台
            file_output: 是否输出到文件
            file_name: 日志文件名
            
        Returns:
            配置好的日志器
        """
        if name in self.loggers:
            return self.loggers[name]
        
        # 创建日志器
        logger = logging.getLogger(name)
        logger.setLevel(level or self.default_level)
        
        # 避免重复添加处理器
        if logger.handlers:
            logger.handlers.clear()
        
        # 控制台处理器
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level or self.default_level)
            
            # 使用彩色格式化器
            console_formatter = ColoredFormatter(self.console_format)
            console_handler.setFormatter(console_formatter)
            
            logger.addHandler(console_handler)
        
        # 文件处理器
        if file_output:
            if file_name is None:
                file_name = f"{name.replace('.', '_')}.log"
            
            log_file = self.log_dir / file_name
            
            # 使用轮转文件处理器
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=self.file_max_bytes,
                backupCount=self.file_backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(level or self.default_level)
            
            # 文件格式化器（不使用颜色）
            file_formatter = logging.Formatter(self.default_format)
            file_handler.setFormatter(file_formatter)
            
            logger.addHandler(file_handler)
        
        # 防止日志传播到根日志器
        logger.propagate = False
        
        # 缓存日志器
        self.loggers[name] = logger
        
        return logger
    
    def get_logger(self, name: str) -> logging.Logger:
        """获取日志器
        
        Args:
            name: 日志器名称
            
        Returns:
            日志器
        """
        if name not in self.loggers:
            return self.setup_logger(name)
        return self.loggers[name]
    
    def set_level(self, level: int):
        """设置所有日志器的级别
        
        Args:
            level: 日志级别
        """
        self.default_level = level
        
        for logger in self.loggers.values():
            logger.setLevel(level)
            for handler in logger.handlers:
                handler.setLevel(level)
    
    def set_level_by_name(self, name: str, level: int):
        """设置指定日志器的级别
        
        Args:
            name: 日志器名称
            level: 日志级别
        """
        if name in self.loggers:
            logger = self.loggers[name]
            logger.setLevel(level)
            for handler in logger.handlers:
                handler.setLevel(level)
    
    def add_file_handler(
        self,
        name: str,
        file_name: str,
        level: Optional[int] = None,
        max_bytes: Optional[int] = None,
        backup_count: Optional[int] = None
    ):
        """为指定日志器添加文件处理器
        
        Args:
            name: 日志器名称
            file_name: 文件名
            level: 日志级别
            max_bytes: 最大文件大小
            backup_count: 备份文件数量
        """
        if name not in self.loggers:
            self.setup_logger(name)
        
        logger = self.loggers[name]
        log_file = self.log_dir / file_name
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes or self.file_max_bytes,
            backupCount=backup_count or self.file_backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(level or self.default_level)
        
        file_formatter = logging.Formatter(self.default_format)
        file_handler.setFormatter(file_formatter)
        
        logger.addHandler(file_handler)
    
    def remove_handlers(self, name: str):
        """移除指定日志器的所有处理器
        
        Args:
            name: 日志器名称
        """
        if name in self.loggers:
            logger = self.loggers[name]
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)
                handler.close()
    
    def cleanup(self):
        """清理所有日志器"""
        for name in list(self.loggers.keys()):
            self.remove_handlers(name)
        self.loggers.clear()
    
    def get_log_files(self) -> list:
        """获取所有日志文件
        
        Returns:
            日志文件路径列表
        """
        if not self.log_dir.exists():
            return []
        
        return [f for f in self.log_dir.iterdir() if f.is_file() and f.suffix == '.log']
    
    def clear_old_logs(self, days: int = 30):
        """清理旧日志文件
        
        Args:
            days: 保留天数
        """
        if not self.log_dir.exists():
            return
        
        cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        for log_file in self.log_dir.iterdir():
            if log_file.is_file() and log_file.suffix == '.log':
                if log_file.stat().st_mtime < cutoff_time:
                    try:
                        log_file.unlink()
                        print(f"删除旧日志文件: {log_file}")
                    except Exception as e:
                        print(f"删除日志文件失败 {log_file}: {e}")
    
    def get_log_dir(self) -> Path:
        """获取日志目录
        
        Returns:
            日志目录路径
        """
        return self.log_dir
    
    def setup_root_logger(self, level: int = logging.INFO):
        """设置根日志器
        
        Args:
            level: 日志级别
        """
        if self._root_configured:
            return
        
        # 配置根日志器
        logging.basicConfig(
            level=level,
            format=self.default_format,
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self._root_configured = True

# 全局日志管理器实例
_logger_manager = LoggerManager()

def setup_logger(
    name: str,
    level: Optional[int] = None,
    console_output: bool = True,
    file_output: bool = True,
    file_name: Optional[str] = None
) -> logging.Logger:
    """设置日志器（全局函数）
    
    Args:
        name: 日志器名称
        level: 日志级别
        console_output: 是否输出到控制台
        file_output: 是否输出到文件
        file_name: 日志文件名
        
    Returns:
        配置好的日志器
    """
    return _logger_manager.setup_logger(
        name, level, console_output, file_output, file_name
    )

def get_logger(name: str) -> logging.Logger:
    """获取日志器（全局函数）
    
    Args:
        name: 日志器名称
        
    Returns:
        日志器
    """
    return _logger_manager.get_logger(name)

def set_global_log_level(level: int):
    """设置全局日志级别
    
    Args:
        level: 日志级别
    """
    _logger_manager.set_level(level)

def cleanup_loggers():
    """清理所有日志器"""
    _logger_manager.cleanup()

def clear_old_logs(days: int = 30):
    """清理旧日志文件
    
    Args:
        days: 保留天数
    """
    _logger_manager.clear_old_logs(days)

def get_log_directory() -> Path:
    """获取日志目录
    
    Returns:
        日志目录路径
    """
    return _logger_manager.get_log_dir()

def configure_logging_from_settings(settings):
    """从设置配置日志
    
    Args:
        settings: 应用设置对象
    """
    # 获取日志级别
    log_level_str = settings.get('advanced.log_level', 'INFO')
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)
    
    # 设置全局日志级别
    set_global_log_level(log_level)
    
    # 如果启用调试模式，设置为DEBUG级别
    if settings.get('advanced.debug_mode', False):
        set_global_log_level(logging.DEBUG)
    
    # 清理旧日志
    retention_days = settings.get('data.backup_retention_days', 30)
    clear_old_logs(retention_days)

# 日志级别常量
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

# 便捷函数
def debug(msg: str, logger_name: str = "app"):
    """记录调试信息"""
    get_logger(logger_name).debug(msg)

def info(msg: str, logger_name: str = "app"):
    """记录信息"""
    get_logger(logger_name).info(msg)

def warning(msg: str, logger_name: str = "app"):
    """记录警告"""
    get_logger(logger_name).warning(msg)

def error(msg: str, logger_name: str = "app"):
    """记录错误"""
    get_logger(logger_name).error(msg)

def critical(msg: str, logger_name: str = "app"):
    """记录严重错误"""
    get_logger(logger_name).critical(msg)

def exception(msg: str, logger_name: str = "app"):
    """记录异常（包含堆栈跟踪）"""
    get_logger(logger_name).exception(msg)

if __name__ == "__main__":
    # 测试日志功能
    logger = setup_logger("test", level=logging.DEBUG)
    
    logger.debug("这是一条调试信息")
    logger.info("这是一条信息")
    logger.warning("这是一条警告")
    logger.error("这是一条错误")
    logger.critical("这是一条严重错误")
    
    try:
        1 / 0
    except Exception:
        logger.exception("捕获到异常")
    
    print(f"日志文件保存在: {get_log_directory()}")