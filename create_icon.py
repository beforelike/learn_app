#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用图标生成器
"""

import os
from pathlib import Path

def create_svg_icon():
    """创建SVG图标"""
    svg_content = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="512" height="512" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
    <rect width="512" height="512" fill="#2196F3" rx="64"/>
    <text x="256" y="320" font-family="Arial, sans-serif" font-size="120" 
          fill="white" text-anchor="middle" font-weight="bold">数</text>
    <text x="256" y="420" font-family="Arial, sans-serif" font-size="60" 
          fill="white" text-anchor="middle">建模</text>
</svg>"""
    
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)
    
    with open(data_dir / 'icon.svg', 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print("✅ SVG图标已创建")

def create_png_icon():
    """创建PNG图标（使用PIL）"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # 创建512x512的图标
        img = Image.new('RGB', (512, 512), color='#2196F3')
        draw = ImageDraw.Draw(img)
        
        # 尝试加载字体
        try:
            # Windows字体
            font_large = ImageFont.truetype('msyh.ttc', 120)
            font_small = ImageFont.truetype('msyh.ttc', 60)
        except:
            try:
                # Linux字体
                font_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 120)
                font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 60)
            except:
                # 默认字体
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()
        
        # 绘制文字
        text1 = '数'
        text2 = '建模'
        
        # 计算文字位置
        bbox1 = draw.textbbox((0, 0), text1, font=font_large)
        text1_width = bbox1[2] - bbox1[0]
        text1_height = bbox1[3] - bbox1[1]
        x1 = (512 - text1_width) // 2
        y1 = (512 - text1_height) // 2 - 50
        
        bbox2 = draw.textbbox((0, 0), text2, font=font_small)
        text2_width = bbox2[2] - bbox2[0]
        x2 = (512 - text2_width) // 2
        y2 = y1 + text1_height + 20
        
        draw.text((x1, y1), text1, fill='white', font=font_large)
        draw.text((x2, y2), text2, fill='white', font=font_small)
        
        # 保存图标
        data_dir = Path('data')
        data_dir.mkdir(exist_ok=True)
        img.save(data_dir / 'icon.png')
        
        # 创建启动画面
        splash = Image.new('RGB', (1080, 1920), color='#1976D2')
        splash_draw = ImageDraw.Draw(splash)
        
        # 在启动画面上绘制文字
        try:
            splash_font = ImageFont.truetype('msyh.ttc', 200)
        except:
            splash_font = font_large
        
        splash_text = '数学建模'
        splash_bbox = splash_draw.textbbox((0, 0), splash_text, font=splash_font)
        splash_width = splash_bbox[2] - splash_bbox[0]
        splash_x = (1080 - splash_width) // 2
        splash_y = 800
        
        splash_draw.text((splash_x, splash_y), splash_text, fill='white', font=splash_font)
        splash.save(data_dir / 'presplash.png')
        
        print("✅ PNG图标和启动画面已创建")
        return True
        
    except ImportError:
         print("⚠️  PIL库未安装，跳过PNG图标创建")
         return False

def main():
    """主函数"""
    print("🎨 创建应用图标...")
    
    # 创建SVG图标
    create_svg_icon()
    
    # 尝试创建PNG图标
    if not create_png_icon():
        print("\n💡 提示: 安装PIL库以生成PNG图标")
        print("pip install Pillow")
    
    print("\n✅ 图标创建完成")

if __name__ == '__main__':
    main()
