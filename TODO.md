# 壳中客 Kezhongke - 统一开发进度看板 (v3.1)

## 0. 当前运行状态 (System Status)
*   **后端 API**: ● 运行中 (Port 8000, systemd 守护, Proxy via Nginx /api/)
*   **数据库**: ● 运行中 (PostgreSQL 16 Docker, 127.0.0.1)
*   **缓存**: ● 运行中 (Redis 7 Docker, 127.0.0.1)
*   **HTTPS**: ● 已启用 (TLSv1.2/1.3, HTTP→HTTPS 301重定向)
*   **外网访问**: https://kezhongke.cn/api/health

## 1. 技术栈 (Modern Stack 2026)
- **后端**: `uv` (Python 3.12) + `FastAPI` + `SQLModel` + `Postgres/Redis`
- **发信**: `Aliyun Direct Mail SDK`
- **设计**: `Liquid Glass (液态玻璃)` 视觉规范

## 2. 核心架构
- **Identity Provider (IdP)**: 统一身份认证，支持 JWT 穿透。
- **Project Mounter**: 内容挂载与反向代理。
- **Shared Navigation**: 导航栏拆分为共享组件 (shared/nav.css + shared/nav.js)，一处修改全站同步。

## 3. 开发进度 (Implementation Phases)

### Phase 1: 身份、鉴权与个人中心 (DONE)
- [x] 基于 Redis 的 OTP 验证码系统
- [x] 阿里云邮件推送集成 (hello@kezhongke.cn)
- [x] JWT 登录与 RBAC 权限系统
- [x] 登录/注册 UI (Liquid Glass 风格)
- [x] 用户模型扩展 (Nickname, Avatar, Bio)
- [x] 个人信息管理接口 (GET/PATCH /users/me)
- [x] 首页与全局导航栏登录态动态显示
- [x] 登出功能

### Phase 2: 内容挂载系统 (DONE)
- [x] 文章元数据管理 (PostgreSQL)
- [x] Nginx 静态目录别名配置 (已配置 /content/ 安全静态别名，关闭目录索引)
- [x] Markdown/PDF 安全预览引擎 (通过 /api/articles/{slug}/preview 进行路径校验、类型限制与安全预览)

### Phase 2.5: 首页与期刊联动 (DONE)
- [x] 首页「最新洞察」查看全部按钮 → 跳转 /journal
- [x] 首页洞察卡片改为动态拉取（API 驱动，替换硬编码占位内容）

### Phase 2.6: 导航栏组件化 (DONE)
- [x] 提取导航栏 CSS 为 shared/nav.css
- [x] 提取导航栏 HTML + 登录态 JS 为 shared/nav.js（动态注入）
- [x] 各页面移除内联导航栏，改为引用共享组件（journal/about/grow/path/atelier 已完成）
- [x] 修复全站下拉卡片标签不匹配（`<button>` → `<div>`）与透明度问题（0.7 → 0.92）
- [x] 导航栏 z-index 统一（nav z-[9999], dropdown z-[100], modal z-[10001]）
- [x] 首页导航栏组件化适配（移除残留 canvas 节点，保留原 `body::before inset: -12%` 视觉背景，修复底部空白滚动）
- [x] 共享 `.liquid-glass` 基础样式补回 shared/nav.css，恢复首页卡片与期刊卡片的玻璃容器背景、边框、阴影
- [x] 共享导航资源加版本号 `v=20260509-glass2`，避免浏览器继续使用旧缓存
- [x] 用户下拉菜单改为 CSS/JS 稳定显隐，不再依赖运行时 Tailwind `group-hover:*` 生成

### Phase 3: 项目引擎与生态 (PENDING)
- [ ] 项目注册管理接口
- [ ] 动态项目导航岛 (Frontend Component)

## 4. API 接口清单
- [x] POST /api/auth/request-otp - 请求OTP
- [x] POST /api/auth/verify-otp - 验证并注册
- [x] POST /api/auth/login - 登录
- [x] POST /api/auth/logout - 登出
- [x] GET /api/auth/me - 获取个人资料
- [x] PATCH /api/auth/me - 更新个人资料
- [x] GET /api/articles - 文章列表获取
- [x] GET /api/articles/{slug} - 文章详情获取
- [x] GET /api/articles/{slug}/preview - 安全预览 Markdown/PDF 内容
- [x] POST /api/articles - 创建文章 (需Admin/Author权限)

## 5. 运维与安全 (DONE)
- [x] 宝塔面板卸载
- [x] 安全加固: DB/Redis 绑定 127.0.0.1，防火墙清理
- [x] HTTPS: 阿里云证书 + Nginx TLSv1.2/1.3 + HTTP→HTTPS 301重定向
- [x] Uvicorn 进程守护: systemd kezhongke-api.service, 开机自启, 异常自动重启

## 6. 本地开发工作流 (Local Development Workflow)
1. **启动本地数据库**: 确保本地 Docker Desktop 运行中，执行 `docker-compose up -d db redis`
2. **初始化环境与数据库**: 执行 `uv sync` 和 `uv run alembic upgrade head`
3. **启动后端服务**: 执行 `uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`
4. **启动前端代理服务**: 在新终端执行 `python3 dev_server.py`
5. **本地预览**: 访问 `http://localhost:3000` 进行开发测试
6. **同步到服务器**: 将本地代码 commit 推送到远端，服务器 pull 后 `systemctl restart kezhongke-api`

## 7. 维护说明
- 导航栏修改方式: 编辑 `/var/www/kezhongke/shared/nav.css` 或 `nav.js`，全站自动生效
- 首页底部空白滚动已修复：不要恢复 `<canvas id="liquid-canvas">`，否则脚本会把 canvas 设为视口尺寸并重新撑高页面。
- `.liquid-glass` 是多个页面共用的基础容器样式，必须保留在 shared/nav.css 中；移除后首页入口卡片会失去玻璃背景。

---
*更新时间: 2026-05-09 (CST)*
