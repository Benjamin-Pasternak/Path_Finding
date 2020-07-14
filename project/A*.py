import sys
import timeit
import tracemalloc
from time import sleep
import numpy as np
from min_heap import *
from gen_maze import *


# this file imports user selected grid
# num is the user's number choice
def create_arr(num):
    if num < 10:
        temp = './arrs/randGrid/0' + str(num) + '.txt'
    elif num < 50:
        temp = './arrs/randGrid/' + str(num) + '.txt'
    else:
        temp = './arrs/backTrackerMazes/' + str(num) + '.txt'
    grid = np.loadtxt(fname=temp, dtype=bool)
    return grid


class state:
    def __init__(self, pos):
        self.children = []
        self.parent = None
        self.path = None
        self.pos = pos
        self.g = 0
        self.h = 0
        self.f = 0
        self.search = 0
        self.in_open = False

    # override
    def __eq__(self, other):
        return self.pos == other.pos

    # override
    def __repr__(self):
        # retstr = str(self.pos) + "\ng h f: " + str(self.g) + " " + str(self.h) + " " + str(self.f)
        # if self.parent is not None:
        #     retstr = retstr + "\nparent" + str(self.parent.pos)
        # if len(self.children) > 0:
        #     retstr = retstr + "\nchildren:" + str(self.children)
        # return retstr
        return str(self.pos)

    def update_f(self):
        self.f = self.g + self.h

    def manhattan_distance(self, target):
        self.h = abs(self.pos[0] - target[0]) + abs(self.pos[1] - target[1])

    # flag = False to ignore blockage
    def find_children(self, maze, closed, blocked, flag=True):
        neighbors = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        for action in neighbors:
            temp_pos = (self.pos[0] + action[0], self.pos[1] + action[1])
            if 0 <= temp_pos[0] < maze.size[0] and 0 <= temp_pos[1] < maze.size[1]:
                if temp_pos in closed or temp_pos in blocked:
                    continue
                if flag and maze.grid[temp_pos[0]][temp_pos[1]]:
                    closed.append(temp_pos)
                    blocked.append(temp_pos)
                    continue
                self.children.append(temp_pos)

    def find_children_addaptive(self, maze, closed, blocked, closed2, a_flag, flag=True):
        neighbors = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        for action in neighbors:
            temp_pos = (self.pos[0] + action[0], self.pos[1] + action[1])
            if 0 <= temp_pos[0] < maze.size[0] and 0 <= temp_pos[1] < maze.size[1]:
                if temp_pos in closed or temp_pos in blocked:
                    continue
                if flag and maze.grid[temp_pos[0]][temp_pos[1]] and a_flag:
                    closed.append(temp_pos)
                    blocked.append(temp_pos)
                    continue
                self.children.append(temp_pos)

# Iterable class for list of states
class states_list:
    def __init__(self):
        self.stateList = []
        self.ptr = 0

    def append(self, state):
        left = 0
        right = len(self.stateList) - 1
        curri = 0
        while left <= right:
            curri = int((left + right) / 2)
            curr = self.stateList[curri]
            if curr.pos[0] + curr.pos[1] < state.pos[0] + state.pos[1]:
                left = curri + 1
                curri += 1
            if curr.pos[0] + curr.pos[1] > state.pos[0] + state.pos[1]:
                right = curri - 1
            if curr.pos[0] + curr.pos[1] == state.pos[0] + state.pos[1]:
                if curr.pos[0] <= state.pos[0]:
                    left = curri + 1
                    curri += 1
                if curr.pos[0] > state.pos[0]:
                    right = curri - 1
        self.stateList.insert(curri, state)

    def __iter__(self):
        # reset index before iteration
        self.ptr = 0
        return self

    def __next__(self):
        if len(self.stateList) > 0 and self.ptr < len(self.stateList):
            self.ptr += 1
            return self.stateList[self.ptr - 1]
        raise StopIteration()

    def find(self, state):
        left = 0
        right = len(self.stateList) - 1

        while left <= right:
            curri = int((left + right) / 2)
            curr = self.stateList[curri]
            if curr.pos[0] + curr.pos[1] < state.pos[0] + state.pos[1]:
                left = curri + 1
            if curr.pos[0] + curr.pos[1] > state.pos[0] + state.pos[1]:
                right = curri - 1
            if curr.pos[0] + curr.pos[1] == state.pos[0] + state.pos[1]:
                if curr.pos[0] < state.pos[0]:
                    left = curri + 1
                if curr.pos[0] > state.pos[0]:
                    right = curri - 1
                if curr.pos[0] == state.pos[0]:
                    return curr

        return None


class maze:
    # constructor
    def __init__(self, grid, backwards, start=None, end=None):
        self.size = (len(grid), len(grid[0]))

        # start
        if start is None:
            self.start = (0, 0)
        else:
            self.start = start

        # end
        if end is None:
            self.end = (self.size[0]-1, self.size[1]-1)
        else:
            self.end = end

        self.state_list = states_list()
        self.grid = grid
        if backwards:
            self.final_path = [self.end]
        else:
            self.final_path = [self.start]
        self.blocked_list = []
        self.max_g = len(grid) * 2

    # return new state with h calculated, else existing state
    def get_state(self, pos):
        temp = self.state_list.find(state(pos))
        if temp is None:
            temp = state(pos)
            temp.manhattan_distance(self.end)
            self.state_list.append(temp)
        return temp
    def get_state_backwards(self,pos):
        temp = self.state_list.find(state(pos))
        if temp is None:
            temp = state(pos)
            temp.manhattan_distance(self.start)
            self.state_list.append(temp)
        return temp

    # return empty list if target is not reached
    def make_path(self, s, g, final=False):
        retlist = [g]
        ptr = g

        if final:
            while ptr.path is not None and ptr is not s:
                retlist.append(ptr.path)
                ptr = ptr.path
        else:
            while ptr.parent is not None and ptr is not s:
                retlist.append(ptr.parent)
                ptr = ptr.parent

        if ptr is not s:
            return []
        retlist.reverse()
        return retlist

    def backwards_astar(self, log=False):
        counter = 0
        # initialize start and end states respectively
        start_state = state(self.start)
        end_state = state(self.end)
        self.state_list.append(start_state)
        self.state_list.append(end_state)

        while end_state is not start_state:
            # input()
            counter = counter + 1
            if log:
                print(start_state.pos)
                print(counter)

            end_state.g = 0
            end_state.children = []
            end_state.parent = None
            end_state.manhattan_distance(start_state.pos)
            end_state.update_f()
            end_state.search = counter


            start_state.g = float('inf')
            start_state.children = []
            start_state.parent = None
            start_state.update_f()
            start_state.search = counter

            open_list = min_heap()
            closed_list = []

            open_list.push((end_state.f * self.max_g - end_state.g, end_state))
            # open_list.push((start_state.f, start_state))

            # ComputePath
            flag = True
            # juicyflag = False
            while start_state.g > open_list.peek():
                # if juicyflag:
                #     break
                # print("open list:" + str(open_list))
                curr_state = open_list.pop()[1]
                # print("closed list:" + str(closed_list))
                closed_list.append(curr_state.pos)
                curr_state.find_children(self, closed_list, self.blocked_list, flag)
                flag = False
                for child_pos in curr_state.children:
                    child = self.get_state_backwards(child_pos)
                    if child.search < counter:
                        child.g = float('inf')
                        child.parent = None
                        child.children = []
                    if child.g > curr_state.g + 1:
                        child.g = curr_state.g + 1
                        child.update_f()
                        child.parent = curr_state
                        if child.in_open and child.search == counter:
                            open_list.reset_priority(child)
                        open_list.push((child.f * self.max_g - child.g, child))
                        # open_list.push((child.f, child))
                    child.search = counter
                    # if curr_state.pos == start_state.pos:
                    #     juicyflag = True

            if open_list.current_size == 0:
                print('Cannot reach target...')
                # print(self.final_path)
                return
            path = self.make_path(end_state, start_state)
            #path.reverse()
            # print("path:" + str(path))
            if len(path) != 0:
                # print("Stepped in")
                i = 1
                while i < len(path) and not grid[path[i].pos[0]][path[i].pos[1]]:
                    # input("ready, press enter")
                    # if not log:
                    #     sleep(0.05)
                    #     draw_grid(grid, path[i].pos)
                    if end_state.path is path[i]:
                        end_state.path = None
                    else:
                        pup = path[i].path
                        path[i].path = end_state
                        self.final_path.append(path[i].pos)
                    end_state = path[i]
                    i += 1
        #print("movement:" + str(self.final_path))
        # print("result:" + str(self.make_path(self.start, end_state, True)))

############################################################################################################
############################################################################################################
############################################################################################################
                                                #backwards A*
############################################################################################################
############################################################################################################
############################################################################################################

    def astar(self, log=False):
        counter = 0
        # initialize start and end states respectively
        start_state = state(self.start)
        end_state = state(self.end)
        self.state_list.append(start_state)
        self.state_list.append(end_state)

        while start_state is not end_state:
            # input()
            counter = counter + 1
            if log:
                print(start_state.pos)
                print(counter)

            start_state.g = 0
            start_state.children = []
            start_state.parent = None
            start_state.manhattan_distance(end_state.pos)
            start_state.update_f()
            start_state.search = counter

            end_state.g = float('inf')
            end_state.children = []
            end_state.parent = None
            end_state.update_f()
            end_state.search = counter

            open_list = min_heap()
            closed_list = []

            open_list.push((start_state.f * self.max_g - start_state.g, start_state))
            # open_list.push((start_state.f, start_state))

            # ComputePath
            peek = open_list.peek()
            flag = True
            while end_state.g > open_list.peek():
                # print("open list:" + str(open_list))
                curr_state = open_list.pop()[1]
                # print("closed list:" + str(closed_list))
                closed_list.append(curr_state.pos)
                curr_state.find_children(self, closed_list, self.blocked_list, flag)
                flag = False
                for child_pos in curr_state.children:
                    child = self.get_state(child_pos)
                    if child.search < counter:
                        child.g = float('inf')
                        child.parent = None
                        child.children = []
                    if child.g > curr_state.g + 1:
                        child.g = curr_state.g + 1
                        child.update_f()
                        child.parent = curr_state
                        if child.in_open and child.search == counter:
                            open_list.reset_priority(child)
                        open_list.push((child.f * self.max_g - child.g, child))
                        # open_list.push((child.f, child))
                    child.search = counter

            if open_list.current_size == 0:
                print('Cannot reach target...')
                # print(self.final_path)
                return
            path = self.make_path(start_state, end_state)
            # print("path:" + str(path))
            if len(path) != 0:
                # print("Stepped in")
                i = 1
                while i < len(path) and not grid[path[i].pos[0]][path[i].pos[1]]:
                    # input("ready, press enter")
                    # if not log:
                    #     sleep(0.05)
                    #     draw_grid(grid, path[i].pos)
                    if start_state.path is path[i]:
                        start_state.path = None
                    else:
                        pup = path[i].path
                        path[i].path = start_state
                        self.final_path.append(path[i].pos)
                    start_state = path[i]
                    i += 1
        # print("movement:" + str(self.final_path))
        # print("result:" + str(self.make_path(self.start, end_state, True)))

############################################################################################################
############################################################################################################
############################################################################################################
                                            # Adaptive A*
############################################################################################################
############################################################################################################
############################################################################################################

    # adaptive: f actual = actual path cost computed by previous a* - current g value
    # forward same thing but does h new at beginning of planning step
    # a* uses new herusitic at beginning of next planning
    # no need to do anything special on first iteration i think
    def adaptive_astar(self, log=False):
        flag_addapt = True
        first_iteration_flag = False
        gcount = 0

        counter = 0
        # initialize start and end states respectively
        start_state = state(self.start)
        end_state = state(self.end)
        self.state_list.append(start_state)
        self.state_list.append(end_state)
        # should be path.length-1 or 2
        f_actual = 0
        while start_state is not end_state:
            if first_iteration_flag:
                for x in closed_list2:
                    x.h = f_actual - x.g
            first_iteration_flag = True
            # if first_iteration_flag:
            #     for
            #     start_state.h = f_actual - start_state.g
            # first_iteration_flag = True
            #for x in closed_list:


            # input()
            counter = counter + 1
            if log:
                print(start_state.pos)
                print(counter)

            start_state.g = 0
            start_state.children = []
            start_state.parent = None
            #start_state.manhattan_distance(end_state.pos)
            start_state.update_f()
            start_state.search = counter

            end_state.g = float('inf')
            end_state.children = []
            end_state.parent = None
            end_state.update_f()
            end_state.search = counter

            open_list = min_heap()
            closed_list = []
            closed_list2 = []

            open_list.push((start_state.f * self.max_g - start_state.g, start_state))
            # open_list.push((start_state.f, start_state))

            # ComputePath
            peek = open_list.peek()
            flag = True
            while end_state.g > open_list.peek():
                # print("open list:" + str(open_list))
                curr_state = open_list.pop()[1]
                # print("closed list:" + str(closed_list))
                closed_list2.append(curr_state)
                closed_list.append(curr_state.pos)
                gcount = gcount + 1
                #print(gcount)
                curr_state.find_children_addaptive(self, closed_list, self.blocked_list, closed_list2, flag_addapt,
                                                   flag)
                flag = False
                for child_pos in curr_state.children:
                    child = self.get_state(child_pos)
                    if child.search < counter:
                        child.g = float('inf')
                        child.parent = None
                        child.children = []
                    if child.g > curr_state.g + 1:
                        child.g = curr_state.g + 1
                        child.update_f()
                        child.parent = curr_state
                        if child.in_open and child.search == counter:
                            open_list.reset_priority(child)
                        open_list.push((child.f * self.max_g - child.g, child))
                        # open_list.push((child.f, child))
                    child.search = counter

            if open_list.current_size == 0:
                print('Cannot reach target...')
                #print(self.final_path)
                return
            path = self.make_path(start_state, end_state)
            # -1 because we arent including start state in distance calc
            f_actual = len(path) - 1
            # print("path:" + str(path))
            if len(path) != 0:
                # print("Stepped in")
                i = 1
                while i < len(path) and not grid[path[i].pos[0]][path[i].pos[1]]:
                    # input("ready, press enter")
                    # if not log:
                    #     sleep(0.05)
                    #     draw_grid(grid, path[i].pos)
                    if start_state.path is path[i]:
                        start_state.path = None
                    else:
                        pup = path[i].path
                        path[i].path = start_state
                        self.final_path.append(path[i].pos)
                    start_state = path[i]
                    i += 1
        #print("movement:" + str(self.final_path))
        # print("result:" + str(self.make_path(self.start, end_state, True)))
        return gcount





















#
# s000
# 0001
# 0010
# 0000


tracemalloc.start()
# # grid = [[False, False, False, False],
# #         [False, False, False, True],
# #         [False, False, True, False],
# #         [False, False, False, False]]
#
# # grid = [[False, False, False, False],
# #         [False, False, False, False],
# #         [False, False, False, False],
# #         [False, False, False, False]]
# # grid = maze_generator(190, 0.4, True)
# # Cannot reach target...
# grid = [[False, False, True, False],
#         [False, True, True, False],
#         [False, True, False, False],
#         [False, False, False, False]]
#
#
#
# # Current memory usage is 3.342218MB; Peak was 3.361932MB
# # Time Taken: 11.730602829s
#
grid = create_arr(int(input("grid#")))
#
a = input("Log? (y/n)")
if a is "y":
    ab = True
else:
    ab = False
#
# # 0110000010
# # 0001000000
# # 0000000000
# # 0000010110
# # 0000001000
# # 0000000100
# # 0001100000
# # 1000100001
# # 0000001100
# # 1100100000
# # grid = [[False, False, False, False, True, True, False, False, True, False],
# #         [True, False, False, True, False, True, False, True, False, False],
# #         [False, False, True, True, False, False, False, True, True, False],
# #         [True, True, False, True, False, True, False, False, True, False],
# #         [False, True, True, False, False, False, False, False, False, False],
# #         [False, True, True, False, False, False, False, True, True, False],
# #         [False, True, False, False, True, True, False, False, True, True],
# #         [True, False, True, True, True, True, True, True, False, False],
# #         [True, False, True, True, False, True, True, True, True, True],
# #         [False, False, False, False, True, True, True, True, False, False]]
# # Output
# # movement:[(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (6, 1), (7, 1), (8, 1), (8, 2), (9, 2), (9, 3),
# #           (8, 3), (8, 4), (8, 5), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9)]
test_maze = maze(grid, False)
start = timeit.default_timer()
test_maze.adaptive_astar(ab)
stop = timeit.default_timer()
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
tracemalloc.stop()
time = stop - start
print('Time Taken: {}s'.format(time))

i=0
time_mem = []
while i <=49 :
    grid = create_arr(i)
    test_maze = maze(grid, False)
    start = timeit.default_timer()
    tracemalloc.start()
    c = test_maze.adaptive_astar(False)
    stop = timeit.default_timer()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    time = stop - start
    time_mem.append((c ,time, peak/10**6))
    print(i)
    i+=1

print(time_mem)
