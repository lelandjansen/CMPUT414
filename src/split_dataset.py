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
from random import shuffle

TRAIN_PERCENT = 0.7
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(DIR_PATH, '../out/')

def write_file(fname, lines):
	f = fname + '.txt'
	with open(f, 'w') as out:
		for l in lines:
			out.write("{}\n".format(l))


# find images in our `out` dataset and change their path 
# to the expected `data/414/*.png` format
files = [os.path.join('data/414/', f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.split('.')[-1] == 'png']
shuffle(files)

# split the test and train images
train = files[:int(len(files) * TRAIN_PERCENT)]
test = files[int(len(files) * TRAIN_PERCENT):]

# write the split txt files to disk
write_file('train', train)
write_file('test', test)
