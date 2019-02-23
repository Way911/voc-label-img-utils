import cv2
import os
import glob
from shutil import copyfile

def remove_noise(img, path, prefix):
    # read Danish doc image 
    # img = cv2.imread('source/20190107_142818.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = cv2.GaussianBlur(img,(7,7), 0 , 0)
    img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv2.THRESH_BINARY,5,2)
    # ret, thresh_img = cv2.threshold(img, 180, 255, cv2.THRESH_BINARY_INV)
    # cv2.imshow('grey image',res)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    print('{}/{}.jpg'.format(dest_folder, filename))
    cv2.imwrite('{}/{}.jpg'.format(dest_folder, filename), img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

os.chdir('source')
dest_folder = '../result'
for img_file in glob.glob('*.jpg'):
    # Load image using OpenCV
    image = cv2.imread(img_file)
    filename = os.path.splitext(img_file)[0]
    xml = filename + '.xml'
    copyfile(xml, '{}/{}'.format(dest_folder, xml))
    remove_noise(image, path=dest_folder, prefix=filename)
