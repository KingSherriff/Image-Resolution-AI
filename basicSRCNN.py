# check package versions
import sys
import keras
import cv2
import numpy
import matplotlib
import skimage

print('Python: {}'.format(sys.version))
print('Keras: {}'.format(keras.__version__))
print('OpenCV: {}'.format(cv2.__version__))
print('NumPy: {}'.format(numpy.__version__))
print('Matplotlib: {}'.format(matplotlib.__version__))
print('Scikit-Image: {}'.format(skimage.__version__))

from keras.models import Sequential
from keras.layers import Conv2D
from keras.optimizers import Adam
from skimage.measure import compare_ssim as ssim
from matplotlib import pyplot as plt
import cv2
import numpy as np
import math
import os

# define a function for peak signal-to-noise ratio (PSNR)
def psnr(target, ref):
         
    # assume RGB image
    target_data = target.astype(float)
    ref_data = ref.astype(float)

    diff = ref_data - target_data
    diff = diff.flatten('C')

    rmse = math.sqrt(np.mean(diff ** 2.))

    return 20 * math.log10(255. / rmse)

# define function for mean squared error (MSE)
def mse(target, ref):
    # the MSE between the two images is the sum of the squared difference between the two images
    err = np.sum((target.astype('float') - ref.astype('float')) ** 2)
    err /= float(target.shape[0] * target.shape[1])
    
    return err

# define function that combines all three image quality metrics
def compare_images(target, ref):
    scores = []
    scores.append(psnr(target, ref))
    scores.append(mse(target, ref))
    scores.append(ssim(target, ref, multichannel =True))
    
    return scores

def prepareImage(file: str, interpolation: int):
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

prepareImages('', 0)

# test the generated images using the image quality metrics

for file in os.listdir('images/'):

    # open target and reference images
    target = cv2.imread('images/{}'.format(file))
    ref = cv2.imread('source/{}'.format(file))

    # calculate score
    scores = compare_images(target, ref)

    # print all three scores with new line characters (\n)
    print('{}\nPSNR: {}\nMSE: {}\nSSIM: {}\n'.format(file, scores[0], scores[1], scores[2]))

# define the SRCNN model
def model():

    # define model type
    SRCNN = Sequential()

    # add model layers
    SRCNN.add(Conv2D(filters=128, kernel_size = (9, 9), kernel_initializer='glorot_uniform',
                     activation='relu', padding='valid', use_bias=True, input_shape=(None, None, 1)))
    SRCNN.add(Conv2D(filters=64, kernel_size = (3, 3), kernel_initializer='glorot_uniform',
                     activation='relu', padding='same', use_bias=True))
    SRCNN.add(Conv2D(filters=1, kernel_size = (5, 5), kernel_initializer='glorot_uniform',
                     activation='linear', padding='valid', use_bias=True))

    # define optimizer
    adam = Adam(lr=0.0003)

    # compile model
    SRCNN.compile(optimizer=adam, loss='mean_squared_error', metrics=['mean_squared_error'])

    return SRCNN


