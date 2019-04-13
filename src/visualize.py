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
from multiprocessing import Pool

SLEEP = 0.5
DIR_PATH = os.path.dirname(os.path.realpath(__file__))

def enumerate_files():
    path = os.path.join(DIR_PATH, '../data/sydney-urban-objects-dataset/objects/')
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    files  = [f for f in files if f.endswith('.csv')]
    vehicles = [f for f in files if
            '4wd' in f or
            'bus' in f or
            'car' in f or
            'trailer' in f or
            'truck' in f or 
            'van' in f or
            'ute' in f]
    pedestrians = [f for f in files if 'pedestrian' in f]
    other = [f for f in files if f not in vehicles and f not in pedestrians]
    return (other, vehicles, pedestrians)


def generate_perspectives(f, style):
    path = os.path.join(DIR_PATH, '../data/sydney-urban-objects-dataset/objects/', f)
    xyz = np.loadtxt(open(path, 'rb'), delimiter=',', usecols=range(3,6))
    x_min, y_min, z_min = xyz.min(axis=0)
    x_max, y_max, z_max = xyz.max(axis=0)
    x_center = (x_min + x_max) / 2.0
    y_center = (y_min + y_max) / 2.0
    z_center = (z_min + z_max) / 2.0
    xyz = np.array([(p[0] - x_center, p[1] - y_center, p[2] - z_center) for p in xyz])
    # v = pptk.viewer(xyz, xyz[:, 0])
    v = pptk.viewer(xyz)
     
    images = []
    for phi in np.arange(0.0, pi, pi / 8.0):
        for theta in np.arange(0.0, 2 * pi, pi / 4.0):
            r = 7.5
            if style != 'plain':
                print 'unknown style'
                return
            x_min, y_min, z_min = xyz.min(axis=0)
            x_max, y_max, z_max = xyz.max(axis=0)
            x_center = (x_min + x_max) / 2.0
            y_center = (y_min + y_max) / 2.0
            z_center = (z_min + z_max) / 2.0
            # camera_x = r * math.sin(phi) * math.cos(theta)
            # camera_y = r * math.sin(phi) * math.sin(theta)
            # camera_z = r * math.cos(phi)
            # colors = []
            # for p in xyz:
            #     distance = sqrt((camera_x-p[0])**2 + (camera_y-p[1])**2 + (camera_z-p[2])**2)
            #     colors.append(distance)
            # v.attributes(colors)
            # v.color_map('cool')
            v.set(lookat = [x_center, y_center, z_center],
                  phi = phi,
                  theta = theta,
                  r = r,
                  point_size = 0.02,
                  bg_color = [0, 0, 0, 0],
                  show_grid = False,
                  show_info = False,
                  show_axis = False)
            time.sleep(SLEEP)
            path = os.path.join(DIR_PATH, '../out/tmp',
                '{}-{}.png'.format(phi, theta))
            images.append(path)
            v.capture(path)
    time.sleep(SLEEP)
    v.close()
    return images


def join_perspectives(f, images, style):
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
    pre, _ = os.path.splitext(f)
    path = os.path.join(DIR_PATH, '../out/', '{}.{}.png'.format(style, pre))
    new_image.thumbnail((new_image.size[0] / 3, new_image.size[1] / 3), Image.ANTIALIAS)
    new_image.save(path)
    return path


def make_label(f, object_class):
    image = Image.open(f) 
    pre, _ = os.path.splitext(f)
    f = pre + '.txt'
    with open(f, 'a') as out:
        if object_class == 0:
            out.write("")
        else:
            for x in np.arange(0.0, image.width, image.width / 8.0):
                for y in np.arange(0.0, image.height, image.height / 8.0):
                    out.write(
                        '{} {} {} {} {}\n'.format(
                            object_class-1,
                            (x + image.width / 8.0 / 2.0) / image.width,
                            (y + image.height / 8.0 / 2.0) / image.height,
                            (image.width / 8.0) / image.width,
                            (image.height / 8.0) / image.height))
    return f


def main():
    types = enumerate_files()
    style = 'plain'
    for t in range(len(types)):
        for item in types[t]:
            perspectives = generate_perspectives(item, style)
            f = join_perspectives(item, perspectives, style)
            f = make_label(f, t)


if __name__ == '__main__':
    main()
