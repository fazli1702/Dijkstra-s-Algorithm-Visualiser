import pygame
from constant import *
from graph import Graph

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dijkstra's Algorithm")

def main():
    run = True
    graph = Graph(WIN)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()