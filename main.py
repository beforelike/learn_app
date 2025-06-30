#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数学建模学习进度追踪应用 - Python版本 (Kivy)
作者: AI Assistant
版本: 2.0.0
描述: 基于Kivy的跨平台数学建模学习管理应用
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path
import os

from src.core.app_manager import AppManager
from src.utils.logger import setup_logger
from src.config.settings import AppSettings

class HomeScreen(Screen):
    """主页面"""
    
    def __init__(self, app_manager, **kwargs):
        super().__init__(**kwargs)
        self.app_manager = app_manager
        self.build_ui()
    
    def build_ui(self):
        """构建主页面UI"""
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # 标题
        title = Label(
            text='数学建模学习应用',
            font_size='24sp',
            font_name='Chinese',
            size_hint_y=None,
            height=dp(60),
            color=(0.2, 0.6, 1, 1)
        )
        main_layout.add_widget(title)
        
        # 当前任务信息
        self.task_info = Label(
            text='正在加载当前任务...',
            font_size='16sp',
            font_name='Chinese',
            size_hint_y=None,
            height=dp(100),
            text_size=(None, None),
            halign='center'
        )
        main_layout.add_widget(self.task_info)
        
        # 进度条
        progress_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(80))
        progress_layout.add_widget(Label(text='学习进度', font_size='14sp', font_name='Chinese', size_hint_y=None, height=dp(30)))
        
        self.progress_bar = ProgressBar(max=100, value=0, size_hint_y=None, height=dp(20))
        progress_layout.add_widget(self.progress_bar)
        
        self.progress_label = Label(text='0%', font_size='12sp', size_hint_y=None, height=dp(30))
        progress_layout.add_widget(self.progress_label)
        
        main_layout.add_widget(progress_layout)
        
        # 操作按钮
        button_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(120))
        
        complete_btn = Button(
            text='完成当前任务',
            font_size='16sp',
            background_color=(0.2, 0.8, 0.2, 1)
        )
        complete_btn.bind(on_press=self.complete_task)
        button_layout.add_widget(complete_btn)
        
        next_btn = Button(
            text='下一天',
            font_size='16sp',
            background_color=(0.2, 0.6, 1, 1)
        )
        next_btn.bind(on_press=self.next_day)
        button_layout.add_widget(next_btn)
        
        main_layout.add_widget(button_layout)
        
        # 笔记区域
        notes_layout = BoxLayout(orientation='vertical', spacing=dp(5))
        notes_layout.add_widget(Label(text='学习笔记', font_size='14sp', size_hint_y=None, height=dp(30)))
        
        self.notes_input = TextInput(
            multiline=True,
            hint_text='在这里记录你的学习笔记和心得...',
            font_size='12sp'
        )
        notes_layout.add_widget(self.notes_input)
        
        save_notes_btn = Button(
            text='保存笔记',
            font_size='14sp',
            size_hint_y=None,
            height=dp(40),
            background_color=(0.8, 0.6, 0.2, 1)
        )
        save_notes_btn.bind(on_press=self.save_notes)
        notes_layout.add_widget(save_notes_btn)
        
        main_layout.add_widget(notes_layout)
        
        self.add_widget(main_layout)
        
        # 定时刷新
        Clock.schedule_once(self.refresh_data, 0.5)
    
    def refresh_data(self, dt=None):
        """刷新数据显示"""
        try:
            # 获取当前任务
            current_task = self.app_manager.get_current_task()
            if current_task:
                task_text = f"第{self.app_manager.progress['current_day']}天\n"
                task_text += f"任务: {current_task.get('title', '未知任务')}\n"
                task_text += f"难度: {current_task.get('difficulty', 'N/A')}\n"
                task_text += f"预计时间: {current_task.get('estimated_time', 'N/A')}"
                self.task_info.text = task_text
            
            # 更新进度
            stats = self.app_manager.get_learning_stats()
            progress = stats.get('completion_rate', 0)
            self.progress_bar.value = progress
            self.progress_label.text = f"{progress:.1f}%"
            
            # 加载笔记
            current_day = self.app_manager.progress['current_day']
            note = self.app_manager.get_task_note(current_day)
            self.notes_input.text = note
            
        except Exception as e:
            self.task_info.text = f"加载数据失败: {e}"
    
    def complete_task(self, instance):
        """完成当前任务"""
        try:
            if self.app_manager.complete_current_task():
                popup = Popup(
                    title='任务完成',
                    content=Label(text='恭喜！任务已完成'),
                    size_hint=(0.6, 0.4)
                )
                popup.open()
                Clock.schedule_once(lambda dt: popup.dismiss(), 2)
                Clock.schedule_once(self.refresh_data, 0.5)
            else:
                popup = Popup(
                    title='提示',
                    content=Label(text='任务已经完成或无法完成'),
                    size_hint=(0.6, 0.4)
                )
                popup.open()
                Clock.schedule_once(lambda dt: popup.dismiss(), 2)
        except Exception as e:
            popup = Popup(
                title='错误',
                content=Label(text=f'完成任务失败: {e}'),
                size_hint=(0.6, 0.4)
            )
            popup.open()
            Clock.schedule_once(lambda dt: popup.dismiss(), 3)
    
    def next_day(self, instance):
        """进入下一天"""
        try:
            self.app_manager.next_day()
            Clock.schedule_once(self.refresh_data, 0.1)
            popup = Popup(
                title='提示',
                content=Label(text='已进入下一天'),
                size_hint=(0.6, 0.4)
            )
            popup.open()
            Clock.schedule_once(lambda dt: popup.dismiss(), 1.5)
        except Exception as e:
            popup = Popup(
                title='错误',
                content=Label(text=f'操作失败: {e}'),
                size_hint=(0.6, 0.4)
            )
            popup.open()
            Clock.schedule_once(lambda dt: popup.dismiss(), 3)
    
    def save_notes(self, instance):
        """保存笔记"""
        try:
            current_day = self.app_manager.progress['current_day']
            note = self.notes_input.text
            self.app_manager.set_task_note(current_day, note)
            popup = Popup(
                title='提示',
                content=Label(text='笔记已保存'),
                size_hint=(0.6, 0.4)
            )
            popup.open()
            Clock.schedule_once(lambda dt: popup.dismiss(), 1.5)
        except Exception as e:
            popup = Popup(
                title='错误',
                content=Label(text=f'保存失败: {e}'),
                size_hint=(0.6, 0.4)
            )
            popup.open()
            Clock.schedule_once(lambda dt: popup.dismiss(), 3)

class ProgressScreen(Screen):
    """进度页面"""
    
    def __init__(self, app_manager, **kwargs):
        super().__init__(**kwargs)
        self.app_manager = app_manager
        self.build_ui()
    
    def build_ui(self):
        """构建进度页面UI"""
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # 标题
        title = Label(
            text='学习进度',
            font_size='24sp',
            size_hint_y=None,
            height=dp(60),
            color=(0.2, 0.6, 1, 1)
        )
        main_layout.add_widget(title)
        
        # 统计信息
        self.stats_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(200))
        main_layout.add_widget(self.stats_layout)
        
        # 任务列表
        tasks_label = Label(
            text='最近完成的任务',
            font_size='18sp',
            size_hint_y=None,
            height=dp(40)
        )
        main_layout.add_widget(tasks_label)
        
        # 滚动视图
        scroll = ScrollView()
        self.tasks_layout = BoxLayout(orientation='vertical', spacing=dp(5), size_hint_y=None)
        self.tasks_layout.bind(minimum_height=self.tasks_layout.setter('height'))
        scroll.add_widget(self.tasks_layout)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
        
        # 定时刷新
        Clock.schedule_once(self.refresh_data, 0.5)
    
    def refresh_data(self, dt=None):
        """刷新进度数据"""
        try:
            # 清空统计布局
            self.stats_layout.clear_widgets()
            
            # 获取统计信息
            stats = self.app_manager.get_learning_stats()
            
            # 添加统计卡片
            stats_items = [
                ('总天数', str(stats.get('total_days', 0))),
                ('已完成', str(stats.get('completed_days', 0))),
                ('完成率', f"{stats.get('completion_rate', 0):.1f}%"),
                ('当前天数', str(stats.get('current_day', 1))),
                ('当前阶段', str(stats.get('current_stage', 1))),
                ('当前周', str(stats.get('current_week', 1))),
                ('连续天数', str(stats.get('current_streak', 0))),
                ('学习时间', f"{stats.get('total_study_time', 0)}小时")
            ]
            
            for label_text, value_text in stats_items:
                card = BoxLayout(orientation='vertical', spacing=dp(5))
                
                # 添加背景色
                with card.canvas.before:
                    Color(0.1, 0.1, 0.1, 0.8)
                    card.rect = Rectangle(size=card.size, pos=card.pos)
                card.bind(size=self._update_rect, pos=self._update_rect)
                
                card.add_widget(Label(text=label_text, font_size='12sp', size_hint_y=None, height=dp(25)))
                card.add_widget(Label(text=value_text, font_size='16sp', color=(0.2, 0.8, 1, 1)))
                
                self.stats_layout.add_widget(card)
            
            # 清空任务列表
            self.tasks_layout.clear_widgets()
            
            # 获取任务历史
            history = self.app_manager.get_task_history(10)
            
            for task in history:
                task_card = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(60))
                
                # 添加背景色
                with task_card.canvas.before:
                    Color(0.05, 0.05, 0.05, 0.9)
                    task_card.rect = Rectangle(size=task_card.size, pos=task_card.pos)
                task_card.bind(size=self._update_rect, pos=self._update_rect)
                
                # 任务信息
                info_layout = BoxLayout(orientation='vertical')
                info_layout.add_widget(Label(
                    text=f"第{task.get('day', 'N/A')}天: {task.get('title', '未知任务')}",
                    font_size='14sp',
                    text_size=(None, None),
                    halign='left'
                ))
                info_layout.add_widget(Label(
                    text=f"难度: {task.get('difficulty', 'N/A')} | 时间: {task.get('estimated_time', 'N/A')}",
                    font_size='12sp',
                    color=(0.7, 0.7, 0.7, 1),
                    text_size=(None, None),
                    halign='left'
                ))
                
                task_card.add_widget(info_layout)
                
                # 完成状态
                status_label = Label(
                    text='✓ 已完成',
                    font_size='12sp',
                    color=(0.2, 0.8, 0.2, 1),
                    size_hint_x=None,
                    width=dp(80)
                )
                task_card.add_widget(status_label)
                
                self.tasks_layout.add_widget(task_card)
            
            if not history:
                self.tasks_layout.add_widget(Label(
                    text='暂无完成的任务',
                    font_size='14sp',
                    color=(0.7, 0.7, 0.7, 1),
                    size_hint_y=None,
                    height=dp(40)
                ))
                
        except Exception as e:
            error_label = Label(
                text=f'加载进度数据失败: {e}',
                font_size='14sp',
                color=(1, 0.3, 0.3, 1)
            )
            self.stats_layout.add_widget(error_label)
    
    def _update_rect(self, instance, value):
        """更新背景矩形"""
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

class MathModelingApp(App):
    """数学建模学习应用主类"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 配置中文字体支持
        self.setup_chinese_font()
        
        self.logger = setup_logger('MathModelingApp')
        self.settings = AppSettings()
        self.app_manager = AppManager()
        
        self.logger.info("数学建模学习应用启动")
    
    def setup_chinese_font(self):
        """配置中文字体支持"""
        try:
            import platform
            from kivy.config import Config
            
            # 设置Kivy配置以支持中文
            Config.set('kivy', 'default_font', ['Roboto', 'data/fonts/Roboto-Regular.ttf'])
            
            if platform.system() == 'Windows':
                font_paths = [
                    'C:/Windows/Fonts/msyh.ttc',  # 微软雅黑
                    'C:/Windows/Fonts/simhei.ttf',  # 黑体
                    'C:/Windows/Fonts/simsun.ttc',  # 宋体
                    'C:/Windows/Fonts/msyhbd.ttc',  # 微软雅黑粗体
                ]
            else:  # Linux/Android
                font_paths = [
                    '/system/fonts/NotoSansCJK-Regular.ttc',
                    '/system/fonts/DroidSansFallback.ttf',
                    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                    '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
                ]
            
            font_registered = False
            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        # 注册中文字体
                        LabelBase.register(name='Chinese', fn_regular=font_path)
                        # 设置为默认字体
                        LabelBase.register(name='Roboto', fn_regular=font_path)
                        font_registered = True
                        print(f"成功注册中文字体: {font_path}")
                        break
                    except Exception as font_error:
                        print(f"注册字体失败 {font_path}: {font_error}")
                        continue
            
            if not font_registered:
                print("警告: 未找到可用的中文字体，可能会出现显示问题")
                
        except Exception as e:
            print(f"字体配置错误: {e}")
    
    def build(self):
        """构建应用界面"""
        try:
            # 设置窗口
            Window.clearcolor = (0.05, 0.05, 0.05, 1)
            Window.size = (800, 600)
            
            # 创建屏幕管理器
            sm = ScreenManager()
            
            # 添加主页面
            home_screen = HomeScreen(self.app_manager, name='home')
            sm.add_widget(home_screen)
            
            # 添加进度页面
            progress_screen = ProgressScreen(self.app_manager, name='progress')
            sm.add_widget(progress_screen)
            
            # 创建主布局
            main_layout = BoxLayout(orientation='vertical')
            
            # 导航栏
            nav_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
            
            home_btn = Button(
                text='主页',
                font_size='16sp',
                font_name='Chinese',
                background_color=(0.2, 0.6, 1, 1)
            )
            home_btn.bind(on_press=lambda x: setattr(sm, 'current', 'home'))
            nav_layout.add_widget(home_btn)
            
            progress_btn = Button(
                text='进度',
                font_size='16sp',
                font_name='Chinese',
                background_color=(0.8, 0.4, 0.2, 1)
            )
            progress_btn.bind(on_press=lambda x: setattr(sm, 'current', 'progress'))
            nav_layout.add_widget(progress_btn)
            
            main_layout.add_widget(nav_layout)
            main_layout.add_widget(sm)
            
            return main_layout
            
        except Exception as e:
            self.logger.error(f"应用构建错误: {e}")
            # 返回错误页面
            error_layout = BoxLayout(orientation='vertical', padding=dp(20))
            error_layout.add_widget(Label(
                text=f'应用启动失败: {e}',
                font_size='16sp',
                color=(1, 0.3, 0.3, 1)
            ))
            return error_layout
    
    def on_stop(self):
        """应用停止时的清理"""
        try:
            self.app_manager.save_all_data()
            self.logger.info("应用正常退出")
        except Exception as e:
            self.logger.error(f"清理资源时出错: {e}")

def main():
    """主函数"""
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("错误: 需要Python 3.8或更高版本")
        sys.exit(1)
    
    # 创建并运行应用
    app = MathModelingApp()
    app.run()

if __name__ == "__main__":
    main()