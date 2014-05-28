from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL, Qt, QDir
from PyQt4.QtGui import *
import sys
from works.Scrapper import Scrapper

import xlrd

__author__ = 'Rabbi'


class Form(QMainWindow):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.createGui()
        self.fileName = None
        self.urlList = []

    def createGui(self):
        self.labelFile = QLabel('<font size=15><b>Select File with url list: </b></font>')
        self.btnBrowse = QPushButton('&Browse')
        self.btnBrowse.clicked.connect(self.urlListSelected)
        self.btnScrap = QPushButton('&Scrap Data')
        self.btnScrap.clicked.connect(self.scrapAction)

        layout = QHBoxLayout()
        layout.addWidget(self.labelFile)
        layout.addWidget(self.btnBrowse)
        layout.addWidget(self.btnScrap)

        self.browser = QTextBrowser()
        layoutMain = QVBoxLayout()
        layoutMain.addLayout(layout)
        layoutMain.addWidget(self.browser)
        widget = QWidget()
        widget.setLayout(layoutMain)

        self.setCentralWidget(widget)
        screen = QDesktopWidget().screenGeometry()
        self.resize(screen.width() - 300, screen.height() - 300)
        self.setWindowTitle('Scrapper')
        self.scrapper = None

    def scrapAction(self):
        try:
            self.scrapper = Scrapper(self.urlList)
            self.scrapper.start()
            self.scrapper.notifyScrapper.connect(self.notifyInfo)
        except Exception, x:
            print x

    def urlListSelected(self):
        self.fileName = QtGui.QFileDialog.getOpenFileName(self, "Select Text File", QDir.homePath() + "/Desktop")
        ## just for test
        x1 = xlrd.open_workbook(self.fileName, encoding_override="utf_16_le")
        sheet = x1.sheet_by_index(0)
        rn = sheet.nrows
        for i in range(rn):
            print sheet.cell_value(i, 0)
        ## endtest
        f = open(self.fileName, 'rb')
        self.lists = f.readlines()
        f.close()
        if self.lists is not None:
            for line in self.lists:
                self.urlList.append(line)

    def notifyInfo(self, data):
        try:
            self.browser.document().setMaximumBlockCount(1000)
            self.browser.append(data)
        except Exception, x:
            print x.message


class MainView:
    def __init__(self):
        pass

    def showMainView(self):
        app = QApplication(sys.argv)
        form = Form()
        form.show()
        sys.exit(app.exec_())
