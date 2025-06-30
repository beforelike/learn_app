#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI组件模块
包含各种用户界面组件
"""

from .progress_card import ProgressCard
from .task_detail import TaskDetailFrame
from .stats_panel import StatsPanel
from .history_panel import HistoryPanel
from .settings_panel import SettingsPanel

__all__ = [
    'ProgressCard',
    'TaskDetailFrame', 
    'StatsPanel',
    'HistoryPanel',
    'SettingsPanel'
]