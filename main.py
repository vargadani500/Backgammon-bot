import sys
from robots import *
from draw_functions import *

# Initializing pygame
pygame.init()

# Creating the window
Screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Backgammon")


def main():
    # Setting the game up
    board = Board()
    board.set()
    dice = Dice(chip_size*6, chip_size*.5)

    # First roll (No doubles)
    first = True

    sum_of_wins = 0
    total_games = 0
    human_turn = False
    start_pos, end_pos = 0, 0
    turn = []

    # Reading
    white_bot = globals()[settings.W_Player]
    black_bot = globals()[settings.B_Player]

    roll_button = Button(pygame.Rect(chip_size*3.5, chip_size*.5, chip_size * 2, chip_size), "Roll")
    restart_button = Button(pygame.Rect(chip_size*9, chip_size*.5, chip_size * 2, chip_size), "Restart")
    while True:
        # Making moves
        if not human_turn:
            if board.winner == 0:
                if dice.turn == 1:
                    # Check if human player
                    if settings.W_Player == "human":
                        human_turn = True
                    else:
                        if first:
                            dice.roll(first=first)
                            first = False
                        else:
                            dice.roll()
                        # Get the bots decision
                        turn = white_bot(board, dice)
                else:
                    # Check if human player
                    if settings.B_Player == "human":
                        human_turn = True
                    else:
                        if first:
                            dice.roll(first=first)
                            first = False
                        else:
                            dice.roll()
                        # Get the bots decision
                        turn = black_bot(board, dice)
                if not human_turn:
                    for move in turn:
                        board.make_move(dice, move)
                    dice.remaining = ()
                    dice.turn *= -1
            else:
                first = True
                sum_of_wins += board.winner
                board.winner = 0
                board.set()
                total_games += 1
                if total_games % 1 == 0:
                    b_wins = int(total_games / 2 - sum_of_wins / 2)
                    w_wins = int(total_games / 2 + sum_of_wins / 2)

                    print(f"Total games: {total_games}\nCurrent standing: ({settings.B_Player}){b_wins}:{w_wins}({settings.W_Player})")


        # Pygame events
        for event in pygame.event.get():
            if not board.get_valid_turns(dice)[0]:
                if dice.remaining:
                    dice.turn *= -1
                    human_turn = False
                elif roll_button.check(event):
                    if first:
                        dice.roll(first=first)
                        first = False
                    else:
                        dice.roll()
            if restart_button.check(event):
                board.set()
                dice.turn = 1
                dice.remaining = ()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and human_turn:
                start_pos = get_point_from_mouse(pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONUP and human_turn:
                end_pos = get_point_from_mouse(pygame.mouse.get_pos())
                move = ()
                if start_pos is None or end_pos is None:
                    break
                for i in board.get_valid_moves(dice):
                    if start_pos == i[0] and end_pos == i[1]:
                        move = i
                        break
                if not move:
                    print("Not a valid move")
                    print("Your move:", start_pos, end_pos)
                    print("Valid moves:", *board.get_valid_moves(dice))
                    break
                in_a_turn = False
                for turn in board.get_valid_turns(dice)[0]:
                    if move in turn:
                        in_a_turn = True
                        break
                if not in_a_turn:
                    print("No turns with this move")
                    break
                board.make_move(dice, move)
                if not dice.remaining:
                    dice.turn *= -1
                    human_turn = False

        # Pygame graphics
        clear(Screen)
        # Menu
        draw_dice(Screen, dice)
        restart_button.draw(Screen)
        roll_button.draw(Screen)
        # Board
        draw_board(Screen)
        draw_pieces(Screen, board)
        # Clock for fps
        pygame.time.Clock().tick(settings.fps)
        # This updates the screen
        pygame.display.update()


if __name__ == '__main__':
    main()
