from langchain_tavily import TavilySearch
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()

def agent_tools():
    llm = init_chat_model(
        model="deepseek-flash",
        model_provider="deepseek"
    )

    search = TavilySearch(max_results = 5)

    tools = [search]

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="你是一个智能助手，请调用工具帮助用户"
    )

    res = agent.invoke(
        {"messages": [
            {"role": "user", "content": "2026年9月19日杭州的天气怎么样"}
        ]}
    )

    print(res["messages"][-1].content)

if __name__ == '__main__':
    agent_tools()