import pygame
import sys
import numpy as np
import random

# Initializing pygame
pygame.init()
pygame.display.set_caption("Backgammon")

# The size of a chip, everything else is scaled from it
# The board is 13.5*15.5 with borders and 11.5*13.5 without it
chip_size = 50

Height = 14.5*chip_size
Width = 14.5*chip_size
Screen = pygame.display.set_mode((Width, Height))

# Frames per second
fps = 60

#Initializing Fonts
pygame.font.init()
comic_sans = pygame.font.SysFont('Comic Sans MS', chip_size//2)

def clear():
    Screen.fill((0, 0, 0))


def set_board():
    state = np.zeros(24, int)
    state[0] = 5
    state[4] = -3
    state[6] = -5
    state[11] = 2
    state[12:] = -state[:12]
    return state


def draw_board():
    y_offset = chip_size * 2.5
    pygame.draw.rect(Screen, (245, 208, 135), [0, chip_size*2, chip_size*14.5, chip_size*12.5])

    # First row
    x_offset = 0
    for j in range(2):
        for i, x in enumerate(range(chip_size//2, 6*chip_size, chip_size)):
            if i % 2 == 0:
                color = (255, 255, 255)
            else:
                color = (135, 0, 0)
            pygame.draw.polygon(Screen, color, [(x + x_offset, y_offset), (x + chip_size/2 + x_offset, chip_size*5+y_offset), (x + chip_size + x_offset, y_offset) ])
        x_offset = chip_size * 7.5

    # Second row
    x_offset = 0
    for j in range(2):
        for i, x in enumerate(range(chip_size//2, 6*chip_size, chip_size)):
            if i % 2 == 0:
                color = (135, 0, 0)
            else:
                color = (255, 255, 255)
            pygame.draw.polygon(Screen, color, [(x + x_offset, chip_size * 14), (x + chip_size/2 + x_offset, chip_size*6.5+y_offset), (x + chip_size + x_offset, chip_size * 14) ])
        x_offset = chip_size * 7.5

    # Holders
    pygame.draw.rect(Screen, (0, 0, 0), [chip_size//2, y_offset, chip_size * 13.5, chip_size * 11.5+1], 4)
    pygame.draw.rect(Screen, (0, 0, 0), [chip_size*6.5, y_offset, chip_size * 1.5, chip_size * 11.5], 2)
    pygame.draw.rect(Screen, (0, 0, 0), [chip_size * 6.75, y_offset + chip_size*.25, chip_size * 1, chip_size * 4], 2)
    pygame.draw.rect(Screen, (0, 0, 0), [chip_size * 6.75, y_offset + chip_size*7.25, chip_size * 1, chip_size * 4], 2)


def draw_pieces(state):
    state = state.reshape((2, 12))

    # First row
    x_offset = 0
    for j in range(2):
        for i, x in enumerate(range(chip_size//2, 6*chip_size, chip_size)):
            chip_count = abs(state[(0, i + j * 6)])
            if state[(0, i+j*6)] > 0:
                for k in range(chip_count):
                    if k < 5:
                        pygame.draw.circle(Screen, (255, 255, 255), (x + x_offset + chip_size / 2, chip_size * 3+chip_size*k), chip_size / 2)
                        pygame.draw.circle(Screen, (0, 0, 0), (x + x_offset + chip_size / 2, chip_size * 3+chip_size*k), chip_size / 2, 2)
            elif state[(0, i+j*6)] < 0:
                for k in range(chip_count):
                    if k < 5:
                        pygame.draw.circle(Screen, (135, 0, 0), (x + x_offset + chip_size / 2, chip_size * 3+chip_size*k), chip_size / 2)
                        pygame.draw.circle(Screen, (0, 0, 0), (x + x_offset + chip_size / 2, chip_size * 3+chip_size*k), chip_size / 2, 2)
            if chip_count > 5:
                text_surface = comic_sans.render(f"+{chip_count-5}", False, (0, 0, 0))
                Screen.blit(text_surface, (x + x_offset+chip_size/10, chip_size*2.6))
        x_offset = chip_size * 7.5

    # Second row
    x_offset = 0
    for j in range(2):
        for i, x in enumerate(range(chip_size//2, 6*chip_size, chip_size)):
            chip_count = abs(state[(1, i + j * 6)])
            if state[(1, i+j*6)] > 0:
                for k in range(chip_count):
                    if k < 5:
                        pygame.draw.circle(Screen, (255, 255, 255), (x + x_offset + chip_size / 2, chip_size * 13.5-chip_size*k),chip_size / 2)
                        pygame.draw.circle(Screen, (0, 0, 0), (x + x_offset + chip_size / 2, chip_size * 13.5-chip_size*k),chip_size / 2, 2)
            elif state[(1, i+j*6)] < 0:
                for k in range(chip_count):
                    if k < 5:
                        pygame.draw.circle(Screen, (135, 0, 0), (x + x_offset + chip_size / 2, chip_size * 13.5-chip_size*k),chip_size / 2)
                        pygame.draw.circle(Screen, (0, 0, 0), (x + x_offset + chip_size / 2, chip_size * 13.5-chip_size*k), chip_size / 2,2)
            if chip_count > 5:
                text_surface = comic_sans.render(f"+{chip_count-5}", False, (0, 0, 0))
                Screen.blit(text_surface, (x + x_offset+chip_size/10, chip_size*13.1))
        x_offset = chip_size * 7.5
    return state


def main():
    state = set_board()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clear()
        draw_board()
        draw_pieces(state)
        pygame.time.Clock().tick(fps)
        pygame.display.update()


if __name__ == '__main__':
    main()
