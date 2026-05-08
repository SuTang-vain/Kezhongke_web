# 归档文档：壳中客 Kezhongke - 后端与挂载系统开发文档 (v2.6)

状态：历史归档，不再作为当前开发进度主文档使用。当前主文档请查看 `TODO.md`。

## 0. 当前运行状态 (System Status)
*   **后端 API**: ● 运行中 (Port 8000, Proxy via Nginx /api/)
*   **数据库**: ● 运行中 (PostgreSQL 16 Docker)
*   **缓存**: ● 运行中 (Redis 7 Docker)
*   **监控**: ● 运行中 (Aliyun Argus Agent 4.0.0)
*   **外网访问**: 已开通 (http://39.105.42.19/api/health)

## 1. 技术栈 (Modern Stack 2026)
- **包管理**: `uv` (Python 3.12)
- **框架**: `FastAPI` + `SQLModel`
- **数据库**: `PostgreSQL` + `Redis`
- **发信**: `Aliyun Direct Mail SDK`

## 2. 核心架构
- **Identity Provider (IdP)**: 统一身份认证，支持 JWT 穿透。
- **Project Mounter**: 支持静态目录挂载与反向代理挂载。

## 3. 开发进度 (Implementation Phases)

### Phase 0: 基础设施 (100% DONE)
- [x] ECS 环境初始化 (uv, Docker, Python 3.12)
- [x] 数据库与缓存容器化部署 (Postgres, Redis)
- [x] 数据库迁移框架初始化 (Alembic + SQLModel)

### Phase 1: 身份与鉴权 (100% DONE)
- [x] 基于 Redis 的 OTP (验证码) 生成与校验服务
- [x] 基础 Auth 接口实现 (request-otp, verify-otp)
- [x] 阿里云邮件推送 SDK 集成 (AccessKey 已配置)
- [x] **[RESOLVED]** 调试真实邮件送达问题 - 修复 endpoint: dm.aliyuncs.com
- [x] 用户数据库注册逻辑 (验证码通过后创建用户)
- [x] JWT 登录与权限中间件 (Role-based Access Control)

### Phase 2: 内容管理 (PENDING)
- [ ] 文章元数据 API
- [ ] Markdown/PDF 安全预览引擎 (Path Traversal Protection)

### Phase 3: 项目挂载引擎 (PENDING)
- [ ] 项目注册管理接口 (Static/Proxy/External)
- [ ] Nginx 动态路由配置模板

### Phase 4: 前端集成 (IN PROGRESS - 50%)
- [x] 登录注册页面 (/auth) - UI优化完成，左右布局+品牌IP+LiquidGlass输入框
- [ ] 动态项目导航岛

### 新增 API 接口 (v2.6)
- [x] POST /api/auth/request-otp - 请求OTP验证码
- [x] POST /api/auth/verify-otp - 验证OTP并注册用户
- [x] POST /api/auth/login - 用户登录
- [x] GET /api/auth/me - 获取当前用户信息
- [x] POST /api/auth/logout - 用户登出

### 登录注册页面功能 (v2.6)
- [x] 登录注册页面 - 左右布局
- [x] 左侧：品牌IP形象 + slogan + 特色标签
- [x] 右侧：登录/注册表单
- [x] Liquid Glass 风格输入框
- [x] 响应式设计（移动端适配）
- [ ] 首页登录状态展示（用户头像/昵称）
- [ ] 登出功能


## 2.1 前端交互设计 (v2.6 新增)
- **顶部状态菜单栏**: 即刻连接 按钮
- **交互流程**:
  1. 首页点击即刻连接 → 跳转登录/注册页面
  2. 用户完成登录/注册 → 返回首页（带已登录状态）
  3. 首页根据登录状态显示用户信息/登出按钮
- **关于页面**: 作为辅助入口（非主要流程），可从底部导航或Footer进入

## 4. 待解决问题 (Open Questions & Debugging)
1.  ~~**邮件未收到**: 已修复 endpoint 配置 (dm.cn-beijing → dm.aliyuncs.com)~~
2.  **安全加固**: ✅ 已完成 (DB/Redis 绑定 127.0.0.1，防火墙清理 8888)
3.  **HTTPS**: ✅ 已配置 (阿里云证书 + Nginx TLSv1.2/1.3 + HTTP→HTTPS 301重定向)

---
*更新时间: 2026-05-07 18:50 (CST)*
