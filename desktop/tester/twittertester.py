import yt_dlp

def download_twitter_video(url, quality="best", output_format="mp4"):
    try:
        # YT-DLP ayarları
        ydl_opts = {
            'format': f'{quality}+bestaudio/best',  # Belirli kaliteyi seç
            'outtmpl': '%(title)s.%(ext)s',  # Çıkış dosya ismi
            'postprocessors': []
        }

        # MP3 veya MP4 formatını belirle
        if output_format == "mp3":
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',  # Çıktı formatı MP3
                'preferredquality': '192',  # Ses kalitesi (opsiyonel)
            })
        elif output_format == "mp4":
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',  # Çıktı formatı MP4
            })

        # Video veya ses indirme işlemi
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"{output_format.upper()} formatında dosya başarıyla indirildi: {url}")

    except Exception as e:
        print(f"Hata oluştu: {e}")

def main():
    # Kullanıcıdan URL, kalite ve format girdisi al
    url = input("Twitter video linkini girin: ")
    quality = input("Kaliteyi girin (best, 360, 720, 1080): ").strip() or "best"
    output_format = input("Çıkış formatını seçin (mp3/mp4): ").strip().lower() or "mp4"
    
    # Geçerli format olup olmadığını kontrol et
    if output_format not in ["mp3", "mp4"]:
        print("Geçersiz format seçimi! Lütfen 'mp3' veya 'mp4' giriniz.")
        return

    download_twitter_video(url, quality, output_format)

if __name__ == "__main__":
    main()
