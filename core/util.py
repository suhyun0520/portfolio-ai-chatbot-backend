# core/util.py
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from core.config import settings

# - embeddings: 문서 chunk와 질문을 벡터로 변환 (검색의 기반)
embeddings = OpenAIEmbeddings(
    model=settings.EMBED_MODEL,
    api_key=settings.OPENAI_API_KEY
)

# - llm: 검색된 chunk를 컨텍스트로 받아 자연어 답변 생성
llm = ChatOpenAI(
    model=settings.OPENAI_MODEL,
    api_key=settings.OPENAI_API_KEY,
    temperature=0.2
)

# 판정/계획용 LLM (JSON 뽑기 안정화용)
planner_llm = ChatOpenAI(
    model=settings.OPENAI_MODEL,
    api_key=settings.OPENAI_API_KEY,
    temperature=0
)

# pinecone 벡터 DB
pc = Pinecone(api_key=settings.PINECONE_API_KEY)

portfolio_index = pc.Index("portfolio-chat")

portfolio_vs = PineconeVectorStore(
    index=portfolio_index,
    embedding=embeddings,
    namespace="portfolio-namespace"
)

# Chroma 벡터 DB
vectorStore = Chroma(
    collection_name=settings.COLLECTION,
    embedding_function=embeddings,   # ✅ 여기 반드시 embeddings 객체
    persist_directory=settings.CHROMA_DIR,
)