from twitterFiles.twitterDownloadForm import Ui_TwitterDownloader
import sys
from PyQt5 import QtWidgets

class TwitterDownloadForm(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_TwitterDownloader()
        self.ui.setupUi(self)
        self.parent = parent  

    def closeEvent(self, event):
        if self.parent:
            self.parent.show()
        event.accept()  