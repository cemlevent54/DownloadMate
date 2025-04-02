from .youtubeService import YoutubeDownloadService
from datetime import datetime

class YoutubeDownloadAPI:
    def __init__(self):
        self.youtube_service = YoutubeDownloadService()

    def download(self, url: str, type: str):
        # Zaman damgası ile benzersiz bir dosya adı oluştur
        timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        file_name = f"{timestamp}"  # Dosya adı sadece zaman damgası

        if type == "video":
            return self.youtube_service.download_video(url, file_name)
        elif type == "audio":
            return self.youtube_service.download_audio(url, file_name)
        else:
            raise ValueError("Geçersiz indirme türü! 'audio' veya 'video' olmalıdır.")
