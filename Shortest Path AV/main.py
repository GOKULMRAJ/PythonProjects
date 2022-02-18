import math
import pygame
from queue import PriorityQueue

DIM = 600
window = pygame.display.set_mode((DIM, DIM))
pygame.display.set_caption("A* Algorithm Visualizer")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)


class Grid:
    def __init__(self, row, col, width, TR):
        self.row = row
        self.col = col
        self.width = width
        self.TR = TR
        self.x = col * width
        self.y = row * width
        self.N = []
        self.color = WHITE

    def get_pos(self):
        return self.row, self.col

    def is_close(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_blocked(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == CYAN

    def is_end(self):
        return self.color == ORANGE

    def is_path(self):
        return self.color == BLUE

    def reset(self):
        self.color = WHITE

    def set_close(self):
        self.color = RED

    def set_open(self):
        self.color = GREEN

    def set_blocked(self):
        self.color = BLACK

    def set_start(self):
        self.color = CYAN

    def set_end(self):
        self.color = ORANGE

    def set_path(self):
        self.color = BLUE

    def FORM(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def UN(self, cell):
        if self.row < self.TR - 1 and not cell[self.row + 1][self.col].is_blocked():
            self.N.append(cell[self.row + 1][self.col])
        if (self.row < self.TR - 1 and self.col < self.TR - 1) and not cell[self.row + 1][self.col + 1].is_blocked():
            self.N.append(cell[self.row + 1][self.col + 1])
        if (self.row < self.TR - 1 and self.col > 0) and not cell[self.row + 1][self.col - 1].is_blocked():
            self.N.append(cell[self.row + 1][self.col - 1])
        if self.row > 0 and not cell[self.row - 1][self.col].is_blocked():
            self.N.append(cell[self.row - 1][self.col])
        if (self.row > 0 and self.col < self.TR - 1) and not cell[self.row - 1][self.col + 1].is_blocked():
            self.N.append(cell[self.row - 1][self.col + 1])
        if (self.row > 0 and self.col > 0) and not cell[self.row - 1][self.col - 1].is_blocked():
            self.N.append(cell[self.row - 1][self.col - 1])
        if self.col < self.TR - 1 and not cell[self.row][self.col + 1].is_blocked():
            self.N.append(cell[self.row][self.col + 1])
        if self.col > 0 and not cell[self.row][self.col - 1].is_blocked():
            self.N.append(cell[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def H(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def form_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cell = Grid(i, j, gap, rows)
            grid[i].append(cell)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GRAY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GRAY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for cell in row:
            cell.FORM()

    draw_grid(win, rows, width)
    pygame.display.update()


def mouse_position(pos, rows, width):
    gap = width // rows
    x, y = pos

    row = y // gap
    col = x // gap

    return row, col


def algorithm(fun, grid, start, end):
    cnt = 0
    open_queue = PriorityQueue()
    open_queue.put((0, cnt, start))
    parent = {}
    G = {cell: float('inf') for row in grid for cell in row}
    G[start] = 0
    F = {cell: float('inf') for row in grid for cell in row}
    F[start] = H(start.get_pos(), end.get_pos())
    open_set = {start}

    while not open_queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        node = open_queue.get()[2]
        open_set.remove(node)
        if node == end:
            X = parent[end]
            while X != start:
                fun()
                X.set_path()
                X = parent[X]
            return True

        for neighbour in node.N:
            TempG = G[node] + 1

            if TempG < G[neighbour]:
                parent[neighbour] = node
                G[neighbour] = TempG
                F[neighbour] = G[neighbour] + H(neighbour.get_pos(), end.get_pos())
                if neighbour not in open_set:
                    cnt += 1
                    open_queue.put((F[neighbour], cnt, neighbour))
                    open_set.add(neighbour)
                    if neighbour != end:
                        neighbour.set_open()

        fun()
        if node != start:
            node.set_close()

    return False


def main():
    ROWS = 40
    grid = form_grid(ROWS, DIM)
    start = None
    end = None
    run = True

    while run:

        draw(window, grid, ROWS, DIM)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = mouse_position(pos, ROWS, DIM)
                cell = grid[row][col]
                if not start and cell != end:
                    start = cell
                    start.set_start()
                elif not end and cell != start:
                    end = cell
                    end.set_end()
                elif cell != end and cell != start:
                    cell.set_blocked()
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = mouse_position(pos, ROWS, DIM)
                cell = grid[row][col]
                cell.reset()
                if cell == start:
                    start = None
                elif cell == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if start is not None and end is not None:
                        for row in grid:
                            for cell in row:
                                if cell.is_open() or cell.is_close() or cell.is_path():
                                    cell.reset()
                                cell.N.clear()
                                cell.UN(grid)
                        algorithm(lambda: draw(window, grid, ROWS, DIM), grid, start, end)

                if event.key == pygame.K_r:
                    start = None
                    end = None
                    for row in grid:
                        for cell in row:
                            cell.N.clear()
                            cell.reset()

    pygame.quit()


if __name__ == '__main__':
    main()
