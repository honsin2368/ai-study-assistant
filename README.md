# ASTUDYA

基于 Python、FastAPI 和 Google Gemini API 构建的 AI 学习助手，提供快速问答、交互式教学和学习资料辅助分析。项目包含可自定义的 Web 工作台，并已部署在线演示版本。

[在线体验](https://astudya-honsin.onrender.com/) · [项目仓库](https://github.com/honsin2368/ai-study-assistant)

> 在线演示使用 Render 免费实例，长时间无人访问后可能休眠，首次打开需要等待。为控制模型调用额度，演示站点设置了全站共享的请求频率限制。

## 核心功能

| 模块 | 功能说明 |
| --- | --- |
| 快速解答 | 输入学习问题，调用 Gemini 返回解释、示例或代码 |
| 交互式教学 | 按步骤讲解和追问，参考最近最多 12 条对话消息继续教学 |
| 文件辅助学习 | 支持图片、PDF、TXT、Markdown、CSV、JSON、Python、DOCX、PPTX、XLSX 等学习资料 |
| 快捷提问 | 添加、编辑、删除常用问题，最多保留 8 条 |
| 个性化界面 | 日间、雾灰、夜间主题；配色、字体、阅读设置和玻璃卡片效果 |
| 背景构图 | 自定义背景图片，支持缩放、上下左右定位、90° 旋转和恢复居中 |
| 本地保存 | 快捷提问与界面偏好使用浏览器本地存储；背景图片使用 IndexedDB |

图片与 PDF 作为文件内容交给 Gemini；Office 文档由后端提取可读取的文字与表格数据。背景上传支持 JPG、PNG、WebP，HEIF／HEIC 可尝试在浏览器中转换为 JPG，不经过 ASTUDYA 后端上传。

## 技术架构

| 层次 | 技术 |
| --- | --- |
| 前端 | HTML、CSS、原生 JavaScript |
| 后端 | Python、FastAPI、Pydantic |
| AI 模型 | Google Gen AI SDK、Gemini API |
| 文件处理 | pypdf、python-docx、python-pptx、openpyxl |
| 本地存储 | localStorage、IndexedDB |
| 服务与部署 | Uvicorn、GitHub、Render |

### 请求流程

1. 前端根据是否包含附件向后端发送请求：纯文字使用 `POST /api/ask`（JSON），带文件使用 `POST /api/ask-with-files`（FormData）。
2. FastAPI 校验请求与附件，执行基础调用频率限制。
3. 后端根据所选学习模式准备提示词；交互式教学会加入客户端提交的近期对话。
4. 后端调用 Gemini API，前端接收回答并展示 Markdown 格式内容。

API Key 通过后端环境变量管理，不暴露到浏览器。目前没有用户登录、服务端会话数据库或跨设备同步。

## 本地运行

需要 Python 3 环境与可用的 Gemini API Key。以下以 Windows PowerShell 为例。

**1. 获取项目**

~~~powershell
git clone https://github.com/honsin2368/ai-study-assistant.git
cd ai-study-assistant
~~~

**2. 安装依赖**

~~~powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-deploy.txt
~~~

**3. 配置环境变量**

在项目根目录创建 `.env`，填写自己的密钥与实际可用的模型 ID：

~~~dotenv
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=your_model_id
~~~

`.env` 已加入 `.gitignore`，不要把真实密钥提交到仓库。

**4. 启动服务**

~~~powershell
.\.venv\Scripts\python.exe -m uvicorn web.app:app --reload
~~~

浏览器访问 `http://127.0.0.1:8000`。

## 项目结构

~~~text
ai-study-assistant/
├── web/
│   ├── app.py                 # FastAPI 路由、Gemini 调用与限流
│   ├── attachments.py         # 附件校验及内容提取
│   └── index.html             # Web 界面与交互逻辑
├── tests/
│   └── test_uploads.py        # 文件处理与接口测试
├── main.py                    # 独立的命令行学习任务管理器
├── requirements-deploy.txt    # Web 运行依赖
├── requirements.txt           # 开发环境依赖
└── README.md
~~~

项目从命令行学习任务管理器逐步扩展为 Web 应用。`main.py` 目前与 Web 学习助手独立，尚未整合到网页。

## 测试与部署

仓库包含 10 项自动化测试，覆盖 TXT、DOCX、PPTX、XLSX 解析、PDF 页数限制、异常文件处理、文件提问接口与教学历史。测试曾在本地通过；接口测试采用模拟 Gemini 响应，不等于已覆盖所有真实模型调用场景。

~~~powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
~~~

线上使用 Render Web Service，连接 GitHub 的 `main` 分支：

| 配置项 | 值 |
| --- | --- |
| Build Command | `pip install -r requirements-deploy.txt` |
| Start Command | `uvicorn web.app:app --host 0.0.0.0 --port $PORT` |
| 环境变量 | `GEMINI_API_KEY`、`GEMINI_MODEL` |

## 已知限制

- 每次最多上传 2 个文件，单文件不超过 6 MB、总计不超过 10 MB，PDF 最多 30 页。Office 文件无法保证保留图片、动画或完整排版。
- 附件只用于当次请求，服务端不长期保存。上传的学习资料会提交给 Gemini，请勿包含密码等敏感信息。
- 全站基础限流为每分钟 4 次、每小时 20 次，计数在服务进程内存中，尚不能替代正式的用户级配额管理。
- 快捷提问、界面偏好与背景图片仅保存在当前浏览器中，清除网站数据或更换设备后无法自动同步。
- 部分从微博等平台下载的图片仍可能无法解码，已在 [Issue #4](https://github.com/honsin2368/ai-study-assistant/issues/4) 记录。HEIF 转 JPG 功能已通过手机人工测试，但不保证兼容所有 HEIF 编码。
- 尚未实现用户登录、服务端历史会话持久化、知识库检索（RAG）或完整端到端自动化测试。

## 关于项目

这是一个持续迭代的个人学习项目。开发过程中使用 AI 辅助需求分析、代码实现和调试，并通过本地测试、Git 版本管理及线上验证逐步完善。本文仅描述已实现的功能和已知限制。
