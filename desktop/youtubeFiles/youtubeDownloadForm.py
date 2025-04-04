# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'youtubeDownloadForm.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from youtubeFiles.youtubeDownloader import YouTubeDownloader
from .form_controller import YouTubeFormController
import os
import platform
import re

# youtube download form
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Youtube Downloader")
        MainWindow.resize(800, 600)
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        MainWindow.setStyleSheet("QMainWindow {background-color: #CD201F;}")
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Header label
        self.headerLabel = QtWidgets.QLabel(self.centralwidget)
        self.headerLabel.setGeometry(QtCore.QRect(270, 70, 271, 81))
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        font.setPointSize(10)
        self.headerLabel.setFont(font)
        self.headerLabel.setStyleSheet("QLabel {color: white;font-weight: 900;\n"
"};")
        self.headerLabel.setObjectName("headerLabel")
        
        # Link text box
        self.linkTxtBox = QtWidgets.QLineEdit(self.centralwidget)
        self.linkTxtBox.setGeometry(QtCore.QRect(50, 150, 551, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setFamily("Rockwell")
        self.linkTxtBox.setFont(font)
        self.linkTxtBox.setObjectName("linkTxtBox")
        
        # Format group box
        self.formatGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.formatGroupBox.setGeometry(QtCore.QRect(40, 230, 171, 161))
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        self.formatGroupBox.setFont(font)
        self.formatGroupBox.setStyleSheet("color: white;font-weight: 900;\n"
"")
        self.formatGroupBox.setObjectName("formatGroupBox")
        
        # Format group box - mp4 radio button
        self.mp4Radio = QtWidgets.QRadioButton(self.formatGroupBox)
        self.mp4Radio.setGeometry(QtCore.QRect(20, 80, 141, 20))
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        self.mp4Radio.setFont(font)
        self.mp4Radio.setObjectName("mp4Radio")
        self.mp4Radio.setStyleSheet("color: white;font-weight: 900;")
        self.mp4Radio.setChecked(False)
        
        # Format group box - mp3 radio button
        self.mp3Radio = QtWidgets.QRadioButton(self.formatGroupBox)
        self.mp3Radio.setGeometry(QtCore.QRect(20, 40, 141, 20))
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        self.mp3Radio.setFont(font)
        self.mp3Radio.setObjectName("mp3Radio")
        self.mp3Radio.setStyleSheet("color: white;font-weight: 900;")
        self.mp3Radio.setChecked(False)
        
        # Search button
        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchButton.setGeometry(QtCore.QRect(630, 150, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.searchButton.setFont(font)
        self.searchButton.setStyleSheet("QPushButton {\n"
"                background-color: #FFFFFF; /* Beyaz arka plan */\n"
"                color: #CD201F; /* Kırmızı yazı */\n"
"                font-size: 14px;\n"
"                font-weight: bold;\n"
"                border: 2px solid #CD201F; /* Kırmızı kenar */\n"
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
        
        # Quality group box
        self.qualityGroupbox = QtWidgets.QGroupBox(self.centralwidget)
        self.qualityGroupbox.setGeometry(QtCore.QRect(250, 230, 201, 221))
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        self.qualityGroupbox.setFont(font)
        self.qualityGroupbox.setStyleSheet("color: white;font-weight: 900;\n")
        self.qualityGroupbox.setObjectName("qualityGroupbox")
        
        # Quality Radio Buttons (360p)
        self.radio360p = QtWidgets.QRadioButton(self.qualityGroupbox)
        self.radio360p.setGeometry(QtCore.QRect(40, 80, 141, 20))
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        self.radio360p.setFont(font)
        self.radio360p.setObjectName("radio360p")
        self.radio360p.setStyleSheet("color: white;font-weight: 900;")
        self.radio360p.setChecked(False)
        
        # Quality Radio Buttons (480p)
        self.radio480p = QtWidgets.QRadioButton(self.qualityGroupbox)
        self.radio480p.setGeometry(QtCore.QRect(40, 40, 141, 20))
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        self.radio480p.setFont(font)
        self.radio480p.setObjectName("radio480p")
        self.radio480p.setStyleSheet("color: white;font-weight: 900;")
        self.radio480p.setChecked(False)        
        
        # Quality Radio Buttons (720p)
        self.radio720p = QtWidgets.QRadioButton(self.qualityGroupbox)
        self.radio720p.setGeometry(QtCore.QRect(40, 120, 141, 20))
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        self.radio720p.setFont(font)
        self.radio720p.setObjectName("radio720p")
        self.radio720p.setStyleSheet("color: white;font-weight: 900;")
        self.radio720p.setChecked(False)
        
        # Quality Radio Buttons (1080p)
        self.radio1080p = QtWidgets.QRadioButton(self.qualityGroupbox)
        self.radio1080p.setGeometry(QtCore.QRect(40, 160, 141, 20))
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        self.radio1080p.setFont(font)
        self.radio1080p.setObjectName("radio1080p")
        self.radio1080p.setStyleSheet("color: white;font-weight: 900;")
        self.radio1080p.setChecked(False)
        
        # Downloads label
        self.downloadsFolderButton = QtWidgets.QPushButton(self.centralwidget)
        self.downloadsFolderButton.setGeometry(QtCore.QRect(630, 400, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.downloadsFolderButton.setFont(font)
        self.downloadsFolderButton.setStyleSheet("QPushButton {\n"
"                background-color: #FFFFFF; /* Beyaz arka plan */\n"
"                color: #CD201F; /* Kırmızı yazı */\n"
"                font-size: 14px;\n"
"                font-weight: bold;\n"
"                border: 2px solid #CD201F; /* Kırmızı kenar */\n"
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
        self.downloadsFolderButton.setObjectName("downloadsFolderButton")
        # self.downloadsFolderButton.clicked.connect(self.open_downloads_folder)
        
        # Result label
        self.resultLabel = QtWidgets.QLabel(self.centralwidget)
        self.resultLabel.setGeometry(QtCore.QRect(580, 240, 151, 81))
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        self.resultLabel.setFont(font)
        self.resultLabel.setText("")
        self.resultLabel.setObjectName("resultLabel")
        
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        # connect the search button to the search function
        self.youtube_controller = YouTubeFormController(self)
        self.youtube_downloader = YouTubeDownloader()
        # self.searchButton.clicked.connect(self.download_video)
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "🔴 Youtube Downloader"))
        self.headerLabel.setText(_translate("MainWindow", "Download Youtube Videos"))
        self.formatGroupBox.setTitle(_translate("MainWindow", "Format"))
        self.mp4Radio.setText(_translate("MainWindow", "mp4"))
        self.mp3Radio.setText(_translate("MainWindow", "mp3"))
        self.searchButton.setText(_translate("MainWindow", "Download"))
        self.qualityGroupbox.setTitle(_translate("MainWindow", "Quality"))
        self.radio360p.setText(_translate("MainWindow", "480p"))
        self.radio480p.setText(_translate("MainWindow", "360p"))
        self.radio720p.setText(_translate("MainWindow", "720p"))
        self.radio1080p.setText(_translate("MainWindow", "1080p"))
        self.downloadsFolderButton.setText(_translate("MainWindow", "Downloads"))
    
    