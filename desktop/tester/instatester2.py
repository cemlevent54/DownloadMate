import yt_dlp

def download_instagram_video_with_quality(link, quality="1080p"):
    try:
        ydl_opts = {
            'format': f'bestvideo[height<={quality}]+bestaudio/best',  # Kaliteyi ayarla
            'outtmpl': '%(title)s.%(ext)s',  # Çıkış dosyası adı
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'  # Çıkış formatı
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])  # Videoyu indir
        print(f"Video başarıyla indirildi ({quality}) kalitesinde.")

    except Exception as e:
        print(f"Hata oluştu: {e}")

def main():
    link = input("Enter the Instagram video link: ")
    quality = input("Enter the desired quality (360, 480, 720, 1080p): ")
    download_instagram_video_with_quality(link, quality)

if __name__ == "__main__":
    main()
