import pygame
import random

pygame.font.init()

s_width = 800
s_height = 700
grid_width = 300
grid_height = 600
block_size = 30

top_left_x = (s_width - grid_width) // 2
top_left_y = s_height - grid_height

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

figure = [O, I, S, Z, L, J, T]
figure_color = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


# генерация поля
def grid_add(locked_pos={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c
    return grid


class Shape1(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = figure_color[figure.index(shape)]
        self.rotation = 0


def convert(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def draw_shape(shape, surface):
    font = pygame.font.SysFont('Arial', 30)
    label = font.render('Следующая:', 1, (255, 255, 255))

    sx = top_left_x + grid_width + 50
    sy = top_left_y + grid_height / 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j * block_size, sy + i * block_size,
                                                        block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))


def loose(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


# ограничение места
def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def get_shape():
    return Shape1(5, 0, random.choice(figure))


# название следюущих двух функций говорит само за себя
def text_top(surface, text, size, color):
    font = pygame.font.SysFont("Arial", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + grid_width / 2 - (label.get_width() / 2),
                         top_left_y + grid_height / 2 - label.get_height() / 2))


# убираем ненужный мусор
def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc


# счет
def update_score(nscore):
    score = max_score()

    with open('score.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def max_score():
    with open('score.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + grid_width, sy + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy),
                             (sx + j * block_size, sy + grid_height))


# окно
def draw_window(surface, grid, score=0, last_score=0):
    surface.fill((0, 0, 0))
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 60)
    label = font.render('', 1, (255, 255, 255))
    surface.blit(label, (top_left_x + grid_width / 2 - (label.get_width() / 2), 30))
    font = pygame.font.SysFont('Arial', 30)
    label = font.render('СЧЕТ: ' + str(score), 1, (255, 255, 255))
    sx = top_left_x + grid_width + 50
    sy = top_left_y + grid_height / 2 - 100
    surface.blit(label, (sx + 20, sy + 160))
    label = font.render('Лучший счет ' + last_score, 1, (255, 255, 255))
    sx = top_left_x - 200
    sy = top_left_y + 200
    surface.blit(label, (sx + 10, sy + 100))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * block_size, top_left_y + i * block_size,
                                                   block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, grid_width, grid_height), 5)
    draw_grid(surface, grid)


def main(start):
    last_score = max_score()
    pos_const = {}
    grid = grid_add(pos_const)
    change_fig = False
    run = True
    now_figure = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while run:
        grid = grid_add(pos_const)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            now_figure.y += 1
            if not (valid_space(now_figure, grid)) and now_figure.y > 0:
                now_figure.y -= 1
                change_fig = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            # управление
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    now_figure.x -= 1
                    if not (valid_space(now_figure, grid)):
                        now_figure.x += 1
                if event.key == pygame.K_RIGHT:
                    now_figure.x += 1
                    if not (valid_space(now_figure, grid)):
                        now_figure.x -= 1
                if event.key == pygame.K_DOWN:
                    now_figure.y += 1
                    if not (valid_space(now_figure, grid)):
                        now_figure.y -= 1
                if event.key == pygame.K_UP:
                    now_figure.rotation += 1
                    if not (valid_space(now_figure, grid)):
                        now_figure.rotation -= 1

        shape_pos = convert(now_figure)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = now_figure.color

        if change_fig:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                pos_const[p] = now_figure.color
            now_figure = next_piece
            next_piece = get_shape()
            change_fig = False
            score += clear_rows(grid, pos_const) * 10

        draw_window(start, grid, score, last_score)
        draw_shape(next_piece, start)
        pygame.display.update()

        if loose(pos_const):
            text_top(start, "Проигрыш", 80, ("red"))
            pygame.display.update()
            pygame.time.delay(2000)
            run = False
            update_score(score)


# главное меню, с него все начинается
def main_menu(start):
    run = True
    while run:
        start.fill((0, 0, 0))
        text_top(start, 'Нажмите любую кнопку для начала игры', 48, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(start)

    pygame.display.quit()
    pygame.mixer.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)
