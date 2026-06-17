<!-- markdownlint-disable MD033 MD041 -->

<div align="center">

<img alt="Commander-AI" src="https://img.shields.io/badge/Commander-AI-6366f1?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCI+PHBhdGggZD0iTTEyIDJMMiA3bDEwIDUgMTAtNS0xMC01eiIvPjxwYXRoIGQ9Ik0yIDE3bDEwIDUgMTAtNSIvPjxwYXRoIGQ9Ik0yIDEybDEwIDUgMTAtNSIvPjwvc3ZnPg==" alt="logo" />

# Commander-AI

**AI 指挥官 — 基于 MaaFramework 的 NIKKE 后台自动化助手**

支持后台运行 · 全分辨率 · 跨平台 · 由某不知名 AI 自主迭代维护

<p align="center">
  <img alt="MaaFramework" src="https://img.shields.io/badge/MaaFramework-v2.0+-blue?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0id2hpdGUiPjxwYXRoIGQ9Ik0xMiAyTDIgN2wxMCA1IDEwLTVMMTIgMnpNMiAxMmwxMCA1IDEwLTVNMCAxN2wxMCA1IDEwLTVNMiA3djEwIi8+PC9zdmc+" />
  <img alt="platform" src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-blueviolet" />
  <img alt="license" src="https://img.shields.io/github/license/min09577/Commander-AI" />
  <br/>
  <img alt="commit" src="https://img.shields.io/github/commit-activity/m/min09577/Commander-AI" />
  <img alt="stars" src="https://img.shields.io/github/stars/min09577/Commander-AI?style=social" />
</p>

---

> **中文** | Commander-AI 是基于 [MaaFramework](https://github.com/MaaXYZ/MaaFramework) 的 NIKKE 自动化工具，任务流程借鉴 [DoroHelper](https://github.com/1204244136/DoroHelper)。由某不知名 AI 自主迭代维护，AGPL-3.0 协议。
>
> **English** | Commander-AI is a MaaFramework-based NIKKE automation tool, with task flows inspired by [DoroHelper](https://github.com/1204244136/DoroHelper). Maintained autonomously by an anonymous AI. AGPL-3.0.
>
> **日本語** | Commander-AI は [MaaFramework](https://github.com/MaaXYZ/MaaFramework) ベースの NIKKE 自動化ツールです。タスクフローは [DoroHelper](https://github.com/1204244136/DoroHelper) を参考にしています。某匿名 AI が自律的に反復保守。AGPL-3.0。
>
> **한국어** | Commander-AI는 [MaaFramework](https://github.com/MaaXYZ/MaaFramework) 기반 NIKKE 자동화 도구입니다. 작업 흐름은 [DoroHelper](https://github.com/1204244136/DoroHelper)를 참고했습니다. 익명의 AI가 자율적으로 유지 관리합니다. AGPL-3.0.

</div>

---

## 关于本仓库

Commander-AI 是 NIKKE 日常任务的全新自动化方案，基于 [MaaFramework](https://github.com/MaaXYZ/MaaFramework) 构建。

与 AHK 版 [DoroHelper-AI](https://github.com/min09577/DoroHelper-AI) 不同，Commander-AI 支持：

- **后台运行** — 游戏窗口可以最小化，不妨碍日常使用
- **全分辨率** — 不再局限于 720p/1080p
- **跨平台** — Windows / Linux / macOS
- **可视化管线** — 任务流程可拖拽编辑

---

## 项目起源

本项目的任务流程设计，借鉴了 [DoroHelper](https://github.com/1204244136/DoroHelper) 的实践经验。

DoroHelper 创始于 2024 年 7 月，由以下贡献者接力完成：
- **@kyokakawaii** — 创始开发者（2024.07 ~ 2025.01）
- **@1204244136** — 接手维护（2025.04 ~ 2026.05）

向他们致敬。Commander-AI 是对 DoroHelper 任务逻辑的独立重实现，代码和架构完全独立。

---

## 功能概览

一键清理 NIKKE 日常事务，包括：

| 模块 | 功能 |
|------|------|
| 商店 | 付费商店、普通商店、竞技场商店、废铁商店 |
| 模拟室 | 普通模拟室、模拟室超频 |
| 竞技场 | 收菜、新人竞技场、特殊竞技场、冠军竞技场 |
| 无限之塔 | 企业塔、通用塔 |
| 拦截战 | 普通拦截、异常拦截 |
| 常规奖励 | 派遣、好感度、好友点数、邮件、任务、通行证 |
| 妙妙工具 | 剧情模式、极速爆裂、推图模式 |

---

## 快速开始

### 1. 下载

从 [Releases](https://github.com/min09577/Commander-AI/releases) 下载最新版本。

### 2. 安装 MaaFramework Runtime

Commander-AI 需要 MaaFramework v2.0+ 运行时。

### 3. 运行

启动 Commander-AI，选择 NIKKE 窗口，点击开始即可。

---

## 开发

### 项目结构

```
Commander-AI/
├── assets/
│   └── resource/
│       ├── image/          # 图像识别模板
│       ├── model/ocr/      # OCR 模型文件
│       └── pipeline/       # 任务管线 JSON
├── interface.json          # MaaFramework 项目接口
└── LICENSE                 # AGPL-3.0
```

### 技术栈

- **框架**: [MaaFramework](https://github.com/MaaXYZ/MaaFramework) (LGPL-3.0)
- **任务管线**: JSON 低代码 + Python 自定义扩展
- **OCR**: PaddleOCR ONNX
- **图像识别**: 模板匹配 + 特征检测

---

## 致谢

- [MaaFramework](https://github.com/MaaXYZ/MaaFramework) — 底层自动化框架
- [DoroHelper](https://github.com/1204244136/DoroHelper) — 任务流程参考
- [M9A](https://github.com/Maa1999/M9A) — 代码参考

---

## 许可证

本项目采用 [AGPL-3.0](LICENSE) 许可证。

Commander-AI 是一款独立的开源软件，与 Shift Up / Level Infinite / NIKKE 无任何关联。
