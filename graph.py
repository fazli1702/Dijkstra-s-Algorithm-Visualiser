import pygame
from constant import *

class Graph:
    def __init__(self, win):
        self.win = win
        self.draw_graph()

    def draw_graph(self):
        self.win.fill(WHITE)

        for y in range(0, HEIGHT, SQUARE_SIZE):
            pygame.draw.line(self.win, BLACK, (0, y), (WIDTH, y))

        for x in range(0, WIDTH, SQUARE_SIZE):
            pygame.draw.line(self.win, BLACK, (x, 0), (x, HEIGHT))