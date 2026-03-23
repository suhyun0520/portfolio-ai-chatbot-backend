from fastapi import APIRouter
from schemas.chat import ChatReq
from fastapi import FastAPI, UploadFile, File
from crud.chat import get_chat,ingest_docx, vector_store_insert

router = APIRouter()

@router.post("/v1/chat")
def chat_route(req: ChatReq):
    """
    답변 받아오기
    """
    print("라우터 호출 확인")
    return get_chat(req=req)

@router.post("/v1/ingest/docx")
async def ingest_docx_route(file: UploadFile = File(...)):
    """
    문서 업로드 하기
    """
    print("문서 라우팅 호출 확인")
    return await vector_store_insert(file=file)