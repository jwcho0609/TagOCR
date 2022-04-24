"""
Settings window for motor parameter control and testing.
"""


from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import config as c
import math
from time import sleep
import RPi.GPIO as GPIO


PUL = c.PUL
DIR = c.DIR
ENA = c.ENA

GPIO.setmode(GPIO.BCM)
GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

# Assign pins based on BCM mode


class MotorThread(QRunnable):
    def __init__(self, direc, steps, steps_per_s):
        super().__init__()
        self.dir = direc
        self.steps = steps
        self.steps_per_s = steps_per_s
    

    def run(self):
        print("Testing pressed...") 

        # Enable motor
        GPIO.output(ENA, GPIO.HIGH)
        
        # Set motor direction
        if self.dir == 0:
            GPIO.output(DIR, GPIO.LOW)
        elif self.dir == 1:
            GPIO.output(DIR, GPIO.HIGH)
        else:
            None
        
        # Translate velocity to delay between pulses (s per step)
        delay = 1 / self.steps_per_s
        
        # Initialize pulse step
        GPIO.output(PUL, GPIO.LOW)
        
        # Driving loop
        for i in range(self.steps):
            GPIO.output(PUL, GPIO.HIGH)
            sleep(delay / 2)
            GPIO.output(PUL, GPIO.LOW)
            sleep(delay / 2)

        sleep(5)
        print(self.steps)
        print(self.steps_per_s)
        travel_time = (1 / self.steps_per_s) * self.steps
        print(travel_time)
        print("Testing ended...")


class SettingsWindow(QWidget):

    def __init__(self):
        super().__init__()

        input_gb = QGroupBox('Input controls')
        output_gb = QGroupBox('Output values')
        test_gb = QGroupBox('Test')

        grid = QGridLayout()
        vbox1 = QVBoxLayout()
        vbox2 = QVBoxLayout()
        vbox3 = QVBoxLayout()

        # input
        self.pul_per_rev = QLabel('Pulse per revolution:')
        self.ppr_spin = QSpinBox()
        self.ppr_spin.setRange(0, 1000)
        self.ppr_spin.setValue(c.pulse_per_rev)
        self.ppr_spin.setSingleStep(1)
        self.rpm_lbl = QLabel('RPM:')
        self.rpm_spin = QSpinBox()
        self.rpm_spin.setRange(0, 100)
        self.rpm_spin.setValue(c.travel_rpm)
        self.rpm_spin.setSingleStep(1)

        vbox1.addWidget(self.pul_per_rev)
        vbox1.addWidget(self.ppr_spin)
        vbox1.addWidget(self.rpm_lbl)
        vbox1.addWidget(self.rpm_spin)
        vbox1.addStretch(2)

        # output
        self.steps_per_deg = QLabel('Steps per degree:')
        self.spd = QLabel(str(round(self.ppr_spin.value() / 360, 4)))
        self.sps = QLabel('Steps per second:')
        self.sps_num = QLabel(str(round(self.rpm_spin.value() * self.ppr_spin.value() / 60, 4)))

        vbox2.addWidget(self.steps_per_deg)
        vbox2.addWidget(self.spd)
        vbox2.addWidget(self.sps)
        vbox2.addWidget(self.sps_num)
        vbox2.addStretch(2)

        # test
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        self.dir = QLabel('Direction:')
        self.dir_cb = QComboBox()
        self.dir_cb.addItem('0')
        self.dir_cb.addItem('1')
        self.travel_deg = QLabel('Travel degrees:')
        self.trv_spin = QSpinBox()
        self.trv_spin.setRange(0, 3600)
        self.trv_spin.setSingleStep(1)
        self.steps_lbl = QLabel('Steps:')
        self.steps_count = QLabel(str(math.floor(self.trv_spin.value() * float(self.spd.text()))))
        self.testBtn = QPushButton('Test', self)

        hbox1.addWidget(self.dir)
        hbox1.addWidget(self.dir_cb)
        hbox2.addWidget(self.steps_lbl)
        hbox2.addWidget(self.steps_count)
        vbox3.addLayout(hbox1)
        vbox3.addWidget(self.travel_deg)
        vbox3.addWidget(self.trv_spin)
        vbox3.addLayout(hbox2)
        vbox3.addWidget(self.testBtn)

        input_gb.setLayout(vbox1)
        output_gb.setLayout(vbox2)
        test_gb.setLayout(vbox3)

        self.applyBtn = QPushButton('Apply', self)
        self.resetBtn = QPushButton('Reset', self)
        self.quitBtn = QPushButton('Close', self)
        self.quitBtn.resize(self.quitBtn.sizeHint())
        self.quitBtn.clicked.connect(self.closeWindow)

        self.status = QLabel('All changes saved')

        hbox = QHBoxLayout()
        hbox.addWidget(self.resetBtn)
        hbox.addWidget(self.applyBtn)
        hbox.addWidget(self.quitBtn)

        grid.addWidget(input_gb, 0, 0)
        grid.addWidget(output_gb, 0, 1)
        grid.addWidget(self.status, 1, 0)
        grid.addLayout(hbox, 1, 2)
        grid.addWidget(test_gb, 0, 2)

        self.setLayout(grid)

        self.ppr_spin.valueChanged.connect(self.value_changed)
        self.rpm_spin.valueChanged.connect(self.value_changed)
        self.trv_spin.valueChanged.connect(self.value_changed)
        self.applyBtn.clicked.connect(self.save_vals)
        self.resetBtn.clicked.connect(self.reset)
        self.testBtn.clicked.connect(self.test_drive)

        self.setWindowTitle('Settings')

    def save_vals(self):
        c.pulse_per_rev = self.ppr_spin.value()
        c.travel_rpm = self.rpm_spin.value()
        c.steps_per_degree = c.pulse_per_rev / 360
        self.status.setText('All changes saved!')
        self.status.setStyleSheet("color: green")

    def reset(self):
        global pool
        self.ppr_spin.setValue(c.pulse_per_rev)
        self.rpm_spin.setValue(c.travel_rpm)
        self.spd.setText(str(round(self.ppr_spin.value() / 360, 4)))
        self.sps_num.setText(str(round(self.rpm_spin.value() * self.ppr_spin.value() / 60, 4)))
        self.steps_count.setText(str(math.floor(self.trv_spin.value() * float(self.spd.text()))))
        self.status.setText('Current input values')
        self.status.setStyleSheet("color: yellow")

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeWindow(self):
        self.close()

    def value_changed(self):
        self.spd.setText(str(round(self.ppr_spin.value() / 360, 4)))
        self.sps_num.setText(str(round(self.rpm_spin.value() * self.ppr_spin.value() / 60, 4)))
        self.steps_count.setText(str(math.floor(self.trv_spin.value() * float(self.spd.text()))))
        self.status.setText('Unsaved changes')
        self.status.setStyleSheet("color: red")

    def test_drive(self):
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        print(threadCount)
        steps = math.floor(self.trv_spin.value() * c.steps_per_degree)
        direction = int(self.dir_cb.currentText())
        steps_per_s = c.travel_rpm * c.pulse_per_rev / 60
        thread = MotorThread(direction, steps, steps_per_s)
        c.pool.start(thread)
