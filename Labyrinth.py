import pygame
import math

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

WIDTH = 22
HEIGHT = 22
MARGIN = 3

class Field:
     def __init__(self, row, col, margin, height, width, total_rows):
          self.row = row
          self.col = col
          self.color = WHITE
          self.neighbors = []
          self.width = width
          self.height = height
          self.margin = margin
          self.total_rows = total_rows

     def get_pos(self):
          return self.row, self.col

     def is_closed(self):
          return self.color == GREEN

     def is_open(self):
          return self.color == GREEN

     def is_barrier(self):
          return self.color == BLACK

     def is_start(self):
          return self.color == BLUE

     def is_end(self):
          return self.color == BLUE

     def make_start(self):
          self.color = BLUE

     def make_closed(self):
          self.color = GREEN

     def make_open(self):
          self.color = GREEN

     def make_barrier(self):
          self.color = BLACK

     def make_end(self):
          self.color = BLUE

     def make_path(self):
          self.color = BLUE

     def draw(self, screen):
          pygame.draw.rect(screen, self.color, [(self.margin + self.width) * self.col + self.margin,(self.margin + self.height) * self.row + self.margin, self.width, self.height])

     def update_neighbors(self, grid):
          self.neighbors = []

          if(self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier()):
              self.neighbors.append(grid[self.row + 1][self.col])

          if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
               self.neighbors.append(grid[self.row - 1][self.col])

          if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
               self.neighbors.append(grid[self.row][self.col + 1])

          if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
               self.neighbors.append(grid[self.row][self.col - 1])


class Grid:
     def __init__(self, rows, margin, height, width, start, end, win):
          self.rows = rows
          self.height = width
          self.grid = []
          self.margin = margin
          self.height = height
          self.width = width
          self.win = win

          for i in range(rows):
               self.grid.append([])
               for j in range(rows):
                    field = Field(i, j, margin, height, width, rows)
                    self.grid[i].append(field)

          self.start = self.grid[start[0]][start[1]]
          self.end = self.grid[end[0]][end[1]]

          self.start.make_start()
          self.end.make_end()

     def euklidischeDistanz(self, node):  # heuristic function
          return math.sqrt(((self.end.col - node.col) ** 2) + ((node.row - self.end.row) ** 2))

     def manhattenDistanz(self, node):  # heuristic function
          return abs(self.end.col - node.col) + abs(node.row - self.end.row)

     def nodesInParth(self, node, parent):
          current = node
          counter = 1
          while current != self.start:
               counter += 1
               current = parent[current]
          return counter

     def adjacentNodesUnmarked(self, coordinates, explored):
          adjacent = []
          possible = [(coordinates[0] + coordinates[1]),
                      (coordinates[0] - coordinates[1]),
                      (coordinates[0], coordinates[1] + 1),
                      (coordinates[0], coordinates[1] - 1)]

          for element in possible:
               if(not element in explored and element[0] >= 0 and element[0] <= self.width and element[1] >= 0 and element[1] <= self.height):
                    adjacent.append(element)
          return adjacent

     def markPath(self, parent, node):
          field = node
          while(field != self.start):
               field.make_path()
               field = parent[field]
               self.draw()
          self.start.make_path()
          self.draw()

     # TODO A* function for shortest path

     def drawGrid(self):
          for row in range(self.rows):
               for col in range(self.rows):
                    pygame.draw.rect(win,self.grid[row][col].color, [(self.margin + self.width) * col + self.margin, (self.margin + self.height)])

     def draw(self):
          for row in self.grid:
               for field in row:
                    field.draw(self.win)

     def start(self):
          SIZE = 1000
          WIN = pygame.display.set_mode((SIZE, SIZE))
          pygame.display.set_caption('Starting')
          ROWS = 20
          WIDTH = 22
          HEIGHT = 22
          MARGIN = 3
          grid = Grid(ROWS, MARGIN, HEIGHT, WIDTH, (19,0), (0,19), WIN)

          start = None
          end = None

          run = True
          while run:
               grid.draw()
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         run = False

                    if event.type == pygame.KEYDOWN:
                         if event.key == pygame.K_SPACE:
                              for row in grid.grid:
                                   for spot in row:
                                        spot.update_neighbors(grid.grid)
                              grid.aStart()

          pygame.quit()

     Grid.start()
