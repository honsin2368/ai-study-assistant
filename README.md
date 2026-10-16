
# AI Study Assistant

一个基于 Python 和 Gemini API 的个人 AI 学习助手项目。

目前已实现命令行任务管理和 Web AI 学习问答功能，正在持续完善。

当前功能

Web AI 学习助手（V0.1）

- 通过网页输入学习问题
- 使用 FastAPI 接收用户请求
- 调用 Gemini API 生成学习回答
- 支持通俗解释、举例和练习题
- 根据提示词区分普通问候和学习问题
- API Key 通过本地环境变量配置

命令行任务管理器

- 添加、查看、完成和删除学习任务
- 查看任务统计与完成率
- 按关键词连续搜索学习任务
- 使用 JSON 保存任务数据

技术栈

- Python
- FastAPI、Uvicorn
- HTML、CSS、JavaScript
- Gemini API（Google Gen AI SDK）
- JSON
- Git / GitHub

本地运行 Web 版本

需要 Python 3 和可使用的 Gemini API Key。

1. 克隆本仓库并进入项目目录。
2. 创建 Python 虚拟环境。
3. 安装 requirements.txt 中的依赖。
4. 在项目根目录新建 `.env` 文件：

GEMINI_API_KEY=填写你自己的API密钥
GEMINI_MODEL=填写可用的Gemini模型ID

5. 启动服务。

Windows PowerShell 示例：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn web.app:app --reload
```

在浏览器打开：

http://127.0.0.1:8000

注意：`.env` 包含敏感配置，已加入 `.gitignore`，不得上传到公开仓库。

运行命令行版本

在项目目录运行：

```powershell
python main.py
```

学习任务数据保存在本地 `tasks.json` 中。

项目结构

- `main.py`：命令行任务管理程序
- `web/app.py`：FastAPI 后端与 Gemini 模型调用
- `web/index.html`：Web 页面及请求逻辑
- `requirements.txt`：Python 依赖清单
- `.gitignore`：Git 忽略规则

已完成的测试

- CLI 添加、完成、删除、搜索和数据保存
- Web 页面与 Python 后端通信
- Gemini API 生成真实学习回答
- 普通问候与学习问题的回答测试
- 模型请求异常时的基本错误提示

已知不足

- 尚未实现多轮对话历史管理
- 网页尚未支持 Markdown 格式渲染
- 暂无自动化测试
- Web 与 CLI 任务管理功能尚未整合
- 项目目前主要用于本地开发与学习，尚未部署

后续规划

- V0.2：优化 Markdown 渲染、加载状态和页面体验
- V0.3：增加快速解答与交互式教学双模式
- V0.4：整合学习任务管理功能
- 后续：学习知识库、RAG 和项目部署

开发说明

本项目是个人学习与实践项目，开发过程中使用 AI 工具辅助学习、代码编写与调试。

持续记录实际完成的功能、遇到的问题和解决过程。
