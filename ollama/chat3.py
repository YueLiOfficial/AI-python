import requests
import json

messages = [
    {"role": "system", "content": "你是一个友好的AI助手，请用简洁的语言回答我"}
]

def chat(inputmsg):
    # 将用户输入加入历史
    messages.append({"role": "user", "content":inputmsg})

    resp = requests.post(
        url="http://localhost:11434/api/chat",
        json={
            "model": "qwen3.5:4b",
            "messages": messages,
            "stream": True,
            "think": False
        },
        stream=True,
    )

    reply = ""
    for lines in resp.iter_lines():
        if not lines:
            continue

        msg = json.loads(lines)

        content = msg["message"]["content"]
        print(content, end='', flush=True)

        reply += content

        if msg.get("done"):
            messages.append({"role": "assistant", "content": reply})
            return reply

while True:
    user_input = input("你:")

    if user_input.lower() in ("exit", "quit"):
        break

    print("AI:", end='')
    chat(user_input)

