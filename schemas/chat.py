from pydantic import BaseModel
from core.config import settings

class ChatReq(BaseModel):
    question : str
    top_k: int = settings.TOP_K
    dist_threshold: float = settings.DIST_THRESHOLD