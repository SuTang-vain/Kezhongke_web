# 壳中客 Kezhongke 官方网站

围绕 AI、多智能体协作、人文技术实践与社区共建展开的官方门户。

**核心理念：共鸣 · 协作 · 共建**

## 项目简介

壳中客官方网站不是传统品牌展示页，也不是单纯的技术博客，而是一个可感知的生态入口。用户进入后，能立即感受到品牌的思想气质、知识体系、人才路径与共建机制。

## 页面结构

| 页面 | 目录 | 说明 |
| --- | --- | --- |
| 首页 | `home/` | 品牌首屏，建立壳中客 Kezhongke 品牌识别 |
| 关于 | `about/` | 品牌理念与团队介绍 |
| 成长 | `grow/` | 人才培养与教程体系 |
| 期刊 | `journal/` | 深度文章、研究札记与人文观察 |

每个页面目录包含：
- `code.html` — 页面源码（基于 Tailwind CSS）
- `screen.png` — 页面设计稿截图

## 设计系统

设计系统基于 **Liquid Glass** 美学，融合中国传统人文温度与前沿技术的通透质感。

- 配色：以 **Soft Amber (#D94B2B)** 为核心点缀色，**Paper White** 为基底
- 字体：标题使用 **思源宋体（Source Han Serif SC）**，正文使用 **Inter**
- 组件：毛玻璃卡片（Glass Cards）、液态按钮（Liquid Buttons）、浮动导航岛
- 圆角：超椭圆曲线（Squircle），最小 24px 圆角，保持"液滴"视觉语言

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

## 快速开始

直接在浏览器中打开任意页面的 `code.html` 即可预览：

```bash
# 例如打开首页
open home/code.html
```

## 负责人

耀月

## License

All rights reserved.
