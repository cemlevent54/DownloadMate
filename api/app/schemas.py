from pydantic import BaseModel
from typing import Literal
from typing import Optional

class YouTubeDownloadRequest(BaseModel):
    url: str
    type: Literal['video', 'audio']  # 'video' ya da 'audio' dışında bir değer almaz
    cookies: Optional[str] = None


class TwitterDownloadRequest(BaseModel):
    url: str
    type: Literal['video', 'audio']  # 'video' ya da 'audio' dışında bir değer almaz
    

class InstagramDownloadRequest(BaseModel):
    url: str
    type: Literal['video', 'audio']  # 'video' ya da 'audio' dışında bir değer almaz
    cookies: Optional[str] = None  # <-- burası yeni
