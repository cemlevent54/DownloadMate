# twitterFiles/form_controller.py

import os
import re
from PyQt5 import QtWidgets
from .downloader import TwitterDownloader
import datetime

class TwitterFormController:
    def __init__(self, ui):
        self.ui = ui
        self.downloader = TwitterDownloader()
        self.setup_connections()

    def setup_connections(self):
        self.ui.searchButton.clicked.connect(self.download_video)
        self.ui.downloadsButton.clicked.connect(self.open_downloads_folder)

    def download_video(self):
        raw_url = self.ui.linkTxtBox.text().strip()

        if not raw_url:
            QtWidgets.QMessageBox.warning(None, "Hata", "Lütfen bir URL girin!")
            return

        url = self.normalize_twitter_url(raw_url)  # ✅ Normalleştirme burada

        twitter_url_pattern = re.compile(
            r"^(https?:\/\/)?(www\.)?(twitter\.com|x\.com)\/i\/status\/([0-9]+)$"
        )
        if not twitter_url_pattern.match(url):
            QtWidgets.QMessageBox.warning(None, "Hata", "Lütfen geçerli bir Twitter bağlantısı girin!")
            return

        format_choice = self.ui.get_selected_format()
        quality_choice = self.ui.get_selected_quality()

        try:
            if format_choice == "mp3":
                self.downloader.download_audio_only(url)
                QtWidgets.QMessageBox.information(None, "Başarılı", "Ses başarıyla indirildi!")
            else:
                self.downloader.download_video(url, quality_choice)
                QtWidgets.QMessageBox.information(None, "Başarılı", "Video başarıyla indirildi!")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Hata", f"İndirme sırasında hata oluştu:\n{e}")
        self.reset_form()

    def normalize_twitter_url(self, url: str) -> str:
        match = re.search(r"(?:twitter\.com|x\.com)/[^/]+/status/(\d+)", url)
        if match:
            tweet_id = match.group(1)
            return f"https://x.com/i/status/{tweet_id}"
        return url


    def reset_form(self):
        self.ui.linkTxtBox.clear()
        for btn in [self.ui.mp3Radio, self.ui.mp4Radio,
                    self.ui.quality360p, self.ui.quality480p,
                    self.ui.quality720p, self.ui.quality1080p]:
            btn.setAutoExclusive(False)
            btn.setChecked(False)
            btn.setAutoExclusive(True)

    def open_downloads_folder(self):
        folder = self.downloader.download_folder  # <-- Burada `downloads_folder` olarak düzeltildi
        if not os.path.exists(folder):
            os.makedirs(folder)
        os.startfile(folder)
