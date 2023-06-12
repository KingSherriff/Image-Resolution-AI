import pandas as pd
import numpy as np
import cv2 as cv
import os
from skimage import metrics
import imutils
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
                greyA = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                greyB = cv.cvtColor(img_upscaled, cv.COLOR_BGR2GRAY)

                (score, diff) = metrics.structural_similarity(greyA, greyB, full=True)
                diff = (diff * 255).astype('uint8')
                print('SSIM: ' + str(score))
                print('MSE: ' + str(mse(img, img_upscaled)))
            elif interpolation == 1:
                img_downscaled = cv.resize(img, (int(width/4), int(height/4)), cv.INTER_CUBIC)
                img_upscaled = cv.resize(img_downscaled, (int(width), int(height)), cv.INTER_CUBIC)
                cv.imwrite(os.getcwd() + '/upscaled_' + file + "/upscaled_" + filename,img_upscaled)
                psnr = cv.PSNR(img, img_upscaled)
                print('PSNR: ' + str(psnr))
                greyA = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                greyB = cv.cvtColor(img_upscaled, cv.COLOR_BGR2GRAY)
            
                (score, diff) = metrics.structural_similarity(greyA, greyB, full=True)
                diff = (diff * 255).astype('uint8')
                print('SSIM: ' + str(score))
                print('MSE: ' + str(mse(img, img_upscaled)))
            else:
                print("ERROR on interpolation input!")
                exit

#setup('bsds', 0)

def mse(img, img_upscaled):
    h, w, t = img.shape
    diff = cv.subtract(img, img_upscaled)
    err = np.sum(diff**2)
    mse = err/(float(h*w))
    return mse

def evaluate(file: str):
    originalImg = cv.imread(file + '/' + filename)
    alteredImg = cv.imread('upscaled_' + file + '/upscaled_' + filename)
    psnr = cv.PSNR(originalImg, alteredImg)

    greyA = cv.cvtColor(originalImg, cv.COLOR_BGR2GRAY)
    greyB = cv.cvtColor(alteredImg, cv.COLOR_BGR2GRAY)

    (score, diff) = skimage.measure.compare_ssim(greyA, greyB)
    diff = (diff * 255).astype('uint8')
    print('PSNR: ' + psnr)
    print('SSIM: ' + score)
