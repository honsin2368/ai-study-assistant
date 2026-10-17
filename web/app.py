
import os
import time
from collections import deque
from pathlib import Path
from threading import Lock
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from google import genai
from google.genai import types, errors
from pydantic import BaseModel, Field


ROOT_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = Path(__file__).resolve().parent

load_dotenv(ROOT_DIR / ".env")

app = FastAPI()


# 请求数据结构
class ChatMessage(BaseModel):
    role: Literal["user", "model"]
    text: str = Field(max_length=4000)


class Question(BaseModel):
    question: str = Field(max_length=4000)
    mode: Literal["quick", "tutor"] = "quick"
    history: list[ChatMessage] = Field(
        default_factory=list,
        max_length=12
    )


# 公开演示版：简单的全站调用限制
minute_requests = deque()
hour_requests = deque()
request_lock = Lock()

MINUTE_LIMIT = 4
HOUR_LIMIT = 20


def allow_ai_request():
    now = time.monotonic()

    with request_lock:
        while minute_requests and now - minute_requests[0] >= 60:
            minute_requests.popleft()

        while hour_requests and now - hour_requests[0] >= 3600:
            hour_requests.popleft()

        if len(minute_requests) >= MINUTE_LIMIT:
            return False

        if len(hour_requests) >= HOUR_LIMIT:
            return False

        minute_requests.append(now)
        hour_requests.append(now)

        return True


@app.get("/")
def home():
    return FileResponse(WEB_DIR / "index.html")


QUICK_INSTRUCTION = (
    "你是一位清晰、准确的中文 AI 学习助手。"
    "请直接回答用户的问题，必要时提供例子或代码。"
    "回答要有条理，不要强制每次都出练习题。"
    "如果用户只是打招呼，请简短回应。"
)


TUTOR_INSTRUCTION = (
    "你是一位耐心的中文学习导师。"
    "请每次重点讲解一个知识点。"
    "使用通俗语言，必要时举一个简单例子。"
    "讲解后提出一道简短问题，并等待用户回答。"
    "根据之前的对话判断用户是否理解。"
    "回答正确时简短肯定，再继续下一步。"
    "回答错误时指出误区，换一种方式解释。"
    "不要一次提出很多道题。"
    "用户明确要求直接答案时，可以直接回答。"
    "不要假装用户已经掌握尚未确认的知识。"
)


@app.post("/api/ask")
def ask(data: Question):
    question = data.question.strip()

    if not question:
        return {
            "answer": "请先输入一个问题。",
            "ok": False
        }

    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL")

    if not api_key or not model:
        return {
            "answer": "Gemini 配置缺失，请检查环境变量。",
            "ok": False
        }

    # 检查调用次数，超过限制就不请求 Gemini
    if not allow_ai_request():
        return {
            "answer": (
                "当前演示站点的 AI 请求较多，"
                "请稍后再试。"
            ),
            "ok": False
        }

    if data.mode == "tutor":
        instruction = TUTOR_INSTRUCTION
        contents = []

        for message in data.history:
            text = message.text.strip()

            if not text:
                continue

            contents.append(
                types.Content(
                    role=message.role,
                    parts=[
                        types.Part.from_text(text=text)
                    ]
                )
            )

        contents.append(
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=question)
                ]
            )
        )

    else:
        instruction = QUICK_INSTRUCTION
        contents = question

    try:
        with genai.Client(api_key=api_key) as client:
            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=instruction
                ),
            )

        return {
            "answer": response.text or "模型没有返回文本回答。",
            "ok": True
        }

    except errors.APIError as error:
        return {
            "answer": (
                f"Gemini API 请求失败，错误码：{error.code}\n"
                "请稍后重试，或检查模型额度与配置。"
            ),
            "ok": False
        }

    except Exception:
        return {
            "answer": (
                "请求出现异常，请检查网络或服务器运行状态。"
            ),
            "ok": False
        }
