from .instagramService import InstagramDownloadService
from datetime import datetime 
from typing import Optional

class InstagramDownloadAPI:
    def __init__(self):
        self.instagram_service = InstagramDownloadService()
    
    def download(self, url: str, type: str, cookies: Optional[str] = None):
        try:
            timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
            file_name = f"{timestamp}"  # Dosya adı zaman damgası

            # 🍪 cookies argümanı eklendi
            result_path = self.instagram_service.download_media(
                url=url,
                file_name=file_name,
                media_type=type,
                cookies=cookies
            )

            if result_path is None:
                raise Exception("Instagram medya indirilemedi. 'None' döndü.")

            return result_path

        except Exception as e:
            raise Exception(f"InstagramDownloadAPI -> İndirme sırasında hata oluştu: {e}")