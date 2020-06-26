

class node:
    def __init__(self, parent=None, pos=None):
        self.parent = parent
        self.pos = pos

        self.g = 0
        self.h = 0
        self.f = 0

