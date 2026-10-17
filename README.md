# ASTUDYA · AI Study Assistant（V0.3）

> 一款基于 **Python、FastAPI 与 Gemini API** 的个人 AI 学习助手。支持**快速解答、交互式教学、可编辑的快捷提问和图文／文档辅助学习**，并提供个性化玻璃拟态界面。

**[在线体验](https://astudya-honsin.onrender.com/)** · **[源代码](https://github.com/honsin2368/ai-study-assistant)**

> **在线体验提示：** 网站使用 Render 免费 Web Service，长时间无人访问后可能休眠，首次打开需等待服务唤醒。为控制模型调用额度，公开演示站点采用全站共享的基础限流。

## 项目概述

ASTUDYA 是一个以“提出问题—理解知识—继续练习”为核心的学习工具。用户可以直接获取知识解答，也可以选择循序渐进的教学方式，让 AI 根据前面的问答继续讲解；也可以上传课程截图、PDF 或 Office 文档，结合自己的文字问题分析学习资料。

项目从 Python 命令行任务管理器起步，逐步扩展为可公开访问的 Web 应用。**命令行任务管理器与 Web 学习助手目前是两个独立模块，尚未整合。**

## 核心功能

| 功能 | 实现情况 |
| --- | --- |
| **快速解答** | 用户输入问题，后端调用 Gemini 返回解释、示例或代码 |
| **交互式教学** | 使用独立的导师提示词，结合历史问答逐步讲解并提出问题 |
| **上下文连续对话** | 教学模式由前端提交最近最多 12 条消息，后端按角色构造 Gemini 会话内容 |
| **自定义快捷提问** | 用户可新增、编辑、删除常用提问，最多保存 8 条；保存在当前浏览器中 |
| **多格式文件提问** | 结合提问上传图片、PDF、TXT／MD／CSV／JSON／PY、Word（DOCX）、PPT（PPTX）、Excel（XLSX） |
| **附件内容处理** | 图片与 PDF 以附件内容交给 Gemini；Office 文件由后端提取可读取的文本／表格数据 |
| **富文本回答展示** | 前端自行渲染常见 Markdown 内容，包括标题、列表、代码块等 |
| **一屏式学习工作台** | 桌面端并列展示提问区和回答区；长回答可在内容区滚动 |
| **界面个性化** | 日间／雾灰／夜间色调、玻璃卡片和控件透明度、字体、配色及阅读行距 |
| **背景图设置** | 上传自定义图片、调整横纵向取景与模糊效果、选择原图／1080p／4K 尺寸适配 |
| **设置保留** | 在当前浏览器使用本地存储保存界面偏好及背景图片 |
| **公开演示保护** | 后端限制输入长度、附件数量和大小，设置基础全站限流，并通过环境变量读取 API Key |

> **画质说明：** 1080p 和 4K 是背景图片的目标输出尺寸选项，不是 AI 超分辨率修复；低分辨率原图放大后不一定更清晰。
>
> **文件说明：** 每次最多上传 **2 个文件**，单个不超过 **6 MB**、合计不超过 **10 MB**，PDF 最多 **30 页**。Office 文档会提取部分文字或表格，不保证保留图片、动画与完整排版；文本内容过长时会截取。上传的附件会送往 Gemini 处理，请勿上传包含密码或个人敏感信息的文件。服务端不长期保存附件。

## 界面展示

当前 Web 端支持日间与夜间主题以及个性化背景。

**截图待补充：** 为保证展示内容可信，计划放入两张从实际应用截取的截图，而不是使用模拟 Gemini 回答的设计稿：

- `docs/screenshots/day-mode.png` —— 日间模式与快速解答。
- `docs/screenshots/night-mode.png` —— 夜间模式与交互式教学。

截图文件加入仓库后，会在这里直接嵌入展示。

## 技术栈

| 层次 | 技术 |
| --- | --- |
| 后端 | Python、FastAPI、Pydantic |
| AI 模型接口 | Google Gen AI SDK（Gemini API） |
| 前端 | HTML、CSS、原生 JavaScript（FormData、多文件选择、浏览器本地存储） |
| 服务器 | Uvicorn |
| 配置管理 | `python-dotenv` / 环境变量 |
| 文档处理 | `python-docx`、`python-pptx`、`openpyxl`、`pypdf` |
| 数据与存储 | 浏览器本地存储（界面偏好、快捷提问）；JSON 文件（CLI 任务数据） |
| 版本管理与部署 | Git、GitHub、Render |

### 请求处理流程

```text
浏览器（web/index.html）
    │
    ├── 纯文字提问：POST /api/ask（JSON）
    └── 文字 + 文件：POST /api/ask-with-files（FormData）
                 │
                 ▼
          FastAPI（web/app.py）
                 │
      输入校验 → 基础限流 → 选择教学模式
                 │
          ┌──────┴──────┐
          │   文件解析   │
          │ 图片/PDF直传 │
          │ Office提文本 │
          └──────┬──────┘
                 ▼
             Gemini API
                 │
                 ▼
            返回 AI 回答
```

API Key 只在后端通过环境变量读取，不放入浏览器代码。教学历史由前端随请求提交，**当前没有用户账号、服务端历史数据库或跨设备会话同步**。快捷提问和外观设置只存储在当前浏览器；附件仅用于当次请求，不作为云端知识库保存。

## 本地运行

需要 Python 3（开发时使用 Python 3.14）和你自己的可用 Gemini API Key。

### 1. 下载代码

```powershell
git clone https://github.com/honsin2368/ai-study-assistant.git
cd ai-study-assistant
```

### 2. 创建虚拟环境并安装依赖

以下是 Windows PowerShell 示例：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-deploy.txt
```

`requirements-deploy.txt` 是 Web 部署所需的精简依赖清单；`requirements.txt` 保留了开发环境使用的完整依赖清单。

### 3. 配置环境变量

在仓库根目录创建 `.env` 文件，填写自己的凭证和实际可用的模型 ID：

```dotenv
GEMINI_API_KEY=在这里填写你的API密钥
GEMINI_MODEL=在这里填写你可用的Gemini模型ID
```

**切勿把真实 API Key 提交到 GitHub。** 仓库的 `.gitignore` 已忽略 `.env`。

### 4. 启动网站

```powershell
.\.venv\Scripts\python.exe -m uvicorn web.app:app --reload
```

打开浏览器访问：**http://127.0.0.1:8000**

### 5. 运行独立的命令行任务管理器

```powershell
.\.venv\Scripts\python.exe main.py
```

CLI 提供添加、查看、完成、删除、搜索学习任务和统计完成率等功能；任务保存在本地 `tasks.json`。

## 项目结构

```text
ai-study-assistant/
├── main.py                    # 独立的 CLI 学习任务管理器
├── web/
│   ├── app.py                 # FastAPI 路由、Gemini 调用、基础限流
│   ├── attachments.py         # 图片/PDF 校验与 Office 文本提取
│   └── index.html             # Web 界面、自定义提问与附件上传
├── tests/
│   └── test_uploads.py        # 附件解析与接口自动化测试
├── requirements-deploy.txt    # 线上精简依赖
├── requirements.txt           # 开发环境依赖
├── .gitignore
└── README.md
```

其中 `.env`（API Key）和 `tasks.json`（本地任务数据）在运行时由个人自行创建或生成，不应提交包含个人信息或密钥的文件。

## Render 部署说明

本项目使用 GitHub 代码仓库连接 Render 的 **Python Web Service**。

| 配置项 | 值 |
| --- | --- |
| Branch | `main` |
| Root Directory | 留空 |
| Build Command | `pip install -r requirements-deploy.txt` |
| Start Command | `uvicorn web.app:app --host 0.0.0.0 --port $PORT` |
| Environment Variables | `GEMINI_API_KEY`、`GEMINI_MODEL`（在 Render 后台配置） |

免费实例可能自动休眠，因此首次访问速度不代表常驻服务器的性能。

## 测试与当前限制

**已完成的人工验证：** V0.2 的本地与公网快速问答、交互式多轮教学、主题和个性化设置及保存；V0.3 的本地自定义快捷提问、TXT／图片／PDF／Office 文件结合文字提问。命令行版本曾验证任务管理与 JSON 保存功能。

**已完成的自动化测试：** `tests/test_uploads.py` 中的 **10 项用例通过**，覆盖 TXT／DOCX／PPTX／XLSX 解析、PDF 页数限制、错误文件拒绝、后端文件提问及导师历史请求。该测试使用模拟 Gemini 响应，不代表真实云端模型的每种文件格式都一定处理成功。

在项目目录执行：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

**当前限制：**

- 已有基础单元测试，但尚未实现完整端到端自动化测试、用户登录、云端会话持久化和知识库检索（RAG）。
- 公开网站仍需在新版部署完成后重新进行一次实际验收；合并代码不等于线上运行一定正常。
- 快捷提问与个性化设置只保存在当前浏览器，更换设备或清除站点数据后无法同步。
- 部分 Office 元素（如图形、动画、图片）未被提取；文件内容限制可能导致部分内容被截断。
- CLI 任务管理与 Web 页面尚未整合。
- 基础限流按**整个服务**统计（每分钟最多 4 次、每小时最多 20 次），不是按用户独立计数；计数存于进程内存，实例重启后重置，不能替代正式的安全或成本控制方案。
- 公开演示站点的可用性和响应速度受到 Render 免费服务、Gemini 服务与 API 配额影响。

## 后续计划

- 补充真实运行截图、更多边界场景和完整端到端自动化测试。
- 改进公网接口的安全防护和额度控制。
- 将 CLI 学习任务管理整合进 Web 端。
- 根据学习需要进一步探索知识整理和检索增强功能。

---

**开发说明：** 这是一个个人学习实践项目，开发过程中结合 AI 辅助进行需求分析、代码编写、调试和界面迭代。README 仅陈述已实现或已验证的能力；计划中的功能不作为已完成成果展示。
