import yt_dlp
import subprocess
import os
import shutil
import re  # Karakter temizleme için
import FFmpegHelper.FFmpegHelper as FFmpegHelper

class YouTubeDownloader:
    def __init__(self):
        self.downloads_folder = self.create_downloads_folder()
        self.ffmpeg_path = self.check_ffmpeg_path()
        self.ffmpeg_helper = FFmpegHelper.FFmpegHelper()
        print("FFmpegHelper: ", self.ffmpeg_helper)

    def check_ffmpeg_path(self):
        """
        FFmpeg'in mevcut olup olmadığını kontrol eder ve yolunu döner.
        """
        # ffmpeg_path = shutil.which("ffmpeg")
        ffmpeg_path = os.path.join(os.getcwd(), "setup", "ffmpeg", "bin", "ffmpeg.exe") 
        if ffmpeg_path:
            print(f"FFmpeg bulundu: {ffmpeg_path}")
        else:
            # FFmpeg, sistem PATH'inde değilse, manuel olarak yolu belirliyoruz
            ffmpeg_path = os.path.join(os.getcwd(), "setup", "ffmpeg", "bin", "ffmpeg.exe")
            print(f"FFmpeg manuel olarak ayarlandı: {ffmpeg_path}")

            # FFmpeg'in yüklü olmadığını tespit ettiğimizde PATH'e ekliyoruz
            if not self.ffmpeg_helper.is_user_admin():
                print("Yönetici izni gerekiyor. Yönetici olarak çalıştırmak ister misiniz?")
                if self.ffmpeg_helper.ask_for_admin_permission():
                    self.ffmpeg_helper.add_ffmpeg_to_path()  # FFmpeg yolunu PATH'e ekle
                    print("FFmpeg PATH'e eklendi.")
                else:
                    print("Yönetici izni verilmedi. FFmpeg PATH'e eklenemedi.")
            else:
                # Eğer yönetici izni varsa, manuel olarak PATH'e ekleyelim
                self.add_ffmpeg_to_system_path(ffmpeg_path)
                    
        return ffmpeg_path

    def create_downloads_folder(self):
        """
        İndirme klasörü oluşturur.
        """
        folder_name = "youtubeDownloads"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            print(f"'{folder_name}' klasörü oluşturuldu.")
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
        print("FFmpeg: ", self.ffmpeg_path)
        print(f"Video dosyası tam yolu: {os.path.abspath(video_file)}")
        print(f"Ses dosyası tam yolu: {os.path.abspath(audio_file)}")
        print(f"Çıktı dosyası tam yolu: {os.path.abspath(output_file)}")
        if not self.ffmpeg_path:
            print("Hata: FFmpeg yüklü değil veya bulunamadı.")
            return

        print("Video ve ses birleştiriliyor...")
        try:
            subprocess.run([
                self.ffmpeg_path,   # FFmpeg'in yolda bulunduğu dosya
                '-i', video_file,   # Video dosyasının yolu
                '-i', audio_file,   # Ses dosyasının yolu
                '-c:v', 'copy',     # Video codec'ini kopyala
                '-c:a', 'aac',      # Ses codec'ini AAC olarak ayarla
                '-b:a', '192k',     # Sesin bit hızını 192kbit/s olarak ayarla
                '-shortest',        # En kısa dosyaya göre kes
                '-y',               # Var olan dosyayı zorla üzerine yaz
                '-loglevel', 'error', # Hata mesajlarını göster
                output_file         # Çıktı dosyasının adı
            ], check=True, capture_output=True, text=True)


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
