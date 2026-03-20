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


def clear():
    Screen.fill((0, 0, 0))


def draw_board():
    y_offset = chip_size * 2.5
    pygame.draw.rect(Screen, (245, 208, 135), [0, chip_size*2, chip_size*14.5, chip_size*12.5])

    # First row
    x_offset = 0
    for i in range(2):
        for i, x in enumerate(range(chip_size//2, 6*chip_size, chip_size)):
            if i % 2 == 0:
                color = (255, 255, 255)
            else:
                color = (135, 0, 0)
            pygame.draw.polygon(Screen, color, [(x + x_offset, y_offset), (x + chip_size/2 + x_offset, chip_size*5+y_offset), (x + chip_size + x_offset, y_offset) ])
        x_offset = chip_size * 7.5

    # Second row
    x_offset = 0
    for i in range(2):
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


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clear()
        draw_board()
        pygame.time.Clock().tick(fps)
        pygame.display.update()


if __name__ == '__main__':
    main()
