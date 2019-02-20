import cv2
import os
import xml.etree.ElementTree as ET
import math
import glob
import numpy as np

def rotate_image(image, deg):
    if deg == 90:
        return np.rot90(image)
    if deg == 180:
        return np.rot90(image, 2)
    if deg == 270:
        return np.rot90(image, -1)  # Reverse 90 deg rotation

def rotate(image, xml, angle=270, path='', prefix=''):
    new_filename = prefix + '_r'
    h, w = image.shape[:2]
    rotated = rotate_image(image, angle)
    cv2.imwrite(path + '/{}.jpg'.format(new_filename),
                rotated, [cv2.IMWRITE_JPEG_QUALITY, 100])

    annotation = ET.Element('annotation')
    ET.SubElement(annotation, 'folder').text = 'images'
    ET.SubElement(annotation, 'filename').text = new_filename + '.jpg'
    ET.SubElement(annotation, 'path').text = 'images/' + \
        new_filename + '.jpg'

    source = ET.SubElement(annotation, 'source')
    ET.SubElement(source, 'database').text = 'Unknown'

    imageSize = ET.SubElement(annotation, 'size')
    ET.SubElement(imageSize, 'height').text = str(w)
    ET.SubElement(imageSize, 'width').text = str(h)
    ET.SubElement(imageSize, 'depth').text = str(rotated.shape[2])

    ET.SubElement(annotation, 'segmented').text = '0'
    for member in xml.findall('object'):
        xmin = int(member[4][0].text)
        ymin = int(member[4][1].text)
        xmax = int(member[4][2].text)
        ymax = int(member[4][3].text)
        obj = ET.SubElement(annotation, 'object')
        ET.SubElement(obj, 'name').text = member[0].text
        ET.SubElement(obj, 'pose').text = member[1].text
        ET.SubElement(obj, 'truncated').text = member[2].text
        ET.SubElement(obj, 'difficult').text = member[3].text

        bndbox = ET.SubElement(obj, 'bndbox')
        ET.SubElement(bndbox, 'xmin').text = str(h - ymin)
        ET.SubElement(bndbox, 'ymin').text = str(xmin)
        ET.SubElement(bndbox, 'xmax').text = str(h - ymax)
        ET.SubElement(bndbox, 'ymax').text = str(xmax)

    tree = ET.ElementTree(annotation)
    if tree.find('object') != None:
        tree.write(path + '/{}.xml'.format(new_filename))


os.chdir('source')
for img_file in glob.glob('*.jpg'):
    # Load image using OpenCV and
    # expand image dimensions to have shape: [1, None, None, 3]
    # i.e. a single-column array, where each item in the column has the pixel RGB value
    image = cv2.imread(img_file)
    filename = os.path.splitext(img_file)[0]
    xml = ET.parse(filename + '.xml')
    rotate(image, xml, angle=270, path='../result', prefix=filename)
