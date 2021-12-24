import pygame
import random

pygame.font.init()

s_width = 800
s_height = 700
grid_width = 300
grid_height = 600
block_size = 30

left_x = (s_width - grid_width) // 2
left_y = s_height - grid_height


# тут будут фигуры
# figure = [O, I, S, Z, L, J, T]


def grid_add(locked_pos={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c
    return grid


def draw_grid(surface, grid):
    sx = left_x
    sy = left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + grid_width, sy + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy),
                             (sx + j * block_size, sy + grid_height))


def text_cen(surface, text, size, color):
    font = pygame.font.SysFont("Arial", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (left_x + grid_width / 2 - (label.get_width() / 2),
                         left_y + grid_height / 2 - label.get_height() / 2))


def draw_window(surface, grid, score=0):
    surface.fill((0, 0, 0))

    pygame.font.init()

    font = pygame.font.SysFont('Arial', 30)
    label = font.render('Счет: ' + str(score), 1, (255, 255, 255))

    sx = left_x + grid_width + 50
    sy = left_y + grid_height/2 - 100

    surface.blit(label, (sx + 20, sy + 160))
    # last score
    label = font.render('Лучший счет:' + "0", 1, (255, 255, 255))

    sx = left_x - 200
    sy = left_y + 200

    surface.blit(label, (sx + 20, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (left_x + j*block_size, left_y + i*block_size,
                                                   block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (left_x, left_y, grid_width, grid_height), 5)

    draw_grid(surface, grid)


def main(start):
    locked_positions = {}
    grid = grid_add(locked_positions)
    run = True
    clock = pygame.time.Clock()
    score = 0

    while run:
        grid = grid_add(locked_positions)
        clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

        draw_window(start, grid, score)
        pygame.display.update()


# меню
def main_menu(start):
    run = True
    while run:
        start.fill((0, 0, 0))
        text_cen(start, 'Нажмите любую кнопку', 48, ("white"))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(start)

    pygame.display.quit()


start = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(start)
