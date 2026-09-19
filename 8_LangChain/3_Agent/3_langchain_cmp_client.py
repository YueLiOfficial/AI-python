from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
import asyncio
from dotenv import load_dotenv

load_dotenv()

client = MultiServerMCPClient(
    connections= {
        "calculator": {
            "transport": "streamable_http",
            "url": "http://localhost:8000/mcp"
        }
    }
)

def print_message(message):
    if isinstance(message, AIMessage):
        if message.content:
            print(f"AI回复: {message.content}")
        if message.tool_calls:
            print(f"AI调用tool: {message.tool_calls}")
    elif isinstance(message, HumanMessage):
        print(f"User输入: {message.content}")
    elif isinstance(message, ToolMessage):
        print(f"Tools调用结果: {message.content}")
    else:
         print("未知消息类型")

async def main():
    tools = await client.get_tools()

    print("= " * 30)
    print(f"tools = {tools}")

    llm = init_chat_model(
        model="deepseek-flash",
        model_provider="deepseek"
    )

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="你是一个计算助手，请调用工具帮我计算结果"
    )

    res = await agent.ainvoke(
        {
            "messages": [{"role": "user", "content": "计算2+5"}]
        }
    )

    print("= " * 30)
    print(f"原始输出: {res}")

    print("= " * 30)
    print(f"模型最终回复: {res['messages'][-1].content}")

    print("+ " * 30)
    for message in res["messages"]:
        print_message(message)
        print()

if __name__ == "__main__":
    asyncio.run(main())