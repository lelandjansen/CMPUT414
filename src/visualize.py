#!/usr/bin/env python2
import numpy as np
import pptk
import time
from math import pi
import os
import sys
from PIL import Image
import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))

xyz = pptk.rand(100, 3)
v = pptk.viewer(xyz, xyz[:, 2])
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
            time.sleep(0.1)
            path = os.path.join(dir_path, '../out/tmp',
                '{}-{}-{}.png'.format(phi, theta, r))
            images.append(path)
            v.capture(path)
time.sleep(0.1)
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
