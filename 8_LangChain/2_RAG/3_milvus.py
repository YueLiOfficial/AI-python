from dill.pointers import parent
from langchain_classic.tools.office365 import messages_search
from pymilvus import MilvusClient, AnnSearchRequest, RRFRanker
from pymilvus.client.types import DataType
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from FlagEmbedding import BGEM3FlagModel
from pathlib import Path
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# 创建Client
def get_client():
    return MilvusClient(uri="http://localhost:19530")

# 查看所有collection
def show_all_collections(client: MilvusClient):
    print(client.list_collections())

# 新建collection
def create_collection(client: MilvusClient, collection_name: str):
    if not client.has_collection(collection_name):
        # 1. 定义collection结构
        schema = client.create_schema(
            auto_id=True
        )
        schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
        schema.add_field(field_name="metadata", datatype=DataType.JSON)
        schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=2000)
        schema.add_field(field_name="dense_vector", datatype=DataType.FLOAT_VECTOR, dim=1024)
        schema.add_field(field_name="sparse_vector", datatype=DataType.SPARSE_FLOAT_VECTOR)

        # 2. 定义索引
        index_params = client.prepare_index_params()
        index_params.add_index(field_name="dense_vector", index_type="HNSW", metric_type="L2")
        index_params.add_index(field_name="sparse_vector", index_type="SPARSE_INVERTED_INDEX", metric_type="IP")

        client.create_collection(
            collection_name=collection_name,
            schema=schema,
            index_params=index_params
        )

def insert_data(client: MilvusClient, model:BGEM3FlagModel, collection_name: str):
    # 加载文档
    documents = UnstructuredWordDocumentLoader(
        file_path=Path(__file__).parent / "assets" / "sample.docx",
        mode="single"
    ).load()

    # 对文档切片
    chunks = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "。", "！", "？", "，"],
        chunk_size=400,
        chunk_overlap=50
    ).split_documents(documents)

    # 3. 对数据进行向量化
    res = model.encode(
        sentences=[chunk.page_content for chunk in chunks],
        return_dense=True,
        return_sparse=True
    )

    dense_vectors = res["dense_vecs"]
    sparse_vectors = res["lexical_weights"]

    # 构建data
    data = []

    for chunk, dense, sparse in zip(chunks, dense_vectors, sparse_vectors):
        data.append({
            "text": chunk.page_content,
            "metadata": chunk.metadata,
            "dense_vector": dense,
            "sparse_vector": sparse
        })

    res = client.insert(
        collection_name=collection_name,
        data=data
    )

    print(res)

# 将query转换为向量
def encode_query(model: BGEM3FlagModel, query: str):
    res = model.encode(
        sentences=[query],
        return_dense=True,
        return_sparse=True
    )

    return {
        "dense_vector": res["dense_vecs"][0],
        "sparse_vector": res["lexical_weights"][0]
    }

# 稠密向量检索
def dense_search(client: MilvusClient, collection_name: str, model: BGEM3FlagModel, query: str):
    # 将query转换为向量
    dense = encode_query(model, query)["dense_vector"]

    res = client.search(
        collection_name=collection_name,
        data=[dense],
        anns_field="dense_vector",
        limit=5,
        search_params={"metric_type": "L2"},
        output_fields=["id", "metadata", "text"]
    )

    return res

# 稀疏向量检索
def sparse_search(client: MilvusClient, collection_name: str, model: BGEM3FlagModel, query: str):
    sparse = encode_query(model, query)["sparse_vector"]

    res = client.search(
        collection_name=collection_name,
        data=[sparse],
        anns_field="sparse_vector",
        limit=5,
        search_params={"metric_type": "IP"},
        output_fields=["id", "metadata", "text"],
    )

    return res

# 混合向量检索
def hybrid_vector_search(client: MilvusClient, collection_name: str, model: BGEM3FlagModel, query: str):
    query_vectors = encode_query(model, query)

    dense_vector = query_vectors["dense_vector"]
    sparse_vector = query_vectors["sparse_vector"]

    # 稠密检索结果
    dense_req = AnnSearchRequest(
        data=[dense_vector],
        anns_field="dense_vector",
        param={"metric_type": "L2"},
        limit=5
    )

    # 稀疏检索结果
    sparse_req = AnnSearchRequest(
        data=[sparse_vector],
        anns_field="sparse_vector",
        param={"metric_type": "IP"},
        limit=5
    )

    # 混合检索
    res = client.hybrid_search(
        collection_name=collection_name,
        reqs=[dense_req, sparse_req],
        ranker=RRFRanker(),
        limit=5,
        output_fields=["id", "metadata", "text"]
    )

    return res

def rag_demo(client: MilvusClient, model: BGEM3FlagModel, query: str):
    # 定义LLM
    llm = init_chat_model(
        model="deepseek-flash",
        model_provider="openai"
    )

    # 定义提示词模板
    prompt_template = ChatPromptTemplate(
        messages=[
            ("system", "你是一名资深法律专家，只能根据提供的上下文回答问题，不得使用上下文之外的信息。如果上下文无法回答问题，请回复：上下文无法解答该问题。不要补充、推测或扩展上下文中的内容。"),
            ("user", "请根据上下文: {context}, 帮我解决以下问题：{query}")
        ]
    )

    #混合检索
    res = hybrid_vector_search(client, "demo_collection", model, query)

    context = '\n'.join([row["entity"]["text"] for row in res[0]])

    chain = prompt_template | llm

    res = chain.invoke({"context": context, "query": query})

    print("========== RETRIEVED ==========")
    print(f"context: {context}\n query: {query}")
    print("========== ANSWER ==========")
    print(res.content)

if __name__ == '__main__':
    client = get_client()
    embed_model = BGEM3FlagModel(Path(__file__).parent.parent / "bge-m3")
    # show_all_collections(client)
    # create_collection(client, "demo_collection")
    # insert_data(client=client, model=embed_model, collection_name="demo_collection")
    # res = dense_search(client, "demo_collection", embed_model, "我酒驾了")
    # res = sparse_search(client, "demo_collection", embed_model, "我酒驾了")
    # res = hybrid_vector_search(client, "demo_collection", embed_model, "我酒驾了")
    # print(res)

    rag_demo(client, embed_model, "中国的首都是哪里")
