[app]

# 应用基本信息
title = 数学建模学习应用
package.name = mathmodeling
package.domain = com.mathmodeling

# 源代码
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,txt,md
source.exclude_dirs = tests,bin,.vscode,.git,__pycache__
source.exclude_patterns = license,images/*/*.jpg

# 版本信息
version = 1.0
version.regex = __version__ = ['"](.*?)['"]
version.filename = %(source.dir)s/main.py

# 应用要求
requirements = python3,kivy==2.1.0,kivymd==1.1.1,requests,certifi,charset-normalizer,idna,urllib3

# 图标和启动画面
icon.filename = %(source.dir)s/data/icon.png
presplash.filename = %(source.dir)s/data/presplash.png

# 方向和全屏
orientation = portrait
fullscreen = 0

# Android特定设置
[buildozer]

# 构建目录
bin_dir = ./.buildozer/bin

[app:android]

# Android API设置
android.api = 30
android.minapi = 21
android.ndk = 23b
android.sdk = 30

# 权限
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE

# 架构
android.archs = arm64-v8a,armeabi-v7a

# 签名（调试模式）
android.debug_artifact = apk

# 启动模式
android.bootstrap = sdl2

# Gradle设置
android.gradle_dependencies = 
android.add_src = 
android.add_aars = 
android.add_jars = 

# 构建优化
android.skip_update = False
android.accept_sdk_license = True

# 清单文件设置
android.manifest.intent_filters = 
android.manifest.launch_mode = standard

[buildozer:global]

# 日志级别
log_level = 2

# 并行构建
warn_on_root = 1
