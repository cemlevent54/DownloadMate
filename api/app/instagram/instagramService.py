import instaloader
import os
import shutil
import datetime
from .utils import sanitize_filename
import re
from moviepy import VideoFileClip

class InstagramDownloadService:
    def __init__(self):
        self.download_folder = "instagramDownloads"
        self.instaloader = instaloader.Instaloader(
            download_comments=False,
            download_geotags=False,
            download_video_thumbnails=False,
            save_metadata=False
        )
        self.create_downloads_folder()
        
    def create_downloads_folder(self):
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
            print(f"[+] Klasör oluşturuldu: {self.download_folder}")

    def extract_shortcode(self, url):
        """
        Instagram bağlantısından geçerli shortcode bilgisini çıkarır.
        """
        match = re.search(r"(?:/p/|/reel/|/tv/)([A-Za-z0-9_-]+)", url)
        if match:
            return match.group(1)
        else:
            raise ValueError("Geçerli bir Instagram bağlantısı değil.")

    def sanitize_and_get_title(self, url):
        """
        Post başlığını güvenli bir dosya adına çevirip döner.
        """
        try:
            shortcode = self.extract_shortcode(url)
            post = instaloader.Post.from_shortcode(self.instaloader.context, shortcode)
            raw_title = post.caption or f"Instagram_Post_{shortcode}"
            return sanitize_filename(raw_title[:50])
        except Exception as e:
            print(f"[sanitize_and_get_title] Hata: {e}")
            return "instagram_video"

    

    def download_media(self, url, file_name=None, media_type="video"):
        """
        Instagram videosunu indirir.
        media_type = 'video' -> .mp4, 'audio' -> .mp3
        """
        try:
            shortcode = self.extract_shortcode(url)
            post = instaloader.Post.from_shortcode(self.instaloader.context, shortcode)
            
            print(f"[▶] İndirme başlatılıyor: {shortcode}")
            self.instaloader.download_post(post, target=self.download_folder)

            # .mp4 dosyasını bul
            mp4_files = [f for f in os.listdir(self.download_folder) if f.endswith(".mp4")]
            if not mp4_files:
                print("[!] .mp4 dosyası bulunamadı.")
                return None

            latest_file = max(mp4_files, key=lambda f: os.path.getctime(os.path.join(self.download_folder, f)))
            mp4_path = os.path.join(self.download_folder, latest_file)

            if media_type == "audio":
                mp3_path = os.path.join(self.download_folder, f"{file_name}.mp3")
                clip = VideoFileClip(mp4_path)
                clip.audio.write_audiofile(mp3_path)
                clip.close()

                os.remove(mp4_path)  # .mp4 dosyasını sil
                self.clean_folder()
                print(f"[🎵] Ses dosyası oluşturuldu: {mp3_path}")
                return mp3_path

            else:  # video
                new_name = f"{file_name}.mp4"
                new_path = os.path.join(self.download_folder, new_name)
                shutil.move(mp4_path, new_path)
                self.clean_folder()
                print(f"[🎥] Video dosyası oluşturuldu: {new_path}")
                return new_path

        except Exception as e:
            print(f"[download_media] Hata: {e}")
            return None 


    def clean_folder(self):
        """
        Klasördeki .txt, .json ve .xz dosyalarını temizler (diğer içerikler korunur).
        """
        for file in os.listdir(self.download_folder):
            full_path = os.path.join(self.download_folder, file)
            if file.endswith((".txt", ".json", ".xz")):
                try:
                    os.remove(full_path)
                    print(f"[🧹] Gereksiz dosya silindi: {file}")
                except Exception as e:
                    print(f"[clean_folder] Silinirken hata oluştu: {e}")
    
    