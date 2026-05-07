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

### Phase 1: 身份、鉴权与个人中心 (IN PROGRESS)
- [x] 基于 Redis 的 OTP 验证码系统
- [x] 阿里云邮件推送集成 (hello@kezhongke.cn)
- [x] JWT 登录与 RBAC 权限系统
- [x] 登录/注册 UI (Liquid Glass 风格)
- [ ] **[NEW]** 用户模型扩展 (Nickname, Avatar, Bio)
- [ ] **[NEW]** 个人信息 management 接口 (GET/PATCH /users/me)
- [ ] **[NEW]** 首页导航栏登录态动态显示

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
- [ ] **[TODO]** PATCH /api/auth/me - 更新个人资料

## 5. 待解决问题
1.  **安全加固**: 关闭 DB/Redis 外部端口。
2.  **HTTPS**: Certbot SSL 证书申请。

---
*更新时间: 2026-05-07 23:00 (CST)*
