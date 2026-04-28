from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# 라우터 가져오기
from routers import chat

# ------------------------------------------------------------
# 2) FastAPI 앱 생성 + CORS 설정
# - 프론트엔드에서 호출하려면 CORS 허용 필요
# - allow_origins=["*"] 는 개발 편의용(배포 시 도메인 제한 권장)
# ------------------------------------------------------------
app = FastAPI(title="Docx RAG MVP")

origins = os.getenv("ALLOWED_ORIGINS","").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins != [""] else ["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
