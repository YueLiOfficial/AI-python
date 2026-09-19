from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()

def demo():
    llm = init_chat_model(
        model="deepseek-flash",
        model_provider="deepseek"
    )

    checkpointer = InMemorySaver()

    agent = create_agent(
        model=llm,
        checkpointer=checkpointer
    )

    config1 = {
        "configurable": {
            "thread_id": "user_001"
        }
    }

    config2 = {
        "configurable": {
            "thread_id": "user_002"
        }
    }

    print("===============第一次调用===============")
    res = agent.invoke(
        {
            "messages": [("user", "我叫月漓")]
        },
        config=config1
    )

    print(res["messages"][-1].content)

    print("===============第二次调用===============")
    res = agent.invoke(
        {
            "messages": [("user", "我叫什么")]
        },
        config=config1
    )

    print(res["messages"][-1].content)

if __name__ == "__main__":
    demo()