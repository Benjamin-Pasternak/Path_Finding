import sys
import matplotlib as mpl
import numpy as np
from min_heap import *


# this file imports user selected grid
# num is the user's number choice
def create_arr(num):
    temp = './arrs/backTrackerMazes/' + str(num) + '.txt'
    grid = np.loadtxt(fname=temp, dtype=bool)
    return grid


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

    # override
    def __repr__(self):
        retstr = str(self.pos) + "\ng h f: " + str(self.g) + " " + str(self.h) + " " + str(self.f)
        if self.parent is not None:
            retstr = retstr + "\nparent" + str(self.parent.pos)
        if len(self.children) > 0:
            retstr = retstr + "\nchildren:" + str(self.children)
        return retstr

    def update_f(self):
        self.f = self.g + self.h

    def manhattan_distance(self, target):
        self.h = abs(self.pos[0] - target[0]) + abs(self.pos[1] - target[1])

    # flag = False to ignore blockage
    def find_children(self, maze, closed, flag=True):
        neighbors = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        for action in neighbors:
            temp_pos = (self.pos[0] + action[0], self.pos[1] + action[1])
            if 0 <= temp_pos[0] < maze.size[0] and 0 <= temp_pos[1] < maze.size[1]:
                if temp_pos in closed:
                    continue
                if flag and maze.grid[temp_pos[0]][temp_pos[1]]:
                    closed.append(temp_pos)
                    continue
                self.children.append(temp_pos)


# Iterable class for list of states
class states_list:
    def __init__(self):
        self.stateList = []
        self.ptr = 0

    def append(self, state):
        index = 0
        for i in self.stateList:
            if i.pos[0] + i.pos[1] < state.pos[0] + state.pos[1]:
                index = index + 1
                continue
            if i.pos[0] + i.pos[1] == state.pos[0] + state.pos[1]:
                if i.pos[0] < state.pos[0]:
                    index = index + 1
                    continue
                break
        self.stateList.insert(index, state)

    def __iter__(self):
        # reset index before iteration
        self.ptr = 0
        return self

    def __next__(self):
        if len(self.stateList) > 0 and self.ptr < len(self.stateList):
            self.ptr += 1
            return self.stateList[self.ptr - 1]
        raise StopIteration()


class maze:
    # constructor
    def __init__(self, grid, start=None, end=None):
        self.size = (len(grid), len(grid[0]))
        if start is None:
            self.start = (0, 0)
        else:
            self.start = start
        if end is None:
            self.end = (self.size[0], self.size[1])
        else:
            self.end = end
        self.state_list = states_list()
        self.grid = grid
        self.final_path = [self.start]

    # return empty list if target is not reached
    def make_path(self, s, g):
        retlist = [g]
        ptr = g
        while ptr.parent is not None:
            retlist.append(ptr.parent)
            if ptr is s:
                break
            ptr = ptr.parent
        if ptr is not s:
            return []
        retlist.reverse()
        return retlist

    def astar(self):
        counter = 0
        # initialize start and end states respectively
        start_state = state(None, self.start)
        end_state = state(None, self.end)
        self.state_list.append(start_state)
        self.state_list.append(end_state)

        while start_state is not end_state:
            print(start_state.pos)
            counter = counter + 1

            start_state.g = 0
            start_state.manhattan_distance(end_state.pos)
            start_state.update_f()
            start_state.search = counter

            end_state.g = float('inf')
            end_state.update_f()
            end_state.search = counter

            open_list = min_heap()
            closed_list = []

            open_list.push((start_state.f, start_state))

            # ComputePath()
            flag = True
            while end_state.g > open_list.peek():
                curr_state = open_list.pop()[1]
                # curr_state = state(None, (0, 0))
                # if curr_state.pos in closed_list:
                #     continue
                closed_list.append(curr_state.pos)
                curr_state.find_children(self, closed_list, flag)
                flag = False
                for child_pos in curr_state.children:
                    child = state(None, child_pos)
                    if child in self.state_list:
                        child = self.state_list.stateList[self.state_list.ptr - 1]
                    else:
                        child.manhattan_distance(end_state.pos)
                    if child.search < counter:
                        child.g = float('inf')
                        child.search = counter
                    if child.g > curr_state.g + 1:
                        child.g = curr_state.g + 1
                        child.update_f()
                        child.parent = curr_state
                        if child in open_list:
                            open_list.reset_priority(child)
                        open_list.push((child.f, child))

            path = self.make_path(start_state, end_state)
            if len(path) == 0:
                sys.exit('CANNOT REACH TARGET...')
            start_state = path[1]
            self.final_path.append(path[1].pos)


grid = [[False, False, False, False, False],
        [False, False, True, False, False],
        [False, False, True, True, False],
        [False, False, True, True, False],
        [False, False, False, True, False]]
test_maze = maze(grid, (4, 1), (4, 4))
test_maze.astar()
