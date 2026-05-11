# 工作记录：服务器运维、HTTPS、安全加固、导航栏组件化

日期：2026-05-09  
项目：壳中客 Kezhongke 官方网站  
涉及环境：本地 `/Users/tangyaoyue/Kezhongke_web`，ECS `/var/www/kezhongke`、`/var/www/kezhongke_backend`

## 1. 工作目标

完成 TODO 中的运维安全项（HTTPS、安全加固），推进前端体验优化（首页期刊联动、导航栏组件化），并建立共享导航栏架构以解决全站同步维护问题。

## 2. 开发内容

### 2.1 TODO 文档更新（v2.7 → v3.0）

- 合并清理：用户手动归档删除了 `TODO_BACKEND_CONTENT.md`，保留单一 `TODO.md`
- 版本迭代：
  - v2.8：新增 Uvicorn 进程守护、登出功能、运维安全独立为已完成节
  - v2.9：新增 Phase 2.5（首页期刊联动）
  - v3.0：新增 Phase 2.6（导航栏组件化），核心架构新增 Shared Navigation 说明

### 2.2 宝塔面板卸载

- 原因：服务器仅 1.8GB 内存，宝塔占用不必要资源；已习惯 SSH 管理
- 操作：执行 `bt-uninstall.sh`，清理防火墙 8888 端口
- 内存释放：674MB → 637MB
- 磁盘释放：7.7GB → 7.0GB

### 2.3 HTTPS 配置

- 证书来源：阿里云 SSL 证书 `/Users/tangyaoyue/Downloads/24920351_kezhongke/`（kezhongke.cn.pem + .key）
- Nginx 配置：
  - 上传证书到 `/etc/nginx/ssl/`
  - 新增 443 server block：TLSv1.2/1.3、现代加密套件、HSTS
  - HTTP 80 → HTTPS 301 重定向
  - www.kezhongke.cn / IP 访问统一重定向到 https://kezhongke.cn
- 防火墙：放行 443 端口

### 2.4 安全加固

- DB/Redis 端口绑定：docker-compose.yml 中 `0.0.0.0:5432` → `127.0.0.1:5432`，`0.0.0.0:6379` → `127.0.0.1:6379`
- 容器重启：`docker compose down && docker compose up -d`
- 防火墙清理：移除 8888 端口（宝塔已卸载）
- 验证：公网扫描 5432/6379 不可访问，本机连接正常

### 2.5 Uvicorn 进程守护

- 创建 `/etc/systemd/system/kezhongke-api.service`
- 配置：`Restart=always`、`RestartSec=5`、依赖 `docker.service`、开机自启
- 日志：stdout → `uvicorn.log`，stderr → `uvicorn-error.log`
- 绑定地址改为 `127.0.0.1`（不再对外暴露 8000）

### 2.6 首页期刊联动（Phase 2.5）

#### 查看全部跳转
- 将「最新洞察」区域的 `<button>` 改为 `<a href="/journal">`

#### 洞察卡片动态化
- 移除硬编码的两张占位卡片（"多智能体网络中的信任重建机制"、"液态玻璃视觉范式解析"）
- 新增 `#insights-loading`、`#insights-container`、`#insights-empty` 三个动态容器
- JS 从 `/api/articles/` 拉取最新 2 篇文章，渲染为 Liquid Glass 风格卡片
- 点击卡片跳转 `/article?slug=xxx`，与期刊页数据同步

### 2.7 导航栏组件化（Phase 2.6）

#### 问题发现
- 全站 6 个页面各自内联导航栏 CSS（~140 行）、HTML（~60 行）、JS（~120 行）
- 首页存在 HTML 标签不匹配（`<button>` 用 `</a>` 闭合），导致渲染错乱
- 用户下拉卡片背景 `rgba(255,255,255,0.7)` 过于透明，深色背景下可读性差
- 修改导航需同步 6 个文件，维护成本高

#### 解决方案
提取共享组件 `/var/www/kezhongke/shared/`：
- `nav.css`：导航栏全部样式（`#top-nav`、`.nav-link`、`.nav-cta`、`.user-dropdown` 等）
- `nav.js`：导航栏 HTML 动态注入 + 登录态管理（auth/me、logout、profile editor）+ 搜索 + 活跃页面高亮

#### 执行内容
- 基准代码取自首页已修复的版本（`<div>` 替代 `<button>`，dropdown 透明度 0.92）
- Python 脚本批量处理 6 个页面（home、journal、about、grow、path、atelier）：
  - 精确定位并移除内联 CSS、nav HTML、profile modal、auth script
  - 插入 `<link rel="stylesheet" href="/shared/nav.css" />`
  - 插入 `<script src="/shared/nav.js"></script>`
- z-index 统一：nav `z-[9999]`、dropdown `z-[100]`、profile modal `z-[10001]`

#### 后续修复记录
- 首页底部空白滚动的直接原因是残留 `<canvas id="liquid-canvas">` 仍在文档流中，脚本将其尺寸设为视口宽高后撑出额外一屏。
- 修复方式改为移除首页残留 canvas 节点，保留原 `body::before inset: -12%` 环境背景，避免改变原有背景透明度和玻璃观感。
- 用户下拉菜单显隐不再依赖运行时注入的 Tailwind `group-hover:*` 类，改由 `shared/nav.css` 的 `#user-profile:hover / :focus-within / .is-open` 控制，并由 `nav.js` 支持点击开关、Esc 与点击外部关闭。
- 组件化时遗漏的 `.liquid-glass` 基础样式已补回 `shared/nav.css`，恢复首页三大入口卡片、Logo 容器和期刊卡片一致的玻璃背景、边框与阴影。
- 6 个页面的共享导航资源引用已加版本号 `v=20260509-glass2`，避免浏览器继续使用旧缓存。

## 3. 部署操作

### 3.1 服务器文件变更

| 文件 | 操作 |
|------|------|
| `/etc/nginx/ssl/kezhongke.cn.pem` | 新增（SSL 证书） |
| `/etc/nginx/ssl/kezhongke.cn.key` | 新增（SSL 私钥） |
| `/etc/nginx/conf.d/kezhongke_nginx.conf` | 修改（HTTPS 配置） |
| `/etc/systemd/system/kezhongke-api.service` | 新增（进程守护） |
| `/var/www/kezhongke_backend/docker-compose.yml` | 修改（端口绑定 127.0.0.1） |
| `/var/www/kezhongke/shared/nav.css` | 新增（共享导航栏样式） |
| `/var/www/kezhongke/shared/nav.js` | 新增（共享导航栏逻辑） |
| `/var/www/kezhongke/home/code.html` | 修改（期刊联动 + 导航栏组件化 + 移除残留 canvas） |
| `/var/www/kezhongke/journal/code.html` | 修改（导航栏组件化 + 共享资源版本号） |
| `/var/www/kezhongke/about/code.html` | 修改（导航栏组件化 + 共享资源版本号） |
| `/var/www/kezhongke/grow/code.html` | 修改（导航栏组件化 + 共享资源版本号） |
| `/var/www/kezhongke/path/code.html` | 修改（导航栏组件化 + 共享资源版本号） |
| `/var/www/kezhongke/atelier/code.html` | 修改（导航栏组件化 + 共享资源版本号） |
| `/var/www/kezhongke/TODO.md` | 修改（v2.7 → v3.1） |

### 3.2 服务重载

- `systemctl daemon-reload && systemctl enable kezhongke-api && systemctl start kezhongke-api`
- `nginx -t && systemctl reload nginx`
- `docker compose down && docker compose up -d`（数据库/Redis 端口变更）
- `firewall-cmd --permanent --add-service=https && firewall-cmd --reload`

## 4. 验证结果

### 4.1 HTTPS
- `https://kezhongke.cn` — 200，HTTP/2
- `http://kezhongke.cn` — 301 → HTTPS
- `https://www.kezhongke.cn` — 301 → `https://kezhongke.cn`

### 4.2 安全加固
- `127.0.0.1:5432` / `127.0.0.1:6379` — 仅本机监听
- 公网 5432/6379 不可访问

### 4.3 进程守护
- `systemctl status kezhongke-api` — active (running)
- API 验证通过：`https://kezhongke.cn/api/health`

### 4.4 导航栏组件化
- 6 个页面均引用 `shared/nav.css` + `shared/nav.js`
- 0 处内联导航残留
- 首页下拉菜单显示正常
- 下拉菜单显隐由共享 CSS/JS 控制，不再依赖动态 Tailwind `group-hover:*`

### 4.5 首页期刊联动
- 洞察卡片从 API 动态拉取，与期刊页数据同步
- 「查看全部」跳转到 /journal

### 4.6 首页视觉回归
- 首页不再包含 `<canvas id="liquid-canvas">` 节点，避免底部空白滚动复发
- `body::before inset: -12%` 保持原值，背景透明度与原页面一致
- `.liquid-glass` 已进入共享样式，首页入口卡片恢复玻璃背景、边框和阴影

## 5. 当前状态

- Phase 1（身份鉴权）：已完成
- Phase 2（内容挂载）：已完成
- Phase 2.5（首页期刊联动）：已完成
- Phase 2.6（导航栏组件化）：已完成
- 运维安全：已完成（HTTPS + 安全加固 + 进程守护）

## 6. 后续建议

1. 后续修改导航栏优先改 `shared/nav.css` 和 `shared/nav.js`，避免重新复制内联导航。
2. 保留 `.liquid-glass` 在共享样式中，避免页面卡片恢复为透明裸容器。
3. 继续推进 Phase 3（项目引擎与生态）

---
*更新时间: 2026-05-09 (CST)*

---

## 附录：后续工作（同日 17:00-19:00）

### A. 文章封面图系统

#### 数据模型扩展
- Article 模型新增 `cover_image: Optional[str]` 字段
- Alembic 迁移 `f468afac6d94_add_cover_image_to_article` 已执行
- 修复迁移脚本缺少 `import sqlmodel` 的问题

#### 封面图上传
- 创建 `/var/www/kezhongke_content/covers/` 目录
- 上传封面图：
  - `ai-engineering-paper-to-product.png`（后端开发的范式转移）
  - `youth-ai-knowledge-propagation.png`（面向青年群体的 AI 前沿知识传播）
- 数据库更新：通过 psql 更新对应文章的 cover_image 字段

#### 前端渲染
- 期刊页 Featured 文章：有 cover_image 时显示 `<img>`，无图时保留渐变色占位
- 期刊页列表卡片：有封面图时在顶部显示 `h-48` 图片区域，无图时不显示
- 首页洞察卡片：同上逻辑

### B. 工坊页真实项目挂载

- 「原型库 Prototypes」更名为「项目工坊 Projects」
- 第一个占位卡片替换为真实项目 **AetheL**：
  - 链接：https://github.com/SuTang-vain/AetheL（新标签页打开）
  - Logo：上传 `/kezhongke_logo/aethel-logo.png` 替换 Material 图标
  - 介绍：面向产品构思的 AI 认知工作区
  - 状态标签：开发中 · Active

### C. 生长页真实教程挂载

- 第一个占位卡片替换为真实教程 **Handy Multi-Agent**：
  - 链接：飞书文档（https://dcnk566ts94k.feishu.cn/wiki/Ft45w5wFMidIqMkx95Qc0eDvnHf）
  - 标签：DataWhale × CAMEL 共建课程（琥珀色高亮）
  - 介绍：基于 CAMEL 框架的多智能体开发教程
  - 标签和标题经过视觉优化：单一共建课程标签、干净标题、统一行间距

### D. 服务器文件变更（追加）

| 文件 | 操作 |
|------|------|
| `/var/www/kezhongke_backend/app/models/article.py` | 修改（新增 cover_image 字段） |
| `/var/www/kezhongke_backend/alembic/versions/f468afac6d94_...` | 新增（数据库迁移） |
| `/var/www/kezhongke_content/covers/ai-engineering-paper-to-product.png` | 新增（封面图） |
| `/var/www/kezhongke_content/covers/youth-ai-knowledge-propagation.png` | 新增（封面图） |
| `/var/www/kezhongke/kezhongke_logo/aethel-logo.png` | 新增（项目 logo） |
| `/var/www/kezhongke/journal/code.html` | 修改（封面图渲染） |
| `/var/www/kezhongke/home/code.html` | 修改（封面图渲染） |
| `/var/www/kezhongke/atelier/code.html` | 修改（更名 + AetheL 项目挂载） |
| `/var/www/kezhongke/grow/code.html` | 修改（Handy Multi-Agent 教程挂载） |
| `/var/www/kezhongke/TODO.md` | 修改（v3.1 → v3.2） |
