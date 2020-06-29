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
    def pop(self):
        retval = self.heap_list[1]
        self.heap_list[1] = self.heap_list[self.current_size]
        self.current_size = self.current_size - 1
        self.heap_list.pop()
        self.sift_down(1)
        return retval

    # returns but does not remove smallest element in heap
    def peek(self):
        return self.heap_list[1]

# k = min_heap()
# k.push((1, "happy"))
# k.push((2, "happy"))
# k.push((3, "happy"))
# k.push((9, "happy"))
# k.push((7, "happy"))
# k.push((20, "happy"))
# k.push((4, "happy"))
# k.push((5, "happy"))
# print(k.heap_list)
# k.pop()
# print(k.heap_list)
# print(k.peek())
# print(k.heap_list)
