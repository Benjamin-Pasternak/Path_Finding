# remove import later
import sys


class min_heap:
    # constructor
    def __init__(self):
        self.heap_list = [0]
        self.current_size = 0

    # The `SIFT UP' operation starts with a value in a leaf node. It moves the value up the path towards the root by
    # successively exchanging the value with the value in the node above. The operation continues until the value
    # reaches a position where it is less than its parent, or, failing that, until it reaches the root node.
    def sift_up(self, i):
        while i // 2 > 0:
            if self.heap_list[i][0] < self.heap_list[i // 2][0]:
                temp = self.heap_list[i // 2]
                self.heap_list[i // 2] = self.heap_list[i]
                self.heap_list[i] = temp
            i = i // 2

    # insert item into heap
    def push(self, k):
        self.heap_list.append(k)
        self.current_size = self.current_size + 1
        self.sift_up(self.current_size)

    # SIFT DOWN starts with a value in any node. It moves the value down the tree by successively exchanging the
    # value with the smaller of its two children. The operation continues until the value reaches a position where it
    # is less than both its children, or, failing that, until it reaches a leaf.
    def sift_down(self, i):
        while (i * 2) <= self.current_size:
            mc = self.min_child(i)
            if self.heap_list[i][0] > self.heap_list[mc][0]:
                temp = self.heap_list[i]
                self.heap_list[i] = self.heap_list[mc]
                self.heap_list[mc] = temp
            i = mc

    # find the minimum child between two positions
    def min_child(self, i):
        if i * 2 + 1 > self.current_size:
            return i * 2
        else:
            if self.heap_list[i * 2][0] < self.heap_list[i * 2 + 1][0]:
                return i * 2
            else:
                return i * 2 + 1

    # remove minimum item from list: returns the "popped" minimum element
    # input: void
    # output: state: minimum element
    def pop(self):
        # print('1: original heaplist')
        # print(self.heap_list )
        # print(' \n')
        retval = self.heap_list[1]
        # print('2: heaplist[1] or retval: ')
        # print(retval )
        # print(' \n')
        self.heap_list[1] = self.heap_list[self.current_size]
        # print('3a: setting heaplist[1] to heaplist[current size] maybe error')
        # print(self.heap_list[1])
        # print(' \n')
        # print('3b: heaplist current: ')
        # print(self.heap_list)
        # print(' \n')
        self.current_size = self.current_size - 1
        # print('4: current size: ')
        # print(self.current_size )
        # print(' \n')
        self.heap_list.pop()
        # print('5: heaplist after pop: ' )
        # print(self.heap_list)
        # print(' \n')
        self.sift_down(1)
        # print('6: heaplist after sift down: ')
        # print(self.heap_list)
        # print(' \n')
        # sys.exit()
        return retval

    # returns but does not remove smallest element in heap
    # input: void
    # output: state with highest priority
    def peek(self):
        return self.heap_list[1][0]

    # rebuilds heap with updated element priority
    # input: list = heap without the 0 at front
    # output: void
    def build_heap(self, list):
        i = len(list) // 2
        self.current_size = len(list)
        self.heap_list = [0] + list[:]
        while i > 0:
            self.sift_down(i)
            i = i - 1

    # # input: state to be updated. output: void. function resets state in the array
    # def reset_priority(self, k):
    #     # removes the 0 at the beginning of the list so that it can be heapified
    #     self.heap_list.pop(0)
    #     # linear search through heap for item to reset priority
    #     for i, x in enumerate(self.heap_list):
    #         # equals
    #         if x[0] - 1 == k[0] and x[1] == k[1]:
    #             temp0 = x[0]
    #             self.heap_list[i] = (temp0, x[1])
    #             break
    #     # build the heap
    #     self.build_heap(self.heap_list)
    #     # print(self.heap_list)

    # input: state to be updated. output: void. function resets state in the array
    def reset_priority(self, k):
        # removes the 0 at the beginning of the list so that it can be heapified
        self.heap_list.pop(0)
        # linear search through heap for item to reset priority
        for i, x in enumerate(self.heap_list):
            # equals
            if x[0] == k.f and x[1].pos == k.pos:
                k = (k.f, k)
                self.heap_list.remove(x)
                break
        # build the heap
        self.build_heap(self.heap_list)
        # print(self.heap_list)

    # def remove_element(self, k):
    #     temp = self.heap_list
    #     for i, x in enumerate(temp):
    #         # equals
    #         print(x[0])
    #         sys.exit()
    #         if x[0] - 1 == k[0] and x[1] == k[1]:
    #             k = (k[0] + 1, k[1])
    #             temp.remove(k)
    #             break
    #     self.heap_list = [0]
    #     for x in temp:
    #         self.heap_list.push((x[0], x[1]))
    #     print(self.heap_list)


    def generate_temp(self):
        temp = []
        count = 0
        for i in self.heap_list:
            if count == 0:
                count += 1
            else:
                temp.append(i[1])
                count+=1
        return temp

            #temp.append(x[1])
        #return temp



# organize minheap also on g
# basically just fix sift up and sift down

# p = min_heap()
# p.push((1, "happy"))
# p.push((2, "happy"))
# p.push((3, "happy"))
# p.push((9, "happy"))
# p.push((7, "happy"))
# p.push((20, "happy"))
# p.push((4, "happy"))
# p.push((5, "happy"))
# print(p.heap_list)
# p.remove_element(p.heap_list[3])
# print(p.heap_list)
# print(p.current_size)
# k = min_heap()
# k.heap_list = [(1, "happy"), (2, "happy"), (3, "happy"), (9, "happy"), (7, "happy"), (20, "happy"), (4, "happy"), (5, "happy")]
# k.buildHeap(k.heap_list)
# print(k.heap_list)
# print(k.current_size)

# print(k.heap_list)
# k.pop()
# print(k.heap_list)
# print(k.peek())
# print(k.heap_list)
# free  after 7 :
