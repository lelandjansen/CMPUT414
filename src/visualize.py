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

SLEEP = 0.2
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DONE = '''
.
..
old
plain.4wd.0.2299.png
plain.4wd.0.2299.txt
plain.4wd.12.3582.png
plain.4wd.12.3582.txt
plain.4wd.13.270.png
plain.4wd.13.270.txt
plain.4wd.15.5563.png
plain.4wd.15.5563.txt
plain.4wd.16.6123.png
plain.4wd.16.6123.txt
plain.4wd.17.6783.png
plain.4wd.17.6783.txt
plain.4wd.18.7288.png
plain.4wd.18.7288.txt
plain.4wd.19.10974.png
plain.4wd.19.10974.txt
plain.4wd.2.3582.png
plain.4wd.2.3582.txt
plain.4wd.4.17038.png
plain.4wd.4.17038.txt
plain.4wd.6.16217.png
plain.4wd.6.16217.txt
plain.car.0.5463.png
plain.car.0.5463.txt
plain.car.10.6994.png
plain.car.10.6994.txt
plain.car.12.16217.png
plain.car.12.16217.txt
plain.car.1.5463.png
plain.car.1.5463.txt
plain.car.17.16217.png
plain.car.17.16217.txt
plain.car.21.16217.png
plain.car.21.16217.txt
plain.car.22.17038.png
plain.car.22.17038.txt
plain.car.25.17038.png
plain.car.25.17038.txt
plain.car.32.5463.png
plain.car.32.5463.txt
plain.car.39.16217.png
plain.car.39.16217.txt
plain.car.41.17589.png
plain.car.41.17589.txt
plain.car.42.17589.png
plain.car.42.17589.txt
plain.car.43.17589.png
plain.car.43.17589.txt
plain.car.46.8444.png
plain.car.46.8444.txt
plain.car.47.17589.png
plain.car.47.17589.txt
plain.car.48.17589.png
plain.car.48.17589.txt
plain.car.50.17589.png
plain.car.50.17589.txt
plain.car.53.23124.png
plain.car.53.23124.txt
plain.car.54.23124.png
plain.car.54.23124.txt
plain.car.55.23124.png
plain.car.55.23124.txt
plain.car.5.5563.png
plain.car.5.5563.txt
plain.car.59.23124.png
plain.car.59.23124.txt
plain.car.60.25322.png
plain.car.60.25322.txt
plain.car.62.2299.png
plain.car.62.2299.txt
plain.car.64.8444.png
plain.car.64.8444.txt
plain.car.66.4043.png
plain.car.66.4043.txt
plain.car.67.270.png
plain.car.67.270.txt
plain.car.68.270.png
plain.car.68.270.txt
plain.car.70.5100.png
plain.car.70.5100.txt
plain.car.71.5229.png
plain.car.71.5229.txt
plain.car.76.20631.png
plain.car.76.20631.txt
plain.car.78.10974.png
plain.car.78.10974.txt
plain.car.80.12346.png
plain.car.80.12346.txt
plain.car.83.12346.png
plain.car.83.12346.txt
plain.car.9.6994.png
plain.car.9.6994.txt
plain.truck.5.270.png
plain.truck.5.270.txt
plain.truck.6.5100.png
plain.truck.6.5100.txt
plain.truck.7.5100.png
plain.truck.7.5100.txt
plain.truck.9.6783.png
plain.truck.9.6783.txt
plain.van.10.2738.png
plain.van.10.2738.txt
plain.van.12.3725.png
plain.van.12.3725.txt
plain.van.14.3983.png
plain.van.14.3983.txt
plain.van.16.4093.png
plain.van.16.4093.txt
plain.van.1.6994.png
plain.van.1.6994.txt
plain.van.17.6994.png
plain.van.17.6994.txt
plain.van.19.5100.png
plain.van.19.5100.txt
plain.van.2.16217.png
plain.van.2.16217.txt
plain.van.24.6123.png
plain.van.24.6123.txt
plain.van.25.7288.png
plain.van.25.7288.txt
plain.van.26.7288.png
plain.van.26.7288.txt
plain.van.27.8254.png
plain.van.27.8254.txt
plain.van.28.8254.png
plain.van.28.8254.txt
plain.van.30.8444.png
plain.van.30.8444.txt
plain.van.31.8444.png
plain.van.31.8444.txt
plain.van.32.11204.png
plain.van.32.11204.txt
plain.van.4.17589.png
plain.van.4.17589.txt
plain.van.7.25322.png
plain.van.7.25322.txt
plain.van.8.12119.png
plain.van.8.12119.txt
plain.van.9.11886.png
plain.van.9.11886.txt
tmp
'''

def enumerate_files():
    path = os.path.join(DIR_PATH, '../data/sydney-urban-objects-dataset/objects/')
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    files  = [f for f in files if f.endswith('.csv')]
    vehicles = [f for f in files if '4wd' in f or 'car' in f or 'truck' in f or 'van' in f]
    pedestrians = [f for f in files if 'pedestrian' in f]
    return (vehicles, pedestrians)


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
            # camera_x = r * math.sin(phi) * math.cos(theta)
            # camera_y = r * math.sin(phi) * math.sin(theta)
            # camera_z = r * math.cos(phi)
            # colors = []
            # for p in xyz:
            #     distance = sqrt((camera_x-p[0])**2 + (camera_y-p[1])**2 + (camera_z-p[2])**2)
            #     colors.append(distance)
            # v.attributes(colors)
            # v.color_map('cool')
            v.set(phi = phi,
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
        for x in np.arange(0.0, image.width, image.width / 8.0):
            for y in np.arange(0.0, image.height, image.height / 8.0):
                out.write(
                    '{} {} {} {} {}\n'.format(
                        object_class,
                        (x + image.width / 8.0 / 2.0) / image.width,
                        (y + image.height / 8.0 / 2.0) / image.height,
                        (image.width / 8.0) / image.width,
                        (image.height / 8.0) / image.height))
    return f


def main():
    vehicles, pedestrians = enumerate_files()
    style = 'plain'
    counter = 0
    for vehicle in vehicles:
        counter += 1
        print counter
        if os.path.splitext(os.path.basename(vehicle))[0] in DONE:
            continue
        os.path.basename("hemanth.txt")
        perspectives = generate_perspectives(vehicle, style)
        f = join_perspectives(vehicle, perspectives, style)
        f = make_label(f, 0)


if __name__ == '__main__':
    main()
