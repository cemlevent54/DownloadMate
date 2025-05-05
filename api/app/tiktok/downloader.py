from .tiktokService import TiktokDownloadService
from datetime import datetime 
from typing import Optional

class TiktokDownloadAPI:
    def __init__(self):
        self.tiktok_service = TiktokDownloadService()
        
    
    def download(self, url:str, type:str):
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f"{timestamp}"
        
        if type == "audio":
            return self.tiktok_service.download_audio_only(url,file_name)
        
        elif type == "video":
            quality = "best"
            return self.tiktok_service.download_video(url, quality, file_name)