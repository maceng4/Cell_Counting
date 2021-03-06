from matplotlib import pyplot as plt
from matplotlib import image as image
from matplotlib import collections as mc
from PIL import Image,ImageOps,ImageEnhance
from skimage.exposure import equalize_adapthist
from skimage.io import imread, imsave
import skimage
import mahotas as mh
import cv2
import numpy as np
import scipy.misc
import argparse

def run(img_file, write_img, type): 
	preprocessed_img = image_preprocessing(img_file,type)
	blob_detection(preprocessed_img)

def image_preprocessing(img_file, type): #filtering, blurring: preprocessing for OpenCV's blob detection
	img = Image.open(img_file)
	img = np.asarray(img)
	img = cv2.GaussianBlur(img,(5,5),0)
	img = equalize_adapthist(img,clip_limit = 0.01) #doesn't seem to do much
	plt.imshow(img)
	plt.show()
	r,g,b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
	#RGBA image
	img_threshold = np.max((np.percentile(r, 60),np.percentile(g, 60),np.percentile(b, 60))) #60th percentile arbitrarily chosen: only pixels brighter than 60th percentile remain
	img[img < img_threshold] = 0
	# img = (img*255).astype(np.uint8)
	# img = cv2.Canny(img,100,100)
	plt.imshow(img)
	plt.show()
	return img


	# r = cv2.adaptiveThreshold(r,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,0) #Since Adaptive Thresholding works only on single channel images, we break the image into three channels, threshold each individiually, then splice them together
	# g = cv2.adaptiveThreshold(g,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,0)
	# b = cv2.adaptiveThreshold(b,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,0)
	# r = np.expand_dims(r, axis=2)
	# g = np.expand_dims(g, axis=2)
	# b = np.expand_dims(b, axis=2)
	# a = np.expand_dims(a, axis=2)
	# img = np.concatenate((r, g, b, a), axis=2)
def blob_detection(preprocessed_img): #returns 2d array of coordinates
	return skimage.feature.blob_log(preprocessed_img)
def write_to_file(write_img, write_file):#write_img is a numpy array, write_file is a filename
	Image.fromarray(write_img).save(write_file)
def main():
    global args
    parser = argparse.ArgumentParser(description='...')
    parser.add_argument("-f", "--file",
                    help="image file to read",
                    type=str, default=None)
    parser.add_argument("-w", "--write_file",
                    help="image file to write to",
                    type=str, default=None)
    parser.add_argument("-t", "--type",
                    help="type of image file",
                    type=str, default="RGBA")
    args = parser.parse_args()
    run(args.file,args.write_file,args.type)

if __name__ == "__main__":
    main()