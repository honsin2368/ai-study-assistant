
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from google import genai
from google.genai import types, errors
from pydantic import BaseModel

# 项目目录与环境配置
ROOT_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = Path(__file__).resolve().parent

load_dotenv(ROOT_DIR / ".env")

app = FastAPI()


class Question(BaseModel):
    question: str


@app.get("/")
def home():
    return FileResponse(WEB_DIR / "index.html")


@app.post("/api/ask")
def ask(data: Question):
    question = data.question.strip()

    if not question:
        return {"answer": "请先输入一个问题。"}

    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL")

    if not api_key or not model:
        return {"answer": "Gemini 配置缺失，请检查 .env 文件。"}

    try:
        with genai.Client(api_key=api_key) as client:
            response = client.models.generate_content(
                model=model,
                contents=question,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "你是一位耐心、专业的中文学习助手。"
                        "当用户向你打招呼时，你只需要简短回应即可"
                        "当用户提出学习、知识解释或编程相关问题时，你需要按照以下要求回答："
                        "请先通俗解释用户的问题，"
                        # "并询问用户是否愿意了解更多相关内容"
                        # "若收到否定回答，则结束回答"
                        # "若收到肯定回答"
                        "再给出一个具体例子，"
                        "最后出一道简单练习题。"
                        "回答清晰、准确，不要过于冗长。"
                    )
                ),
            )

        return {
            "answer": response.text or "模型没有返回文本回答。"
        }

    except errors.APIError as error:
        return {
            "answer": (
                f"Gemini API 请求失败，错误码：{error.code}\n"
                "请检查模型是否可用、免费额度及密钥权限。"
            )
        }

    except Exception:
        return {
            "answer": "请求出现异常，请检查网络或 Python 运行环境。"
        }
