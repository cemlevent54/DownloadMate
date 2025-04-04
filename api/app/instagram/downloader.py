from .instagramService import InstagramDownloadService
from datetime import datetime 

class InstagramDownloadAPI:
    def __init__(self):
        self.instagram_service = InstagramDownloadService()
    
    def download(self, url: str, type: str):
        try:
            timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
            file_name = f"{timestamp}"  # Dosya adı sadece zaman damgası

            result_path = self.instagram_service.download_media(url, file_name, type)

            if result_path is None:
                raise Exception("Instagram medya indirilemedi. 'None' döndü.")

            return result_path

        except Exception as e:
            # Burada exception direkt yükseltiliyor ki FastAPI tarafı detaylı şekilde handle edebilsin
            raise Exception(f"InstagramDownloadAPI -> İndirme sırasında hata oluştu: {e}")
    