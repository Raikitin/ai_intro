import copy
import random
import time
from random import randrange, shuffle
from typing import Self

import pygame
import sys


import pygame
import sys


class ChessboardVisualizer:
    def __init__(self, board_size: int = 8, square_size: int = 60) -> None:
        self.board_size: int = board_size
        self.square_size: int = square_size
        self.width: int = self.board_size * self.square_size
        self.height: int = self.board_size * self.square_size
        self.colors: tuple[tuple[int, int, int], tuple[int, int, int]] = ((255, 255, 255), (0, 0, 0))  # WHITE, BLACK
        self.red: tuple[int, int, int] = (255, 0, 0)
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("8-Queens Problem")

    def draw_board(self, queens: list[int]) -> None:
        self.screen.fill(self.colors[0])

        # Draw the chessboard
        for row in range(self.board_size):
            for col in range(self.board_size):
                color = self.colors[(row + col) % 2]
                pygame.draw.rect(self.screen, color, pygame.Rect(col * self.square_size, row * self.square_size, self.square_size, self.square_size))

        # Draw the queens
        for row in range(self.board_size):
            col = queens[row]
            if col != -1:
                pygame.draw.circle(self.screen, self.red, (col * self.square_size + self.square_size // 2, row * self.square_size + self.square_size // 2), self.square_size // 3)

        pygame.display.flip()

    def quit(self) -> None:
        pygame.quit()
        sys.exit()


class QueensProblem:
    type board = list[int]
    queens: board
    threaded: list[bool]

    def __init__(self, state: board | None = None):
        if state is None:
            # state = list(range(8))
            # shuffle(state)
            state = [randrange(0, 8) for _ in range(8)]
        self.queens = state

    def costs(self) -> int:
        threading = [[False, ] * 8 for _ in range(8)]
        self.threaded = [False, ] * 8
        for i in range(8):
            for j in range(8):
                if i == j:
                    continue
                if self.queens[i] == self.queens[j]:
                    threading[i][j] = True
                    self.threaded[i] = True
                    continue
                if self.queens[j] + j - i == self.queens[i]:
                    self.threaded[i] = True
                    threading[i][j] = True
                    continue
                if self.queens[j] - j + i == self.queens[i]:
                    self.threaded[i] = True
                    threading[i][j] = True
        return sum([x.count(True) for x in threading]) // 2

    def swap(self, other: Self) -> None:
        i1, i2 = randrange(8), randrange(8)
        for j in range(8):
            if j < i1 ^ j < i2:
                self.queens[j], other.queens[j] = other.queens[j], self.queens[j]

    def mutate(self) -> None:
        for i in range(8):
            if self.threaded[i]:
                if randrange(10) == 1:
                    self.queens[i] = randrange(8)


def genetic_algorithm(population: list[QueensProblem]) -> QueensProblem:
    show = ChessboardVisualizer()
    for step in range(100):
        fitness: list[int] = [x.costs() for x in population]
        fitness_sorted = sorted(copy.copy(fitness))
        eliminiere = sum(fitness) / len(fitness)
        if min(fitness) == 0:
            return population[fitness.index(0)]
        elm_list = [x for x in range(len(population)) if fitness[x] <= eliminiere]
        len_elm_list = len(elm_list)
        for i in range(len(population) - len(elm_list)):
            elm_list.append(fitness.index(fitness_sorted[i % len_elm_list]))
        to_swap: list[tuple[int, int]]
        while True:
            to_swap = []
            shuffle(elm_list)
            for i in range(0, len(population), 2):
                if elm_list[i] == elm_list[i + 1]:
                    break
                to_swap.append((elm_list[i], elm_list[i+1]))
            else:
                continue
            break
        min_pop: QueensProblem = min(population, key=lambda x: x.costs())
        show.draw_board(min_pop.queens)
        print(min_pop.costs())
        time.sleep(0.1)
        new_population = copy.deepcopy(population)
        for i1, i2 in to_swap:
            population[i1].swap(population[i2])
        for pop in new_population:
                pop.mutate()
        population = new_population
    return min(population, key=lambda x: x.costs())


start = [QueensProblem() for _ in range(8)]
res = genetic_algorithm(start)
print("\n", res.queens, res.costs())
