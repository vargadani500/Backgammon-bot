from functions import *

# State
# 0-23 is the board from white house to black house
# 24 is removed whites
# 25 is removed blacks
# 26 is white bear off
# 27 is black bear off

# turn = (path, state)


def scorer(state):
    score = 0 # Positive favors white

    # Pieces removed
    score -= state[24]*15 # White
    score -= state[25]*15 # Black

    # Bearing off
    score += state[26]*5 # White
    score += state[27]*5 # Black


    for i, cell in enumerate(state[:24]):
        # Anchors
        if cell > 1 and i<6:
            score += 10
        if cell < -1 and i>18:
            score -= 10
        # Pieces in danger
        if cell == 1 and any([j < 0 for j in state[i+1:min(24, i+7)]]):
            score -= 10
        if cell == -1 and any([j > 0 for j in state[max(0, i-6):i]]):
            score += 10
        # Blocking
        if cell > 1 and i+1<24 and state[i+1] > 1:
            score += 3
        if cell < -1 and i+1<24 and state[i+1] < -1:
            score -= 3
        # Pip count
        if cell > 0:
            score -= cell*(24-i)/2
        if cell < 0:
            score -= (cell+1)*i/2
    return score


def random_bot(board, dice):
    paths = board.get_valid_turns(dice)[0]
    if not paths:
        return []
    return random.choice(paths)


def greedy_bot(board, dice):
    turns = board.get_valid_turns(dice)
    best_move = [[], float("-inf")]

    # Finding the move with the highest score
    for path, state in zip(*turns):
        # Positive is our color now
        score = scorer(state)*dice.turn
        if score > best_move[1]:
            best_move = [path, score]

    return best_move[0]