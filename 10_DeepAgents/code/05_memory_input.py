from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from deepagents.backends import FilesystemBackend
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

root_dir = Path(__file__).parent.resolve()

file_backend = FilesystemBackend(root_dir=root_dir)

llm = init_chat_model(
    model="deepseek-flash",
    model_provider="deepseek",
    extra_body={
        "thinking": {
            "type": "disabled"
        }
    }
)

main_agent = create_deep_agent(
    model=llm,
    system_prompt=(
        "你是一名高情商中文助手。"
        "你的回答要自然、细腻、有陪伴感。"
        "当任务适合拆分时，可以交给子代理处理。"
        "如果用户要求写文案、祝福语、安慰话术，优先结合技能完成。"
    ),
    backend=file_backend,
    skills=["/skills"],
    memory=["/memory/AGENTS.md", "/memory/preferences.md"]
)

result = main_agent.invoke(
    {"messages": [("user", "请帮我写一个中秋节节日祝福")]}
)

print(result["messages"][-1].content)