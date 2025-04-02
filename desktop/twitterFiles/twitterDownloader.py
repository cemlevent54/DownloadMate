# import os
# import yt_dlp
# import datetime


# class TwitDownloader:
#     def __init__(self):
#         self.downloads_folder = self.create_downloads_folder()

#     def create_downloads_folder(self):
#         """
#         İndirme klasörü oluşturur.
#         """
#         folder_name = "twitterDownloads"
#         if not os.path.exists(folder_name):
#             os.makedirs(folder_name)
#             print(f"'{folder_name}' klasörü oluşturuldu.")
#         return folder_name

#     def get_available_formats(self, url):
#         """
#         Videonun desteklediği formatları döner.
#         """
#         try:
#             ydl_opts = {'listformats': True}
#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 info = ydl.extract_info(url, download=False)
#                 formats = [f['format'] for f in info['formats']]
#                 return formats
#         except Exception as e:
#             print(f"Formatlar alınırken hata oluştu: {e}")
#             return []

#     def download_audio_only(self, url, file_name="audio"):
#         """
#         Yalnızca ses indirir.
#         """
#         file_name = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{file_name}"
#         try:
#             ydl_opts = {
#                 'format': 'bestaudio/best',
#                 'outtmpl': os.path.join(self.downloads_folder, file_name),
#                 'postprocessors': [{
#                     'key': 'FFmpegExtractAudio',
#                     'preferredcodec': 'mp3',
#                     'preferredquality': '192',
#                 }]
#             }
#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 ydl.download([url])
#             print(f"Ses başarıyla indirildi: {file_name}")
#         except Exception as e:
#             print(f"Ses indirme sırasında hata oluştu: {e}")

#     def download_video(self, url, quality="best", output_format="mp4"):
#         """
#         Video indirir.
#         """
#         try:
#             ydl_opts = {
#                 'format': f'{quality}+bestaudio/best',
#                 'outtmpl': os.path.join(self.downloads_folder, '%(title)s.%(ext)s'),
#                 'postprocessors': []
#             }

#             if output_format == "mp3":
#                 ydl_opts['postprocessors'].append({
#                     'key': 'FFmpegExtractAudio',
#                     'preferredcodec': 'mp3',
#                     'preferredquality': '192',
#                 })
#             elif output_format == "mp4":
#                 ydl_opts['postprocessors'].append({
#                     'key': 'FFmpegVideoConvertor',
#                     'preferedformat': 'mp4',
#                 })

#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 ydl.download([url])
#             print(f"{output_format.upper()} formatında dosya başarıyla indirildi.")
#         except Exception as e:
#             print(f"Video indirme sırasında hata oluştu: {e}")


# # Örnek kullanım
# # if __name__ == "__main__":
# #     downloader = TwitDownloader()
# #     url = input("Twitter video linkini girin: ").strip()
# #     quality = input("Kaliteyi girin (best, 360, 720, 1080): ").strip() or "best"
# #     output_format = input("Çıkış formatını seçin (mp3/mp4): ").strip().lower() or "mp4"

# #     if output_format not in ["mp3", "mp4"]:
# #         print("Geçersiz format seçimi! Lütfen 'mp3' veya 'mp4' giriniz.")
# #     else:
# #         if output_format == "mp3":
# #             downloader.download_audio_only(url)
# #         else:
# #             downloader.download_video(url, quality, output_format)
