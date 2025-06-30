#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置模块
包含应用程序配置和设置管理
"""

from .settings import AppSettings, get_settings, setup_settings

__all__ = ['AppSettings', 'get_settings', 'setup_settings']