from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from deepagents.backends import FilesystemBackend
from langchain.messages import AIMessage, ToolMessage, HumanMessage
from pathlib import Path
import asyncio

from map_subagent import get_map_subagent
from ticket_subagent import get_ticket_subagent
from summary_subagent import get_summary_subagent

from dotenv import load_dotenv

MAIN_AGENT_PROMPT = """
    你是一名旅游规划总控智能体。
    你的职责是根据用户输入，先抽取关键信息，再调度合适的子智能体完成任务。
    注意: 必须将规划好的内容写到 results文件夹/旅游规划-日期.md文件
    规则：
    1. 先从用户输入中抽取：出发地、目的地、日期/天数、预算、偏好、出行节奏
    2. 如果用户没有明确说明游玩天数，默认按 1 天规划
    3. 如果用户没有明确说明预算，默认按中等预算规划
    4. 如果用户没有明确说明偏好，默认按“经典景点 + 少折腾”规划
    5. 如果用户没有明确说明出行节奏，默认按“舒适型节奏”规划
    6. 景点、路线、地图相关问题交给 map_agent
    7. 火车票、车次、票价、时间建议交给 ticket_agent
    8. 最终结果交给 summary_agent 汇总
    9. 输出必须使用中文
    10. 不做真实购票，只做规划和建议
    11. 不要自己假设不存在的车次、票价或路线。
"""

async def main():
    user_input = input("请输入旅游需求: ").strip()

    map_subagent = get_map_subagent()
    ticket_subagent = await get_ticket_subagent()
    summary_sunagent = get_summary_subagent()

    model = init_chat_model(
        model="deepseek-flash",
        model_provider="deepseek",
        extra_body={
            "thinking": {
                "type": "disabled"
            }
        }
    )

    main_agent = create_deep_agent(
        model=model,
        system_prompt=MAIN_AGENT_PROMPT,
        subagents=[map_subagent, ticket_subagent, summary_sunagent],
        backend=file_backend,
        memory=["/memory/AGENTS.md"],
    )

    print("=================开始规划=================")

    chunks = main_agent.astream({"messages": [("user", user_input)]})

    async for chunk in chunks:
        for _, messages in chunk.items():
            if not messages or "messages" not in messages:
                continue

            message = messages["messages"][-1]
            if isinstance(message, AIMessage):
                if message.tool_calls:
                    for tool_call in message.tool_calls:
                        name = tool_call["name"]
                        args = tool_call["args"]

                        if name == "task":
                            print(f"[调用子智能体]: {args["subagent_type"]}")
                        else:
                            print(f"[调用工具]: {name}, 参数: {args}")
                else:
                    print("=================模型回复=================")
                    print(message.content)
            elif isinstance(message, ToolMessage):
                if message.name == "task":
                    print(f"[子智能体]: {message.content}")
                else:
                    print(f"[工具]: {message.content}")

if __name__ == "__main__":
    load_dotenv(override=True)

    root_dir = Path(__file__).parent.resolve()
    file_backend = FilesystemBackend(root_dir=root_dir)

    asyncio.run(main())
