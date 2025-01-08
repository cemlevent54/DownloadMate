# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'twitterDownloadForm.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from twitterFiles.twitterDownloader import TwitDownloader
import os
import re


class Ui_TwitterDownloader(object):
    def setupUi(self, TwitterDownloader):
        TwitterDownloader.setObjectName("TwitterDownloader")
        TwitterDownloader.resize(800, 592)
        TwitterDownloader.setMaximumSize(QtCore.QSize(800, 600))
        TwitterDownloader.setStyleSheet("QMainWindow {background-color: #1DA1F2;}")
        self.centralwidget = QtWidgets.QWidget(TwitterDownloader)
        self.centralwidget.setObjectName("centralwidget")
        
        # Quality Selection Groupbox
        self.qualityGroupbox = QtWidgets.QGroupBox(self.centralwidget)
        self.qualityGroupbox.setGeometry(QtCore.QRect(250, 240, 201, 221))
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        font.setBold(True)
        font.setWeight(99)
        self.qualityGroupbox.setFont(font)
        self.qualityGroupbox.setStyleSheet("color: white;font-weight: 900;")
        self.qualityGroupbox.setObjectName("qualityGroupbox")
        
        # Quality Selection Radio Buttons
        self.quality480p = QtWidgets.QRadioButton(self.qualityGroupbox)
        self.quality480p.setGeometry(QtCore.QRect(40, 80, 141, 20))
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        font.setBold(True)
        font.setWeight(99)
        self.quality480p.setFont(font)
        self.quality480p.setStyleSheet("color: white;font-weight: 900;")
        self.quality480p.setObjectName("quality480p")
        self.quality480p.setChecked(False)
        
        
        self.quality360p = QtWidgets.QRadioButton(self.qualityGroupbox)
        self.quality360p.setGeometry(QtCore.QRect(40, 40, 141, 20))
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        font.setBold(True)
        font.setWeight(99)
        self.quality360p.setFont(font)
        self.quality360p.setStyleSheet("color: white;font-weight: 900;")
        self.quality360p.setObjectName("quality360p")
        self.quality360p.setChecked(False)
        
        self.quality720p = QtWidgets.QRadioButton(self.qualityGroupbox)
        self.quality720p.setGeometry(QtCore.QRect(40, 120, 141, 20))
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        font.setBold(True)
        font.setWeight(99)
        self.quality720p.setFont(font)
        self.quality720p.setStyleSheet("color: white;font-weight: 900;")
        self.quality720p.setObjectName("quality720p")
        self.quality720p.setChecked(False)
        
        self.quality1080p = QtWidgets.QRadioButton(self.qualityGroupbox)
        self.quality1080p.setGeometry(QtCore.QRect(40, 160, 141, 20))
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        font.setBold(True)
        font.setWeight(99)
        self.quality1080p.setFont(font)
        self.quality1080p.setStyleSheet("color: white;font-weight: 900;")
        self.quality1080p.setObjectName("quality1080p")
        self.quality1080p.setChecked(False)
        
        # Link Textbox
        self.linkTxtBox = QtWidgets.QLineEdit(self.centralwidget)
        self.linkTxtBox.setGeometry(QtCore.QRect(30, 160, 551, 41))
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.linkTxtBox.setFont(font)
        self.linkTxtBox.setObjectName("linkTxtBox")
        
        # Format Selection Groupbox
        self.formatGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.formatGroupBox.setGeometry(QtCore.QRect(40, 240, 171, 161))
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        font.setBold(True)
        font.setWeight(99)
        self.formatGroupBox.setFont(font)
        self.formatGroupBox.setStyleSheet("color: white;font-weight: 900;\n"
"")
        self.formatGroupBox.setObjectName("formatGroupBox")
        
        # Format Selection Radio Buttons
        self.mp4Radio = QtWidgets.QRadioButton(self.formatGroupBox)
        self.mp4Radio.setGeometry(QtCore.QRect(20, 80, 141, 20))
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        font.setBold(True)
        font.setWeight(99)
        self.mp4Radio.setFont(font)
        self.mp4Radio.setStyleSheet("color: white;font-weight: 900;")
        self.mp4Radio.setObjectName("mp4Radio")
        self.mp4Radio.setChecked(False)
        
        self.mp3Radio = QtWidgets.QRadioButton(self.formatGroupBox)
        self.mp3Radio.setGeometry(QtCore.QRect(20, 40, 141, 20))
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        font.setBold(True)
        font.setWeight(99)
        self.mp3Radio.setFont(font)
        self.mp3Radio.setStyleSheet("color: white;font-weight: 900;")
        self.mp3Radio.setObjectName("mp3Radio")
        self.mp3Radio.setChecked(False)
        
        self.downloadsButton = QtWidgets.QPushButton(self.centralwidget)
        self.downloadsButton.setGeometry(QtCore.QRect(620, 410, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.downloadsButton.setFont(font)
        self.downloadsButton.setStyleSheet("QPushButton {\n"
"                background-color: #FFFFFF; /* Beyaz arka plan */\n"
"                color: #1DA1F2; /* Kırmızı yazı */\n"
"                font-size: 14px;\n"
"                font-weight: bold;\n"
"                border: 2px solid #1DA1F2; /* Kırmızı kenar */\n"
"                border-radius: 8px; /* Hafif yuvarlak kenarlar */\n"
"                padding: 6px;\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #657786; /* Hover sırasında açık kırmızı */\n"
"                color: #FFFFFF; /* Yazı beyaz */\n"
"                border: 2px solid #383838;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #657786; /* Basılınca koyu kırmızı */\n"
"                color: #FFFFFF;\n"
"            }")
        self.downloadsButton.setObjectName("downloadsButton")
        
        # Search and Download Button
        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchButton.setGeometry(QtCore.QRect(590, 160, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.searchButton.setFont(font)
        self.searchButton.setStyleSheet("QPushButton {\n"
"                background-color: #FFFFFF; /* Beyaz arka plan */\n"
"                color: #1DA1F2; /* Kırmızı yazı */\n"
"                font-size: 14px;\n"
"                font-weight: bold;\n"
"                border: 2px solid #1DA1F2; /* Kırmızı kenar */\n"
"                border-radius: 8px; /* Hafif yuvarlak kenarlar */\n"
"                padding: 6px;\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #657786; /* Hover sırasında açık kırmızı */\n"
"                color: #FFFFFF; /* Yazı beyaz */\n"
"                border: 2px solid #383838;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #657786; /* Basılınca koyu kırmızı */\n"
"                color: #FFFFFF;\n"
"            }")
        self.searchButton.setObjectName("searchButton")
        
        # Header Label
        self.headerLabel = QtWidgets.QLabel(self.centralwidget)
        self.headerLabel.setGeometry(QtCore.QRect(260, 70, 311, 81))
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(99)
        self.headerLabel.setFont(font)
        self.headerLabel.setStyleSheet("QLabel {color: white;font-weight: 900;\n"
"};")
        self.headerLabel.setObjectName("headerLabel")
        TwitterDownloader.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(TwitterDownloader)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        TwitterDownloader.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(TwitterDownloader)
        self.statusbar.setObjectName("statusbar")
        TwitterDownloader.setStatusBar(self.statusbar)

        self.retranslateUi(TwitterDownloader)
        QtCore.QMetaObject.connectSlotsByName(TwitterDownloader)
        
        self.twitter_downloader = TwitDownloader()
        self.searchButton.clicked.connect(self.download_video)
        self.downloadsButton.clicked.connect(self.open_downloads_folder)

    def retranslateUi(self, TwitterDownloader):
        _translate = QtCore.QCoreApplication.translate
        TwitterDownloader.setWindowTitle(_translate("TwitterDownloader", "Twitter Downloader"))
        self.qualityGroupbox.setTitle(_translate("TwitterDownloader", "Quality"))
        self.quality480p.setText(_translate("TwitterDownloader", "480p"))
        self.quality360p.setText(_translate("TwitterDownloader", "360p"))
        self.quality720p.setText(_translate("TwitterDownloader", "720p"))
        self.quality1080p.setText(_translate("TwitterDownloader", "1080p"))
        self.formatGroupBox.setTitle(_translate("TwitterDownloader", "Format"))
        self.mp4Radio.setText(_translate("TwitterDownloader", "mp4"))
        self.mp3Radio.setText(_translate("TwitterDownloader", "mp3"))
        self.downloadsButton.setText(_translate("TwitterDownloader", "Downloads"))
        self.searchButton.setText(_translate("TwitterDownloader", "Search and Download"))
        self.headerLabel.setText(_translate("TwitterDownloader", "Download Twitter(X) Videos"))
    
    def get_selected_format(self):
        return "mp3" if self.mp3Radio.isChecked() else "mp4"
    
    def get_selected_quality(self):
        if self.quality360p.isChecked():
            return "360"
        elif self.quality480p.isChecked():
            return "480"
        elif self.quality720p.isChecked():
            return "720"
        elif self.quality1080p.isChecked():
            return "1080"
        return "best"
    
    def download_video(self):
        video_url = self.linkTxtBox.text().strip()
        if not video_url:
            QtWidgets.QMessageBox.warning(None, "Hata", "Lütfen bir URL girin!")
            return
        
        twitter_url_pattern = re.compile(
            r"^(https?:\/\/)?(www\.)?(twitter\.com|x\.com)\/([a-zA-Z0-9_]+)\/status\/([0-9]+)$"
        )
        if not twitter_url_pattern.match(video_url):
            QtWidgets.QMessageBox.warning(None, "Hata", "Lütfen geçerli bir Twitter bağlantısı girin!")
            return
        
        format_choice = self.get_selected_format()
        quality_choice = self.get_selected_quality()
        
        try:
           if format_choice == "mp3":
               self.twitter_downloader.download_audio_only(video_url)
               QtWidgets.QMessageBox.information(None, "Başarılı", "Ses başarıyla indirildi!")
           elif format_choice == "mp4" and quality_choice:
               self.twitter_downloader.download_video(video_url, quality_choice)
               QtWidgets.QMessageBox.information(None, "Başarılı", "Video başarıyla indirildi!")
           
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Hata", f"İndirme sırasında hata oluştu: {e}")
            
        self.reset_form()
        self.mp4Radio.setChecked(False)
            
    def reset_form(self):
        """
        Formdaki tüm alanları sıfırlar.
        """
        # TextBox'u temizle
        self.linkTxtBox.clear()

        # Format radio button'larını sıfırla
        self.mp3Radio.setAutoExclusive(False)
        self.mp4Radio.setAutoExclusive(False)
        self.mp3Radio.setChecked(False)
        self.mp4Radio.setChecked(False)
        self.mp3Radio.setAutoExclusive(True)
        self.mp4Radio.setAutoExclusive(True)

        # Quality radio button'larını sıfırla
        self.quality360p.setAutoExclusive(False)
        self.quality480p.setAutoExclusive(False)
        self.quality720p.setAutoExclusive(False)
        self.quality1080p.setAutoExclusive(False)
        self.quality360p.setChecked(False)
        self.quality480p.setChecked(False)
        self.quality720p.setChecked(False)
        self.quality1080p.setChecked(False)
        self.quality360p.setAutoExclusive(True)
        self.quality480p.setAutoExclusive(True)
        self.quality720p.setAutoExclusive(True)
        self.quality1080p.setAutoExclusive(True)
    
    def open_downloads_folder(self):
        """
        Open the downloads folder
        """
        downloads_folder = self.twitter_downloader.downloads_folder
        if not os.path.exists(downloads_folder):
           os.makedirs(downloads_folder)
        
        os.startfile(downloads_folder)   
     
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     TwitterDownloader = QtWidgets.QMainWindow()
#     ui = Ui_TwitterDownloader()
#     ui.setupUi(TwitterDownloader)
#     TwitterDownloader.show()
#     sys.exit(app.exec_())
