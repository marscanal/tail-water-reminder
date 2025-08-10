# 喝水提醒小助手 (前后端分离 + Tauri 桌面应用)

## 结构
- `backend`: FastAPI 后端，提供 REST API 并使用 CSV 存储每日饮水量。
- `frontend`: Vue 3 + Vite 前端，可作为 Web 应用运行，也通过 Tauri 打包为桌面应用。

## 运行

### 1. 启动后端服务
后端服务为前端和桌面应用提供数据接口。

```bash
# 进入后端目录
cd backend

# (如果初次运行) 创建并激活虚拟环境，安装依赖
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# 启动 FastAPI 服务
uvicorn app:app --reload --port 8000
```

### 2. 启动前端

#### 方式一：在浏览器中运行

```bash
# 进入前端目录
cd frontend

# (如果初次运行) 安装依赖
npm install

# 启动 Vite 开发服务器
npm run dev
```
在浏览器中打开 `http://localhost:5173`。Vite 开发服务器已配置将 `/api` 请求代理到 `http://localhost:8000`。

#### 方式二：作为 Tauri 桌面应用运行

确保后端服务已在运行。

```bash
# 进入前端目录
cd frontend

# (如果初次运行) 安装依赖
npm install

# 启动 Tauri 开发模式
npm run tauri:dev
```
这将启动一个本地桌面窗口来调试应用。

## 提醒策略说明

* 本实现把提醒逻辑放在前端：前端从后端读取提醒配置（间隔、站立时长、是否启用），并用 `setInterval` 在客户端触发本地 Notification。好处是无需在服务器维持长连接或后台任务；缺点是在浏览器关闭或页面刷新时提醒会停止。若需要后台持续提醒，可将定时任务放到后端并使用系统通知或额外客户端守护进程。

## 可改进点

* 使用 SQLite 或数据库代替 CSV，增加并发与完整性。
* 使用 WebSocket 推送或 Server-Side scheduling (APScheduler) 实现后端主动推送。
* 加入用户账号/多用户支持并保存历史图表。