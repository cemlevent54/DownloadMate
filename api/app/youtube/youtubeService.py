import os
import yt_dlp
import sys
from datetime import datetime
from .utils import sanitize_filename
from .ffmpeg_manager import FFmpegManager
import re
import subprocess
from moviepy import AudioFileClip
import traceback2 as traceback
from fastapi.logger import logger
from fastapi import HTTPException


class YoutubeDownloadService:
    def __init__(self):
        self.ffmpeg = FFmpegManager()
        
        # PyInstaller kontrolü
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        print("Base dizini:", base_path)

        self.ffmpeg_folder = os.path.join(base_path, "app", "setup", "FFmpeg", "bin")
        self.ffmpeg_exe = os.path.join(self.ffmpeg_folder, "ffmpeg.exe")

        print("FFmpeg dizini:", self.ffmpeg_folder)

        self.folder = self.create_download_folder()
        self.download_folder = "youtubeDownloads"

    def generate_filename(self):
        current_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        return os.path.join(self.folder, current_time)

    def download(self, url, file_name, only_audio=False):
        file_name = sanitize_filename(file_name)
        return self.download_audio(url, file_name) if only_audio else self.download_video(url, file_name)

    def download_video(self, url, file_name):
        output_file = self.generate_filename()
        quality = "best"

        ydl_video_opts = {
            'format': f'{quality}+bestaudio/best',
            'geo_bypass': True,
            'cookiefile': 'cookies.txt', 
            'ffmpeg_location': self.ffmpeg_folder,
            'outtmpl': output_file + '.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }]
        }

        try:
            print(f"Video ve ses indiriliyor: {file_name}")
            with yt_dlp.YoutubeDL(ydl_video_opts) as ydl:
                ydl.download([url])

            # Gerçek dosya yolunu bul
            final_file = output_file + '.mp4'
            if not os.path.exists(final_file):
                raise FileNotFoundError(f"Dosya bulunamadı: {final_file}")

            print(f"Video başarıyla indirildi: {final_file}")
            return final_file

        except Exception as e:
            error_message = str(e)
            print(f"[🔥] download_video() hatası: {error_message}")

            # Ülke kısıtlaması kontrolü
            if "not made this video available in your country" in error_message:
                raise HTTPException(
                    status_code=403,
                    detail="Bu video bulunduğunuz ülke için kullanılamıyor."
                )

            raise

    
    def sanitize_filename(self, filename):
        return re.sub(r'[\\/*?:"<>|]', '', filename)

    

    def download_audio(self, url, file_name):
        try:
            if not file_name:
                file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_UTC")
            file_name = self.sanitize_filename(file_name)

            print(f"[▶️] download_audio() başlatıldı: {file_name}")

            webm_path = self.download_webm_file(url, file_name)
            if not webm_path:
                print("[❌] WebM indirme başarısız.")
                return None

            mp3_path = os.path.join(self.download_folder, file_name + ".mp3")

            success = self.convert_webm_to_mp3(webm_path, mp3_path)
            if not success:
                print("[❌] WebM -> MP3 dönüştürme başarısız.")
                return None

            print(f"[✅] Ses başarıyla indirildi ve dönüştürüldü: {mp3_path}")
            return mp3_path

        except Exception as e:
            print(f"[🔥] download_audio() genel hata: {e}")
            return None


    def convert_webm_to_mp3(self, webm_path, mp3_path):
        try:
            print(f"[🎬] MoviePy ile dönüştürme başlatıldı.")
            print(f"[🛠] Kaynak dosya (webm): {webm_path}")
            print(f"[🛠] Hedef dosya (mp3): {mp3_path}")

            audioclip = AudioFileClip(webm_path)
            audioclip.write_audiofile(mp3_path)
            audioclip.close()

            if os.path.exists(mp3_path):
                print(f"[🎉] MP3 dosyası oluşturuldu: {mp3_path}")
                os.remove(webm_path)
                return True
            else:
                print(f"[❌] MP3 dosyası oluşmadı: {mp3_path}")
                return False

        except Exception as e:
            print(f"[🔥] convert_webm_to_mp3() hata: {e}")
            return False


    def download_webm_file(self, url, file_name):
        webm_path = os.path.join(self.download_folder, file_name + ".webm")
        print(f"[⬇] WebM indirme yolu: {webm_path}")

        ydl_opts = {
            'format': 'bestaudio/best',
            'cookiefile': 'cookies.txt', 
            'geo_bypass': True,
            'outtmpl': webm_path,
            'postprocessors': []
        }

        try:
            print(f"[🔍] WebM indiriliyor: {url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            if os.path.exists(webm_path):
                print(f"[📁] WebM dosyası indirildi: {webm_path}")
                return webm_path
            else:
                print(f"[❌] WebM dosyası bulunamadı: {webm_path}")
                return None

        except Exception as e:
            print(f"[🔥] download_webm_file() hatası: {e}")
            return None

    def create_download_folder(self):
        folder = "youtubeDownloads"
        os.makedirs(folder, exist_ok=True)
        return folder

    def cleanup_files(self, files):
        for file in files:
            if os.path.exists(file):
                os.remove(file)
                print(f"Silindi: {file}")
