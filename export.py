from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pandas as pd
from os.path import exists

import config as c
import datatools


class ExportWindow(QWidget):

    def __init__(self):
        super().__init__()
        grid = QGridLayout()
        time = QDate.currentDate()

        self.namelb = QLabel('File name:')
        self.name = QLineEdit(time.toString(Qt.ISODate)+".csv")
        self.lab = QLabel('Save to:')
        self.dir = QLineEdit()
        self.dirBtn = QPushButton('...')
        self.expBtn = QPushButton('Export')

        grid.addWidget(self.namelb, 0, 0)
        grid.addWidget(self.name, 0, 1)
        grid.addWidget(self.lab, 1, 0)
        grid.addWidget(self.dir, 1, 1)
        grid.addWidget(self.dirBtn, 1, 2)
        grid.addWidget(self.expBtn, 3, 1)

        self.dir.textChanged.connect(self.reset)

        self.dirBtn.clicked.connect(self.getDir)
        self.expBtn.clicked.connect(self.exp)
        self.setLayout(grid)
        self.setWindowTitle('Export')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def reset(self):
        self.dir.setStyleSheet("")

    def getDir(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.dir.setText(file)

    def exp(self):
        path = self.dir.text()
        file = self.name.text()

        if exists(f"{path}/{file}"):
            buttonReply = QMessageBox.question(self, 'Override', "File already exists. \nDo you want to override?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                datatools.data.to_csv(f"{path}/{file}", index=False)
                self.close()
        else:
            try:
                datatools.data.to_csv(f"{path}/{file}", index=False)
                self.close()
            except OSError:
                self.dir.setStyleSheet("background-color: #FF8080")