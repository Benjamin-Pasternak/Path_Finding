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

    # for finding path from immediate node, includes information about blockages, which the other find_children does not
    # can shorten substantially by putting all left right .. into array and then iterating through that in the for loop
    # that would get rid of the giant if block
    def find_children_with_blockage(self, s, grid):
        # directions for finding position of adjacent tiles to current state
        neighbors = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        for i in range(4):
            temp_pos = (s.pos[0] + neighbors[i][0], s.pos[1] + neighbors[i][1])
            # check if new pos is within range and if new spot is walkable
            if 0 <= temp_pos[0] < 101 and 101 > temp_pos[1] >= 0 and not grid[temp_pos[0]][temp_pos[1]]:
                s.children.append(state(s, temp_pos))
            elif 0 <= temp_pos[0] < 101 and 101 > temp_pos[1] >= 0 and grid[temp_pos[0]][temp_pos[1]]:
                grid.blocked.add(temp_pos)
                print(temp_pos)

        print(len(s.children))
        return s

    def find_children_no_blockage(self, s, grid):
        # directions for finding position of adjacent tiles to current state
        neighbors = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        for i in range(4):
            temp_pos = (s.pos[0] + neighbors[i][0], s.pos[1] + neighbors[i][1])
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


# does as title suggests, makes code prettier imo
def f_val_calc(h, g):
    return h + g


class maze:
    # constructor
    def __init__(self, grid):
        self.start = state(None, (0, 0))
        self.goal = state(None, (100, 100))
        self.grid = grid
        self.blocked = set()

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

            #line 24
            open_set = PriorityQueue()
            # like a hash set
            closed_set = set()

            # calc values needed for the search! line 25
            start.h = manhattan_distance(start.pos, goal.pos)
            start.f = f_val_calc(start.h, start.g)
            open_set.put((start.f, start))

            temp1 = open_set.get()
            open_set.put((temp1[0], temp1[1]))

            #beginning of A*
            #flag determines which child gathering function we are using
            # with blockage is for immediatly visible squares
            # no blockage is for after the iteration in A*
            flag = True
            while goal.g > temp1[0]:
                # first open_set.get() = tuple (priority: f, item: state)
                explore = open_set.get()[1]
                closed_set.add(explore)
                if flag:
                    temp = explore.find_children_with_blockage(explore, self.grid)
                    flag = flag+1
                else:
                    explore = explore.find_children_no_blockage(explore, self.grid)

                #what if explore.children = empty???
                # need to figure out tie break
                for child in explore.children:
                    if child.search < counter:
                        child.g = float('inf')
                        child.search = counter
                        #not sure if its actually +1 i'm guessing it is since in c(s,a) should be 1
                        #this is line 9
                    if child.g > explore.g + 1:
                        child.g = explore.g + 1
                        child.parent = explore
                        #on line 12 but need to do stuff with the heap first
                        if child in open_set:









temp = maze(create_arr(50))
#temp.driver()
p = set()
p.add((0,1))
k = state(None, (0, 0))
l = k.find_children_with_blockage(k, temp.grid, p)
print(l[1])
k.pos = (0, 1)
l = k.find_children_with_blockage(k, temp.grid, p)
print(l[1])




#temp.find_children_with_blockage(temp.start, temp.grid, p)
#temp.find_children_no_blockage(temp.start, temp.grid, p)
