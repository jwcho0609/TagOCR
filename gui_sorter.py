"""
Main gui application.
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
import math
from time import sleep
import random

import settings
import datatools
import config as c
from scanalgo import ScanAlgo

cap = cv2.VideoCapture(0)
scan_algo = ScanAlgo(cap)


class scanner(QRunnable):
    def __init__(self, label, tools, scan, poly, span, cot):
        super().__init__()
        self.status = label
        self.tools = tools
        self.scan = scan
        self.poly = poly
        self.span = span
        self.cot = cot

    def run(self):
        global scan_algo
        # sleep(2)

        # call algorithm to capture frames and update the data accordingly
        scan_algo.capture()
        self.tools.update()

        lastScanned = datatools.lastScanned

        self.status.setStyleSheet("color: green;"
                                  "background-color: #7FFFD4;"
                                  "border-style: solid;"
                                  "border-width: 3px;"
                                  "border-color: #1E90FF")

        self.poly.setText(f'Polyester\n{datatools.lastPer[0]}%')
        self.span.setText(f'Spandex\n{datatools.lastPer[1]}%')
        self.cot.setText(f'Cotton\n{datatools.lastPer[2]}%')

        if lastScanned == 'Polyester':
            self.status.setText("Polyester")
            self.tools.lastScan.setText('Polyester')
            self.poly.setStyleSheet("color: green;"
                                    "background-color: #7FFFD4;"
                                    "border-style: solid;"
                                    "border-width: 3px;"
                                    "border-color: #1E90FF")

        elif lastScanned == 'Spandex':
            self.status.setText("Spandex")
            self.tools.lastScan.setText('Spandex')
            self.span.setStyleSheet("color: green;"
                                    "background-color: #7FFFD4;"
                                    "border-style: solid;"
                                    "border-width: 3px;"
                                    "border-color: #1E90FF")

        elif lastScanned == 'Cotton':
            self.status.setText("Cotton")
            self.tools.lastScan.setText('Cotton')
            self.cot.setStyleSheet("color: green;"
                                   "background-color: #7FFFD4;"
                                   "border-style: solid;"
                                   "border-width: 3px;"
                                   "border-color: #1E90FF")

        else:
            self.status.setText("Unknown")
            self.tools.lastScan.setText('Unknown')

        # else:
        #     self.status.setStyleSheet("color: red;"
        #                               "background-color: #FF6464;"
        #                               "border-style: solid;"
        #                               "border-width: 3px;"
        #                               "border-color: #FA8072")
        #     self.status.setText("Failed: scan again")
        #
        #     sleep(1)

        sleep(1)
        self.status.setStyleSheet("color: blue;"
                                  "background-color: #87CEFA;"
                                  "border-style: solid;"
                                  "border-width: 3px;"
                                  "border-color: #1E90FF")
        self.poly.setStyleSheet("color: blue;"
                                "background-color: #87CEFA;"
                                "border-style: solid;"
                                "border-width: 3px;"
                                "border-color: #1E90FF")
        self.span.setStyleSheet("color: blue;"
                                "background-color: #87CEFA;"
                                "border-style: solid;"
                                "border-width: 3px;"
                                "border-color: #1E90FF")
        self.cot.setStyleSheet("color: blue;"
                               "background-color: #87CEFA;"
                               "border-style: solid;"
                               "border-width: 3px;"
                               "border-color: #1E90FF")
        self.poly.setText(f'Polyester\n0%')
        self.span.setText(f'Spandex\n0%')
        self.cot.setText(f'Cotton\n0%')

        self.status.setText("Status")
        self.scan.setEnabled(True)


class CameraThread(QThread):
    changePixmap = pyqtSignal(QImage)
    _run_flag = True

    def run(self):
        global cap
        while self._run_flag:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgbImage = cv2.rotate(rgbImage, cv2.ROTATE_90_CLOCKWISE)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(720, 800, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.w = None
        # Layout declaration
        hbox = QHBoxLayout()
        hboxBot = QHBoxLayout()
        hboxMat = QHBoxLayout()
        vboxL = QVBoxLayout()
        vboxR = QVBoxLayout()

        # Widget for the camera eventually
        self.label1 = QLabel()
        self.testImg = QPixmap('test.png')
        self.label1.setPixmap(self.testImg)
        # label1.resize(testImg.width(), testImg.height())

        # Widget for the status box
        self.status = QLabel('status')
        self.status.setFixedSize(900, 200)
        self.status.setFont(QFont('Arial', 50))
        self.status.setAlignment(QtCore.Qt.AlignCenter)
        self.status.setStyleSheet("color: blue;"
                                  "background-color: #87CEFA;"
                                  "border-style: solid;"
                                  "border-width: 3px;"
                                  "border-color: #1E90FF")

        # Widgets for each material
        self.poly = QLabel('Polyester\n0%')
        self.poly.setFixedSize(300, 100)
        self.poly.setFont(QFont('Arial', 20))
        self.poly.setAlignment(QtCore.Qt.AlignCenter)
        self.poly.setStyleSheet("color: blue;"
                                "background-color: #87CEFA;"
                                "border-style: solid;"
                                "border-width: 3px;"
                                "border-color: #1E90FF")

        self.span = QLabel('Spandex\n0%')
        self.span.setFixedSize(300, 100)
        self.span.setAlignment(QtCore.Qt.AlignCenter)
        self.span.setFont(QFont('Arial', 20))
        self.span.setStyleSheet("color: blue;"
                                "background-color: #87CEFA;"
                                "border-style: solid;"
                                "border-width: 3px;"
                                "border-color: #1E90FF")

        self.cot = QLabel('Cotton\n0%')
        self.cot.setFixedSize(300, 100)
        self.cot.setAlignment(QtCore.Qt.AlignCenter)
        self.cot.setFont(QFont('Arial', 20))
        self.cot.setStyleSheet("color: blue;"
                               "background-color: #87CEFA;"
                               "border-style: solid;"
                               "border-width: 3px;"
                               "border-color: #1E90FF")

        hboxMat.addWidget(self.poly)
        hboxMat.addWidget(self.span)
        hboxMat.addWidget(self.cot)

        # Button for opening settings
        self.setBtn = QPushButton()
        self.setBtn.setIcon(QIcon('source/icon_setting.png'))
        self.setBtn.setIconSize(QtCore.QSize(60, 60))
        self.setBtn.clicked.connect(self.settings_window)
        self.setBtn.setFixedSize(100, 100)

        # Widget for quitting the app
        self.quitBtn = QPushButton('Quit', self)
        self.quitBtn.setFixedSize(100, 100)

        # Right panel buttons
        self.scanBtn = QPushButton('Scan', self)
        self.scanBtn.setFixedSize(400, 100)
        self.scanBtn.setFont(QFont('Arial', 30))

        self.tools = datatools.DataTools()

        # camera
        self.label2 = QLabel()
        self.th = CameraThread(self)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()

        # Right vbox
        vboxR.addWidget(self.status)
        vboxR.addWidget(self.scanBtn)
        vboxR.addLayout(hboxMat)
        vboxR.addStretch(1)
        vboxR.addWidget(self.tools)
        # hboxBot.addStretch(1)
        hboxBot.addWidget(self.setBtn)
        hboxBot.addWidget(self.quitBtn)
        vboxR.addLayout(hboxBot)

        # Left vbox
        vboxL.addWidget(self.label2)
        self.label2.setAlignment(Qt.AlignCenter)

        hbox.addLayout(vboxL)
        hbox.addLayout(vboxR)

        self.setLayout(hbox)

        self.quitBtn.clicked.connect(self.quitAct)
        self.scanBtn.clicked.connect(self.scan)

        self.setWindowTitle('My First Application')
        self.showMaximized()

    def scan(self):
        self.status.setText("Scanning")
        self.scanBtn.setEnabled(False)
        scanThread = scanner(self.status, self.tools, self.scanBtn, self.poly, self.span, self.cot)
        c.pool.start(scanThread)

    def setImage(self, image):
        self.label2.setPixmap(QPixmap.fromImage(image))

    def settings_window(self):
        if self.w is None:
            self.w = settings.SettingsWindow()
        self.w.reset()
        self.w.setGeometry(0, 0, 300, 200)
        self.w.center()
        self.w.show()

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.th.stop()
            event.accept()
        else:
            event.ignore()

    def quitAct(self):
        global scan_algo
        print('Quit')
        scan_algo.test()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
