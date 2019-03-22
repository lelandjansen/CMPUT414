#!/usr/bin/env python2
import numpy as np
import pptk
import time
from math import pi
from math import sqrt
import os
import sys
from PIL import Image
import datetime

sleep = 0.2
dir_path = os.path.dirname(os.path.realpath(__file__))

# xyz = pptk.rand(100, 3)

path = os.path.join(dir_path,
        '../data/sydney-urban-objects-dataset/objects/car.23.17038.csv')
xyz = np.loadtxt(open(path, 'rb'), delimiter=',', usecols=range(3,6))
x_min, y_min, z_min = xyz.min(axis=0)
x_max, y_max, z_max = xyz.max(axis=0)
x_center = (x_min + x_max) / 2.0
y_center = (y_min + y_max) / 2.0
z_center = (z_min + z_max) / 2.0
v = pptk.viewer(xyz, xyz[:, 0])
 
images = []
for phi in np.arange(0, 2 * pi, pi / 4.0): # [-pi/12, 0, pi/12]:
    for theta in np.arange(0, 2 * pi, pi / 4.0):
        v.set(lookat = [x_center, y_center, z_center],
              phi = phi,
              theta = theta,
              r = 6.5,
              point_size = 0.02,
              bg_color = [0, 0, 0, 0],
              show_grid = False,
              show_info = False,
              show_axis = False)
        time.sleep(sleep)
        path = os.path.join(dir_path, '../out/tmp',
            '{}-{}.png'.format(phi, theta))
        images.append(path)
        v.capture(path)
time.sleep(sleep)
v.close()

images = map(Image.open, images) 
widths, heights = zip(*(image.size for image in images))
total_width = sum(widths)
total_height = sum(heights)
n = int(sqrt(len(images)))
images = [images[i:i+n] for i in xrange(0, len(images), n)]
offset = images[0][0].size[0]
new_image = Image.new('RGB', (offset * len(images), offset * len(images[0])))
y_offset = 0
for row in images:
    x_offset = 0
    for image in row:
        new_image.paste(image, (x_offset, y_offset))
        x_offset += offset
    y_offset += offset
path = os.path.join(dir_path, '../out/',
        '{}.png'.format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
new_image.thumbnail((new_image.size[0] / 3, new_image.size[1] / 3), Image.ANTIALIAS)
new_image.save(path)
