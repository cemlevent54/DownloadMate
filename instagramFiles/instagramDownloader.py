import instaloader
import os
import re
import shutil
import datetime

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
        """
        İndirme klasörü oluşturur.
        """
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
            print(f"{self.download_folder} klasörü oluşturuldu.")
        else:
            print(f"{self.download_folder} klasörü zaten mevcut.")
    
    def delete_unnecessary_files(self):
        """
        İndirilen klasördeki gereksiz dosyaları siler (sadece .mp4 kalır).
        """
        for file in os.listdir(self.download_folder):
            if not file.endswith(".mp4"):  # Sadece .mp4 dosyalarını koru
                os.remove(os.path.join(self.download_folder, file))
                print(f"Gereksiz dosya silindi: {file}")
    
    def sanitize_filename(self, filename):
        """
        Dosya adını geçersiz karakterlerden temizler.
        """
        sanitized = re.sub(r'[\\/*?:"<>|]', "", filename)
        return sanitized
    
    def sanitize_and_get_title(self, url):
        """
        Videonun başlığını temizlenmiş halde döner.
        """
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(self.instaloader.context, shortcode)
        raw_title = post.caption or f"Instagram_Post_{shortcode}"  # Başlık yoksa varsayılan
        sanitized_title = self.sanitize_filename(raw_title[:50])  # 50 karakterle sınırla
        return sanitized_title

    def download_video_and_audio(self, url, file_name):
        """
        Video ve ses dosyasını indirir.
        """
        try:
            shortcode = url.split("/")[-2]
            post = instaloader.Post.from_shortcode(self.instaloader.context, shortcode)

            if not file_name:
                file_name = self.sanitize_and_get_title(url)
                
            
            self.instaloader.download_post(post, target=self.download_folder)
            
            # İndirilen dosya adını bul ve yeniden adlandır
            for file in os.listdir(self.download_folder):
                if file.endswith(".mp4") and shortcode in file:
                    new_path = os.path.join(self.download_folder, file_name + ".mp4")
                    shutil.move(os.path.join(self.download_folder, file), new_path)
                    print(f"Video indirildi: {new_path}")
                    self.delete_unnecessary_files()  # Gereksiz dosyaları sil
                    return new_path
        except Exception as e:
            print(f"Hata oluştu (Video ve Ses): {e}")
    
    def download(self, url):
        """
        Video indirme işlemini başlatır.
        """
        try:
            download_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
            sanitized_title = self.sanitize_and_get_title(url)
            file_name = f"{download_time}"
            
            self.download_video_and_audio(url, file_name)
            # delete .txt files
            for file in os.listdir(self.download_folder):
                if file.endswith(".txt"):
                    os.remove(os.path.join(self.download_folder, file))
        except Exception as e:
            print(f"İndirme sırasında hata oluştu: {e}")

# if __name__ == "__main__":
#     downloader = InstagramDownloader()

#     # Kullanıcıdan giriş al
#     url = input("Instagram video linkini girin: ")
#     downloader.download(url)
