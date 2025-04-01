from PyQt5 import QtWidgets
import os, re
from urllib.parse import urlparse, parse_qs  # EKLENDİ
from .downloader import YouTubeDownloader

class YouTubeFormController:
    def __init__(self, ui):
        self.ui = ui
        self.downloader = YouTubeDownloader()
        self.connect_signals()

    def connect_signals(self):
        self.ui.searchButton.clicked.connect(self.download_video)
        self.ui.downloadsFolderButton.clicked.connect(self.open_downloads_folder)

    def get_selected_format(self):
        return "mp3" if self.ui.mp3Radio.isChecked() else "mp4"

    def get_selected_quality(self):
        if self.ui.radio360p.isChecked():
            return "134"
        elif self.ui.radio480p.isChecked():
            return "135"
        elif self.ui.radio720p.isChecked():
            return "136"
        elif self.ui.radio1080p.isChecked():
            return "137"
        return None

    # 🔧 EKLENEN TEMİZLEME FONKSİYONU
    def normalize_youtube_url(self, url: str) -> str:
        parsed_url = urlparse(url)
        query = parse_qs(parsed_url.query)
        video_id = query.get("v")
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id[0]}"
        return url

    def download_video(self):
        raw_url = self.ui.linkTxtBox.text().strip()
        if not raw_url:
            return self.show_error("Lütfen bir URL girin!")

        # 👇 Burada URL'yi normalize ediyoruz
        url = self.normalize_youtube_url(raw_url)

        if not re.match(r"^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})$", url):
            return self.show_error("Lütfen geçerli bir YouTube bağlantısı girin!")

        format_choice = self.get_selected_format()
        quality_choice = self.get_selected_quality()

        try:
            title = self.downloader.sanitize_and_get_title(url)
            quality_map = {
                "134": "360p", "135": "480p", "136": "720p", "137": "1080p"
            }
            file_name = f"{title}_{format_choice}_{quality_map.get(quality_choice, 'default')}"

            if format_choice == "mp3":
                self.downloader.download_audio_only(url, file_name)
                self.show_info("Ses başarıyla indirildi!")
            elif format_choice == "mp4" and quality_choice:
                v, a, out = self.downloader.download_video_and_audio(url, quality_choice, file_name)
                self.show_info("Video başarıyla indirildi!")
            else:
                self.show_error("Lütfen geçerli bir kalite seçin!")

            self.reset_form()
        except Exception as e:
            self.show_error(f"Bir hata oluştu: {e}")

    def open_downloads_folder(self):
        folder = self.downloader.download_folder
        if not os.path.exists(folder):
            os.makedirs(folder)
        os.startfile(folder)

    def reset_form(self):
        self.ui.linkTxtBox.clear()
        for btn in [
            self.ui.mp3Radio, self.ui.mp4Radio,
            self.ui.radio360p, self.ui.radio480p,
            self.ui.radio720p, self.ui.radio1080p
        ]:
            btn.setAutoExclusive(False)
            btn.setChecked(False)
            btn.setAutoExclusive(True)

    def show_error(self, message):
        QtWidgets.QMessageBox.warning(None, "Hata", message)

    def show_info(self, message):
        QtWidgets.QMessageBox.information(None, "Bilgi", message)
