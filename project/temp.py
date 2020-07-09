import sys
import os
import matplotlib as mpl
import numpy as np
from min_heap import *
import time


# to do list
# 1. fix sift up and sift down to be able to prioritize based on high or low g
# 2. finish the program

# this file imports user selected grid
# num is the user's number choice
# def create_arr(num):
#     temp = './arrs/backTrackerMazes/' + str(num) + '.txt'
#     grid = np.loadtxt(fname=temp, dtype=bool)
#     return grid
#     # print(grid)


class state:
    def __init__(self, parent, pos):
        self.children = []
        self.parent = parent
        self.pos = pos
        self.g = 0
        self.h = 0
        self.f = 0
        self.search = 0

    # override default tostring
    def __repr__(self):
        return str(self.pos) + "\ng h f: " + str(self.g) + " " + str(self.h) + " " + str(self.f)

    # #override
    # def __eq__(self, other):
    #     return self.pos[0] == other.pos[0] and self.pos[1] == other.pos[1]

    def update_f(self):
        self.f = self.g + self.h

    # for finding path from immediate node, includes information about blockages, which the other find_children does not
    # can shorten substantially by putting all left right .. into array and then iterating through that in the for loop
    # that would get rid of the giant if block
    def find_children_with_blockage(self, s, grid, closed_list):
        # directions for finding position of adjacent tiles to current state
        neighbors = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        for i in range(4):
            temp_pos = (s.pos[0] + neighbors[i][0], s.pos[1] + neighbors[i][1])
            # print(any(x.pos == temp_pos for x in closed_list))
            # sys.exit()
            # check if new pos is within range and if new spot is walkable
            # if 0 <= temp_pos[0] < 101 and 101 > temp_pos[1] >= 0 and not grid[temp_pos[0]][temp_pos[1]]:
            if 0 <= temp_pos[0] <= 4 and 4 >= temp_pos[1] >= 0 and grid.grid[temp_pos[0]][temp_pos[1]] is not True \
                    and any(x.pos == temp_pos for x in closed_list) == False:
                s.children.append(state(s, temp_pos))
            # elif 0 <= temp_pos[0] < 101 and 101 > temp_pos[1] >= 0 and grid.grid[temp_pos[0]][temp_pos[1]]:
            elif 0 <= temp_pos[0] <= 4 and 4 >= temp_pos[1] >= 0 and grid.grid[temp_pos[0]][temp_pos[1]] is True \
                and any(x.pos==temp_pos for x in closed_list) == False:
                grid.blocked.append(temp_pos)
                # print(temp_pos)
        # print(grid.blocked)
        # print(len(s.children))
        # print(s.children[0].pos)
        # sys.exit()
        return s

    def find_children_no_blockage(self, s, grid, closed_list):
        # directions for finding position of adjacent tiles to current state
        neighbors = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        for i in range(4):
            temp_pos = (s.pos[0] + neighbors[i][0], s.pos[1] + neighbors[i][1])
            # check if new pos is within range and if new spot is walkable
            # if 0 <= temp_pos[0] < 101 and 101 > temp_pos[1] >= 0 and temp_pos not in grid.blocked:
            if 0 <= temp_pos[0] <= 4 and 4 >= temp_pos[1] >= 0 and temp_pos not in grid.blocked \
                    and any(x.pos == temp_pos for x in closed_list) == False:
                s.children.append(state(s, temp_pos))
                # print(temp_pos)

        # print(len(s.children))
        return s




def find_path(s, start):
    path = []
    tmp = s
    while tmp is not start and tmp is not None:
        path.append(tmp.pos)
        tmp = tmp.parent
    return path


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
        # self.start = state(None, (0, 0))
        # self.goal = state(None, (100, 100))
        self.start = state(None, (4, 2))
        self.goal = state(None, (4, 4))
        self.grid = grid
        self.blocked = []
        self.path = []

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
            goal.g = 1000

            # line 24
            open_set = min_heap()
            # like a hash set
            closed_set = []

            # calc values needed for the search! line 25
            start.h = manhattan_distance(start.pos, goal.pos)
            start.f = f_val_calc(start.h, start.g)
            open_set.push((start.f, start))
            print("start: " + str(start))

            # beginning of A*
            # flag determines which child gathering function we are using
            # with blockage is for immediately visible squares
            # no blockage is for after the iteration in A*

            flag = True
            # when does this stop? I think it will stop if you cant find anything to expand??? but how???
            # print(self.start.g)
            # print(self.start.h)
            # print(open_set.heap_list)
            # print(open_set.peek())
            # sys.exit()
            temp_value = open_set.peek()
            # print(open_set.heap_list)
            while goal.g > temp_value:  # open_set.peek():
                # first open_set.get() = tuple (priority: f, item: state)
                # print(open_set.heap_list)
                # print('ITERATION 1')
                # print(open_set.heap_list)
                if open_set.current_size == 0:
                    break
                explore = open_set.pop()
                explore = explore[1]
                if explore.pos == goal.pos:
                    goal.parent = explore.parent
                    break
                closed_set.append(explore)
                if flag:
                    explore.children = []
                    explore = explore.find_children_with_blockage(explore, self, closed_set)
                    flag = False
                else:
                    explore = explore.find_children_no_blockage(explore, self, closed_set)  # , self.blocked)

                print(explore.children)

                # what if explore.children = empty???
                # need to figure out tie break
                count = 0
                for child in explore.children:
                    count = count + 1
                    if child.search < counter:
                        child.g = 1000
                        child.search = counter
                    if child.g > explore.g + 1:
                        # print(True)
                        # print('woof \n \n')
                        child.g = explore.g + 1
                        child.parent = explore
                        # new 12:37 pm july 7 2020
                        child.h = manhattan_distance(child.pos, goal.pos)
                        child.f = child.h + child.g
                        print("child: " + str(child))
                        # on line 12 but need to do stuff with the heap first
                        # if child has already been explored by some other parent, then you need to reset its f value
                        # time.sleep(5)
                        # if count == 3:
                            #print(len(open_set.heap_list))
                        temp = open_set.generate_temp()
                        # print(len(temp))
                        # self.checker(child, temp)
                        if any(x.pos == child.pos for x in temp):  # self.checker(child, open_set.heap_list):
                            open_set.reset_priority(child)
                        open_set.push((child.f, child))
                        ### HEREERERERERERER
                    # open_set.printer()
                    # print(open_set.heap_list)
                    if count == 4:
                        sys.exit()

            # since heap always has 0 as first element, empty heap will be 1 long
            if open_set.current_size == 1:
                sys.exit('CANNOT REACH TARGET...')

            # do we reset everything after this!!! YES WE DO!
            # this should be valid
            optimistic_path = find_path(goal,start)
            #optimistic_path.reverse()

            # moving agent along the path
            reverse_it = len(optimistic_path)-1
            while reverse_it >= 0:
                # basically if point on grid is blocked or true its no good
                if optimistic_path[reverse_it] not in self.blocked and \
                        self.grid[optimistic_path[reverse_it][0]][optimistic_path[reverse_it][1]] != True \
                        and start.pos != goal.pos:
                    self.path.append(optimistic_path[reverse_it])
                    new_start = None
                    for i, x in enumerate(start.children):
                        a = x.pos == optimistic_path[reverse_it]
                        if x.pos == optimistic_path[reverse_it]:
                            new_start = start.children[i]
                    start = new_start
                else:
                    break
                reverse_it -= 1

    def check_if_valid_path(self):
        for i in self.path:
            if self.grid[i[0]][i[1]] == True:
                print('bad_Path')
        print('good path')

    def checker(self, child, heap):
        for i, x in enumerate(heap):
            if i != 0:
                if child.pos[0] == heap[i][0].pos[1] and child.pos[1] == heap[i][1].pos[1]:
                    return True
        return False

        # now to move the agent


# sys.exit()
grid = [[False, False, False, False, False],
        [False, False, True, False, False],
        [False, False, True, True, False],
        [False, False, True, True, False],
        [False, False, False, True, False]]
# print(grid[4][1])
# sys.exit()
temp_grid = maze(grid)
temp_grid.driver()
print('hiya')
temp_grid.check_if_valid_path()

# temp = maze(create_arr(50))
# temp.driver()
# p = set()
# p.add((0, 1))
# k = state(None, (0, 0))
# l = k.find_children_with_blockage(k, temp.grid, p)
# print(l[1])
# k.pos = (0, 1)
# l = k.find_children_with_blockage(k, temp.grid, p)
# print(l[1])


# temp.find_children_with_blockage(temp.start, temp.grid, p)
# temp.find_children_no_blockage(temp.start, temp.grid, p)
