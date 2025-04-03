from datetime import datetime
import os
import yt_dlp
import re


class TwitterDownloadService:
    def __init__(self):
        self.download_folder = "twitterDownloads"
        self.create_download_folder()
    
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

            ffmpeg_dir = os.path.join(os.getcwd(), "app", "setup", "FFmpeg", "bin")
            ffmpeg_exe = os.path.join(ffmpeg_dir, "ffmpeg.exe")
            if not os.path.exists(ffmpeg_exe):
                print(f"[!] FFmpeg bulunamadı: {ffmpeg_exe}")
                return None

            # .mp3 uzantısını koyma — yt_dlp zaten ekleyecek
            outtmpl_path = os.path.join(self.download_folder, file_name)

            ydl_opts = {
                'format': 'bestaudio/best',
                'ffmpeg_location': ffmpeg_dir,
                'outtmpl': outtmpl_path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # En son oluşan .mp3 dosyasını bul ve döndür
            mp3_files = [f for f in os.listdir(self.download_folder) if f.endswith(".mp3")]
            if not mp3_files:
                print("[!] mp3 dosyası bulunamadı.")
                return None

            latest_mp3 = max(mp3_files, key=lambda f: os.path.getctime(os.path.join(self.download_folder, f)))
            latest_mp3_path = os.path.join(self.download_folder, latest_mp3)

            print(f"[✔] Ses indirildi: {latest_mp3}")
            return latest_mp3_path

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
