from functions import *


def random_bot(board, dice):
    paths = board.get_valid_turns(dice)[0]
    if not paths:
        return []
    return random.choice(paths)