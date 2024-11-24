import sys
from PyQt5 import QtWidgets
from mainFiles.mainForm import Ui_DownloadMate
from youtubeFiles.youtubeDownloadForm import Ui_MainWindow


class MainForm(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DownloadMate()
        self.ui.setupUi(self)

        # YouTube Downloader butonuna tıklama olayını tanımlıyoruz.
        self.ui.youtubeDownloader.clicked.connect(self.openYoutubeDownloadForm)

    def openYoutubeDownloadForm(self):
        # YouTube Download Form'u aç ve MainForm'u kapat
        self.youtubeDownloadForm = YoutubeDownloadForm(self)
        self.youtubeDownloadForm.show()
        self.hide()  # MainForm'u kapatmak yerine gizliyoruz


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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainForm = MainForm()
    mainForm.show()
    sys.exit(app.exec_())
