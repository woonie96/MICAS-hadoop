from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QLabel, QVBoxLayout

import logging

from hdfs import InsecureClient
import sys
logging.basicConfig(level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(name='maibn')

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ip_displqy = QtWidgets.QTextBrowser(self.centralwidget)
        self.ip_displqy.setGeometry(QtCore.QRect(30, 30, 111, 31))
        self.ip_displqy.setObjectName("ip_displqy")
        self.port_display = QtWidgets.QTextBrowser(self.centralwidget)
        self.port_display.setGeometry(QtCore.QRect(30, 80, 111, 31))
        self.port_display.setObjectName("port_display")
        self.user_display = QtWidgets.QTextBrowser(self.centralwidget)
        self.user_display.setGeometry(QtCore.QRect(30, 130, 111, 31))
        self.user_display.setObjectName("user_display")
        self.ip_input = QtWidgets.QTextEdit(self.centralwidget)
        self.ip_input.setGeometry(QtCore.QRect(190, 30, 171, 31))
        self.ip_input.setObjectName("ip_input")
        self.port_input = QtWidgets.QTextEdit(self.centralwidget)
        self.port_input.setGeometry(QtCore.QRect(190, 80, 171, 31))
        self.port_input.setObjectName("port_input")
        self.user_input = QtWidgets.QTextEdit(self.centralwidget)
        self.user_input.setGeometry(QtCore.QRect(190, 130, 171, 31))
        self.user_input.setObjectName("user_input")
        self.file_input = QtWidgets.QTextEdit(self.centralwidget)
        self.file_input.setGeometry(QtCore.QRect(190, 180, 501, 31))
        self.file_input.setObjectName("file_input")
        self.file_open_button = QtWidgets.QPushButton(self.centralwidget)
        self.file_open_button.setGeometry(QtCore.QRect(40, 180, 93, 28))
        self.file_open_button.setObjectName("file_open_button")
        self.upload_button = QtWidgets.QPushButton(self.centralwidget)
        self.file_open_button.clicked.connect(self.openFileNameDialog)
        self.upload_button.setGeometry(QtCore.QRect(660, 490, 93, 28))
        self.upload_button.setObjectName("upload_button")
        self.upload_button.clicked.connect(self.upload_file)

        self.mkdir_button = QtWidgets.QPushButton(self.centralwidget)
        self.mkdir_button.setGeometry(QtCore.QRect(40, 240, 111, 28))
        self.mkdir_button.setObjectName("mkdir_button")
        self.directory_input = QtWidgets.QTextEdit(self.centralwidget)
        self.directory_input.setGeometry(QtCore.QRect(190, 240, 251, 31))
        self.directory_input.setObjectName("directory_input")
        self.dir_input = QtWidgets.QTextEdit(self.centralwidget)
        self.dir_input.setGeometry(QtCore.QRect(590, 30, 171, 31))
        self.dir_input.setObjectName("dir_input")
        self.dir_display = QtWidgets.QTextBrowser(self.centralwidget)
        self.dir_display.setGeometry(QtCore.QRect(430, 30, 111, 31))
        self.dir_display.setObjectName("dir_display")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.ip_displqy.setHtml(_translate("MainWindow",
                                           "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                           "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                           "p, li { white-space: pre-wrap; }\n"
                                           "</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">IP Address</p></body></html>"))
        self.port_display.setHtml(_translate("MainWindow",
                                             "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                             "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                             "p, li { white-space: pre-wrap; }\n"
                                             "</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                             "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Port</p></body></html>"))
        self.user_display.setHtml(_translate("MainWindow",
                                             "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                             "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                             "p, li { white-space: pre-wrap; }\n"
                                             "</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                             "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Username</p></body></html>"))
        self.file_open_button.setText(_translate("MainWindow", "File Open"))
        self.upload_button.setText(_translate("MainWindow", "Upload"))
        self.mkdir_button.setText(_translate("MainWindow", "Make DIrectory"))
        self.dir_display.setHtml(_translate("MainWindow",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Upload dir</p></body></html>"))

    def upload_file(self):
        ip_address = self.ip_input.toPlainText()
        port_number = self.port_input.toPlainText()
        user_name = self.user_input.toPlainText()
        upload_file = self.dir_input.toPlainText()
        host_address = 'http://'+ip_address + ':' + port_number
        hadoop = InsecureClient(host_address,user_name)
        hadoop.upload('',upload_file)

    def openFileNameDialog(self):
        fname = QFileDialog.getOpenFileName(self)
        self.file_input.setText(fname[0])


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())



