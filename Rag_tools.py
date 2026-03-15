import os
from langchain.tools import tool
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
DB_PATH = './neko_chroma_db'
embeddings = HuggingFaceEmbeddings(model_name='moka-ai/m3e-base')
if os.path.exists(DB_PATH):
    vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    retriever = vector_db.as_retriever(search_kwargs={'k': 3})
    print('[RAG] 向量数据库加载成功！')
else:
    retriever = None
    print(f'[RAG] 猫猫哭哭: 找不到向量数据库路径 {DB_PATH}')
@tool
def query_knowledge_base(query: str) -> str:
    if retriever is None:
        return '本地知识库尚未建立或加载失败。'
    try:
        docs = retriever.invoke(query)
        if not docs:
            return '知识库中没有找到与该问题相关的参考内容。'
        context = '\n\n'.join([f'【参考片段 {i + 1}】:\n{doc.page_content}' for i, doc in enumerate(docs)])
        return f'从知识库中检索到以下信息，请根据这些信息回答用户：\n\n{context}'
    except Exception as e:
        return f'检索知识库时发生错误: {e}'