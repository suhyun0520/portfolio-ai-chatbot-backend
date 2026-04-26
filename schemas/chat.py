from pydantic import BaseModel


class ChatReq(BaseModel):
    question : str
    top_k: int = 5
    dist_threshold: float = 0.25