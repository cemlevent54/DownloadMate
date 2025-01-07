import sys
from PyQt5 import QtWidgets

from mainFiles.mainForm import Ui_DownloadMate
from youtubeFiles.youtubeDownloadForm import Ui_MainWindow
from twitterFiles.twitterDownloadForm import Ui_TwitterDownloader
from instagramFiles.instagramDownloadForm import Ui_InstagramLoader


class MainForm(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DownloadMate()
        self.ui.setupUi(self)

        # YouTube Downloader butonuna tıklama olayını tanımlıyoruz.
        self.ui.youtubeDownloader.clicked.connect(self.openYoutubeDownloadForm)
        self.ui.twitterDownloader.clicked.connect(self.openTwitterDownloadForm)
        self.ui.instagramDownloader.clicked.connect(self.openInstagramDownloadForm)
        
        
    def openYoutubeDownloadForm(self):
        # YouTube Download Form'u aç ve MainForm'u kapat
        self.youtubeDownloadForm = YoutubeDownloadForm(self)
        self.youtubeDownloadForm.show()
        self.hide()  # MainForm'u kapatmak yerine gizliyoruz
    
    def openInstagramDownloadForm(self):
        # Instagram Download Form'u aç ve MainForm'u kapat
        self.instagramDownloadForm = InstagramDownloadForm(self)
        self.instagramDownloadForm.show()
        self.hide()
    
    def openTwitterDownloadForm(self):
        # Twitter Download Form'u aç ve MainForm'u kapat
        self.twitterDownloadForm = TwitterDownloadForm(self)
        self.twitterDownloadForm.show()
        self.hide()


class YoutubeDownloadForm(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.parent = parent  # MainForm'u referans olarak alıyoruz

    def closeEvent(self, event):
        # YoutubeDownloadForm kapanırken MainForm'u tekrar gösteriyoruz
        if self.parent:
            self.parent.show()
        event.accept()  # Kapatma olayını kabul ediyoruz

class InstagramDownloadForm(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_InstagramLoader()
        self.ui.setupUi(self)
        self.parent = parent  # MainForm'u referans olarak alıyoruz

    def closeEvent(self, event):
        # InstagramDownloadForm kapanırken MainForm'u tekrar gösteriyoruz
        if self.parent:
            self.parent.show()
        event.accept()  # Kapatma olayını kabul ediyoruz

class TwitterDownloadForm(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_TwitterDownloader()
        self.ui.setupUi(self)
        self.parent = parent  # MainForm'u referans olarak alıyoruz

    def closeEvent(self, event):
        # TwitterDownloadForm kapanırken MainForm'u tekrar gösteriyoruz
        if self.parent:
            self.parent.show()
        event.accept()  # Kapatma olayını kabul ediyoruz
        




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainForm = MainForm()
    mainForm.show()
    sys.exit(app.exec_())
