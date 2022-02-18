import pygame
import random

pygame.init()


class Layout:
    Black = 0, 0, 0
    White = 255, 255, 255
    Green = 0, 255, 0
    Red = 255, 0, 0
    Blue = 0, 0, 255
    BG_COLOR = White
    GRADIENT = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]
    FONT = pygame.font.SysFont('cambria', 20)
    B_FONT = pygame.font.SysFont('cambria', 40, True)
    Edge = 100
    Top = 200

    def __init__(self, width, height, L):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Sorting Algorithm Visualizer')
        self.set_list(L)

    def set_list(self, L):
        self.L = L
        self.min = min(L)
        self.max = max(L)
        self.bar_width = round((self.width - self.Edge) / len(L))
        self.bar_height = round((self.height - self.Top) / (self.max - self.min))
        self.x = self.Edge // 2


def generate(num, _min, _max):
    lst = []

    for _ in range(num):
        val = random.randint(_min, _max)
        lst.append(val)
    return lst


def draw_screen(create, algo='', ascending=None):
    create.window.fill(create.BG_COLOR)

    control = create.FONT.render("R - Reset | S - Sort | A - Ascending | D - Descending", 1, create.Black)
    create.window.blit(control, (create.width / 2 - control.get_width() / 2, 10))

    control = create.FONT.render("I - Insertion Sort (Default) | M - Merge Sort | Q - Quick Sort | H - Heap Sort", 1,
                                 create.Red)
    create.window.blit(control, (create.width / 2 - control.get_width() / 2, 40))

    if ascending is not None:
        sort = create.B_FONT.render(f"{algo} - {'Ascending' if ascending else 'Descending'}", 1, create.Blue)
        create.window.blit(sort, (create.width / 2 - sort.get_width() / 2, 80))

    draw_list(create)
    pygame.display.update()


def draw_list(create, bar_color={}, clear=False):
    if clear:
        rect = (create.x, create.Top, create.width - create.Edge, create.width - create.Top)
        pygame.draw.rect(create.window, create.BG_COLOR,
                         (create.x, create.Top - 32, create.width - create.Edge, create.width - create.Top))

    for i, val in enumerate(create.L):
        x = create.x + i * create.bar_width
        y = create.height - (val - create.min) * create.bar_height

        color = create.GRADIENT[i % 3]
        if i in bar_color:
            color = bar_color[i]
        pygame.draw.rect(create.window, color, (x, y, create.bar_width, (val - create.min) * create.bar_height))
        Text = pygame.font.SysFont('cambria', 10).render(f"{val}",
                                                         1, create.Blue)
        create.window.blit(Text, (x + create.bar_width / 2, y - 24))

    if clear:
        pygame.display.update()


def insertion_sort(create, Asc=True, first=0, last=0):
    for i in range(1, len(create.L)):
        num = create.L[i]
        for j in range(i - 1, -1, -1):
            if (num < create.L[j] and Asc) or (num > create.L[j] and not Asc):
                create.L[j + 1], create.L[j] = create.L[j], create.L[j + 1]
                draw_list(create, {j: create.Green, j + 1: create.Red}, True)
                yield True
            else:
                break


def merge_sort(create, Asc=True, first=0, last=0):
    if last > first:
        mid = (first + last) // 2
        yield from merge_sort(create, Asc, first, mid)
        yield from merge_sort(create, Asc, mid + 1, last)
        n1 = mid - first + 1
        n2 = last - mid

        L = [0] * n1
        R = [0] * n2

        for i in range(n1):
            L[i] = create.L[first + i]
        for j in range(n2):
            R[j] = create.L[mid + j + 1]

        k = first
        i1 = 0
        j1 = 0
        while i1 < n1 and j1 < n2:
            if (L[i1] <= R[j1] and Asc) or (L[i1] >= R[j1] and not Asc):
                create.L[k] = L[i1]
                i1 += 1
                draw_list(create, {k: create.Green}, True)
                yield True
            elif (R[j1] <= L[i1] and Asc) or (R[j1] >= L[i1] and not Asc):
                create.L[k] = R[j1]
                j1 += 1
                draw_list(create, {k: create.Red}, True)
                yield True
            k += 1
        while i1 < n1:
            create.L[k] = L[i1]
            i1 += 1
            draw_list(create, {k: create.Green}, True)
            yield True
            k += 1
        while j1 < n2:
            create.L[k] = R[j1]
            j1 += 1
            draw_list(create, {k: create.Red}, True)
            yield True
            k += 1


def quick_sort(create, Asc=True, first=0, last=0):
    j = last - 1
    i = first
    k = last
    while j > i:
        if (create.L[i] > create.L[last] > create.L[j] and Asc) or (
                create.L[i] < create.L[last] < create.L[j] and not Asc):
            create.L[i], create.L[j] = create.L[j], create.L[i]
            draw_list(create, {i: create.Red, j: create.Green}, True)
            yield True
            j -= 1
            i += 1
        elif (create.L[last] >= create.L[i] and Asc) or (
                create.L[last] <= create.L[i] and not Asc):
            i += 1
        elif (create.L[last] <= create.L[j] and Asc) or (
                create.L[last] >= create.L[j] and not Asc):
            j -= 1

    if (create.L[j] > create.L[last] and Asc) or (create.L[j] < create.L[last] and not Asc):
        k = j
        create.L[last], create.L[j] = create.L[j], create.L[last]
        draw_list(create, {j: create.Red, last: create.Green}, True)
        yield True
    elif (create.L[j + 1] > create.L[last] and Asc) or (create.L[j + 1] < create.L[last] and not Asc):
        k = j + 1
        create.L[last], create.L[j + 1] = create.L[j + 1], create.L[last]
        draw_list(create, {j: create.Red, last: create.Green}, True)
        yield True

    if k - 1 > first:
        yield from quick_sort(create, Asc, first, k - 1)
    if last > k + 1:
        yield from quick_sort(create, Asc, k + 1, last)


def heap_sort(create, Asc=True, first=0, last=0):
    n = last + 1

    for i in range(n // 2, -1, -1):
        yield from heapify(create, n, i, Asc)

    for i in range(n - 1, 0, -1):
        create.L[i], create.L[0] = create.L[0], create.L[i]
        draw_list(create, {0: create.Red, i: create.Green}, True)
        yield True

        yield from heapify(create, i, 0, Asc)


def heapify(create, n, i, Asc):
    Max = i
    left = 2 * i + 1
    right = 2 * i + 2
    draw_list(create, {left: create.Red, right: create.Red, Max: create.Green}, True)
    yield True

    if left < n and ((create.L[i] < create.L[left] and Asc) or (create.L[i] > create.L[left] and not Asc)):
        Max = left

    if right < n and ((create.L[Max] < create.L[right] and Asc) or (create.L[Max] > create.L[right] and not Asc)):
        Max = right

    if Max != i:
        create.L[i], create.L[Max] = create.L[Max], create.L[i]
        draw_list(create, {Max: create.Red, i: create.Green}, True)
        yield True
        yield from heapify(create, n, Max, Asc)


def main():
    run = True
    clock = pygame.time.Clock()
    n = 50
    m = 0
    M = 100
    lst = generate(n, m, M)
    create = Layout(1200, 600, lst)
    flag = False
    Asc = True
    Algorithm = insertion_sort
    Names = {insertion_sort: "Insertion Sort", merge_sort: "Merge Sort", quick_sort: "Quick Sort",
             heap_sort: "Heap Sort"}
    Generator = None

    while run:
        pygame.display.update()
        clock.tick(60)
        if flag:
            try:
                next(Generator)
            except StopIteration:
                flag = False
        else:
            draw_screen(create)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate(n, m, M)
                create.set_list(lst)
                flag = False
            elif event.key == pygame.K_SPACE and not flag:
                flag = True
                draw_screen(create, Names[Algorithm], Asc)
                Algorithm(create, Asc)
                Generator = Algorithm(create, Asc, 0, len(lst) - 1)
            elif event.key == pygame.K_a and not flag:
                Asc = True
            elif event.key == pygame.K_d and not flag:
                Asc = False
            elif event.key == pygame.K_m and not flag:
                Algorithm = merge_sort
            elif event.key == pygame.K_q and not flag:
                Algorithm = quick_sort
            elif event.key == pygame.K_h and not flag:
                Algorithm = heap_sort

    pygame.quit()


if __name__ == '__main__':
    main()
