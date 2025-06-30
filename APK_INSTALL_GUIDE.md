# 📱 APK安装问题解决指南

## ❌ 常见安装错误

### 1. "解析安装包出错"

**原因：**
- APK文件损坏或格式不正确
- APK不是真正的Android安装包
- 设备架构不兼容

**解决方案：**
1. 重新下载APK文件
2. 使用专业工具构建的APK
3. 检查设备兼容性

### 2. "应用未安装"

**原因：**
- 存储空间不足
- 权限设置问题
- 签名验证失败

**解决方案：**
1. 清理设备存储空间
2. 允许"未知来源"安装
3. 使用正确签名的APK

## ✅ 正确的APK构建方法

### 方法1: GitHub Actions（推荐）

1. **上传代码到GitHub**
   ```bash
   git add .
   git commit -m "准备构建APK"
   git push origin main
   ```

2. **触发自动构建**
   - 推送代码后自动开始构建
   - 或在GitHub Actions页面手动触发

3. **下载构建的APK**
   - 在Actions页面下载Artifacts
   - 或从Releases页面下载

### 方法2: WSL2环境构建

1. **安装WSL2**
   ```powershell
   wsl --install
   ```

2. **在WSL2中构建**
   ```bash
   cd /mnt/c/path/to/project
   chmod +x build_local_fixed.sh
   ./build_local_fixed.sh
   ```

### 方法3: Docker构建

1. **构建Docker镜像**
   ```bash
   docker build -t mathmodeling-app .
   ```

2. **运行构建容器**
   ```bash
   docker run -v $(pwd):/app mathmodeling-app
   ```

## 🔧 构建环境要求

### 系统要求
- **操作系统**: Linux (Ubuntu 18.04+推荐)
- **Python**: 3.8-3.10
- **Java**: OpenJDK 8或11
- **内存**: 至少4GB RAM
- **存储**: 至少10GB可用空间

### 必要工具
```bash
# Ubuntu/Debian
sudo apt-get install -y     python3 python3-pip python3-venv     build-essential git     openjdk-8-jdk     autoconf libtool pkg-config     zlib1g-dev libncurses5-dev     libncursesw5-dev libtinfo5     cmake libffi-dev libssl-dev     libsdl2-dev libsdl2-image-dev     libsdl2-mixer-dev libsdl2-ttf-dev
```

## 📱 APK安装步骤

### Android设备设置

1. **允许未知来源安装**
   - 设置 → 安全 → 未知来源 ✅
   - 或安装时选择"允许此来源"

2. **检查存储空间**
   - 确保至少有100MB可用空间
   - 清理不必要的文件

3. **检查Android版本**
   - 最低要求: Android 5.0 (API 21)
   - 推荐: Android 8.0+ (API 26+)

### 安装过程

1. **下载APK文件**
   - 从GitHub Releases下载
   - 或从构建Artifacts下载

2. **传输到设备**
   - USB传输
   - 云存储下载
   - 邮件发送

3. **安装APK**
   - 点击APK文件
   - 按照提示完成安装
   - 授予必要权限

## 🛠️ 故障排除

### 构建失败

1. **检查依赖**
   ```bash
   pip install -r requirements.txt
   buildozer android debug
   ```

2. **清理构建缓存**
   ```bash
   buildozer android clean
   rm -rf .buildozer
   ```

3. **更新工具**
   ```bash
   pip install --upgrade buildozer cython
   ```

### 安装失败

1. **重启设备**
2. **清除应用数据**
3. **重新下载APK**
4. **检查设备兼容性**

### 运行问题

1. **权限问题**
   - 手动授予应用权限
   - 检查存储权限

2. **字体问题**
   - 确保系统支持中文
   - 重启应用

3. **崩溃问题**
   - 查看系统日志
   - 重新安装应用

## 📞 获取帮助

如果遇到问题：

1. **查看构建日志**
   - GitHub Actions日志
   - 本地构建输出

2. **检查Issue页面**
   - 搜索类似问题
   - 查看解决方案

3. **提交新Issue**
   - 详细描述问题
   - 提供错误日志
   - 说明设备信息

## 📋 检查清单

构建前确认：
- [ ] Linux环境或WSL2
- [ ] Python 3.8-3.10
- [ ] Java 8或11
- [ ] 足够的存储空间
- [ ] 网络连接正常

安装前确认：
- [ ] Android 5.0+
- [ ] 允许未知来源
- [ ] 足够的存储空间
- [ ] APK文件完整

---

**记住：只有使用专业构建工具创建的APK才能正常安装！** 🎯
