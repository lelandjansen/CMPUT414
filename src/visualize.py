#!/usr/bin/env python2
import numpy as np
import pptk
import time
from math import pi
import os
import sys
from PIL import Image
import datetime
import math

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
for phi in [-pi/12, 0, pi/12]:
    for theta in [-pi/12, 0, pi/12]:
        for r in [5, 5.5, 6]:
            camera_x = r*math.sin(theta)*math.cos(phi)
            camera_y = r*math.sin(theta)*math.sin(phi)
            camera_z = r*math.cos(theta)
            
            colors = []
            for p in xyz:
               distance = math.sqrt((camera_x-p[0])**2 + (camera_y-p[1])**2 + (camera_z-p[2])**2)
               colors.append(distance)
            v.attributes(colors)
            
            v.set(lookat = [x_center, y_center, z_center],
                  phi = phi,
                  theta = theta,
                  r = r,
                  point_size = 0.01,
                  bg_color = [0, 0, 0, 0],
                  show_grid = False,
                  show_info = False,
                  show_axis = False)
            time.sleep(sleep)
            path = os.path.join(dir_path, '../out/tmp',
                '{}-{}-{}.png'.format(phi, theta, r))
            images.append(path)
            v.capture(path)
time.sleep(sleep)
v.close()

images = map(Image.open, images) 
widths, heights = zip(*(image.size for image in images))
total_width = sum(widths)
max_height = max(heights)
new_image = Image.new('RGB', (total_width, max_height))
x_offset = 0
for image in images:
    new_image.paste(image, (x_offset, 0))
    x_offset += image.size[0]
path = os.path.join(dir_path, '../out/',
        '{}.png'.format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
new_image.save(path)
