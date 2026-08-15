import requests

resp = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model":"qwen3.5:4b",
        "messages":[
            {"role": "system", "content": "你是一个幽默的助手"},
            {"role": "user", "content": "用三句话介绍你自己"}
        ],
        "stream": False,
        "think": False
    },
)

print(resp.json()["message"]["content"])
