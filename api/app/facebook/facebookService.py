from datetime import datetime
import os
import yt_dlp
import re
from moviepy import AudioFileClip
from requests.utils import cookiejar_from_dict

class FacebookDownloadService:
    def __init__(self):
        self.download_folder = "facebookDownloads"
        self.create_download_folder()
        self.cookies = None
    
    def create_download_folder(self):
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
            print(f"[+] Klasör oluşturuldu: {self.download_folder}")

    def sanitize_filename(self, filename):
        return re.sub(r'[\\/*?:"<>|]', '', filename)
    
    def download_audio_only(self, url, file_name=None):
        try:
            if not file_name:
                file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_UTC")
            file_name = self.sanitize_filename(file_name)

            webm_path = os.path.join(self.download_folder, f"{file_name}.webm")
            mp3_path = os.path.join(self.download_folder, f"{file_name}.mp3")

            # yt_dlp ile sadece sesi .webm formatında indir
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': webm_path,
                'postprocessors': []  # Ses dönüştürmesini biz yapacağız
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            if not os.path.exists(webm_path):
                print("[❌] WebM dosyası indirilemedi.")
                return None

            # moviepy ile .mp3'e dönüştür
            audioclip = AudioFileClip(webm_path)
            audioclip.write_audiofile(mp3_path)
            audioclip.close()

            # Temizlik
            os.remove(webm_path)
            print(f"[✔] Ses indirildi ve dönüştürüldü: {mp3_path}")
            return mp3_path

        except Exception as e:
            print(f"[download_audio_only] Hata: {e}")
            return None



    def download_video(self, url, quality="best", file_name=None):
        try:
            if not file_name:
                file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_UTC")
            file_name = self.sanitize_filename(file_name)

            ydl_opts = {
                'format': f'{quality}+bestaudio/best',
                'outtmpl': os.path.join(self.download_folder, f"{file_name}.mp4"),
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }]
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(f"[✔] Video indirildi: {file_name}.mp4")
            return os.path.join(self.download_folder, f"{file_name}.mp4")
        except Exception as e:
            print(f"[download_video] Hata: {e}")
            return None