# 喝水提醒小助手 (Tauri + Capacitor + Node.js)

一个跨平台的喝水提醒应用，支持 Windows 桌面和 Android 移动端。

## 技术架构

- **后端**: Node.js + Express + WebSocket，负责定时任务调度。
- **桌面端 (Windows)**: Tauri + Vue 3，Tauri 负责创建桌面应用外壳，并在启动时自动运行内置的 Node.js 后端。
- **移动端 (Android)**: Capacitor + Vue 3，将前端应用打包成原生 Android App。
- **核心逻辑**:
    - **Windows**: 由 Node.js 后端定时通过 WebSocket 向 Tauri 前端发送通知指令，前端调用系统原生通知。
    - **Android**: 由 Capacitor App 在本地通过 `setInterval` 创建定时器，并调用 Capacitor 本地通知插件来发送通知，以适应移动端环境。

## 项目结构

- `backend/`: Node.js 后端服务。
- `frontend/`: Vue 3 前端项目，同时也是 Tauri 和 Capacitor 的容器。
    - `src/`: 前端源码。
    - `src-tauri/`: Tauri 的 Rust 源码和配置。
    - `capacitor.config.json`: Capacitor 配置文件。
- `package.json`: 项目根目录的 `package.json`，用于统一管理和启动项目。

## 如何使用

### 1. 环境准备

- 安装 [Node.js](https://nodejs.org/)
- 安装 [Rust](https://www.rust-lang.org/tools/install) 环境（用于 Tauri）
- 安装 [Android Studio](https://developer.android.com/studio)（用于安卓打包）
- 在项目根目录运行 `npm install` 来安装所有依赖。

### 2. 开发模式运行 (Windows 桌面)

在项目**根目录**运行以下命令：

```bash
npm run start
```

此命令会使用 `concurrently` 同时启动两项服务：
1.  Node.js 后端服务。
2.  Tauri 开发窗口，并加载前端应用。

应用启动后，会根据默认间隔（30分钟）发送桌面通知。你可以在应用内修改提醒间隔。

### 3. 打包和运行安卓 App

1.  **进入前端目录**:
    ```bash
    cd frontend
    ```

2.  **添加 Android 平台** (只需运行一次):
    ```bash
    npx cap add android
    ```

3.  **同步前端代码和依赖**到 Android 项目:
    ```bash
    npx cap sync
    ```

4.  **在 Android Studio 中打开项目**:
    ```bash
    npx cap open android
    ```

5.  在 Android Studio 中，你可以：
    -  点击 "Run 'app'" 按钮，在连接的设备或模拟器上运行 App。
    -  通过 `Build > Build Bundle(s) / APK(s) > Build APK(s)` 来生成可安装的 APK 文件。
