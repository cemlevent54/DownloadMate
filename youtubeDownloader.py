import yt_dlp
import subprocess
import os
import shutil
import re  # Karakter temizleme için

class YouTubeDownloader:
    def __init__(self):
        self.downloads_folder = self.create_downloads_folder()
        self.ffmpeg_path = self.check_ffmpeg_path()

    def check_ffmpeg_path(self):
        """
        FFmpeg'in mevcut olup olmadığını kontrol eder ve yolunu döner.
        """
        ffmpeg_path = shutil.which("ffmpeg")
        if ffmpeg_path:
            print(f"FFmpeg bulundu: {ffmpeg_path}")
            return ffmpeg_path
        else:
            ffmpeg_path = "C:/ffmpeg/bin/ffmpeg.exe"
            print(f"FFmpeg manuel olarak ayarlandı: {ffmpeg_path}")
            return ffmpeg_path

    def create_downloads_folder(self):
        """
        İndirme klasörü oluşturur.
        """
        folder_name = "downloads"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            print(f"'{folder_name}' klasörü oluşturuldu.")
        else:
            print(f"'{folder_name}' klasörü zaten mevcut.")
        return folder_name

    def sanitize_filename(self, filename):
        """
        Dosya adını geçersiz karakterlerden temizler.
        """
        return re.sub(r'[\\/*?:"<>|]', '', filename)

    def get_available_formats(self, url):
        """
        Videonun desteklediği formatları döner.
        """
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            available_formats = {f['format_id']: f"{f['resolution']} - {f['ext']}" for f in formats if 'resolution' in f}
        return available_formats

    def sanitize_and_get_title(self, url):
        """
        Videonun başlığını temizlenmiş halde döner.
        """
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'video').replace(" ", "_")
            return self.sanitize_filename(video_title)

    def download_audio_only(self, url, file_name):
        """
        Sadece ses indirir.
        """
        audio_format = "140"  # Orta kalite ses formatı

        ydl_opts_audio = {
            'format': audio_format,
            'outtmpl': os.path.join(self.downloads_folder, f"{file_name}.mp3"),
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'},
            ],
        }

        print("Sadece ses indiriliyor...")
        with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
            ydl.download([url])
        print(f"Ses indirme tamamlandı: {file_name}.mp3")

    def download_video_and_audio(self, url, quality, file_name):
        """
        Video ve ses dosyalarını indirir.
        """
        video_format = quality  # Kullanıcının belirttiği kalite
        audio_format = "140"  # Orta kalite ses formatı

        # Video indirme ayarları
        ydl_opts_video = {
            'format': video_format,
            'outtmpl': os.path.join(self.downloads_folder, "video.mp4"),
        }

        # Ses indirme ayarları
        ydl_opts_audio = {
            'format': audio_format,
            'outtmpl': os.path.join(self.downloads_folder, "audio.m4a"),
        }

        print("Video indiriliyor...")
        with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
            ydl.download([url])

        print("Ses indiriliyor...")
        with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
            ydl.download([url])

        return os.path.join(self.downloads_folder, "video.mp4"), os.path.join(self.downloads_folder, "audio.m4a"), os.path.join(self.downloads_folder, f"{file_name}.mp4")

    def merge_video_and_audio(self, video_file, audio_file, output_file):
        """
        Video ve ses dosyalarını birleştirir ve geçici dosyaları temizler.
        """
        if not self.ffmpeg_path:
            print("Hata: FFmpeg yüklü değil veya bulunamadı.")
            return

        print("Video ve ses birleştiriliyor...")
        try:
            subprocess.run([
                self.ffmpeg_path, '-i', video_file, '-i', audio_file, '-c:v', 'copy', '-c:a', 'aac', output_file
            ], check=True)
            print(f"Birleştirme tamamlandı! Çıktı dosyası: {output_file}")

            # Geçici dosyaları sil
            if os.path.exists(video_file):
                os.remove(video_file)
                print(f"Geçici dosya silindi: {video_file}")
            if os.path.exists(audio_file):
                os.remove(audio_file)
                print(f"Geçici dosya silindi: {audio_file}")

        except subprocess.CalledProcessError as e:
            print(f"Bir hata oluştu: {e}")
