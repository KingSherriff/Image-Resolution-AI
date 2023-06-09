# check package versions
import sys
import keras
import numpy
import cv2
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
from skimage.metrics import structural_similarity as ssim
from matplotlib import pyplot as plt
import cv2 as cv
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

prepareImage('bsds', 0)

# test the generated images using the image quality metrics

for file in os.listdir('images/'):

    # open target and reference images
    target = cv.imread('images/{}'.format(file))
    ref = cv.imread('source/{}'.format(file))

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

# define necessary image processing functions

def modcrop(img, scale):
    tmpsz = img.shape
    sz = tmpsz[0:2]
    sz = sz - np.mod(sz, scale)
    img = img[0:sz[0], 1:sz[1]]
    return img


def shave(image, border):
    img = image[border: -border, border: -border]
    return img
# define main prediction function

def predict(image_path):
    
    # load the srcnn model with weights
    srcnn = model()
    srcnn.load_weights('3051crop_weight_200.h5')
    
    # load the degraded and reference images
    path, file = os.path.split(image_path)
    degraded = cv.imread(image_path)
    ref = cv.imread('source/{}'.format(file))
    
    # preprocess the image with modcrop
    ref = modcrop(ref, 3)
    degraded = modcrop(degraded, 3)
    
    # convert the image to YCrCb - (srcnn trained on Y channel)
    temp = cv.cvtColor(degraded, cv.COLOR_BGR2YCrCb)
    
    # create image slice and normalize  
    Y = numpy.zeros((1, temp.shape[0], temp.shape[1], 1), dtype=float)
    Y[0, :, :, 0] = temp[:, :, 0].astype(float) / 255
    
    # perform super-resolution with srcnn
    pre = srcnn.predict(Y, batch_size=1)
    
    # post-process output
    pre *= 255
    pre[pre[:] > 255] = 255
    pre[pre[:] < 0] = 0
    pre = pre.astype(np.uint8)
    
    # copy Y channel back to image and convert to BGR
    temp = shave(temp, 6)
    temp[:, :, 0] = pre[0, :, :, 0]
    output = cv.cvtColor(temp, cv.COLOR_YCrCb2BGR)
    
    # remove border from reference and degraged image
    ref = shave(ref.astype(np.uint8), 6)
    degraded = shave(degraded.astype(np.uint8), 6)
    
    # image quality calculations
    scores = []
    scores.append(compare_images(degraded, ref))
    scores.append(compare_images(output, ref))
    
    # return images and scores
    return ref, degraded, output, scores
ref, degraded, output, scores = predict('images/flowers.bmp')

# print all scores for all images
print('Degraded Image: \nPSNR: {}\nMSE: {}\nSSIM: {}\n'.format(scores[0][0], scores[0][1], scores[0][2]))
print('Reconstructed Image: \nPSNR: {}\nMSE: {}\nSSIM: {}\n'.format(scores[1][0], scores[1][1], scores[1][2]))


# display images as subplots
fig, axs = plt.subplots(1, 3, figsize=(20, 8))
axs[0].imshow(cv.cvtColor(ref, cv.COLOR_BGR2RGB))
axs[0].set_title('Original')
axs[1].imshow(cv.cvtColor(degraded, cv.COLOR_BGR2RGB))
axs[1].set_title('Degraded')
axs[2].imshow(cv.cvtColor(output, cv.COLOR_BGR2RGB))
axs[2].set_title('SRCNN')

# remove the x and y ticks
for ax in axs:
    ax.set_xticks([])
    ax.set_yticks([])

for file in os.listdir('images'):

    # perform super-resolution
    ref, degraded, output, scores = predict('images/{}'.format(file))

    # display images as subplots
    fig, axs = plt.subplots(1, 3, figsize=(20, 8))
    axs[0].imshow(cv.cvtColor(ref, cv.COLOR_BGR2RGB))
    axs[0].set_title('Original')
    axs[1].imshow(cv.cvtColor(degraded, cv.COLOR_BGR2RGB))
    axs[1].set_title('Degraded')
    axs[1].set(xlabel = 'PSNR: {}\nMSE: {} \nSSIM: {}'.format(scores[0][0], scores[0][1], scores[0][2]))
    axs[2].imshow(cv.cvtColor(output, cv.COLOR_BGR2RGB))
    axs[2].set_title('SRCNN')
    axs[2].set(xlabel = 'PSNR: {} \nMSE: {} \nSSIM: {}'.format(scores[1][0], scores[1][1], scores[1][2]))

    # remove the x and y ticks
    for ax in axs:
        ax.set_xticks([])
        ax.set_yticks([])

    print('Saving {}'.format(file))
    fig.savefig('output/{}.png'.format(os.path.splitext(file)[0]))
    plt.close()
