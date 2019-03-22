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
import math

sleep = 0.2
dir_path = os.path.dirname(os.path.realpath(__file__))

path = os.path.join(dir_path,
        '../data/sydney-urban-objects-dataset/objects/car.23.17038.csv')
xyz = np.loadtxt(open(path, 'rb'), delimiter=',', usecols=range(3,6))
x_min, y_min, z_min = xyz.min(axis=0)
x_max, y_max, z_max = xyz.max(axis=0)
x_center = (x_min + x_max) / 2.0
y_center = (y_min + y_max) / 2.0
z_center = (z_min + z_max) / 2.0
xyz = np.array([(p[0] - x_center, p[1] - y_center, p[2] - z_center) for p in xyz])
v = pptk.viewer(xyz, xyz[:, 0])
 
images = []
for phi in np.arange(0.0, pi, pi / 8.0):
    for theta in np.arange(0.0, 2 * pi, pi / 8.0):
        r = 6.5
        camera_x = r * math.sin(phi) * math.cos(theta)
        camera_y = r * math.sin(phi) * math.sin(theta)
        camera_z = r * math.cos(phi)
        print camera_x, camera_y, camera_z
        colors = []
        for p in xyz:
            distance = sqrt((camera_x-p[0])**2 + (camera_y-p[1])**2 + (camera_z-p[2])**2)
            colors.append(distance)
        v.attributes(colors)
        v.color_map('cool')
        v.set(phi = phi,
              theta = theta,
              r = r,
              point_size = 0.4,
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
