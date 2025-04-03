from .instagramService import InstagramDownloadService
from datetime import datetime 

class InstagramDownloadAPI:
    def __init__(self):
        self.instagram_service = InstagramDownloadService()
    
    def download(self, url: str, type: str):
        timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        file_name = f"{timestamp}"  # Dosya adı sadece zaman damgası
        
        return self.instagram_service.download_media(url,file_name,type)
    