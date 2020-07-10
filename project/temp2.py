import sys
import os
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import tracemalloc
from min_heap import *
import time, timeit

# to do list
# 1. fix sift up and sift down to be able to prioritize based on high or low g
# 2. finish the program

# this file imports user selected grid
# num is the user's number choice
def create_arr(num):
    temp = './arrs/randGrid/' + str(num) + '.txt'
    grid = np.loadtxt(fname=temp, dtype=bool)
    return grid
    # print(grid)


