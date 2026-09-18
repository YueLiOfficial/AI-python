from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain.chat_models import init_chat_model

load_dotenv()

class Prime(BaseModel):
    prime: list[int] = Field(description="素数")
    count: list[int] = Field(description="小于素数的素数个数")

def output_for_json_parser():
    json_parser = JsonOutputParser(pydantic_object=Prime)

    sys_message = json_parser.get_format_instructions()

    messages = [
        ("system", sys_message),
        ("user", "请任意输出5个100-1000之间的素数，并输出小于该素数的素数个数")
    ]

    model = init_chat_model(
        model="gpt-5.6-sol",
        model_provider="openai"
    )

    res = model.invoke(messages)

    print(res)

    res = json_parser.parse(res.content)
    print("==================================================")
    print(res)
    print(type(res))

def output_with_structured_output():
    class CalendarEvent(BaseModel):
        name: str
        date: str
        participants: list[str]

    model = init_chat_model(
        model="gpt-5.6-sol",
        model_provider="openai"
    )

    new_model = model.with_structured_output(schema=CalendarEvent)

    res = new_model.invoke("Alice and Bob are going to a science fair on Friday.")

    print(res)
    print(type(res))

if __name__ == "__main__":
    # output_for_json_parser()
    output_with_structured_output()
