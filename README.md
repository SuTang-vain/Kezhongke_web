# Kezhongke Web

壳中客 Kezhongke 官方网站，围绕 AI、多智能体协作、人文技术实践与社区共建展开。

**核心理念：共鸣 · 协作 · 共建**

线上访问：

- `http://39.105.42.19/`
- `http://kezhongke.cn/`
- `http://www.kezhongke.cn/`

## 项目简介

壳中客官方网站不是传统品牌展示页，也不是单纯的技术博客，而是一个可感知的生态入口。用户进入后，能立即感受到品牌的思想气质、知识体系、人才路径与共建机制。

## 页面结构

| 页面 | 目录 | 说明 |
| --- | --- | --- |
| 首页 | `home/` | 品牌首屏，建立壳中客 Kezhongke 品牌识别 |
| 生长 | `grow/` | 教程体系与知识演进网络 |
| 路径 | `path/` | 人才培养体系与试点项目 |
| 工坊 | `atelier/` | 开放原型与共建议题 |
| 期刊 | `journal/` | 深度文章、研究札记与人文观察 |
| 关于 | `about/` | 品牌理念与团队介绍 |

每个页面目录包含：

- `code.html`：页面源码，基于 Tailwind CSS CDN
- `screen.png`：部分页面保留的设计稿或视觉截图

## 部署与同步

服务器部署目录：

```bash
/var/www/kezhongke
```

Nginx 当前挂载关系：

| 路径 | 文件 |
| --- | --- |
| `/` | `/var/www/kezhongke/home/code.html` |
| `/about` | `/var/www/kezhongke/about/code.html` |
| `/grow` | `/var/www/kezhongke/grow/code.html` |
| `/journal` | `/var/www/kezhongke/journal/code.html` |
| `/path` | `/var/www/kezhongke/path/code.html` |
| `/atelier` | `/var/www/kezhongke/atelier/code.html` |
| `/kezhongke_logo/` | `/var/www/kezhongke/kezhongke_logo/` |

本项目已配置部署脚本：

```bash
./deploy.sh
```

该脚本将代码同步至远程服务器 `ecs-server` (`39.105.42.19`)，并配置 Nginx 访问权限。

## 设计系统

设计系统基于 **Liquid Glass** 美学，融合中国传统人文温度与前沿技术的通透质感。

- 配色：以 **Soft Amber (#D94B2B)** 为核心点缀色，**Paper White** 为基底
- 字体：标题使用 **思源宋体（Source Han Serif SC）**，正文使用 **Inter**
- 组件：毛玻璃卡片（Glass Cards）、液态按钮（Liquid Buttons）、浮动导航岛、内嵌搜索胶囊
- 圆角：超椭圆曲线（Squircle），最小 24px 圆角，保持"液滴"视觉语言

### 导航栏规范

顶部导航在所有页面保持一致：

- 双语导航项：`首页 Home`、`成长 Grow`、`路径 Path`、`工坊 Atelier`、`期刊 Journal`、`关于 About`
- 搜索框嵌入导航栏内部，不使用外部弹出层
- 当前页使用橙色文字与细下划线高亮
- 页面显式锁定浅色渲染，避免移动浏览器或系统深色模式把页面整体压暗

详细设计规范见 `liquid_humanism/DESIGN.md`。

## 产品需求文档

完整 PRD 见 [`kezhongke_prd_v1.1.md`](kezhongke_prd_v1.1.md)，涵盖产品定位、用户画像、设计原则、页面结构等内容。

## 用户画像

- **学术探索者** — 关注 AI、社会学、认知科学，寻求系统化知识入口
- **产业实践者** — 关注 AI Agent 与自动化落地，寻求真实案例与合作
- **社区共建者** — 开发者、设计师、研究者，参与开放原型与内容共创

## 技术栈

- HTML + [Tailwind CSS](https://tailwindcss.com)（CDN 引入）
- Google Fonts（思源宋体 + Inter）
- Material Symbols 图标
- 原生 CSS Liquid Glass 效果
- Nginx 静态站点部署

## 快速开始

静态页面可以直接在浏览器中打开，也可以启动本地 HTTP 服务预览：

```bash
open home/code.html

# 或在项目根目录启动本地服务
python3 -m http.server 8765
```

## 负责人

耀月

## License

All rights reserved.
