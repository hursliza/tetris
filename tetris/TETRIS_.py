import pygame
import os
import random

pygame.font.init()
pygame.mixer.init()

screen_width = 650
screen_height = 745
field_width = 300
field_height = 600
block_size = 30
fall_speed = 0.25
rows = int(field_height / block_size)
columns = int(field_width / block_size)

win = pygame.display.set_mode((screen_width, screen_height))
pygame.key.set_repeat(100, 25)
pygame.display.set_caption('Tetris')
menu = pygame.image.load('media/menu.png')
dark = pygame.image.load('media/dark.png')
light = pygame.image.load('media/light.png')
tick = pygame.image.load('media/tick.png')
if not os.path.isfile('scores.txt'):
    with open('scores.txt', 'w+') as file:
        file.write(str('0'))
theme = dark
font_col = (255, 255, 255)
bg_col = (0, 0, 0)

form_size = 22
add_blocks = False
forget_scores = False

field_corner_x = 80
field_corner_y = 100

S = [['ooooo',
      'oooooo',
      'ooxxoo',
      'oxxooo',
      'ooooo'],
     ['ooooo',
      'ooxoo',
      'ooxxo',
      'oooxo',
      'ooooo']]

Z = [['ooooo',
      'ooooo',
      'oxxoo',
      'ooxxo',
      'ooooo'],
     ['ooooo',
      'ooxoo',
      'oxxoo',
      'oxooo',
      'ooooo']]

I = [['ooxoo',
      'ooxoo',
      'ooxoo',
      'ooxoo',
      'ooooo'],
     ['ooooo',
      'xxxxo',
      'ooooo',
      'ooooo',
      'ooooo']]

O = [['ooooo',
      'ooooo',
      'oxxoo',
      'oxxoo',
      'ooooo']]

J = [['ooooo',
      'oxooo',
      'oxxxo',
      'ooooo',
      'ooooo'],
     ['ooooo',
      'ooxxo',
      'ooxoo',
      'ooxoo',
      'ooooo'],
     ['ooooo',
      'ooooo',
      'oxxxo',
      'oooxo',
      'ooooo'],
     ['ooooo',
      'ooxoo',
      'ooxoo',
      'oxxoo',
      'ooooo']]

L = [['ooooo',
      'oooxo',
      'oxxxo',
      'ooooo',
      'ooooo'],
     ['ooooo',
      'ooxoo',
      'ooxoo',
      'ooxxo',
      'ooooo'],
     ['ooooo',
      'ooooo',
      'oxxxo',
      'oxooo',
      'ooooo'],
     ['ooooo',
      'oxxoo',
      'ooxoo',
      'ooxoo',
      'ooooo']]

T =  [['ooooo',
      'ooxoo',
      'oxxxo',
      'ooooo',
      'ooooo'],
     ['ooooo',
      'ooxoo',
      'ooxxo',
      'ooxoo',
      'ooooo'],
     ['ooooo',
      'ooooo',
      'oxxxo',
      'ooxoo',
      'ooooo'],
     ['ooooo',
      'ooxoo',
      'oxxoo',
      'ooxoo',
      'ooooo']]


V = [['ooooo',
      'ooooo',
      'oxooo',
      'oxxoo',
      'ooooo'],
     ['ooooo',
      'oxxoo',
      'oxooo',
      'ooooo',
      'ooooo'],
     ['ooooo',
      'ooxxo',
      'oooxo',
      'ooooo',
      'ooooo'],
     ['ooooo',
      'ooooo',
      'oooxo',
      'oosxxo',
      'ooooo']]


C = [['ooooo',
      'oxxoo',
      'oxooo',
      'oxxoo',
      'ooooo'],
     ['ooooo',
      'oxxxo',
      'oxoxo',
      'ooooo',
      'ooooo'],
     ['ooooo',
      'oxxoo',
      'ooxoo',
      'oxxoo',
      'ooooo'],
     ['ooooo',
      'ooooo',
      'oxoxo',
      'oxxxo',
      'ooooo']]

Q = [['ooooo',
      'oxxoo',
      'oxxoo',
      'ooxoo',
      'ooooo'],
     ['ooooo',
      'ooxxo',
      'oxxxo',
      'ooooo',
      'ooooo'],
     ['ooooo',
      'ooxoo',
      'ooxxo',
      'ooxxo',
      'ooooo'],
     ['ooooo',
      'ooooo',
      'oxxxo',
      'oxxoo',
      'ooooo']]

X = [['ooooo',
      'ooxoo',
      'oxxxo',
      'ooxoo',
      'ooooo']]

classic_shapes = [S, Z, I, O, J, L, T]
additional_shapes = [V, C, Q, X]

shapes = classic_shapes

colours = [(30, 170, 10),
           (250, 230, 55),
           (255, 45, 45),
           (220, 70, 220),
           (255, 130, 0),
           (30, 90, 170),
           (135, 240, 215),
           (122, 14, 64),
           (93, 186, 131),
           (76, 189, 255),
           (162, 67, 193)]


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.colour = colours[shapes.index(shape)]
        self.rotation = 0


def create_field(unavailable_pos={}):
    field = [[(0, 0, 0) for i in range(columns)] for i in range(rows)]

    for i in range(len(field)):
        for j in range(len(field[i])):
            if (j, i) in unavailable_pos:
                c = unavailable_pos[(j, i)]
                field[i][j] = c

    return field


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == 'x':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def available_space(shape, field):
    available_positions = [[(j, i) for j in range(columns) if field[i][j] == bg_col] for i in range(rows)]
    available_positions = [j for sub in available_positions for j in sub]

    converted = convert_shape_format(shape)

    for pos in converted:
        if pos not in available_positions:
            if pos[1] > -1:
                return False
    return True


def check_game_status(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def random_shape():
    return Piece(5, 0, random.choice(shapes))


def label(text, size, colour, surface):
    font = pygame.font.Font('media/myfont.ttf', size)
    label = font.render(text, 1, colour)

    surface.blit(label, (
        field_corner_x + field_width / 2 - (label.get_width() / 2),
        field_corner_y + field_height / 2 - label.get_height() / 2))


def draw_field_lines(surface, field):
    x_coord = field_corner_x
    y_coord = field_corner_y

    for i in range(len(field)):
        pygame.draw.line(surface, (70, 70, 70), (x_coord, y_coord + i * block_size),
                         (x_coord + field_width, y_coord + i * block_size))
        for j in range(len(field[i])):
            pygame.draw.line(surface, (70, 70, 70), (x_coord + j * block_size, y_coord),
                             (x_coord + j * block_size, y_coord + field_height))


def delete_rows(field, unavailable):
    inc = 0
    for i in range(len(field) - 1, -1, -1):
        row = field[i]
        if bg_col not in row:
            inc += 1
            index = i
            for j in range(len(row)):
                try:
                    del unavailable[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(unavailable), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < index:
                newKey = (x, y + inc)
                unavailable[newKey] = unavailable.pop(key)

    return inc


def draw_next_shape(shape, surface, font_col):
    font = pygame.font.Font('media/myfont.ttf', 20)
    label = font.render('Next Shape', 1, font_col)

    x_coord = field_corner_x + field_width + 70
    y_coord = field_corner_y + field_height / 2 - 100

    converted = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(converted):
        row = list(line)
        for j, column in enumerate(row):
            if column == 'x':
                pygame.draw.rect(surface, shape.colour, (x_coord + j * 30, y_coord + i * 30, 30, 30), 0)
                pygame.draw.rect(surface, (70, 70, 70), (x_coord + j * 30, y_coord + i * 30, 30, 30), 1)

    surface.blit(label, (x_coord + 10, y_coord - 30))


def update_score(new_score):
    score = high_score()

    with open('scores.txt', 'w') as file:
        if int(score) > new_score:
            file.write(str(score))
        else:
            file.write(str(new_score))


def high_score():
    with open('scores.txt', 'r') as file:
        lines = file.readlines()
        score = lines[0].strip()

    return score


def forget_last_score():
    with open('scores.txt', 'w') as file:
        file.write(str('0'))


def draw_window(surface, field, score=0, high_score=0, theme=dark, font_col=(255, 255, 255)):
    surface.blit(theme, (0, 0))

    pygame.font.init()

    font = pygame.font.Font('media/myfont.ttf', 20)
    label = font.render('Score: ' + str(score), 1, font_col)

    x_coord = field_corner_x + field_width + 50
    y_coord = field_corner_y + field_height / 2 - 220

    surface.blit(label, (x_coord, y_coord))

    font = pygame.font.Font('media/myfont.ttf', 20)
    label = font.render('High Score: ' + str(high_score), 1, font_col)

    x_coord = field_corner_x + field_width + 50
    y_coord = field_corner_y + field_height / 2 - 270

    surface.blit(label, (x_coord, y_coord))

    font = pygame.font.Font('media/myfont.ttf', 50)
    label = font.render('Tetris', 1, font_col)

    surface.blit(label, (field_corner_x + field_width / 2 - label.get_width() / 2, 5))

    for i in range(len(field)):
        for j in range(len(field[i])):
            pygame.draw.rect(surface, field[i][j],
                             (field_corner_x + j * block_size, field_corner_y + i * block_size, block_size, block_size),
                             0)

    draw_field_lines(surface, field)
    pygame.draw.rect(surface, (20, 20, 20), (field_corner_x, field_corner_y, field_width, field_height), 3)


def pause(surface, run=True):

    paused = True

    while paused:
        label('Paused', 40, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False


def put_ticks(surface, tick, fall_speed = 0.25, theme = dark, add_blocks = False, forget_scores = False):
    if fall_speed == 0.75:
        surface.blit(tick, (386, 226))

    if fall_speed == 0.25:
        surface.blit(tick, (386, 273))

    if fall_speed == 0.10:
        surface.blit(tick, (386, 322))

    if theme == dark:
        surface.blit(tick, (386, 400))

    if theme == light:
        surface.blit(tick, (386, 449))

    if add_blocks == True:
        surface.blit(tick, (137, 524))

    if forget_scores == True:
        surface.blit(tick, (137, 573))


def main(win, theme, shapes, font_col, fall_speed):
    last_score = high_score()
    unavailable_positions = {}
    field = create_field(unavailable_positions)

    change_piece = False
    run = True
    current_piece = random_shape()
    next_piece = random_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    score = 0

    pygame.mixer.music.load('media/bang.mp3')
    while run:
        field = create_field(unavailable_positions)
        fall_time += clock.get_rawtime()
        clock.tick()


        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (available_space(current_piece, field)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    run = False

                if event.key == pygame.K_SPACE:
                    pause(win, run)

                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not (available_space(current_piece, field)):
                        current_piece.x += 1

                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (available_space(current_piece, field)):
                        current_piece.x -= 1

                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not (available_space(current_piece, field)):
                        current_piece.y -= 1

                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not (available_space(current_piece, field)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                field[y][x] = current_piece.colour

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                unavailable_positions[p] = current_piece.colour
            current_piece = next_piece
            next_piece = random_shape()
            change_piece = False
            if delete_rows(field, unavailable_positions) > 0:
                score += delete_rows(field, unavailable_positions) * columns

                pygame.mixer.music.play()



        max_score = update_score(score)
        draw_window(win, field, score, last_score, theme, font_col)
        draw_next_shape(next_piece, win, font_col)
        pygame.display.update()

        if check_game_status(unavailable_positions):
            label('Game Over', 50, (255, 255, 255), win)
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)


def start_screen(win, classic_shapes, additional_shapes, fall_speed = 0.25, theme = dark, font_col = (255, 255, 255), add_blocks = False, forget_scores = False):
    run = True

    pygame.mixer.music.load('media/sound.mp3')
    pygame.mixer.music.play(-1)

    while run:
        win.blit(menu, (0, 0))
        put_ticks(win, tick, fall_speed, theme, add_blocks, forget_scores)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                global shapes
                x, y = event.pos
                if x > 386 and x < 386 + form_size:
                    if y > 226 and y < 226 + form_size:
                        fall_speed = 0.75
                        put_ticks(win, tick, fall_speed, theme, add_blocks, forget_scores)
                        pygame.display.update()

                    if y > 273 and y < 273 + form_size:
                        fall_speed = 0.25
                        put_ticks(win, tick, fall_speed, theme, add_blocks, forget_scores)
                        pygame.display.update()

                    if y > 322 and y < 322 + form_size:
                        fall_speed = 0.10
                        put_ticks(win, tick, fall_speed, theme, add_blocks, forget_scores)
                        pygame.display.update()

                    if y > 400 and y < 400 + form_size:
                        theme = dark
                        font_col = (255, 255, 255)
                        put_ticks(win, tick, fall_speed, theme, add_blocks, forget_scores)
                        pygame.display.update()

                    if y > 449 and y < 449 + form_size:
                        theme = light
                        font_col = (0, 0, 0)
                        put_ticks(win, tick, fall_speed, theme, add_blocks, forget_scores)
                        pygame.display.update()

                if x > 137 and x < 137 + form_size:
                    if  y > 524 and y < 524 + form_size:

                        add_blocks = True
                        shapes = classic_shapes + additional_shapes

                        put_ticks(win, tick, fall_speed, theme, add_blocks, forget_scores)
                        pygame.display.update()

                    if  y > 573 and y < 573 + form_size:
                        forget_scores = True
                        forget_last_score()

                        put_ticks(win, tick, fall_speed, theme, add_blocks, forget_scores)
                        pygame.display.update()


                if x > 173 and x < 745 and y > 636 and y < 697:
                    main(win, theme, shapes, font_col, fall_speed)
                    pygame.mixer.music.load('media/sound.mp3')
                    pygame.mixer.music.play(-1)
                    shapes = classic_shapes
                    add_blocks = False
                    forget_scores = False

    pygame.display.quit()


start_screen(win, classic_shapes, additional_shapes, fall_speed, theme, font_col, add_blocks, forget_scores)