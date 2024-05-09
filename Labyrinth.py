import pygame
from timeit import default_timer as timer
from queue import PriorityQueue

WIDTH = 600
HEIGHT = 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Labyrinth")

# colors
BACKGROUND = (255, 255, 255)
PATH_CLOSE = (157, 246, 255) # checked fields
PATH_OPEN = (255, 114, 127) # frontier
GRID = (0, 0, 0)
WALL = (122, 122, 122) # Wall and Obstacles
START = (0, 255, 171)
END = (47, 255, 0)
PATH = (255, 210, 76)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = BACKGROUND
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    # return position of the node
    def get_pos(self):
        return self.row, self.col

    # reset
    def reset(self):
        self.color = BACKGROUND

    # mark checked nodes
    def make_close(self):
        self.color = PATH_CLOSE

    # mark the current frontier
    def make_open(self):
        self.color = PATH_OPEN

    # color the wall and obstacles
    def make_wall(self):
        self.color = WALL

    # color the starting point
    def make_start(self):
        self.color = START

    # color the ending point
    def make_end(self):
        self.color = END

    # color the shortest path
    def make_path(self):
        self.color = PATH

    # same as previous but for other purposes

    def is_closed(self):
        return self.color == PATH_CLOSE

    def is_opened(self):
        return self.color == PATH_OPEN

    def is_wall(self):
        return self.color == WALL

    def is_start(self):
        return self.color == START

    def is_end(self):
        return self.color == END

    # draw a node
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    # adding possible next moves (neighbours)
    def update_neighbours(self, grid):
        self.neighbours = []
        # checks for neighbours in -y axis (down)
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():
            self.neighbours.append(grid[self.row + 1][self.col])

        # checks for neighbours in y axis (up)
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.neighbours.append(grid[self.row - 1][self.col])

        # checks for neighbours in -x axis (left)
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():
            self.neighbours.append(grid[self.row][self.col + 1])

        # checks for neighbours in x axis (right)
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
            self.neighbours.append(grid[self.row][self.col - 1])


# heuristic function
def h(p1, p2):
    x1, y1 = p1  # splitting values from the tuples
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


# printing the path found in the algorithms
def print_path(node_path, current, draw, counter_start):
    pygame.display.set_caption("Labyrinth (Constructing Path...)")
    path_count = 0

    while current in node_path:
        current = node_path[current]
        current.make_path()
        path_count += 1
        draw()
    counter_end = timer()
    time_elapsed = counter_end - counter_start
    pygame.display.set_caption(
        f'Time Elapsed: {format(time_elapsed, ".2f")}s | Cells Visted: {len(node_path) + 1} | Shortest Path: {path_count + 1} Cells')


def aStar(draw, grid, start, end, counter_start):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    node_path = {}

    # setting every element to inf
    g_n = {element: float("inf") for row in grid for element in row}
    g_n[start] = 0

    f_n = {element: float("inf") for row in grid for element in row}
    f_n[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}
    while not open_set.empty():
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        # found end
        if current == end:
            print_path(node_path, end, draw, counter_start)
            end.make_end()
            return True

        # computing neighbouring weights
        for neighbour in current.neighbours:
            tmp_g_n = g_n[current] + 1

            if tmp_g_n < g_n[neighbour]:
                node_path[neighbour] = current
                g_n[neighbour] = tmp_g_n
                f_n[neighbour] = tmp_g_n + h(neighbour.get_pos(), end.get_pos())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_n[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()

        draw()
        if current != start:
            current.make_close()

    # error case if end cant be found
    pygame.display.set_caption("Labyrinth (Unable to find the Node)")
    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Node(i, j, gap, rows)
            grid[i].append(spot)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GRID, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GRID, (i * gap, 0), (i * gap, width))


def draw_grid_wall(rows, grid):
    for i in range(rows):
        for j in range(rows):
            if i == 0 or i == rows - 1 or j == 0 or j == rows - 1:
                spot = grid[i][j]
                spot.make_wall()


def draw(win, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    draw_grid_wall(rows, grid)
    pygame.display.update()


def get_mouse_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(win, width):
    ROWS = 20
    grid = make_grid(ROWS, width)

    Start = None
    End = None
    Run = True

    while Run:
        draw(win, grid, ROWS, width)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                Run = False

            if pygame.mouse.get_pressed()[0]:  # [0] -> left mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not Start and spot != End:
                    Start = spot
                    Start.make_start()

                elif not End and spot != Start:
                    End = spot
                    End.make_end()

                elif spot != Start and spot != End:
                    spot.make_wall()

            if pygame.mouse.get_pressed()[2]:  # [2] -> right mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == Start:
                    Start = None
                if spot == End:
                    End = None

            if e.type == pygame.KEYDOWN:

                if not Start and not End:
                    pygame.display.set_caption("Labyrinth (Set Start & End Nodes!)")

                if e.key == pygame.K_SPACE and Start and End:       # space to start the search

                    counter_start = timer()
                    pygame.display.set_caption("Labyrinth (Searching...)")
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)

                    aStar(lambda: draw(win, grid, ROWS, width), grid, Start, End, counter_start)

                if e.key == pygame.K_c:     # c button as reset
                    Start = None
                    End = None
                    pygame.display.set_caption("Labyrinth (Using A* Algorithm)")
                    grid = make_grid(ROWS, width)
    pygame.quit()


main(win, WIDTH)