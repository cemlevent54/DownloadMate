import sys
from PyQt5 import QtWidgets

from mainFiles.mainForm import Ui_DownloadMate
from mainForms.youtube_form import YoutubeDownloadForm
from mainForms.twitter_form import TwitterDownloadForm
from mainForms.instagram_form import InstagramDownloadForm


class MainForm(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DownloadMate()
        self.ui.setupUi(self)

        
        self.ui.youtubeDownloader.clicked.connect(self.openYoutubeDownloadForm)
        self.ui.twitterDownloader.clicked.connect(self.openTwitterDownloadForm)
        self.ui.instagramDownloader.clicked.connect(self.openInstagramDownloadForm)
        
        
    def openYoutubeDownloadForm(self):
        
        self.youtubeDownloadForm = YoutubeDownloadForm(self)
        self.youtubeDownloadForm.show()
        self.hide()  
    
    def openInstagramDownloadForm(self):
        
        self.instagramDownloadForm = InstagramDownloadForm(self)
        self.instagramDownloadForm.show()
        self.hide()
    
    def openTwitterDownloadForm(self):
        
        self.twitterDownloadForm = TwitterDownloadForm(self)
        self.twitterDownloadForm.show()
        self.hide()



 


        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainForm = MainForm()
    mainForm.show()
    sys.exit(app.exec_())
