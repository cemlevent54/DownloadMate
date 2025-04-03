from .twitterService import TwitterDownloadService
from datetime import datetime

class TwitterDownloadAPI:
    def __init__(self):
        self.twitter_service = TwitterDownloadService()
        
    
    def download(self, url:str, type:str):
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f"{timestamp}"
        
        if type == "audio":
            return self.twitter_service.download_audio_only(url,file_name)
        
        elif type == "video":
            quality = "best"
            return self.twitter_service.download_video(url, quality, file_name)