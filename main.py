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
    board = Board()
    board.set()

    dice = Dice(chip_size*6, chip_size*.5, chip_size)
    dice.click() # First dice roll

    roll_button = Button(pygame.Rect(chip_size*3.5, chip_size*.5, chip_size * 2, chip_size), "Roll")
    restart_button = Button(pygame.Rect(chip_size*9, chip_size*.5, chip_size * 2, chip_size), "Restart")
    while True:
        for event in pygame.event.get():
            roll_button.handle_event(event, dice)
            restart_button.handle_event(event, board)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Test
        pairs = board.get_valid_pairs(dice)
        if len(pairs) > 0:
            for move in random.choice(pairs):
                board.make_move(dice, move)
        # Test


        clear(Screen)
        # Menu
        dice.draw(Screen)
        restart_button.draw(Screen)
        roll_button.draw(Screen)
        # Board
        draw_board(Screen)
        draw_pieces(Screen, board.state)
        # Clock for fps
        pygame.time.Clock().tick(fps)
        # This updates the screen
        pygame.display.update()


if __name__ == '__main__':
    main()
