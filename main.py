import sys
from robots import *

if settings.graphics:
    # Initializing pygame
    pygame.init()

    # Creating the window
    Screen = pygame.display.set_mode((settings.Width, settings.Height))
    pygame.display.set_caption("Backgammon")


def main():
    # Setting the game up
    board = Board()
    board.set()
    dice = Dice(chip_size*6, chip_size*.5)

    sum_of_wins = 0
    total_games = 0

    # Reading
    white_bot = globals()[settings.W_Player]
    black_bot = globals()[settings.B_Player]

    roll_button = Button(pygame.Rect(chip_size*3.5, chip_size*.5, chip_size * 2, chip_size), "Roll")
    restart_button = Button(pygame.Rect(chip_size*9, chip_size*.5, chip_size * 2, chip_size), "Restart")
    while True:


        # Making moves
        if board.winner == 0:
            dice.turn *= -1
            dice.roll()
            if dice.turn == 1:
                # Get the bots decision
                turn = white_bot(board, dice)
            else:
                turn = black_bot(board, dice)
            for move in turn:
                board.make_move(dice, move)
        else:
            sum_of_wins += board.winner
            board.winner = 0
            board.set()
            total_games += 1
            if total_games % 100 == 0:
                print(f"Total games: {total_games}\nCurrent standing: ({settings.B_Player}){int(total_games/2-sum_of_wins/2)}:{int(total_games/2+sum_of_wins/2)}({settings.W_Player})")

        # Pygame graphics
        if settings.graphics:
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
            board.draw_pieces(Screen)
            # Clock for fps
            pygame.time.Clock().tick(settings.fps)
            # This updates the screen
            pygame.display.update()


if __name__ == '__main__':
    main()
