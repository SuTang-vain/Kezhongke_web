# 壳中客 Kezhongke - 统一开发进度看板 (v2.7)

## 0. 当前运行状态 (System Status)
*   **后端 API**: ● 运行中 (Port 8000, Proxy via Nginx /api/)
*   **数据库**: ● 运行中 (PostgreSQL 16 Docker)
*   **缓存**: ● 运行中 (Redis 7 Docker)
*   **外网访问**: 已开通 (http://39.105.42.19/api/health)

## 1. 技术栈 (Modern Stack 2026)
- **后端**: `uv` (Python 3.12) + `FastAPI` + `SQLModel` + `Postgres/Redis`
- **发信**: `Aliyun Direct Mail SDK`
- **设计**: `Liquid Glass (液态玻璃)` 视觉规范

## 2. 核心架构
- **Identity Provider (IdP)**: 统一身份认证，支持 JWT 穿透。
- **Project Mounter**: 内容挂载与反向代理。

## 3. 开发进度 (Implementation Phases)

### Phase 1: 身份、鉴权与个人中心 (DONE)
- [x] 基于 Redis 的 OTP 验证码系统
- [x] 阿里云邮件推送集成 (hello@kezhongke.cn)
- [x] JWT 登录与 RBAC 权限系统
- [x] 登录/注册 UI (Liquid Glass 风格)
- [x] **[NEW]** 用户模型扩展 (Nickname, Avatar, Bio)
- [x] **[NEW]** 个人信息 management 接口 (GET/PATCH /users/me)
- [x] **[NEW]** 首页与全局导航栏登录态动态显示

### Phase 2: 内容挂载系统 (PENDING)
- [ ] 文章元数据管理 (PostgreSQL)
- [ ] Markdown/PDF 安全预览引擎
- [ ] Nginx 静态目录别名配置

### Phase 3: 项目引擎与生态 (PENDING)
- [ ] 项目注册管理接口
- [ ] 动态项目导航岛 (Frontend Component)

## 4. API 接口清单
- [x] POST /api/auth/request-otp - 请求OTP
- [x] POST /api/auth/verify-otp - 验证并注册
- [x] POST /api/auth/login - 登录
- [x] GET /api/auth/me - 获取个人资料
- [x] **[DONE]** PATCH /api/auth/me - 更新个人资料

## 5. 待解决问题
1.  **安全加固**: 关闭 DB/Redis 外部端口。
2.  **HTTPS**: Certbot SSL 证书申请。

## 6. 本地开发工作流 (Local Development Workflow)
为支持在本地修改代码并验证，请遵循以下步骤：
1. **启动本地数据库**: 确保本地 Docker Desktop 运行中，执行 `docker-compose up -d db redis`
2. **初始化环境与数据库**: 执行 `uv sync` 和 `uv run alembic upgrade head`
3. **启动后端服务**: 执行 `uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`
4. **启动前端代理服务 (支持跨域与Nginx路由模拟)**: 在新终端执行 `python3 dev_server.py`
5. **本地预览**: 访问 `http://localhost:3000` 进行开发测试。
6. **同步到服务器**: 验证无误后，将本地代码 commit 到 git 并推送到远端，然后在服务器 pull，或直接修改 `deploy.sh` 从本地推送到服务器。

---
*更新时间: 2026-05-07 23:00 (CST)*
