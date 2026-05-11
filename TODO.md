# 壳中客 Kezhongke - 统一开发进度看板 (v3.2)

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
- [x] 文章封面图系统 (Article.cover_image 字段 + /content/covers/ 存储，期刊/首页动态渲染)

### Phase 2.5: 首页与期刊联动 (DONE)
- [x] 首页「最新洞察」查看全部按钮 → 跳转 /journal
- [x] 首页洞察卡片改为动态拉取（API 驱动，替换硬编码占位内容）

### Phase 2.6: 导航栏组件化 (DONE)
- [x] 提取导航栏 CSS 为 shared/nav.css
- [x] 提取导航栏 HTML + 登录态 JS 为 shared/nav.js（动态注入）
- [x] 各页面移除内联导航栏，改为引用共享组件
- [x] 修复全站下拉卡片标签不匹配与透明度问题
- [x] 导航栏 z-index 统一
- [x] 共享 `.liquid-glass` 基础样式、资源版本号、下拉菜单稳定显隐

### Phase 2.7: 真实内容挂载 (DONE)
- [x] 工坊页「原型库 Prototypes」更名为「项目工坊 Projects」
- [x] 工坊页挂载真实项目 AetheL（GitHub 外链跳转 + logo 图标）
- [x] 生长页挂载真实教程 Handy Multi-Agent（飞书外链 + DataWhale × CAMEL 共建课程标签）
- [x] 文章封面图挂载（后端开发的范式转移、面向青年群体的 AI 前沿知识传播）

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
- 文章封面图存储在 `/var/www/kezhongke_content/covers/`，通过 `/content/covers/` 路径访问。
- 工坊项目挂载目前为静态外链，Phase 3 完成后可改为 API 驱动。

---
*更新时间: 2026-05-09 (CST)*
