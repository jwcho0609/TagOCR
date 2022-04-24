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

import datatools


class ScanAlgo:

    def __init__(self, cam):
        super().__init__()
        self.camera = cam
        self.frame1 = None
        self.frame2 = None
        self.frame3 = None

    def get_grayscale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def thresholding(self, image):
        return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    def opening(self, image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    def canny(self, image):
        return cv2.Canny(image, 100, 200)

    def capture(self):
        # ret, self.frame1 = self.camera.read()
        # # cv2.imwrite('img1.jpg', frame)
        # sleep(0.05)
        #
        # ret, self.frame2 = self.camera.read()
        # # cv2.imwrite('img2.jpg', frame1)
        # sleep(0.05)
        #
        # ret, self.frame3 = self.camera.read()
        # # cv2.imwrite('img3.jpg', frame2)
        # sleep(0.05)

        # self.performOCR([self.frame1, self.frame2, self.frame3])
        i = random.randint(1, 6)
        tester = cv2.imread(f'test/test{i}.jpg')
        print(f'test{i}.jpg')
        self.performOCR([tester])

    def performOCR(self, frames):
        polyPer, cotPer, spanPer = [0, 0, 0]
        print("OCR REACHED\n----------------")
        for f in frames:
            print('testing loop entered')
            d = pytesseract.image_to_data(f, lang='eng+fra+spa', output_type=Output.DICT)
            # print(d['text'])              # print statement for checking parsed out text

            # If 1 or less words recognized, please rescan
            print('testing')
            if len(d['text']) <= 1:
                print("Please Rescan")
                break

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
                        print(prev2)
                        spanPer = int(prev2.strip('%'))
                    else:
                        spanPer = int(prev.strip('%'))
                if cottondist >= 0.9:
                    if len(prev.strip()) == 1 or len(prev.strip()) > 4:
                        cotPer = int(prev2.strip('%'))
                    else:
                        cotPer = int(prev.strip('%'))

        print(f"Polyester: {polyPer} %")
        print(f"Spandex: {spanPer} %")
        print(f"Cotton: {cotPer} %\n")

        datatools.addItem(polyPer, spanPer, cotPer)

    def test(self):
        print('testing in the scanning algorithm')