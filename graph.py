from constant import *
import pygame
from queue import PriorityQueue
import math

def get_pos_from_mouse(pos):
    '''return row, col from mouse coordinate'''
    x, y = pos
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return row, col

def is_valid_pos(row, col):
    '''check if row, col is valid'''
    if 0 <= row < ROWS and 0 <= col < COLS:
        return True
    return False


class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x, self.y = self.get_coordinate()
        self.colour = WHITE
        self.neighbours = []

    def get_coordinate(self):
        '''return (x, y) coordinate of node in window'''
        x = SQUARE_SIZE * self.col
        y = SQUARE_SIZE * self.row
        return x, y

    def get_neighbours(self):
        return self.neighbours

    def get_pos(self):
        return self.row, self.col

    def reset(self):
        self.colour = WHITE

    def is_start(self):
        return self.colour == ORANGE

    def is_end(self):
        return self.colour == PURPLE

    def is_open(self):
        '''check if node in open set'''
        return self.colour == GREEN

    def is_closed(self):
        return self.colour == RED

    def is_wall(self):
        return self.colour == BLACK

    def is_path(self):
        return self.colour == BLUE


    def set_start(self):
        self.colour = ORANGE

    def set_end(self):
        self.colour = PURPLE

    def set_open(self):
        self.colour = GREEN

    def set_closed(self):
        self.colour = RED

    def set_wall(self):
        self.colour = BLACK

    def set_path(self):
        self.colour = BLUE

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, SQUARE_SIZE, SQUARE_SIZE))

    def __repr__(self):
        s = 0
        if self.colour != WHITE:
            s = 1
        return str(s)

    def update_neighbours(self, graph):
        # right
        if is_valid_pos(self.row + 1, self.col):
            n_node = graph[self.row + 1][self.col]
            if not n_node.is_wall():
                self.neighbours.append(n_node)

        # left
        if is_valid_pos(self.row - 1, self.col):
            n_node = graph[self.row - 1][self.col]
            if not n_node.is_wall():
                self.neighbours.append(n_node)

        # up
        if is_valid_pos(self.row, self.col + 1):
            n_node = graph[self.row][self.col + 1]
            if not n_node.is_wall():
                self.neighbours.append(n_node)

        # down
        if is_valid_pos(self.row, self.col - 1):
            n_node = graph[self.row][self.col - 1]
            if not n_node.is_wall():
                self.neighbours.append(n_node)


class Graph:
    def __init__(self, win):
        self.graph = []
        self.win = win
        self.start = None
        self.end = None
        self.create_graph()

    def get_node(self, row, col):
        return self.graph[row][col]

    def update(self):
        self.draw_graph()
        pygame.display.update()

    def update_node_neighbours(self):
        for row in self.graph:
            for node in row:
                node.update_neighbours(self.graph)

    def create_graph(self):
        for row in range(ROWS):
            curr_row = []
            for col in range(COLS):
                node = Node(row, col)
                curr_row.append(node)
            self.graph.append(curr_row)

    def left_click(self, mouse_coordinate):
        row, col = get_pos_from_mouse(mouse_coordinate)
        node = self.get_node(row, col)

        if not self.start and node != self.end:
            node.set_start()
            self.start = node

        elif not self.end and node != self.start:
            node.set_end()
            self.end = node

        elif node != self.start and node != self.end:
            node.set_wall()


    def right_click(self, mouse_coordinate):
        row, col = get_pos_from_mouse(mouse_coordinate)
        node = self.get_node(row, col)
        node.reset()

        if node == self.start:
            self.start = None

        elif node == self.end:
            self.end = None

    def dijkstra_vis(self):
        '''visualise a* path finding algorithm on grid / graph'''
        self.update_node_neighbours()

        i = 0
        open_set = PriorityQueue()
        open_set.put((0, i, self.start))  # insert first / start node into open set
        open_set_list = {self.start}  # check if node in p queue as python p queue doens't have method to check
        prev_nodes = {}

        g_score = {}
        for row in self.graph:
            for node in row:
                g_score[node] = math.inf

        g_score[self.start] = 0

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            curr_node = open_set.get()[2]
            open_set_list.remove(curr_node)

            # reach the end - create path
            if curr_node == self.end:
                self.display_path(prev_nodes)
                return True


            for neighbour in curr_node.get_neighbours():
                temp_g_score = g_score[curr_node] + 1  # since all nodes are +1 away from prev visited node
                if temp_g_score < g_score[neighbour]:
                    prev_nodes[neighbour] = curr_node
                    g_score[neighbour] = temp_g_score

                    if neighbour not in open_set_list:
                        i += 1
                        open_set.put((g_score[neighbour], i, neighbour))
                        open_set_list.add(neighbour)
                        if neighbour != self.end:  # ensure that end node does not change colour (user can see end node)
                            neighbour.set_open()

            self.update()

            # update nodes that have been visited (except start & end node to retain original colour)
            if curr_node != self.start:
                curr_node.set_closed()

        return False

    
    def display_path(self, prev_nodes):
        path = []
        curr_node = self.end
        while True:
            prev_node = prev_nodes[curr_node]
            if prev_node == self.start:
                break
            path.append(prev_node)
            curr_node = prev_node

        path.reverse()
        for node in path:
            node.set_path()
            pygame.display.update()


    def print_graph(self):
        print(self.graph)

    def draw_grid(self):
        for y in range(0, HEIGHT, SQUARE_SIZE):
            pygame.draw.line(self.win, GREY, (0, y), (WIDTH, y))

        for x in range(0, WIDTH, SQUARE_SIZE):
            pygame.draw.line(self.win, GREY, (x, 0), (x, HEIGHT))

    def draw_nodes(self):
        for row in self.graph:
            for node in row:
                node.draw(self.win)

    def draw_graph(self):
        '''draw grid and nodes on window'''
        self.win.fill(WHITE)
        self.draw_nodes()
        self.draw_grid()

