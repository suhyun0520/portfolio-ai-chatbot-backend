from fastapi import APIRouter, Request
from schemas.chat import ChatReq
from fastapi import FastAPI, UploadFile, File
from crud.chat import get_chat,ingest_docx, vector_store_insert

router = APIRouter()

@router.post("/v1/chat")
def chat_route(req: ChatReq, request: Request):
    """
    답변 받아오기
    """
    return get_chat(req=req, request=request)

@router.post("/v1/ingest/docx")
async def ingest_docx_route(file: UploadFile = File(...)):
    """
    문서 업로드 하기
    """
    return await vector_store_insert(file=file)