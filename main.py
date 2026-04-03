import sys
from functions import *

# Initializing pygame
pygame.init()

# Creating the window
Screen = pygame.display.set_mode((settings.Width, settings.Height))
pygame.display.set_caption("Backgammon")

# Frames per second
fps = 60


def main():
    board = Board(Screen)
    board.set()
    dice = Dice(chip_size*6, chip_size*.5, chip_size)
    roll_button = Button(pygame.Rect(chip_size*3.5, chip_size*.5, chip_size * 2, chip_size), "Roll")
    restart_button = Button(pygame.Rect(chip_size*9, chip_size*.5, chip_size * 2, chip_size), "Restart")
    while True:
        for event in pygame.event.get():
            roll_button.handle_event(event, dice)
            restart_button.handle_event(event, board)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        clear(Screen)
        # Menu
        dice.draw(Screen)
        restart_button.draw(Screen)
        roll_button.draw(Screen)
        # Board
        draw_board(Screen)
        draw_pieces(Screen, board.state)
        pygame.time.Clock().tick(fps)
        pygame.display.update()


if __name__ == '__main__':
    main()
