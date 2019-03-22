#!/usr/bin/env python2
import numpy as np
import pptk
import time
from math import pi
import os
import sys
from PIL import Image
import datetime

sleep = 0.2
dir_path = os.path.dirname(os.path.realpath(__file__))

xyz = pptk.rand(100, 3)
v = pptk.viewer(xyz, xyz[:, 2])

# path = os.path.join(dir_path,
#         '../data/sydney-urban-objects-dataset/objects/car.61.25322.csv')
# xyz = np.loadtxt(open(path, 'rb'), delimiter=',', usecols=range(1,4))
# x_min, y_min, z_min = xyz.min(axis=0)
# x_max, y_max, z_max = xyz.max(axis=0)
# x_center = (x_min + x_max) / 2.0
# y_center = (y_min + y_max) / 2.0
# z_center = (z_min + z_max) / 2.0
# v.set(lookat = [x_center, y_center, z_center],
# #      phi = 0,
# #      theta = pi,
#       r = 200,
#       view = [x_center, y_center, z_center],
# #      up = [x_center, y_center, z_center],
#       point_size = 1,
#       bg_color = [0, 0, 0, 0],
#       show_grid = False,
#       show_info = True,
#       show_axis = False)
# 
# while True:
#     pass

images = []
for phi in [-pi/12, 0, pi/12]:
    for theta in [-pi/12, 0, pi/12]:
        for r in [2.5, 3, 3.5]:
            v.set(lookat = [0.5, 0.5, 0.5],
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