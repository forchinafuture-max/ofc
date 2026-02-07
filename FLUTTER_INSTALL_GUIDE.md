# Flutter 安装指南

本指南将帮助你在 Windows 系统上安装 Flutter 开发环境，以便后续开发移动应用版本的 OFC 扑克游戏。

## 系统要求

- Windows 7 SP1 或更高版本
- 64 位操作系统
- 至少 4GB RAM
- 至少 1.6GB 可用磁盘空间

## 安装步骤

### 1. 下载 Flutter SDK

1. 访问 [Flutter 官方网站](https://flutter.dev/docs/get-started/install/windows)
2. 点击 "Windows" 下载链接
3. 将下载的 ZIP 文件解压到你想要安装 Flutter 的位置，例如：`C:\src\flutter`

### 2. 配置环境变量

1. 右键点击 "此电脑" → "属性" → "高级系统设置" → "环境变量"
2. 在 "系统变量" 中，找到并编辑 "Path" 变量
3. 添加 Flutter 的 bin 目录路径，例如：`C:\src\flutter\bin`
4. 点击 "确定" 保存更改

### 3. 运行 Flutter 医生

1. 打开命令提示符或 PowerShell
2. 运行以下命令检查 Flutter 安装状态：
   ```
   flutter doctor
   ```
3. 按照输出中的指示解决任何问题

### 4. 安装 Android Studio

1. 访问 [Android Studio 官方网站](https://developer.android.com/studio)
2. 下载并安装 Android Studio
3. 在安装过程中，确保勾选 "Android Virtual Device"
4. 启动 Android Studio，完成初始设置

### 5. 安装 Android SDK

1. 在 Android Studio 中，打开 "File" → "Settings" → "Appearance & Behavior" → "System Settings" → "Android SDK"
2. 确保安装以下 SDK：
   - Android SDK Platform-Tools
   - Android SDK Build-Tools
   - Android SDK Command-line Tools
   - 至少一个 Android SDK Platform

### 6. 配置 Android 设备

#### 使用物理设备
1. 启用设备的开发者选项
2. 启用 USB 调试
3. 使用 USB 线缆连接设备到电脑

#### 使用虚拟设备
1. 在 Android Studio 中，点击 "AVD Manager"
2. 创建一个新的虚拟设备
3. 选择设备类型和系统镜像
4. 启动虚拟设备

### 7. 安装 Visual Studio Code（可选）

1. 访问 [VS Code 官方网站](https://code.visualstudio.com/)
2. 下载并安装 VS Code
3. 安装 Flutter 和 Dart 扩展

## 验证安装

运行以下命令验证所有依赖项是否正确安装：

```
flutter doctor
```

当所有检查都通过后，你就可以开始开发 Flutter 应用了。

## 创建新的 Flutter 项目

```
flutter create ofc_poker_app
cd ofc_poker_app
flutter run
```

## 后续步骤

1. 学习 Flutter 基础教程
2. 了解 Dart 编程语言
3. 探索 Flutter 组件和布局
4. 将我们的 OFC 扑克游戏逻辑迁移到 Flutter 应用中

## 参考资源

- [Flutter 官方文档](https://flutter.dev/docs)
- [Flutter 教程](https://flutter.dev/docs/get-started/tutorial)
- [Dart 编程语言](https://dart.dev/)

---

现在你已经完成了 Flutter 的安装和配置，可以开始开发移动应用版本的 OFC 扑克游戏了！
