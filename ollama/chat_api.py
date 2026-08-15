from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import ollama
from pydantic import BaseModel

client = ollama.Client(host="http://localhost:11434")

app = FastAPI(title="聊天机器人 API")

# 定义客户端POST过来的数据结构
class ChatRequest(BaseModel):
    messages: list


@app.post('/chat')
def chat(req: ChatRequest):
    def generate():
        reply = client.chat(
            model="qwen3.5:4b",
            messages=req.messages,
            stream=True,
            think=False
        )

        for msg in reply:
            yield msg.message.content

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )
