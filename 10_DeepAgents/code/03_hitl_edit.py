# -*- coding: utf-8 -*-
"""
DeepAgents 中断审批机制示例
核心功能：演示高危工具调用前的人工审批流程，支持删除数据库表/文件的审批控制
"""
import os
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from deepagents import create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver  # 内存检查点，用于保存中断状态
from langgraph.types import Command  # 恢复执行的指令类型
from dotenv import load_dotenv, find_dotenv
from rich import print as rprint

# 加载环境变量（DASHSCOPE_API_KEY等），优先查找当前目录的.env文件
load_dotenv(find_dotenv())


# ======================== 1. 定义工具函数 ========================
# 装饰器@tool将普通函数转为LangChain可调用工具，函数文档字符串会作为工具描述给Agent
@tool
def delete_database(table_name: str):
    """
    高危操作：删除数据库表
    :param table_name: 要删除的表名
    :return: 操作结果提示
    """
    print(f"[工具执行] 删除表: {table_name}")
    return f"已成功删除表: {table_name}"


@tool
def select_data(table_name: str):
    """
    普通操作：查询指定表名的数据（无需审批）
    :param table_name: 要查询的表名
    :return: 操作结果提示
    """
    print(f"[工具执行] 查询指定表名数据: {table_name}")
    return f"查询数据成功：{table_name}"


@tool
def delete_file(file_name: str):
    """
    高危操作：删除文件
    :param file_name: 要删除的文件路径/名称
    :return: 操作结果提示
    """
    print(f"[工具执行] 删除文件: {file_name}")
    return f"已成功删除文件: {file_name}"

# 定义模型
model = init_chat_model(
    model="deepseek-flash",
    model_provider="deepseek",
    extra_body={
        "thinking": {
            "type": "disabled"
        }
    }
)

# 定义检查点
checkpointer = InMemorySaver()

# 定义deep_agent
main_agent = create_deep_agent(
    model=model,
    system_prompt="你是一个综合助手，请调用工具帮我实现一些操作。回答需要使用中文",
    tools=[delete_database, select_data, delete_file],
    interrupt_on={
        "delete_database": {"allowed_decisions": ["approve", "reject"]},
        "delete_file": True
    },
    checkpointer=checkpointer
)

config = {
    "configurable": {
        "thread_id": "abc"
    }
}

result1 = main_agent.invoke({"messages": [("user", "请帮我删除数据库中的user表，并查询project表，最后再帮我删除info.txt文件")]}, config=config)

decisions = []

if result1.get("__interrupt__"):
    action_requests = result1["__interrupt__"][0].value["action_requests"]

    for action in action_requests:
        name = action["name"]
        args = action["args"]

        if name == "delete_database":
            if args["table_name"] == "user":
                decisions.append({
                    "type": "reject"
                })
            else:
                decisions.append({
                    "type": "approve"
                })
        elif name == "delete_file":
            if args["file_name"] == "info.txt":
                decisions.append({
                    "type": "edit",
                    "edited_action": {
                        "name": name,
                        "args": {
                            "file_name": "text.txt"
                        }
                    }
                })
            else:
                decisions.append({
                    "type": "approve"
                })
        else:
            decisions.append({
                "type": "approve"
            })

    result2 = main_agent.invoke(
        Command(resume={
            "decisions": decisions
        }),
        config=config,
    )

    print(result2["messages"][-1].content)