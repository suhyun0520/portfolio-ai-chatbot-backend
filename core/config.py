from pydantic_settings import BaseSettings
from pydantic import ConfigDict


# 환경변수 설정값
# - OPENAI_API_KEY: 필수 (없으면 KeyError로 바로 터짐)
# - OPENAI_MODEL: 답변 생성 모델
# - EMBED_MODEL: 임베딩 모델(문서/질문을 벡터로 변환)
# - CHROMA_DIR: chroma DB가 저장될 폴더(로컬 영구 저장)
# - COLLECTION: chroma 컬렉션 이름(※ 3글자 이상 권장/필수인 경우 많음)
# - TOP_K: 검색 시 상위 몇 개 chunk를 가져올지
# - DIST_THRESHOLD: "문서에 없다" 판정 커트라인(점수 체계가 애매할 수 있어 튜닝 필요)

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    PINECONE_API_KEY: str
    OPENAI_MODEL: str
    EMBED_MODEL: str
    CHROMA_DIR: str
    # ⚠️ 예전 에러: "me"는 2글자라 컬렉션 이름 규칙에 걸릴 수 있음
    # 안전하게 기본값은 3글자 이상으로 두는 게 좋음
    COLLECTION: str

    TOP_K: int = 5
    DIST_THRESHOLD: float = 999.0

    DATABASE_URL: str | None = None

    model_config = ConfigDict(env_file=".env", extra="ignore")
 

settings = Settings()
