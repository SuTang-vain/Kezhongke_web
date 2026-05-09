# 工作记录：期刊文章安全预览与内容挂载

日期：2026-05-08  
项目：壳中客 Kezhongke 官方网站  
涉及环境：本地 `/Users/tangyaoyue/Kezhongke_web`，ECS `/var/www/kezhongke`、`/var/www/kezhongke_backend`

## 1. 工作目标

完成 TODO 中 Phase 2「内容挂载系统」的剩余开发，使当前挂载在「期刊」页面的四篇文章能够正常展示：

- 后端开发的范式转移：从工程转化视角审视 AI 工程化的岗位结构演变与能力需求
- 面向青年群体的 AI 前沿知识传播：叙事策略与社群运营框架
- AI 时代青年“冷思考”能力的识别与培养路径
- 多智能体社会学视角下的人机关系分析框架

目标覆盖：

- Markdown/PDF 安全预览引擎
- Nginx 静态目录别名配置
- 期刊列表到文章详情页的完整访问链路
- 本地与服务器双端同步
- GitHub 仓库同步

## 2. 开发内容

### 2.1 后端安全预览接口

新增后端内容预览服务：

- 文件：`app/services/content.py`
- 功能：
  - 限制内容根目录为 `/var/www/kezhongke_content`
  - 阻止绝对路径、空路径、`.`、`..`、空字节等非法路径
  - 使用 `Path.resolve()` 和 `relative_to()` 防止路径穿越
  - 仅允许 `.md`、`.markdown`、`.pdf`
  - Markdown 以 UTF-8 文本返回
  - PDF 返回受控静态访问地址
  - 限制 Markdown 最大 2MB，PDF 最大 50MB

新增 API：

- `GET /api/articles/{slug}/preview`

返回内容包括：

- 文章元数据
- `preview_type`
- `content_type`
- `content_url`
- Markdown `content`

### 2.2 数据模型与配置

更新文件：

- `app/models/article.py`
  - 新增 `ArticlePreview`
  - 支持 Markdown/PDF 预览响应结构
- `app/core/config.py`
  - 新增 `CONTENT_ROOT`
  - 新增 `MARKDOWN_MAX_BYTES`
  - 新增 `PDF_MAX_BYTES`
- `app/api/article.py`
  - 接入 `content_preview_service`
  - 新增 `/preview` 路由

### 2.3 前端文章页

更新文件：

- `article/index.html`

调整内容：

- 文章详情页不再直接拉取 `/content/{file_path}` 作为主要数据源
- 改为请求 `/api/articles/{slug}/preview`
- Markdown 由 API 返回后使用 `marked` 渲染
- 使用 `DOMPurify` 做 HTML 清洗
- 禁止 `style`、`script`、`iframe`、`object`、`embed` 等高风险标签
- 外链自动加 `target="_blank"` 和 `rel="noopener noreferrer"`
- 预留 PDF iframe 预览展示

### 2.4 Nginx 配置

更新文件：

- `kezhongke_nginx.conf`

调整内容：

- 修复 `/` 根路径返回 403 的问题
- 修复 `/article?slug=...` 被目录索引命中导致 403 的问题
- 为 `/journal`、`/article`、`/auth` 等短路径增加精确路由
- `/content/` 改为安全静态别名：
  - `alias /var/www/kezhongke_content/`
  - `autoindex off`
  - 显式声明 Markdown/PDF 类型
  - 添加 `X-Content-Type-Options: nosniff`
  - 添加短缓存头
  - 使用 `try_files $uri =404`

同时在服务器上处理了重复 Nginx 配置：

- 旧配置 `/etc/nginx/conf.d/kezhongke.conf` 已备份为：
  - `/etc/nginx/conf.d/kezhongke.conf.bak-20260508-article-preview`
- 当前保留生效配置：
  - `/etc/nginx/conf.d/kezhongke_nginx.conf`

## 3. 部署操作

### 3.1 同步到 ECS

同步后端文件到：

- `/var/www/kezhongke_backend/app/core/config.py`
- `/var/www/kezhongke_backend/app/models/article.py`
- `/var/www/kezhongke_backend/app/api/article.py`
- `/var/www/kezhongke_backend/app/services/content.py`

同步前端与 Nginx 文件到：

- `/var/www/kezhongke/article/index.html`
- `/var/www/kezhongke/TODO.md`
- `/etc/nginx/conf.d/kezhongke_nginx.conf`

### 3.2 服务重载

执行内容：

- 后端 Python 编译检查：通过
- 重启 `uvicorn app.main:app --host 0.0.0.0 --port 8000`
- `nginx -t`：通过
- `systemctl reload nginx`：完成

### 3.3 文件权限修正

发现第一篇 Markdown 文件权限为 `600`，Nginx 无法读取，返回 403。

修正内容：

- `/var/www/kezhongke_content`
- `/var/www/kezhongke_content/articles`
- `/var/www/kezhongke_content/articles/2026`
- `/var/www/kezhongke_content/articles/2026/*.md`

最终目录权限统一为可遍历，Markdown 文件权限统一为可读。

## 4. 验证结果

### 4.1 后端接口

以下接口验证通过：

- `GET /api/health`：200
- `GET /api/articles/`：200，返回 4 篇文章
- `GET /api/articles/ai-engineering-paper-to-product/preview`：200
- `GET /api/articles/youth-ai-knowledge-propagation/preview`：200
- `GET /api/articles/youth-cold-thinking/preview`：200
- `GET /api/articles/multi-agent-sociology/preview`：200

### 4.2 静态内容别名

以下 Markdown 文件访问验证通过：

- `/content/articles/2026/ai-engineering-paper-to-product.md`：200
- `/content/articles/2026/youth-ai-knowledge-propagation.md`：200
- `/content/articles/2026/youth-cold-thinking.md`：200
- `/content/articles/2026/multi-agent-sociology.md`：200

目录索引验证：

- `/content/articles/2026/`：404，符合关闭目录索引预期

### 4.3 页面访问

以下页面服务侧验证通过：

- `/`：200
- `/journal`：200
- `/article?slug=ai-engineering-paper-to-product`：200

用户侧确认：期刊文章已经能够正常挂载和显示。

## 5. Git 同步

已推送到 GitHub 仓库：

- 仓库：`https://github.com/SuTang-vain/Kezhongke_web`
- 分支：`master`
- 提交：`3f4996b Add secure article content preview`

本次提交文件：

- `TODO.md`
- `app/api/article.py`
- `app/core/config.py`
- `app/models/article.py`
- `app/services/content.py`
- `article/index.html`
- `kezhongke_nginx.conf`

未提交且未推送的本地无关文件：

- `.env`
- `create_article_page.py`
- `journal/code.html.bak`
- `scripts/`

## 6. 当前状态

Phase 2 内容挂载系统已完成：

- Markdown/PDF 安全预览引擎：完成
- Nginx 静态目录别名配置：完成
- 四篇期刊文章：已正常挂载并可阅读
- 本地代码：已更新
- ECS 服务器：已更新并运行
- GitHub：已同步

## 7. 后续建议

仍建议继续处理两个运维项：

1. 关闭 PostgreSQL `5432` 与 Redis `6379` 的公网暴露，仅允许本机或内网访问。
2. 配置 HTTPS，使用 Certbot 或阿里云证书启用全站 TLS。

