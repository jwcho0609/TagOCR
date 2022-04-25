"""
All scanning algorithms related to OCR using Tesseract
"""

from time import sleep
import cv2
import pytesseract
import numpy as np
from pytesseract import Output
import jellyfish as jf
import pandas as pd
import os
import random
import RPi.GPIO as GPIO

import datatools

led = 22
# GPIO.setmode(GPIO.BOARD)
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, True)

resetCount = 0


class ScanAlgo:

    def __init__(self, cam):
        super().__init__()
        self.camera = cam
        self.frame1 = None
        self.frame2 = None
        self.frame3 = None
        self.mainWind = None

    def get_grayscale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def thresholding(self, image):
        return cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)

    def capture(self):
        global led, resetCount
        # GPIO.output(led, True)
        ret, self.frame1 = self.camera.read()
        self.frame1 = cv2.rotate(self.frame1, cv2.ROTATE_180)
        # cv2.imwrite('img1.jpg', self.frame1)
        # GPIO.output(led, False)
        sleep(0.05)

        # GPIO.output(led, True)
        ret, self.frame2 = self.camera.read()
        self.frame2 = cv2.rotate(self.frame2, cv2.ROTATE_180)
        # # cv2.imwrite('img2.jpg', frame1)
        # GPIO.output(led, False)
        sleep(0.05)

        # GPIO.output(led, True)
        ret, self.frame3 = self.camera.read()
        self.frame3 = cv2.rotate(self.frame3, cv2.ROTATE_180)
        # # cv2.imwrite('img3.jpg', frame2)
        GPIO.output(led, False)
        sleep(0.05)

        out = self.performOCR([self.frame1, self.frame2, self.frame3])

        if not out:
            resetCount += 1
            datatools.lastScanned = 'rescan'
            if resetCount == 3:
                self.mainWind.status.setStyleSheet("color: green;"
                                                   "background-color: #7FFFD4;")
                self.mainWind.status.setText('Unknown')
                polyPer, spanPer, cotPer = [0, 0, 0]
                datatools.addItem(polyPer, spanPer, cotPer)
                resetCount = 0
            else:
                self.mainWind.status.setStyleSheet("color: red;"
                                                   "background-color: #FF6464;")
                self.mainWind.status.setText('Please rescan')
            sleep(1.5)
            print('test')
            self.mainWind.status.setStyleSheet("color: blue;"
                                               "background-color: #87CEFA;")
            self.mainWind.status.setText('status')
            GPIO.output(led, True)

    def performOCR(self, frames):
        global led, resetCount

        print("OCR REACHED\n----------------")
        for f in frames:
            polyPer, cotPer, spanPer = [0, 0, 0]
            print('testing loop entered')

            f = self.thresholding(self.get_grayscale(f))
            f = f[1]
            # cv2.imwrite('img1.jpg', f)


            try:
                d = pytesseract.image_to_data(f, lang='eng+fra+spa', output_type=Output.DICT)
            except TypeError as error:
                return 0

            print(d['text'])  # print statement for checking parsed out text        self.span.setFixedSize(100, 25)

            # If 1 or less words recognized, please rescan
            if len(d['text']) <= 1:
                print("Please Rescan")
                return 0

            if not ''.join(d['text']):
                return 0

            try:
                # parse through the array of texts scanned
                for i in range(len(d['text'])):
                    t = d['text'][i]
                    p = i - 1
                    while p >= 1 and len(d['text'][p].strip()) == 0:
                        p = p - 1
                    prev = d['text'][p]

                    p = p - 1
                    while p >= 0 and len(d['text'][p].strip()) == 0:
                        p = p - 1
                    prev2 = d['text'][p]

                    if '%' not in prev and '%' not in prev2:
                        continue

                    t = t.lower()
                    polydist = 1 - jf.levenshtein_distance(t, 'polyester') / len('polyester')
                    spandist = jf.jaro_distance(t, 'spandex')
                    cottondist = jf.jaro_distance(t, 'cotton')

                    if polydist >= 0.75:
                        if len(prev.strip()) == 1 or len(prev.strip()) > 4:
                            polyPer = int(prev2.strip('%'))
                        else:
                            polyPer = int(prev.strip('%'))
                    if spandist >= 0.85:
                        if len(prev.strip()) == 1 or len(prev.strip()) > 4:
                            # print(prev2)
                            spanPer = int(prev2.strip('%'))
                        else:
                            spanPer = int(prev.strip('%'))
                    if cottondist >= 0.9:
                        if len(prev.strip()) == 1 or len(prev.strip()) > 4:
                            cotPer = int(prev2.strip('%'))
                        else:
                            cotPer = int(prev.strip('%'))
                
                print(polyPer)
                print(cotPer)
                print(spanPer)
                
                if polyPer == 0 and cotPer == 0 and spanPer == 0:
                    print("Unknown, rescanning")
                elif max(polyPer, spanPer, cotPer) == polyPer:
                    print("Polyester")
                    break
                elif max(polyPer, spanPer, cotPer) == spanPer:
                    print("Spandex")
                    break
                elif max(polyPer, spanPer, cotPer) == cotPer:
                    print("Cotton")
                    break
            except:
                pass

        print(f"Polyester: {polyPer} %")
        print(f"Spandex: {spanPer} %")
        print(f"Cotton: {cotPer} %\n")

        datatools.addItem(polyPer, spanPer, cotPer)
        resetCount = 0
        GPIO.output(led, True)
        return 1

    def setMain(self, mainWind):
        self.mainWind = mainWind
