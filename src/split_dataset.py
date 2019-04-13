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

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


path = os.path.join(DIR_PATH, '../out/')
files = [os.path.join('data/414/', f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.split('.')[-1] == 'png']
shuffle(files)

def outlines(fname, lines):
	f = fname + '.txt'
	with open(f, 'w') as out:
		for l in lines:
			out.write("{}\n".format(l))

train = files[:int(len(files) * .70)]
test = files[int(len(files) * .70):]

outlines('train', train)
outlines('test', test)
