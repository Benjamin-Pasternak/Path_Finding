import matplotlib as mpl
import numpy as np
from queue import PriorityQueue


# this file imports user selected grid
# num is the user's number choice
def create_arr(num):
    temp = './arrs/backTrackerMazes/' + str(num) + '.txt'
    grid = np.loadtxt(fname=temp, dtype=bool)
    return grid
    #print(grid)


class state:
    def __init__(self, parent, pos):
        self.children = []
        self.parent = parent
        self.pos = pos
        self.g = 0
        self.h = 0
        self.f = 0

    # override
    def __eq__(self, other):
        return self.pos == other.pos


class maze:
    # constructor
    def __init__(self, grid):
        self.start = (0, 0)
        self.end = (100, 100)
        self.grid = grid

    # this function computes the manhattan distance given 2 tuples (x,y)
    # ex: xy1 = (2, 2), xy2 = (4, 4) yields 4
    def manhattan_distance(self, xy1, xy2):
        return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


    def astar(self, grid, start=(0, 0), end=(100, 100)):
        # initialize start and end states respectively
        start_state = state(None, start)
        start_state.g = 0
        start_state.f = 0
        end_state = state(None, end)
        end_state.g = 0
        end_state.f = 0

        # initialize start open and closed lists respectively
        open_list = PriorityQueue()
        closed_list = []

        # add first state gets added into the priority queue
        open_list.put(start_state)

        while open_list.qsize()>0:
            expand_state = open_list.get()

    # need to make sure its walkable terrain
    def find_children(self, s, grid):
        # directions for finding position of adjacent tiles to current state
        left = (-1, 0)
        right = (1, 0)
        up = (0, 1)
        down = (0, -1)

        # find the children by by looking at adjacent squares, and add them to list for the state
        #check also for if squares are walkable
        for i in range(4):
            if i == 0:
                temp_pos = (s.pos[0] + left[0], s.pos[1] + left[1])
                # check if new pos is within range and if new spot is walkable
                if 0 <= temp_pos[0] < 101 and 101 > temp_pos[1] >= 0 and not grid[temp_pos[0]][temp_pos[1]]:
                    s.children.append(state(s, temp_pos))
                    print(temp_pos)
            elif i == 1:
                temp_pos = (s.pos[0] + right[0], s.pos[1] + right[1])
                # check if new pos is within range and if new spot is walkable
                if 0 <= temp_pos[0] < 101 and 101 > temp_pos[1] >= 0 and not grid[temp_pos[0]][temp_pos[1]]:
                    s.children.append(state(s, temp_pos))
                    print(temp_pos)
            elif i == 2:
                temp_pos = (s.pos[0] + up[0], s.pos[1] + up[1])
                # check if new pos is within range and if new spot is walkable
                if 0 <= temp_pos[0] < 101 and 101 > temp_pos[1] >= 0 and not grid[temp_pos[0]][temp_pos[1]]:
                    s.children.append(state(s, temp_pos))
                    print(temp_pos)
            elif i == 3:
                temp_pos = (s.pos[0] + down[0], s.pos[1] + down[1])
                # check if new pos is within range and if new spot is walkable
                if 0 <= temp_pos[0] < 101 and 101 > temp_pos[1] >= 0 and not grid[temp_pos[0]][temp_pos[1]]:
                    s.children.append(state(s, temp_pos))
                    print(temp_pos)
        print(len(s.children))
        return s


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
s = state(None, (1, 1))
k = maze(create_arr(50))
#print (k.grid)

k.find_children(s, k.grid)
