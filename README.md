# 📱 数学建模学习应用

一个基于Python Kivy开发的数学建模学习管理应用，支持Android平台。

## ✨ 功能特性

- 📚 **学习进度管理** - 跟踪你的数学建模学习进度
- 📝 **任务跟踪系统** - 管理学习任务和目标
- 📊 **统计分析功能** - 分析学习数据和趋势
- 📖 **历史记录查看** - 查看过往学习记录
- 🎨 **完整中文支持** - 原生中文界面

## 🚀 快速开始

### 📱 下载APK

1. 访问 [Releases页面](../../releases)
2. 下载最新版本的APK文件
3. 在Android设备上安装

### 🔧 系统要求

- **Android版本**: 5.0+ (API 21)
- **存储空间**: 50MB可用空间
- **权限**: 允许安装未知来源应用

## 🛠️ 自动构建

本项目使用GitHub Actions自动构建APK：

- ✅ 每次推送代码自动触发构建
- ✅ 自动生成应用图标和启动画面
- ✅ 自动发布到Releases页面
- ✅ 支持多架构（arm64-v8a, armeabi-v7a）

## 📖 使用指南

详细的安装和使用指南请查看：
- [APK安装指南](APK_INSTALL_GUIDE.md)
- [完整部署指南](完整部署指南.md)

## 🔧 开发环境

- **Python**: 3.9
- **UI框架**: Kivy 2.1.0 + KivyMD 1.1.1
- **构建工具**: Buildozer
- **CI/CD**: GitHub Actions

## 📄 项目结构

```
├── main.py                 # 主应用入口
├── src/                    # 源代码目录
│   ├── core/              # 核心功能模块
│   ├── gui/               # 用户界面组件
│   ├── utils/             # 工具函数
│   └── config/            # 配置文件
├── data/                   # 应用资源
│   ├── icon.png           # 应用图标
│   └── presplash.png      # 启动画面
├── .github/workflows/      # GitHub Actions配置
├── buildozer.spec         # Android构建配置
└── requirements.txt       # Python依赖
```

## 🎯 应用截图

*即将添加应用截图...*

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

感谢所有开源项目的贡献者，特别是：
- [Kivy](https://kivy.org/) - 跨平台Python GUI框架
- [KivyMD](https://kivymd.readthedocs.io/) - Material Design组件
- [Buildozer](https://github.com/kivy/buildozer) - Android打包工具

---

**开始你的数学建模学习之旅！** 🚀
