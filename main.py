from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QLabel, QVBoxLayout
from tkinter import filedialog
from tkinter import *

import webhdfs
import sys

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.ip_input = QtWidgets.QTextEdit(Dialog)
        self.ip_input.setGeometry(QtCore.QRect(250, 20, 111, 31))
        self.ip_input.setObjectName("ip_input")
        self.port_input = QtWidgets.QTextEdit(Dialog)
        self.port_input.setGeometry(QtCore.QRect(250, 70, 111, 31))
        self.port_input.setObjectName("port_input")
        self.ip_address_display = QtWidgets.QTextBrowser(Dialog)
        self.ip_address_display.setGeometry(QtCore.QRect(120, 20, 101, 31))
        self.ip_address_display.setObjectName("ip_address_display")
        self.port_display = QtWidgets.QTextBrowser(Dialog)
        self.port_display.setGeometry(QtCore.QRect(120, 70, 101, 31))
        self.port_display.setObjectName("port_display")
        self.upload_button = QtWidgets.QPushButton(Dialog)
        self.upload_button.setGeometry(QtCore.QRect(270, 250, 93, 28))
        self.upload_button.setObjectName("upload_button")
        self.upload_button.clicked.connect(self.upload_file)
        self.user_display = QtWidgets.QTextBrowser(Dialog)
        self.user_display.setGeometry(QtCore.QRect(120, 120, 101, 31))
        self.user_display.setObjectName("user_display")
        self.user_input = QtWidgets.QTextEdit(Dialog)
        self.user_input.setGeometry(QtCore.QRect(250, 120, 111, 31))
        self.user_input.setObjectName("user_input")
        self.file_open_button = QtWidgets.QPushButton(Dialog)
        self.file_open_button.setGeometry(QtCore.QRect(10, 190, 93, 28))
        self.file_open_button.setObjectName("file_open_button")
        self.file_open_button.clicked.connect(self.clicked)
        self.label = QLabel()
        layout = QVBoxLayout()
        layout.addWidget(self.file_open_button)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.File_directory_display = QtWidgets.QTextBrowser(Dialog)
        self.File_directory_display.setGeometry(QtCore.QRect(140, 190, 241, 31))
        self.File_directory_display.setObjectName("File_directory_display")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.ip_address_display.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">IP Address</p></body></html>"))
        self.port_display.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Port</p></body></html>"))
        self.upload_button.setText(_translate("Dialog", "Upload"))
        self.user_display.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">User</p></body></html>"))
        self.file_open_button.setText(_translate("Dialog", "File Open"))
        self.File_directory_display.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Directory</p></body></html>"))

    def upload_file(self, Dialog):
        ip_address = self.ip_input.toPlainText()
        port_number = self.port_input.toPlainText()
        user_name = self.user_input.toPlainText()

        host_address='http://'+ip_address+':'+port_number
        webhdfs.upload_to_hdfs(host_address,user_name)

    def openfile(self):
        root = Tk()
        # root.title("Downloader")
        # root.geometry("540x300+100+100")
        # root.resizable(False, False)
        root.file = filedialog.askopenfile(initialdir='',title='select file', filetypes=(('image files', '*.dd'), ('all files','*.*')))
        print (root.dirName)

        root.mainloop()
    def clicked(self):
        fname = QFileDialog.getOpenFileName(self)
        self.File_directory_display.setText(fname[0])

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())


