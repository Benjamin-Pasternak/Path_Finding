import matplotlib as mpl
import heapq
mpl.use('PS')
import matplotlib.pyplot as plt
import numpy as np


col = 5
row = 5
# open set = heapq
#closed set = visited
grid = np.ones((row, col), dtype=bool)
print(grid)


class Node:
    def __init__(self, bool):
        self.g = 0
        self.h = 0
        self.f = 0

