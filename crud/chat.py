# crud/chat.py
import os
from uuid import uuid4
import datetime

from fastapi import UploadFile, File
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore

from schemas.chat import ChatReq
from core.util import llm, pc, embeddings
from core.derived_tools import (
    derive_age_from_text,
    derive_total_experience_from_text,
    derive_company_tenure_from_text,
)

splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=150)


def get_chat(req: ChatReq):
    index = pc.Index("portfolio-chat")
    vs = PineconeVectorStore(
        index=index,
        embedding=embeddings,
        namespace="portfolio-namespace"
    )

    top_k = min(req.top_k or 3, 4)

    # 1. 검색
    results = vs.similarity_search_with_score(req.question, k=top_k)

    if not results:
        print("not result")
        return {
            "answer": "문서에 해당 정보가 없습니다.",
            "sources": []
        }

    # 2. context / sources 만들기
    context_blocks = []
    sources = []

    for doc, score in results:
        tag = f"{doc.metadata.get('source')}#{doc.metadata.get('chunk')}"
        context_blocks.append(f"[SOURCE: {tag}]\n{doc.page_content}")
        sources.append({
            "source": doc.metadata.get("source"),
            "chunk": doc.metadata.get("chunk"),
            "score": score,
            "snippet": doc.page_content[:200].replace("\n", " ")
                      + ("..." if len(doc.page_content) > 200 else "")
        })

    context_text = "\n\n".join(context_blocks)
    q = req.question.lower()

    # # 3. 계산 질문이면 바로 처리
    # if "나이" in q or "몇 살" in q or "만 나이" in q:
    #     answer, note = derive_age_from_text(context_text)
    #     if answer:
    #         return {
    #             "answer": answer,
    #             "sources": sources + [{
    #                 "source": "computed",
    #                 "chunk": None,
    #                 "score": None,
    #                 "snippet": note
    #             }]
    #         }

    # elif "총 경력" in q or "전체 경력" in q or "경력 합산" in q:
    #     answer, note = derive_total_experience_from_text(context_text)
    #     if answer:
    #         return {
    #             "answer": answer,
    #             "sources": sources + [{
    #                 "source": "computed",
    #                 "chunk": None,
    #                 "score": None,
    #                 "snippet": note
    #             }]
    #         }

    # elif ("근무 기간" in q or "재직 기간" in q):
    #     if "엘리엇" in req.question:
    #         answer, note = derive_company_tenure_from_text(context_text, "엘리엇")
    #         if answer:
    #             return {
    #                 "answer": answer,
    #                 "sources": sources + [{
    #                     "source": "computed",
    #                     "chunk": None,
    #                     "score": None,
    #                     "snippet": note
    #                 }]
    #             }

    #     elif "모비루스" in req.question:
    #         answer, note = derive_company_tenure_from_text(context_text, "모비루스")
    #         if answer:
    #             return {
    #                 "answer": answer,
    #                 "sources": sources + [{
    #                     "source": "computed",
    #                     "chunk": None,
    #                     "score": None,
    #                     "snippet": note
    #                 }]
    #             }

    #     elif "WBS" in req.question or "더블유비에스" in req.question:
    #         answer, note = derive_company_tenure_from_text(context_text, "WBS")
    #         if answer:
    #             return {
    #                 "answer": answer,
    #                 "sources": sources + [{
    #                     "source": "computed",
    #                     "chunk": None,
    #                     "score": None,
    #                     "snippet": note
    #                 }]
    #             }
    print("answer llm")
    today = datetime.date.today()
    # 4. 일반 질문이면 LLM으로 답변
    system = (
        "너는 사용자의 .docx 문서를 바탕으로 답변하는 포트폴리오 어시스턴트다.\n"
        "규칙:\n"
        f"1) 현재 일자는 {today}이다.\n"
        "2) 아래 CONTEXT를 우선 근거로 답해라.\n"
        "3) CONTEXT에 정보가 부족하면, 부족하다고 짧게 말한 뒤 일반적인 설명을 덧붙여도 된다.\n"
        "4) 하지만 문서에 없는 사실을 단정해서 말하지 마라.\n"
        "5) 답변은 자연스럽고 이해하기 쉽게 작성해라.\n"
        "6) 답변할때 CONTEXT라는 단어를 쓰지마라, 답변을 하기엔 정보가 부족하다는 식으로 말해라"
    )

    prompt = "CONTEXT:\n\n" + context_text + f"\n\n질문: {req.question}"
    answer = llm.invoke([("system", system), ("human", prompt)]).content

    return {
        "answer": answer,
        "sources": sources
    }


async def ingest_docx(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".docx"):
        return {"ok": False, "error": "현재는 .docx만 지원합니다."}

    os.makedirs("./uploads", exist_ok=True)
    path = os.path.join("./uploads", file.filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    docs = Docx2txtLoader(path).load()
    chunks = splitter.split_documents(docs)

    for i, d in enumerate(chunks):
        d.metadata = {**d.metadata, "source": file.filename, "chunk": i}

    index = pc.Index("portfolio-chat")
    vs = PineconeVectorStore(
        index=index,
        embedding=embeddings,
        namespace="portfolio-namespace"
    )

    ids = [str(uuid4()) for _ in chunks]
    vs.add_documents(documents=chunks, ids=ids)

    return {"ok": True, "source": file.filename, "chunks": len(chunks)}


async def vector_store_insert(file: UploadFile = File(...)):
    return await ingest_docx(file)