import cv2 as cv
import numpy as np
import os
from mss import mss, tools as mss_tools
import time
import keyboard
import datetime


def imread(path, filename):
     return cv.imread(path + filename, cv.IMREAD_GRAYSCALE)

path_game = os.getcwd() + '\\templates_game\\'
im = imread(path_game, 'items.jpg')


x = im.shape[1]
y = im.shape[0]
# xx = slice(x //20 *5, x // 20 *9)
xx = slice(x //20 *8, x // 20 *12)
# xx = slice(x //20 *11, x // 20 *15)

yy = slice(y // 20 *7, y // 20 *11)

cv.imwrite(f'output_image.png', im[yy, xx])

# counter = 0
# with mss() as sct:

#     while True:

#         monitor = sct.monitors[1]
#         im = sct.grab(monitor)
#         im = cv.cvtColor(np.array(im), cv.COLOR_BGR2GRAY)

#         x = im.shape[1]
#         y = im.shape[0]
#         xx = slice(x // 8 *3, x // 8 *5)
#         yy = slice(y // 8 *2, y // 8 *4)


#         # masked_image = cv.bitwise_and(im, im, mask=mask)

#         print(im.shape)
#         print(im[yy, xx].shape)


#         cv.imwrite(f'screenshots/output_image{counter}.png', im[yy, xx])
#         counter += 1
#         time.sleep(1.5)


