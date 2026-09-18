from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain.messages import SystemMessage, HumanMessage
import os

load_dotenv()

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的分析师"),
    ("user", "请分析{text}, 并给出{score}和{reason}")
])

prompt = prompt_template.invoke({"text": "哈利波特电影", "score": "评分", "reason": "理由"})
prompt = prompt_template.format_prompt(
    text = "哈利波特电影", score = "评分", reason = "理由"
)


model = init_chat_model(
    # model="gpt-5.6-sol",
    model="deepseek-flash",
    model_provider="openai",
)

# res = model.invoke(prompt)

messages = [
    SystemMessage(content="你是一个专业的分析师"),
    HumanMessage(content="1+1等于多少")
]

res = model.invoke(prompt)

print(res)