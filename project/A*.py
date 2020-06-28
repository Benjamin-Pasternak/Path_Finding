import matplotlib as mpl
import heapq

mpl.use('PS')
import matplotlib.pyplot as plt
import numpy as np

#this file imports user selected grid
#num is the user's number choice
def create_arr(num):
    temp = './arrs/backTrackerMazes/' + str(num) + '.txt'
    grid = np.loadtxt(fname=temp, dtype=bool)
    print(grid)


# this function computes the manhattan distance given 2 tuples (x,y)
# ex:
# xy1 = (2, 2)
# xy2 = (4, 4)
# yields 4
def manhattan_distance(xy1, xy2):
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


# def compute_path(arr, start, goal):


# priority queue for the openlist

class priority_queue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

# po
# class Grid (arr):
#     def __init__(self, width, height):
#         super.__init__(width, height)
#         self.weights = {}
#     def cost(self, from_node, to_node):
#         return self.weights.get(to_node, 1)


# note heapq should be sorted based on f which is g + h or step cost + heuristic (manhattan distance)
# test stuff


# xy1 = (2, 2)
# xy2 = (4, 4)
# print(manhattan_distance(xy1, xy2))
# print(float('inf'))
# col = 5
# row = 5
# # open set = heapq
# # closed set = visited
# #grid = np.ones((row, col), dtype=bool)
#
# print(grid)
# # print(grid)
