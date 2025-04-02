import instaloader
import os

# Instagram reels veya video linkini al ve indir
def download_reels_or_video(link):
    # Instaloader nesnesi oluştur
    L = instaloader.Instaloader(
        download_comments=False,  # Yorumları indirme
        download_geotags=False,   # Coğrafi etiketleri indirme
        download_video_thumbnails=False,  # Video küçük resimlerini indirme
        save_metadata=False       # Metadata dosyalarını kaydetme
    )

    # URL'den shortcode'u çıkar
    try:
        shortcode = link.split("/")[-2]  # Shortcode, URL'nin son kısmıdır
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        # Hedef klasörü belirle ve indir
        L.download_post(post, target='reels')

        # İndirilen dosyalardan yalnızca .mp4 dosyasını sakla
        cleanup_files('reels')

    except Exception as e:
        print(f"Hata oluştu: {e}")


# Gereksiz dosyaları sil (sadece .mp4 kalsın)
def cleanup_files(folder):
    try:
        for filename in os.listdir(folder):
            if not filename.endswith('.mp4'):  # Sadece .mp4 bırak
                os.remove(os.path.join(folder, filename))
        print("Gereksiz dosyalar temizlendi, sadece .mp4 dosyası kaldı.")
    except Exception as e:
        print(f"Dosyalar temizlenirken bir hata oluştu: {e}")


def main():
    # Kullanıcıdan giriş alın
    link = input("Enter the link of the Instagram reels or video: ")
    download_reels_or_video(link)


if __name__ == "__main__":
    main()
