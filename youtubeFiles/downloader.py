# youtubeFiles/downloader.py

import os
import yt_dlp

from .ffmpeg_manager import FFmpegManager
from .utils import sanitize_filename

class YouTubeDownloader:
    def __init__(self):
        self.folder = self.create_download_folder()
        self.ffmpeg = FFmpegManager()
        self.ffmpeg_folder = os.path.join(os.getcwd(), "setup", "ffmpeg", "bin")  # FFmpeg klasörü

    def create_download_folder(self):
        folder = "youtubeDownloads"
        if not os.path.exists(folder):
            os.makedirs(folder)
        return folder

    def download_audio_only(self, url, file_name):
        ydl_opts = {
            'format': '140',
            'ffmpeg_location': self.ffmpeg_folder,
            'outtmpl': os.path.join(self.folder, f"{file_name}.mp3"),
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'},
            ],
        }
        print("Sadece ses indiriliyor...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Ses başarıyla indirildi: {file_name}.mp3")

    def download_video_and_audio(self, url, video_quality, file_name):
        video_file = os.path.join(self.folder, "video.mp4")
        audio_file = os.path.join(self.folder, "audio.m4a")
        output_file = os.path.join(self.folder, f"{file_name}.mp4")

        ydl_video_opts = {
            'format': video_quality,
            'ffmpeg_location': self.ffmpeg_folder,
            'outtmpl': video_file
        }
        ydl_audio_opts = {
            'format': '140',
            'ffmpeg_location': self.ffmpeg_folder,
            'outtmpl': audio_file
        }

        print("Video indiriliyor...")
        with yt_dlp.YoutubeDL(ydl_video_opts) as ydl:
            ydl.download([url])

        print("Ses indiriliyor...")
        with yt_dlp.YoutubeDL(ydl_audio_opts) as ydl:
            ydl.download([url])

        print("Birleştirme işlemi başlatılıyor...")
        self.ffmpeg.merge(video_file, audio_file, output_file)

        # Geçici dosyaları sil
        if os.path.exists(video_file):
            os.remove(video_file)
            print(f"Silindi: {video_file}")
        if os.path.exists(audio_file):
            os.remove(audio_file)
            print(f"Silindi: {audio_file}")

        return video_file, audio_file, output_file  # 🔥 Bu satır eksikse unpack hatası olur

    def sanitize_and_get_title(self, url):
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'video').replace(" ", "_")
            return sanitize_filename(video_title)
