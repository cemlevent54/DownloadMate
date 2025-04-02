import instaloader
import os
import shutil
import datetime
from .utils import sanitize_filename


class InstagramDownloader:
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
        Instagram bağlantısından shortcode bilgisini çıkarır.
        """
        return url.strip("/").split("/")[-1]

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

    def download_video(self, url, custom_filename=None):
        """
        Instagram postunu indirir, .mp4 dosyasını adlandırır ve dosya yolunu döner.
        """
        try:
            shortcode = self.extract_shortcode(url)
            post = instaloader.Post.from_shortcode(self.instaloader.context, shortcode)

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S_UTC")
            title = custom_filename or f"{timestamp}"

            print(f"[▶] İndirme başlatılıyor: {shortcode}")
            self.instaloader.download_post(post, target=self.download_folder)

            # En son indirilen .mp4 dosyasını bul
            mp4_files = [f for f in os.listdir(self.download_folder) if f.endswith(".mp4")]
            if not mp4_files:
                print("[!] .mp4 dosyası bulunamadı.")
                return None

            latest_file = max(mp4_files, key=lambda f: os.path.getctime(os.path.join(self.download_folder, f)))
            old_path = os.path.join(self.download_folder, latest_file)
            new_name = f"{title}.mp4"
            new_path = os.path.join(self.download_folder, new_name)
            shutil.move(old_path, new_path)
            print(f"[✔] Video yeniden adlandırıldı: {new_name}")

            # Sadece .mp4 dışındaki geçici dosyaları temizle
            self.clean_folder()
            return new_path

        except Exception as e:
            print(f"[download_video] Hata: {e}")
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
