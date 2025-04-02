import os
import yt_dlp
import sys
from datetime import datetime
from .utils import sanitize_filename
from .ffmpeg_manager import FFmpegManager


class YoutubeDownloadService:
    def __init__(self):
        self.ffmpeg = FFmpegManager()

        # ✅ PyInstaller destekli ffmpeg yolu
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS  # PyInstaller kullanıldığında, geçici dosya yolu
        else:
            base_path = os.path.abspath(".")  # Normal çalışma sırasında geçerli dizin
        print("Base dizini:", base_path)

        # FFmpeg dosya yolunun doğru ayarlandığından emin olun
        self.ffmpeg_folder = os.path.join(base_path, "app", "setup", "FFmpeg", "bin")
        print("FFmpeg dizini:", self.ffmpeg_folder)

        # İndirme klasörünü oluştur
        self.folder = self.create_download_folder()

    def generate_filename(self):
        """ Dosya adını tarih ve saatle oluşturur. """
        current_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        file_name = f"{current_time}"
        return os.path.join(self.folder, file_name)

    def download(self, url, file_name, only_audio=False):
        """ URL'den video veya ses indirir. """
        file_name = sanitize_filename(file_name)  # Dosya adını temizle

        if only_audio:
            return self.download_audio(url, file_name)
        else:
            return self.download_video(url, file_name)

    def download_video(self, url, file_name):
        """ Video ve ses dosyasını indirir ve birleştirir. """
        # Dosya adı oluşturuluyor
        output_file = self.generate_filename()  # Dosya adı oluşturuluyor, uzantı eklenmemiş

        # Video ve ses için en iyi formatı seçiyoruz
        ydl_video_opts = {
            'format': 'bestvideo[height<=720]+bestaudio/best',  # Hem video hem de ses için en iyisini seç
            'ffmpeg_location': os.path.join(self.ffmpeg_folder, 'ffmpeg.exe'),
            'outtmpl': output_file,  # Video dosyasının geçici yolu
            'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}],  # Video formatını mp4'e dönüştür
        }

        try:
            # Video ve ses birlikte indiriliyor
            print(f"Video ve ses indiriliyor: {file_name}")
            with yt_dlp.YoutubeDL(ydl_video_opts) as ydl:
                ydl.download([url])

            # Dönüştürme sonrası dosyanın yolunu kontrol et
            if output_file.endswith('.mp4.mp4'):
                output_file = output_file.replace('.mp4.mp4', '.mp4')  # Fazla olan .mp4'ü sil

            # Dosya uzantısını ekleyelim (eğer yoksa)
            if not output_file.endswith('.mp4'):
                output_file += '.mp4'

            # Dosyanın gerçekten mevcut olduğundan emin olun
            if not os.path.exists(output_file):
                raise FileNotFoundError(f"Dosya bulunamadı: {output_file}")

            print(f"Video başarıyla indirildi: {output_file}")
            return output_file

        except Exception as e:
            print(f"Bir hata oluştu: {e}")
            return None




    def download_audio(self, url, file_name):
        """ En iyi kalite sesi indirir ve MP3 olarak kaydeder. """
        # Dosya adı oluşturuluyor
        output_file = self.generate_filename()  # Dosya adı oluşturuluyor, uzantı eklenmemiş

        # YDL (youtube-dl) için ses indirme seçenekleri
        ydl_opts = {
            'format': 'bestaudio/best',  # En iyi ses formatını seç
            'ffmpeg_location': os.path.join(self.ffmpeg_folder, 'ffmpeg.exe'),
            'outtmpl': output_file,  # Geçici dosya yolunu ayarla
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'},  # MP3 formatına dönüştür
            ],
        }

        try:
            print(f"Ses indiriliyor: {file_name}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # MP3 dosyasının uzantısını ekle
            if not output_file.endswith('.mp3'):
                output_file += '.mp3'

            # Dosyanın gerçekten mevcut olduğundan emin olun
            if not os.path.exists(output_file):
                raise FileNotFoundError(f"Dosya bulunamadı: {output_file}")

            print(f"Ses başarıyla indirildi: {output_file}")
            return output_file

        except Exception as e:
            print(f"Bir hata oluştu: {e}")
            return None


    def create_download_folder(self):
        """ İndirme klasörünü oluşturur. """
        folder = "youtubeDownloads"
        if not os.path.exists(folder):
            os.makedirs(folder)
        return folder

    def cleanup_files(self, files):
        """ Geçici dosyaları siler. """
        for file in files:
            if os.path.exists(file):
                os.remove(file)
                print(f"Silindi: {file}")
