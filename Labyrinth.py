import pygame
import math
import graph
import search

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
                    field = Field(j, j, margin, height, width, rows)
                    self.grid[i].append(field)

          self.start = self.grid[start[0]][start[1]]
          self.end = self.grid[end[0]][end[1]]

          self.start.make_start()
          self.end.make_end()




         # TODO other fuctions


     pygame.init()

     size = (500, 500)
     screen = pygame.display.set_mode(size)

     pygame.display.set_caption("My Game")

     done = False

     clock = pygame.time.Clock()

     while not done:
     for event in pygame.event.get():
     if event.type == pygame.QUIT:
              done = True

        # ---
   # The code here ist called once per clock tick
   # Let your algorithm loop here
     # ---

             screen.fill(BLACK)

             # ---
             # The screen is empty here
   # Put your 'drawing' code here
             #
             #   RECTANGEL EXAMPLE
             #
   #   The third Parameter defines the rectangles positioning etc: [y-pos,x-pos,width,height]
   #   pygame.draw.rect(screen,color,[(MARGIN + WIDTH) * y + MARGIN,
   #                        (MARGIN + HEIGHT) * x + MARGIN,WIDTH,HEIGHT])
             # ---


   pygame.display.flip()

   clock.tick(60)

pygame.quit()