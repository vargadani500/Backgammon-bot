import pygame
import sys
import numpy as np
import random

pygame.init()

pygame.display.set_caption("Backgammon")

Height = 1000
Width = 1000
Screen = pygame.display.set_mode((Height, Width))

fps = 60

def clear():
    Screen.fill((0, 0, 0))


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clear()

        pygame.time.Clock().tick(fps)
        pygame.display.update()


if __name__ == '__main__':
    main()
