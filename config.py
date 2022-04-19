"""
Configuration file for initial set-up of motor.
"""

from PyQt5.QtCore import QThreadPool

# Motor GPIO assignment
PUL = 21
DIR = 20
ENA = 16

pulse_per_rev = 800
steps_per_degree = pulse_per_rev / 360
travel_rpm = 400

pool = QThreadPool.globalInstance()
