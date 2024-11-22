from youtubeDownloader import YouTubeDownloader

def main():
    # YouTubeDownloader sınıfını başlat
    downloader = YouTubeDownloader()

    # Kullanıcıdan URL, format ve kalite bilgilerini al
    video_url = input("YouTube video URL'sini girin: ")
    
    print("\nMevcut formatlar listeleniyor...")
    available_formats = downloader.get_available_formats(video_url)
    for format_id, details in available_formats.items():
        print(f"{format_id}: {details}")

    format_choice = input("\nFormat seçin (mp4/mp3): ").strip().lower()

    if format_choice == "mp4":
        quality_choice = input("\nKalite seçin (ör: 134 - 360p, 135 - 480p, 136 - 720p): ").strip()

    # Videonun başlığını alın ve dosya adını oluşturun
    video_title = downloader.sanitize_and_get_title(video_url)

    if format_choice == "mp3":
        # Sadece ses indir
        downloader.download_audio_only(video_url, video_title)
    elif format_choice == "mp4":
        # Video ve ses indir
        try:
            video_file, audio_file, final_video_file = downloader.download_video_and_audio(
                video_url, quality_choice, video_title
            )
            # İndirilen dosyaları birleştir
            downloader.merge_video_and_audio(video_file, audio_file, final_video_file)
        except Exception as e:
            print(f"Hata oluştu: {e}")
    else:
        print("Geçersiz format seçimi!")

if __name__ == "__main__":
    main()
