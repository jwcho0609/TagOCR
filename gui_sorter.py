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
import RPi.GPIO as GPIO

import settings
import datatools
import config as c
import scanalgo
from scanalgo import ScanAlgo

cap = cv2.VideoCapture(0)
scan_algo = ScanAlgo(cap)
GPIO.setwarnings(False)


class scanner(QRunnable):
    def __init__(self, label, tools, scan, poly, span, cot, settings, unk, flag):
        super().__init__()
        self.status = label
        self.tools = tools
        self.scan = scan
        self.poly = poly
        self.span = span
        self.cot = cot
        self.settings = settings
        self.unkBtn = unk
        self.flag = flag

    def run(self):
        global scan_algo
        # sleep(2)

        currPos = datatools.lastScanned
        if currPos == 'None':
            currPos = 'Unknown'

        # call algorithm to capture frames and update the data accordingly
        if not self.flag:
            scan_algo.capture()
        else:
            polyPer, spanPer, cotPer = [0, 0, 0]
            datatools.addItem(polyPer, spanPer, cotPer)
            scanalgo.resetCount = 0

        self.tools.update()

        lastScanned = datatools.lastScanned

        if lastScanned == 'rescan':
            self.scan.setEnabled(True)
            datatools.lastScanned = currPos
            return

        self.status.setStyleSheet("color: green;"
                                  "background-color: #7FFFD4;")

        self.poly.setText(f'Polyester\n{datatools.lastPer[0]}%')
        self.span.setText(f'Spandex\n{datatools.lastPer[1]}%')
        self.cot.setText(f'Cotton\n{datatools.lastPer[2]}%')

        if lastScanned == 'Polyester':
            self.status.setText("Polyester")
            self.tools.lastScan.setText('Polyester')
            self.poly.setStyleSheet("color: green;"
                                    "background-color: #7FFFD4;")

        elif lastScanned == 'Spandex':
            self.status.setText("Spandex")
            self.tools.lastScan.setText('Spandex')
            self.span.setStyleSheet("color: green;"
                                    "background-color: #7FFFD4;")

        elif lastScanned == 'Cotton':
            self.status.setText("Cotton")
            self.tools.lastScan.setText('Cotton')
            self.cot.setStyleSheet("color: green;"
                                   "background-color: #7FFFD4;")

        elif lastScanned == 'Unknown':
            self.status.setText("Unknown")
            self.tools.lastScan.setText('Unknown')
        
        sleep(0.25)
        
        # drive the motor
        self.drive(currPos, lastScanned)

        sleep(1.5)
        self.status.setStyleSheet("color: blue;"
                                  "background-color: #87CEFA;")
        self.poly.setStyleSheet("color: blue;"
                                "background-color: #87CEFA;")
        self.span.setStyleSheet("color: blue;"
                                "background-color: #87CEFA;")
        self.cot.setStyleSheet("color: blue;"
                               "background-color: #87CEFA;")
        self.poly.setText(f'Polyester\n0%')
        self.span.setText(f'Spandex\n0%')
        self.cot.setText(f'Cotton\n0%')

        self.status.setText("Status")
        self.unkBtn.setEnabled(True)
        self.scan.setEnabled(True)

    def drive(self, currPos, new):
        if currPos == 'Unknown':
            if new == 'Polyester':
                direction = 0
                steps = 1
            elif new == 'Spandex':
                direction = 0
                steps = 2
            elif new == 'Cotton':
                direction = 1
                steps = 1
            else:
                return

        elif currPos == 'Polyester':
            if new == 'Unknown':
                direction = 1
                steps = 1
            elif new == 'Spandex':
                direction = 0
                steps = 1
            elif new == 'Cotton':
                direction = 0
                steps = 2
            else:
                return

        elif currPos == 'Spandex':
            if new == 'Polyester':
                direction = 1
                steps = 1
            elif new == 'Unknown':
                direction = 0
                steps = 2
            elif new == 'Cotton':
                direction = 0
                steps = 1
            else:
                return

        else:
            if new == 'Polyester':
                direction = 0
                steps = 2
            elif new == 'Spandex':
                direction = 1
                steps = 1
            elif new == 'Unknown':
                direction = 0
                steps = 1
            else:
                return

        self.settings.test_drive2(direction, 180 * steps)


class CameraThread(QThread):
    changePixmap = pyqtSignal(QImage)
    _run_flag = True

    def run(self):
        global cap
        while self._run_flag:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgbImage = cv2.rotate(rgbImage, cv2.ROTATE_180)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(int(480 * (450 / 640)), 450)
                self.changePixmap.emit(p)

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class MainWindow(QWidget):

    def __init__(self):
        global scan_algo
        super().__init__()
        self.w = settings.SettingsWindow()
        # Layout declaration
        hbox = QHBoxLayout()
        hboxBot = QHBoxLayout()
        hboxMat = QHBoxLayout()
        vboxL = QVBoxLayout()
        vboxR = QVBoxLayout()

        # Widget for the camera eventually
        self.label1 = QLabel()
        # label1.resize(testImg.width(), testImg.height())

        # Widget for the status box
        self.status = QLabel('status')
        self.status.setFixedSize(230, 100)
        self.status.setFont(QFont('Comic Sans', 25))
        self.status.setAlignment(QtCore.Qt.AlignCenter)
        self.status.setStyleSheet("color: blue;"
                                  "background-color: #87CEFA;")

        # Widgets for each material
        self.poly = QLabel('Polyester\n0%')
        self.poly.setFixedSize(153, 60)
        self.poly.setFont(QFont('Comic Sans', 13))
        self.poly.setAlignment(QtCore.Qt.AlignCenter)
        self.poly.setStyleSheet("color: blue;"
                                "background-color: #87CEFA;")

        self.span = QLabel('Spandex\n0%')
        self.span.setFixedSize(153, 60)
        self.span.setAlignment(QtCore.Qt.AlignCenter)
        self.span.setFont(QFont('Comic Sans', 13))
        self.span.setStyleSheet("color: blue;"
                                "background-color: #87CEFA;")

        self.cot = QLabel('Cotton\n0%')
        self.cot.setFixedSize(153, 60)
        self.cot.setAlignment(QtCore.Qt.AlignCenter)
        self.cot.setFont(QFont('Comic Sans', 13))
        self.cot.setStyleSheet("color: blue;"
                               "background-color: #87CEFA;")

        hboxMat.addWidget(self.poly)
        hboxMat.addWidget(self.span)
        hboxMat.addWidget(self.cot)
        hboxMat.setContentsMargins(0, 1, 0, 0)
        hboxMat.setSpacing(0)

        # Button for opening settings
        self.setBtn = QPushButton()
        self.setBtn.setIcon(QIcon('/home/pi/Desktop/TagOCR/source/icon_setting.png'))
        self.setBtn.setIconSize(QtCore.QSize(50, 50))
        self.setBtn.clicked.connect(self.settings_window)
        self.setBtn.setFixedSize(80, 80)

        # Widget for quitting the app
        self.quitBtn = QPushButton('Quit', self)
        self.quitBtn.setFixedSize(80, 80)
        self.quitBtn.setFont(QFont('Comic sans', 16))

        # Widget for manual tag
        self.unkBtn = QPushButton('Unknown', self)
        self.unkBtn.setFixedSize(250, 80)
        self.unkBtn.setFont(QFont('Comic sans', 18))

        # Right panel buttons
        hboxR = QHBoxLayout()
        hboxR.setContentsMargins(0, 0, 0, 0)
        hboxR.setSpacing(0)
        self.scanBtn = QPushButton('SCAN', self)
        self.scanBtn.setStyleSheet("background-color: #B3A369;")
        self.scanBtn.setFixedSize(230, 100)
        self.scanBtn.setFont(QFont('Comic Sans', 25))

        self.tools = datatools.DataTools()
        self.tools.setStyleSheet('background-color: #B3A369;')

        # camera
        self.label2 = QLabel()
        self.label2.setFrameShape(QFrame.NoFrame)
        self.th = CameraThread(self)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()

        # Right vbox
        vboxR.setContentsMargins(0, 0, 0, 0)
        vboxR.setSpacing(0)
        hboxR.addWidget(self.scanBtn)
        hboxR.addWidget(self.status)
        vboxR.addLayout(hboxR)
        vboxR.addLayout(hboxMat)
        vboxR.addStretch(1)
        vboxR.addWidget(self.tools)
        # hboxBot.addStretch(1)
        hboxBot.addWidget(self.unkBtn)
        hboxBot.addWidget(self.setBtn)
        hboxBot.addWidget(self.quitBtn)
        vboxR.addLayout(hboxBot)

        # Left vbox
        vboxL.addWidget(self.label2)
        vboxL.setContentsMargins(0, 0, 0, 0)
        self.label2.setAlignment(Qt.AlignCenter)

        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        hbox.addLayout(vboxL)
        hbox.addLayout(vboxR)

        self.setLayout(hbox)

        self.unkBtn.clicked.connect(self.unkTag)
        self.quitBtn.clicked.connect(self.quitAct)
        self.scanBtn.clicked.connect(self.scan)
        scan_algo.setMain(self)

        self.setWindowTitle('TagOCR by The Bee\'s Knees')
        self.setFixedSize(800, 450)
        self.setStyleSheet('background-color: #54585A;')
        self.show()
        # self.showMaximized()

    def unkTag(self):
        self.scanBtn.setEnabled(False)
        self.unkBtn.setEnabled(False)
        scanThread = scanner(self.status, self.tools, self.scanBtn, self.poly, self.span, self.cot, self.w, self.unkBtn, True)
        c.pool.start(scanThread)

    def scan(self):
        self.status.setText("Scanning")
        self.unkBtn.setEnabled(False)
        self.scanBtn.setEnabled(False)
        scanThread = scanner(self.status, self.tools, self.scanBtn, self.poly, self.span, self.cot, self.w, self.unkBtn, False)
        c.pool.start(scanThread)

    def setImage(self, image):
        self.label2.setPixmap(QPixmap.fromImage(image))

    def settings_window(self):
        self.w.reset()
        self.w.setGeometry(0, 0, 300, 200)
        self.w.center()
        self.w.show()

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.th.stop()
            GPIO.cleanup()
            event.accept()
        else:
            event.ignore()

    def quitAct(self):
        self.close()


def test():
    import motor_drive


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('/home/pi/Desktop/TagOCR/source/beeLogo.png'))
    ex = MainWindow()
    sys.exit(app.exec_())
