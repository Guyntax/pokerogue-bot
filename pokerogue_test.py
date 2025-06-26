import cv2 as cv
import numpy as np
import os
from mss import mss, tools as mss_tools
import time
import keyboard
import datetime



counter = 0
with mss() as sct:

    while True:

        monitor = sct.monitors[1]
        im = sct.grab(monitor)
        im = cv.cvtColor(np.array(im), cv.COLOR_BGR2GRAY)

        x = im.shape[1]
        y = im.shape[0]
        xx = slice(x * 0, x // 2)
        yy = slice(y // 8 *1, y // 8*2)


        # masked_image = cv.bitwise_and(im, im, mask=mask)

        print(im.shape)
        print(im[yy, xx].shape)


        cv.imwrite(f'screenshots/output_image{counter}.png', im[yy, xx])
        counter += 1
        time.sleep(1.5)


