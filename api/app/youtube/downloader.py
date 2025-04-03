from .youtubeService import YoutubeDownloadService
from datetime import datetime
from fastapi.logger import logger

class YoutubeDownloadAPI:
    def __init__(self):
        self.youtube_service = YoutubeDownloadService()

    def download(self, url: str, type: str):
        try:
            logger.info(f"[🧠] YoutubeDownloadAPI.download() çağrıldı - URL: {url}, TYPE: {type}")
            timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
            file_name = f"{timestamp}"

            if type == "video":
                return self.youtube_service.download_video(url, file_name)
            elif type == "audio":
                return self.youtube_service.download_audio(url, file_name)
            else:
                raise ValueError("Geçersiz indirme türü! 'audio' veya 'video' olmalıdır.")
        except Exception as e:
            logger.error(f"[🔥] YoutubeDownloadAPI.download() hata: {e}\n{traceback.format_exc()}")
            raise
