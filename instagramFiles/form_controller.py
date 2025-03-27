# instagramFiles/form_controller.py

import datetime
import os
import re
from PyQt5 import QtWidgets
from .downloader import InstagramDownloader

class InstagramFormController:
    def __init__(self, ui):
        self.ui = ui
        self.downloader = InstagramDownloader()
        self.setup_connections()

    def setup_connections(self):
        self.ui.searchButton.clicked.connect(self.download_video)
        self.ui.downloadsButton.clicked.connect(self.open_downloads_folder)

    def download_video(self):
        url = self.ui.linkTxtBox.text().strip()
        if not url:
            QtWidgets.QMessageBox.warning(None, "Hata", "Lütfen bir link girin.")
            return

        instagram_url_pattern = re.compile(
            r"^(https?:\/\/)?(www\.)?(instagram\.com|instagr\.am)\/p\/[a-zA-Z0-9_-]+\/?$"
        )
        if not instagram_url_pattern.match(url):
            QtWidgets.QMessageBox.warning(None, "Hata", "Lütfen geçerli bir Instagram bağlantısı girin!")
            return

        try:
            timestamp = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
            title = self.downloader.sanitize_and_get_title(url)
            filename = f"{timestamp}_{title}"
            result_path = self.downloader.download_video(url, filename)

            
            if result_path and os.path.exists(result_path):
                QtWidgets.QMessageBox.information(None, "Başarılı", f"İndirilen dosya:\n{os.path.basename(result_path)}")
            else:
                QtWidgets.QMessageBox.warning(None, "Hata", "Video indirilemedi.")

            self.ui.linkTxtBox.clear()
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Hata", f"İndirme sırasında hata oluştu:\n{e}")
            self.ui.linkTxtBox.clear()

    def open_downloads_folder(self):
        folder = self.downloader.download_folder
        if not os.path.exists(folder):
            os.makedirs(folder)
        os.startfile(folder)
