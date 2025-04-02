
import sys
from PyQt5 import QtWidgets
from instagramFiles.instagramDownloadForm import Ui_InstagramLoader

class InstagramDownloadForm(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_InstagramLoader()
        self.ui.setupUi(self)
        self.parent = parent  

    def closeEvent(self, event):
        if self.parent:
            self.parent.show()
        event.accept() 