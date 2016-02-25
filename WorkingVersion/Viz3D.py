# 3D Volume Graph and Backmap
# 2016/02/25
# Cheng Zhang (czhang0328@gmail.com)
# Class and functions in this file is modified from draw_volume.py

from os import listdir
from os.path import isfile, join
import fileinput
import numpy as np
from mayavi import mlab

class Viz3D(object):
    
    