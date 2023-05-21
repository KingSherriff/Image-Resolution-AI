import pandas as pd
import numpy as np
import cv2 as cv
import os
from PIL import Image

def setup(file: str, interpolation: int):
    # Add variable for path string to make things easier
    try:
        print('Created File')
        os.mkdir(os.getcwd() + '/upscaled_' + file, 0o777)
    except:
        print('File already exists')
    for filename in os.listdir(file):
        if filename.endswith('jpg') or filename.endswith('png'):
            img = cv.imread(file + '/' + filename)
            height = img.shape[0]
            width = img.shape[1]
            # Make sure if and elif match up
            # Clean up print statements late
            # Number of Successes/Total
            # No need to print where each one was sent, just where failures failed
            if interpolation == 0:
                img_downscaled = cv.resize(img, (int(width/5), int(height/2)), cv.INTER_LINEAR)
                img_upscaled = cv.resize(img_downscaled, (int(width), int(height)), cv.INTER_LINEAR)
                print(os.getcwd() + '/upscaled_' + file + "/upscaled_" + filename)
                writeSuccess = cv.imwrite(os.getcwd() + '/upscaled_' + file + "/upscaled_" + filename, img_upscaled)
                print('Write Success: ' + f'{writeSuccess}' + ' | ' + file + ' written in ' + '/upscaled_' + file  + ' : upscaled_' + filename)
                psnr = cv.PSNR(img, img_upscaled)
                print('PSNR: ' + str(psnr))
            elif interpolation == 1:
                img_downscaled = cv.resize(img, (int(width/4), int(height/4)), cv.INTER_CUBIC)
                img_upscaled = cv.resize(img_downscaled, (int(width), int(height)), cv.INTER_CUBIC)
                cv.imwrite(os.getcwd() + '/upscaled_' + file + "/upscaled_" + filename,img_upscaled)
                psnr = cv.PSNR(img, img_upscaled)
                print('PSNR: ' + str(psnr))
            else:
                print("ERROR on interpolation input!")
                exit

#setup('bsds', 0)

def evaluate(file: str):
    originalImg = cv.imread(file + '/' + filename)
    alteredImg = cv.imread('upscaled_' + file + '/upscaled_' + filename)
    psnr = cv.PSNR(originalImg, alteredImg)
    print('PSNR: ' + psnr)
