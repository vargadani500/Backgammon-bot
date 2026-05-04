import multiprocessing as mp
from robots import *
import settings


#creating the model
model = BGnet()
prev_model = BGnet()
model.load_state_dict(torch.load("nv_backgammon_model5311.pth15"))
prev_model.load_state_dict(torch.load("nv_backgammon_model5311.pth15"))

def play_headless_game(dummy_arg):
    """
    Playing an entire game without graphics
    - This is set up for multiprocessing
    """
    board = Board()
    board.set()
    dice = Dice(0, 0)

    white_bot = globals()[settings.W_Player]
    black_bot = globals()[settings.B_Player]
    first = True

    while board.winner == 0:
        # First roll (No doubles)
        if first:
            dice.roll(first=first)
            first = False
        else:
            dice.roll()

        if dice.turn == 1:
            if "ai" in settings.W_Player:
                turn = white_bot(board, dice,prev_model)
            else:
                turn = white_bot(board, dice)
        else:
            if "ai" in settings.B_Player:
                turn = black_bot(board, dice,model)
            else:
                turn = black_bot(board, dice)
        for move in turn:
            board.make_move(dice, move)
        dice.remaining = ()
        dice.turn *= -1

    return board.winner

def main():
    board = Board()
    board.set()

    sum_of_wins = 0
    total_games = 0

    # Creating parallel pools
    with mp.Pool(mp.cpu_count()) as pool:
        while True:
            # Giving
            results = pool.map(play_headless_game, range(settings.summation))
            total_games += settings.summation
            sum_of_wins += sum(results)

            b_wins = int(total_games / 2 - sum_of_wins / 2)
            w_wins = int(total_games / 2 + sum_of_wins / 2)

            print(f"Total games: {total_games}\nCurrent standing: ({settings.B_Player}){b_wins}:{w_wins}({settings.W_Player})")

if __name__ == "__main__":
    main()
