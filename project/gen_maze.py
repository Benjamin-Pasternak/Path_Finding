# from numpy.random.mtrand import rand


# broken
# def maze_generator(size, dense, log=False):
#     grid = rand(size, size)
#     grid[0][0] = 1
#     grid[size - 1][size - 1] = 1
#     result = [[False] * size] * size
#     if log:
#         print("generating...")
#     saver = "grid = ["
#     for i in range(size):
#         printer = "# "
#         saver += "["
#         for j in range(size):
#             if grid[i][j] > dense:
#                 result[i][j] = False
#                 printer += "░"
#                 saver += "False"
#             else:
#                 result[i][j] = True
#                 printer += "█"
#                 saver += "True"
#             if j == size - 1:
#                 saver += "]"
#             if i == j == size - 1:
#                 saver += "]"
#             else:
#                 saver += ", "
#         if log:
#             print(printer)
#     if log:
#         print(saver)
#     return result


def draw_grid(grid, agent):
    max_x = 23
    max_y = 80
    if len(grid) > max_x:
        xl = agent[0] - int(max_x / 2)  # (x,  ) lower bound
        xu = agent[0] + int(max_x / 2)  # (x,  ) upper bound
        if xl < 0:
            xl = 0
            xu = max_x
        if xu > len(grid):
            xu = len(grid)
            xl = xu - max_x
    else:
        xl = 0
        xu = len(grid)

    if len(grid[0]) > max_y:
        yl = agent[1] - int(max_y / 2)  # ( , y) lower bound
        yu = agent[1] + int(max_y / 2)  # ( , y) upper bound
        if yl < 0:
            yl = 0
            yu = max_y
        if yu > len(grid[0]):
            yu = len(grid[0])
            yl = yu - max_y
    else:
        yl = 0
        yu = len(grid)

    for i in range(xl, xu):
        line = ""
        for j in range(yl, yu):
            if i == agent[0] and j == agent[1]:
                line += '*'
            elif grid[i][j]:
                line += '█'
            else:
                line += '░'
        print(line)
