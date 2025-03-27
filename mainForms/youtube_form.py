from youtubeFiles.youtubeDownloadForm import Ui_MainWindow
import sys
from PyQt5 import QtWidgets

class YoutubeDownloadForm(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.parent = parent  

    def closeEvent(self, event):
        
        if self.parent:
            self.parent.show()
        event.accept()  