from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.messages import HumanMessage, AIMessage, ToolMessage
from rich import print as rprint
from dotenv import load_dotenv

load_dotenv()

model = init_chat_model(
    model="deepseek-flash",
    model_provider="deepseek",
    extra_body={
        "thinking": {
            "type": "disabled"
        }
    }
)

@tool(parse_docstring=True)
def get_weather(city: str) -> str:
    """
        查询指定城市的天气

        Args:
            city: 城市名字
    """

    return f"{city}的天气晴朗"

@tool(parse_docstring=True)
def get_news(domain: str) -> str:
    """
        查询指定领域的新闻

        Args:
            domain: 指定的领域名字
    """

    return f"{domain}无事发生"

deep_agent = create_deep_agent(
    model=model,
    system_prompt="你是一个AI助手，请调用工具解答用户问题。",
    tools=[get_weather, get_news]
)

chunks = deep_agent.stream(
    input={
        "messages":[HumanMessage(content="请帮我查询杭州市天气和AI领域的新闻")]
    }
)

for chunk in chunks:

    for _, res_messages in chunk.items():
        # 过滤掉中间件的输出
        if not res_messages or "messages" not in res_messages:
            continue

        # 大模型的输出
        message = res_messages["messages"][-1]
        if isinstance(message, AIMessage):
            # 调用工具或子agent
            if message.tool_calls:
                tool_calls = message.tool_calls
                for tool_call in tool_calls:
                    name = tool_call["name"]
                    args = tool_call["args"]

                    # 调用子智能体
                    if name == "task":
                        print(f"[模型决策]: 调用子智能体: {args["subagent_type"]}")
                    else:
                        print(f"[模型决策]: 调用工具: {name}, 参数: {args}")
            else:
                print(f"[最终回复]: {message.content}")

        # tool的输出
        elif isinstance(message, ToolMessage):
            # 子智能体的输出
            if message.name == "task":
                print(f"[子agent]: {message.content}")
            else:
                print(f"[工具]: {message.content}")
