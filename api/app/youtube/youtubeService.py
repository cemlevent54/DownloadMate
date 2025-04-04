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
from typing import Optional


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

    def download(self, url, file_name, only_audio=False, cookies: Optional[str] = None):
        file_name = sanitize_filename(file_name)
        return self.download_audio(url, file_name, cookies=cookies) if only_audio else self.download_video(url, file_name, cookies=cookies)

    def download_video(self, url, file_name, cookies: Optional[str] = None):
        output_file = self.generate_filename()
        quality = "best"
        
        cookie_file_path = None
        if cookies:
            cookie_file_path = os.path.join(self.folder, "youtube_cookies.txt")
            netscape_cookies = self.convert_cookie_string_to_netscape_format(cookies)
            with open(cookie_file_path, "w", encoding="utf-8") as f:
                f.write(netscape_cookies)

        ydl_video_opts = {
            'format': f'{quality}+bestaudio/best',
            'geo_bypass': True,
            'ffmpeg_location': self.ffmpeg_folder,
            'outtmpl': output_file + '.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }]
        }

        # 🧠 Yeni: Cookie string header olarak veriliyor
        if cookies:
            ydl_video_opts['cookiefile'] = cookie_file_path

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

    

    def download_audio(self, url, file_name, cookies: Optional[str] = None):
        try:
            if not file_name:
                file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_UTC")
            file_name = self.sanitize_filename(file_name)

            print(f"[▶️] download_audio() başlatıldı: {file_name}")

            webm_path = self.download_webm_file(url, file_name, cookies=cookies)
            if not webm_path:
                raise Exception("WebM dosyası indirilemedi veya bulunamadı.")

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


    def download_webm_file(self, url, file_name, cookies: Optional[str] = None):
        webm_path = os.path.join(self.download_folder, file_name + ".webm")
        print(f"[⬇] WebM indirme yolu: {webm_path}")

        cookie_file_path = None
        if cookies:
            # 📄 Cookie stringini Netscape formatına çevir
            cookie_file_path = os.path.join(self.folder, "youtube_cookies.txt")
            netscape_cookies = self.convert_cookie_string_to_netscape_format(cookies)
            with open(cookie_file_path, "w", encoding="utf-8") as f:
                f.write(netscape_cookies)
            print(f"[🍪] Çerez dosyası yazıldı: {cookie_file_path}")

        ydl_opts = {
            'format': 'bestaudio/best',
            'geo_bypass': True,
            'outtmpl': webm_path,
            'postprocessors': []
        }

        if cookie_file_path:
            ydl_opts['cookiefile'] = cookie_file_path

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
    
    def convert_cookie_string_to_netscape_format(self, cookie_string: str, domain: str = ".youtube.com") -> str:
        header = "# Netscape HTTP Cookie File\n"
        lines = []
        expiry = "1893456000"  # örnek: yıl 2030 civarı

        for item in cookie_string.split(";"):
            if "=" in item:
                name, value = item.strip().split("=", 1)
                line = f"{domain}\tTRUE\t/\tFALSE\t{expiry}\t{name}\t{value}"
                lines.append(line)

        return header + "\n".join(lines)