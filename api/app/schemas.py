from pydantic import BaseModel
from typing import Literal

class YouTubeDownloadRequest(BaseModel):
    url: str
    type: Literal['video', 'audio']  # 'video' ya da 'audio' dışında bir değer almaz


class TwitterDownloadRequest(BaseModel):
    url: str

class InstagramDownloadRequest(BaseModel):
    url: str
