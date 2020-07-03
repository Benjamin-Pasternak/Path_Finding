import matplotlib as mpl
import numpy as np
from queue import PriorityQueue
# from min_heap import *
import sys

# this file imports user selected grid
# num is the user's number choice
from .min_heap import min_heap


def create_arr(num):
    temp = './arrs/backTrackerMazes/' + str(num) + '.txt'
    grid = np.loadtxt(fname=temp, dtype=bool)
    return grid
    # print(grid)


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

    def update_f(self):
        self.f = self.g + self.h

    # for finding path from immediate node, includes information about blockages, which the other find_children does not
    # can shorten substantially by putting all left right .. into array and then iterating through that in the for loop
    # that would get rid of the giant if block
    def find_children_with_blockage(self, s, grid):
        # directions for finding position of adjacent tiles to current state
        neighbors = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        for action in neighbors:
            temp_pos = (s.pos[0] + action[0], s.pos[1] + action[1])
            # check if new pos is within range and if new spot is walkable
            if 0 <= temp_pos[0] < 101 and 101 > temp_pos[1] >= 0 and not grid[temp_pos[0]][temp_pos[1]]:
                s.children.append(state(None, temp_pos))
            elif 0 <= temp_pos[0] < 101 and 101 > temp_pos[1] >= 0 and grid[temp_pos[0]][temp_pos[1]]:
                grid.blocked.add(temp_pos)
                print(temp_pos)

        print(len(s.children))
        return s

    def find_children_no_blockage(self, s, grid, blocked):
        # directions for finding position of adjacent tiles to current state
        neighbors = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        for action in neighbors:
            temp_pos = (s.pos[0] + action[0], s.pos[1] + action[1])
            # check if new pos is within range and if new spot is walkable
            if 0 <= temp_pos[0] < 101 and 101 > temp_pos[1] >= 0 and temp_pos not in grid.blocked:
                s.children.append(state(s, temp_pos))
                print(temp_pos)

        print(len(s.children))
        return s


# this function computes the manhattan distance given 2 tuples (x,y)
# ex: xy1 = (2, 2), xy2 = (4, 4) yields 4
def manhattan_distance(xy1, xy2):
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


def generate_path(path, goal):
    if goal.parent is None:
        path.append(goal)
    else:
        generate_path(path, goal.parent)
        path.append(goal)


class maze:
    # constructor
    def __init__(self, grid):
        self.start = state(None, (0, 0))
        self.goal = state(None, (100, 100))
        self.grid = grid
        self.blocked = set()
        self.path = [self.start]

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
            goal.g = float('inf')

            # line 24
            open_set = min_heap()
            # like a hash set
            closed_set = set()

            # calc values needed for the search! line 25
            start.h = manhattan_distance(start.pos, goal.pos)
            start.update_f()
            open_set.push((start.f, start))

            # beginning of A*
            # flag determines which child gathering function we are using
            # with blockage is for immediately visible squares
            # no blockage is for after the iteration in A*

            # flag = True
            while goal.g > open_set.peek()[0]:
                # first open_set.get() = tuple (priority: f, item: state)
                explore = open_set.pop()[1]
                closed_set.add(explore)
                # if flag:
                #     explore = explore.find_children_with_blockage(explore, self.grid)
                #     flag = False
                # else:
                #     explore = explore.find_children_no_blockage(explore, self.grid, self.blocked)
                explore = explore.find_children_with_blockage(explore, self.grid)

                # what if explore.children = empty??? will just skip the whole for loop
                # need to figure out tie break
                for child in explore.children:
                    if child.search < counter:
                        child.g = float('inf')
                        child.search = counter
                        # this is line 9
                    if child.g > explore.g + 1:
                        child.g = explore.g + 1
                        child.parent = explore
                        child.h = manhattan_distance(child.pos, goal.pos)
                        child.update_f()
                        # on line 12 but need to do stuff with the heap first
                        if child in open_set.heap_list:
                            open_set.reset_priority(child)
                        open_set.push((child.f, child))

            # since heap always has 0 as first element, empty heap will be 1 long
            if open_set.current_size == 1:
                sys.exit('CANNOT REACH TARGET...')

        # plan is our optimistic path towards goal.
        plan = []
        generate_path(plan, goal)
        self.path = plan
        # now to move the agent
        # for i in self.path:
        #     print(i.pos)


temp = maze(create_arr(50))
# temp.driver()
p = set()
p.add((0, 1))
k = state(None, (0, 0))
l = k.find_children_with_blockage(k, temp.grid, p)
print(l[1])
k.pos = (0, 1)
l = k.find_children_with_blockage(k, temp.grid, p)
print(l[1])

# temp.find_children_with_blockage(temp.start, temp.grid, p)
# temp.find_children_no_blockage(temp.start, temp.grid, p)
