"""
DataTools widget of the main GUI window and the global data lives on this script.
"""

from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import config as c
import math
from time import sleep
import pandas as pd

import export


polyCount = 0
spanCount = 0
cotCount = 0
unkCount = 0

lastScanned = 'None'
lastPer = [0, 0, 0]

itemNum = 1
data = pd.DataFrame(columns=["Item No.", "%Cotton", "%Polyester", "%Spandex", "Class"])


class DataTools(QWidget):

    def __init__(self):
        super().__init__()
        global lastScanned
        self.exp = None

        # Layout initialization
        gb = QGroupBox()
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(0)
        vboxL = QVBoxLayout()
        vboxR = QVBoxLayout()

        # Control buttons (Right vbox)
        self.clearBtn = QPushButton('Clear')
        self.clearBtn.setFixedSize(150, 75)
        self.clearBtn.setFont(QFont('Arial', 20))
        self.exportBtn = QPushButton('Export')
        self.exportBtn.setFixedSize(150, 75)
        self.exportBtn.setFont(QFont('Arial', 20))
        self.lastScanlbl = QLabel('Last scanned:')
        self.lastScan = QLabel(lastScanned)

        vboxR.addWidget(self.lastScanlbl)
        vboxR.addWidget(self.lastScan)
        vboxR.addWidget(self.clearBtn)
        vboxR.addWidget(self.exportBtn)

        # Data visualization (Left vbox)
        self.polylb = QLabel('Polyester')
        self.spanlb = QLabel('Spandex')
        self.cotlb = QLabel('Cotton')
        self.unklb = QLabel('Unknown')
        self.poly = QLabel(str(polyCount))
        self.span = QLabel(str(spanCount))
        self.cot = QLabel(str(cotCount))
        self.unk = QLabel(str(unkCount))

        gb2 = QGroupBox('Current count')
        vboxL.addWidget(self.polylb)
        vboxL.addWidget(self.poly)
        vboxL.addWidget(self.spanlb)
        vboxL.addWidget(self.span)
        vboxL.addWidget(self.cotlb)
        vboxL.addWidget(self.cot)
        vboxL.addWidget(self.unklb)
        vboxL.addWidget(self.unk)

        gb2.setLayout(vboxL)

        # Layout settings for grid
        grid.addWidget(gb2, 0, 0)
        grid.addLayout(vboxR, 0, 1)
        gb.setLayout(grid)

        # Initialize the toolbox layout
        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(gb)

        self.clearBtn.clicked.connect(self.clear)
        self.exportBtn.clicked.connect(self.export)

    def update(self):
        self.poly.setText(str(polyCount))
        self.span.setText(str(spanCount))
        self.cot.setText(str(cotCount))
        self.unk.setText(str(unkCount))

    def clear(self):
        global polyCount, spanCount, cotCount, unkCount, itemNum, data
        polyCount, spanCount, cotCount, unkCount = [0, 0, 0, 0]
        data = pd.DataFrame(columns=["Item No.", "%Cotton", "%Polyester", "%Spandex", "Class"])
        itemNum = 1
        self.update()

    def export(self):
        if self.exp is None:
            self.exp = export.ExportWindow()
        self.exp.setGeometry(0, 0, 300, 200)
        self.exp.center()
        self.exp.show()


def addItem(polyPer, spanPer, cotPer):
    global data, itemNum, polyCount, spanCount, cotCount, unkCount, lastScanned, lastPer
    class_set = None
    lastPer = [polyPer, spanPer, cotPer]

    if not polyPer and not cotPer and not spanPer:
        unkCount += 1
        class_set = 'unk'
        lastScanned = 'Unknown'
    else:
        if max(polyPer, spanPer, cotPer) == polyPer:
            polyCount += 1
            class_set = 'poly'
            lastScanned = 'Polyester'
        elif max(polyPer, spanPer, cotPer) == spanPer:
            spanCount += 1
            class_set = 'spand'
            lastScanned = 'Spandex'
        elif max(polyPer, spanPer, cotPer) == cotPer:
            cotCount += 1
            class_set = 'cott'
            lastScanned = 'Cotton'

    data = data.append({"Item No.": itemNum, "%Cotton": cotPer, "%Polyester": polyPer,
                                             "%Spandex": spanPer, "Class": class_set}, ignore_index=True)

    itemNum += 1
