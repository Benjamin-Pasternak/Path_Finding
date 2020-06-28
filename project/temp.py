import matplotlib as mpl
import numpy as np
from queue import PriorityQueue
import heapq


# this file imports user selected grid
# num is the user's number choice
def create_arr(num):
    temp = './arrs/backTrackerMazes/' + str(num) + '.txt'
    grid = np.loadtxt(fname=temp, dtype=bool)
    return grid
    # print(grid)


class priority_queue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class state:
    def __init__(self, parent, pos):
        self.children = []
        self.parent = parent
        self.pos = pos
        self.g = 0
        self.h = 0
        self.f = 0
        self.search = 0

    # override
    def __eq__(self, other):
        return self.pos == other.pos


# this function computes the manhattan distance given 2 tuples (x,y)
# ex: xy1 = (2, 2), xy2 = (4, 4) yields 4
def manhattan_distance(xy1, xy2):
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


# does as title suggests, makes code prettier imo
def f_val_calc(h, g):
    return h + g


class maze:
    # constructor
    def __init__(self, grid):
        self.start = state(None, (0, 0))
        self.goal = state(None, (100, 100))
        self.grid = grid

    # main
    def driver(self):
        counter = 0
        start = self.start
        goal = self.goal
        # line 18
        while start.pos != goal.pos:
            counter = counter + 1
            start.search = counter
            goal.search = counter

            open_set = PriorityQueue()
            # like a hash set
            closed_set = set()
            # like a hashset
            blocked = set()

            # calc values needed for the search! line 25
            start.h = manhattan_distance(start.pos, goal.pos)
            start.f = f_val_calc(start.h, start.g)
            open_set.put((start.f, start))

            temp1 = open_set.get()
            open_set.put((temp1[0], temp1[1]))

            while goal.g > temp1[0]:
                # first open_set.get() = tuple (priority: f, item: state)
                explore = open_set.get()[1]
                closed_set.add(explore)

                # need to make sure its walkable terrain

    # for finding path from immediate node, includes information about blockages, which the other find_children does not
    def find_children_with_blockage(self, s, grid):
        # directions for finding position of adjacent tiles to current state
        left = (-1, 0)
        right = (1, 0)
        up = (0, 1)
        down = (0, -1)

        # find the children by by looking at adjacent squares, and add them to list for the state
        # check also for if squares are walkable
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

    # computePath line 1
    # while goal.g > open_set.elements[1].g:
    #     print('hi')


temp = maze(create_arr(50))
temp.driver()
