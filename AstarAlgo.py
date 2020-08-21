import pygame
import math
from queue import PriorityQueue
from SPOT import Spot

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

# COLORS
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


# function that returns L distance
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


# reconstructing the path
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


# algorithm
def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()    # returns a lowest one
    open_set.put((0, count, start))    # 0 if the f_score, count is put for tiebreak
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}      # we can check if something is in it cant do it in PriorityQueue

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False


# makes a 2-d list of all spots
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid


# drawing spots
def draw(win, grid):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    pygame.display.update()


# returns the spot co-ordinates we clicked on
def get_clicked_spot(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col


# our main drawing function
def main(win, width):
    ROWS = 50      # can make dense grids
    grid = make_grid(ROWS, width)

    # keeping track of starting and ending spot
    start = None
    end = None

    run = True
    started = False     # so that we can not change when program is running
    while run:
        draw(win, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:     # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_spot(pos, ROWS, width)
                spot = grid[row][col]        # getting clicked spot
                # making start spot
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_spot(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                if spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)

                    algorithm(lambda: draw(win, grid), grid, start, end)

                if event.key == pygame.K_c:         # resetting
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


main(WIN, WIDTH)
