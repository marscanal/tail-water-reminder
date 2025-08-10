# 喝水提醒小助手 (前后端分离示例)

## 结构
- backend: FastAPI 后端，提供 REST API 并使用 CSV 存储每日饮水量
- frontend: Vue 3 + Vite 前端，通过 `/api` 代理调用后端

## 运行
1. 启动后端

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```
```bash
cd backend
.venv\Scripts\activate
uvicorn app:app --reload --port 8000
```

2. 启动前端

```bash
cd frontend
npm install
npm run dev
```
```bash
cd frontend
npm run dev
```

前端 dev server 已配置将 `/api` 代理到 `http://localhost:8000`，因此可直接在浏览器打开 `http://localhost:5173`。

## 提醒策略说明

* 本实现把提醒逻辑放在前端：前端从后端读取提醒配置（间隔、站立时长、是否启用），并用 `setInterval` 在客户端触发本地 Notification。好处是无需在服务器维持长连接或后台任务；缺点是在浏览器关闭或页面刷新时提醒会停止。若需要后台持续提醒，可将定时任务放到后端并使用系统通知或额外客户端守护进程。

## 可改进点

* 使用 SQLite 或数据库代替 CSV，增加并发与完整性。
* 使用 WebSocket 推送或 Server-Side scheduling (APScheduler) 实现后端主动推送。
* 加入用户账号/多用户支持并保存历史图表。

