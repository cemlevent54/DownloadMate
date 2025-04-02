# twitterFiles/downloader.py

import os
import yt_dlp
import datetime


class TwitterDownloader:
    def __init__(self):
        self.download_folder = "twitterDownloads"
        self.create_download_folder()

    def create_download_folder(self):
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
            print(f"[+] Klasör oluşturuldu: {self.download_folder}")

    def sanitize_filename(self, filename):
        import re
        return re.sub(r'[\\/*?:"<>|]', '', filename)

    def download_audio_only(self, url):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f"{timestamp}_audio"

        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(self.download_folder, f"{file_name}.mp3"),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(f"[✔] Ses indirildi: {file_name}.mp3")
            return os.path.join(self.download_folder, f"{file_name}.mp3")
        except Exception as e:
            print(f"[download_audio_only] Hata: {e}")
            return None

    def download_video(self, url, quality="best"):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f"{timestamp}_video"

        try:
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
