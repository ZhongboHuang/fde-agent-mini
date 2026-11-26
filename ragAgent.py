import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.tools import tool

load_dotenv()

api_key = os.environ.get("ZHIPUAI_API_KEY")
if not api_key:
    raise ValueError("请在 .env 文件中设置 ZHIPUAI_API_KEY")

BASE_URL = "https://open.bigmodel.cn/api/paas/v4"

llm = ChatOpenAI(
    model="glm-5.3-flash",
    api_key=api_key,
    base_url=BASE_URL,
    temperature=0.6,
)

embeddings = OpenAIEmbeddings(
    model="embedding-3",
    api_key=api_key,
    base_url=BASE_URL,
    check_embedding_ctx_length=False,
)

# ========== 离线阶段：加载 -> 切分 -> 向量化 -> 入库 ==========
doc_path = os.path.join(os.path.dirname(__file__), "doc", "RAG_test.txt")
with open(doc_path, "r", encoding="utf-8") as f:
    raw_text = f.read()

# 最简切分：按中文句号、分号、换行切开，不做递归切分（无需额外装包）
pieces = re.split(r"[。；;\n]+", raw_text)
chunks = [p.strip() for p in pieces if p.strip()]

vectorstore = InMemoryVectorStore(embeddings)
vectorstore.add_texts(
    texts=chunks,
    metadatas=[{"source": "RAG_test.txt", "chunk": i} for i in range(len(chunks))],
)
print(f"[离线阶段完成] 共入库 {len(chunks)} 个片段")

# ========== 在线阶段：检索 -> 增强上下文 -> 生成回答 ==========
@tool
def search_docs(query: str) -> str:
    """从本地文档中检索与问题相关的片段，并标明出处。"""
    hits = vectorstore.similarity_search(query, k=2)
    if not hits:
        return "文档中未找到相关内容。"
    lines = []
    for h in hits:
        lines.append(f"[来源: {h.metadata['source']} 第 {h.metadata['chunk']} 段] {h.page_content}")
    return "\n".join(lines)


agent = create_agent(
    model=llm,
    tools=[search_docs],
    system_prompt=(
        "你是一个基于本地文档的问答助手。回答前必须先调用 search_docs 检索，"
        "回答中必须标出出处；如果检索不到，就直说文档里没有，不要编造。"
    ),
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "我在哪里工作？单位名称是什么？"}]},
)

print("[在线阶段回答]")
print(result["messages"][-1].content_blocks)
