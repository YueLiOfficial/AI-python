from dotenv import load_dotenv

load_dotenv()

def demo1():
    from langchain.chat_models import init_chat_model
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnableParallel
    import os

    # 定义三个模型
    llm_openai1 = init_chat_model(
        model="gpt-5.6-sol",
        model_provider="openai",
        base_url=os.getenv("CCCODE_OPENAI_BASE_URL"),
        api_key=os.getenv("CCCODE_OPENAI_API_KEY")
    )

    llm_openai2 = init_chat_model(
        model="gpt-5.4",
        model_provider="openai",
        base_url=os.getenv("CCCODE_OPENAI_BASE_URL"),
        api_key=os.getenv("CCCODE_OPENAI_API_KEY")
    )

    llm_deepseek = init_chat_model(
        model="deepseek-flash",
        model_provider="openai",
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # 定义提示词模板
    openai1_prompt_template = ChatPromptTemplate([("user", "对这首诗做一下赏析，分析它蕴含的含义: {poem}")])
    openai2_prompt_template = ChatPromptTemplate([("user", "对这首诗做一下赏析，分析它蕴含的含义: {poem}")])
    deepseek_prompt_template = ChatPromptTemplate([("user", "这是一首诗: {poem}, \
                                                    这是两种赏析：第一种: {openai1}, \
                                                    第二种: {openai2}, \
                                                    请分析这两种赏析哪种更好，并给出理由")])

    # 创建链条
    chain1 = openai1_prompt_template | llm_openai1 | StrOutputParser()
    chain2 = openai2_prompt_template | llm_openai2 | StrOutputParser()
    chain3 = deepseek_prompt_template | llm_deepseek | StrOutputParser()

    main_chain = RunnableParallel(
        poem = lambda x: x["poem"],
        openai1 = chain1,
        openai2 = chain2
    ) | chain3

    poem = '''
        菩提本无树，
        明镜亦非台，
        本来无一物，
        何处惹尘埃。
    '''

    res = main_chain.invoke({"poem": poem})

    print(res)

if __name__ == "__main__":
    demo1()