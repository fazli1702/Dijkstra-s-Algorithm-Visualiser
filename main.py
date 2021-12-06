import pygame
from constant import *
from graph import *

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('A* Pathfinding Algorithm')

def main():
    run = True
    graph = Graph(WIN)
    started = False  # check if animation has started

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            mouse_coordinate = pygame.mouse.get_pos()

            if not started:
                if pygame.mouse.get_pressed()[0]:  # left click
                    graph.left_click(mouse_coordinate)

                if pygame.mouse.get_pressed()[2]:  # right click
                    graph.right_click(mouse_coordinate)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not started:   # return / enter button clicked
                    started = True
                    graph.dijkstra_vis()

        graph.update()

    pygame.quit()


if __name__ == '__main__':
    main()
