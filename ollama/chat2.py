import ollama

client = ollama.Client(host="http://localhost:11434")

resp = client.chat(
    model="qwen3.5:4b",
    messages=[
        {"role": "user", "content": "请用简短的三句话介绍你自己"}
    ],
    stream=True,
    think=False
)

for lines in resp:
    content = lines.message.content
    print(content, end='', flush=True)
