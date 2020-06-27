import matplotlib as mpl
import heapq
mpl.use('PS')
import matplotlib.pyplot as plt
import numpy as np



# this function computes the manhattan distance given 2 tuples (x,y)
# ex:
# xy1 = (2, 2)
# xy2 = (4, 4)
# yields 4
def manhattan_distance(xy1, xy2):
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def compute_path(arr):



# note heapq should be sorted based on f which is g + h or step cost + heuristic (manhattan distance)
# test stuff
xy1 = (2, 2)
xy2 = (4, 4)
print(manhattan_distance(xy1, xy2))
print(float('inf'))
col = 5
row = 5
# open set = heapq
# closed set = visited
grid = np.ones((row, col), dtype=bool)


# print(grid)


class Node:
    def __init__(self, bool):
        self.g = 0
        self.h = 0
        self.f = 0
