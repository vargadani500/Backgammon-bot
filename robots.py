from functions import *

# State
# 0-23 is the board from white house to black house
# 24 is removed whites
# 25 is removed blacks
# 26 is white bear off
# 27 is black bear off

# turn = (path, state)


def scorer(state, color):
    score = .0 # Positive favors white
    pips = 0 # IDE was complaining?

    for i, cell in enumerate(state[:24]):
        # Pip count
        if cell > 0:
            pips -= cell * (24 - i)
        if cell < 0:
            pips -= cell * (i + 1)

        # Anchors
        if cell > 1 and i<6:
            score += i*2
        if cell < -1 and i>17:
            score -= (23-i)*2
        # Pieces in danger
        if cell == 1:
            if any([j < 0 for j in state[i+1:min(24, i+7)]]):
                score -= 10
            elif i >  17 and state[25] != 0:
                score -= 10
        if cell == -1:
            if any([j > 0 for j in state[max(0, i-6):i]]):
                score += 10
            elif i < 6 and state[24] != 0:
                score += 10
        # Blocking
        if cell > 1 and i+1<24 and state[i+1] > 1:
            score += 3
        if cell < -1 and i+1<24 and state[i+1] < -1:
            score -= 3
        # Blocking respawn
        if i > 17 and cell > 1:
            score += 5
        if i < 6  and cell < -1:
            score-= 5

    score += pips/2

    # Bearing off (Theoretically near optimal)
    score += state[26] * 20  # White
    score += state[27] * 20  # Black

    # Hits
    if color*pips > 10: # Winning (Defense)
        score -= state[24] * 10  # White
        score -= state[25] * 10  # Black
    else: # Losing (Attack)
        score -= state[24] * 40  # White
        score -= state[25] * 40  # Black
    return score*color


def human(board, dice):
    return []


def random_bot(board, dice):
    paths = board.get_valid_turns(dice)[0]
    if not paths:
        return []
    return random.choice(paths)


def greedy_bot(board, dice, return_state=False):
    turns = board.get_valid_turns(dice)
    best_move = [[], float("-inf"), board.state]
    # Finding the move with the highest score
    for path, state in zip(*turns):
        score = scorer(state, dice.turn)
        if score > best_move[1]:
            best_move = [path, score, state]
    if return_state:
        return best_move[2]
    return best_move[0]


def hard_bot(board, dice): # Somehow kinda worse
    # Expectiminimax algorithm
    turns = board.get_valid_turns(dice)
    best_move = [[], float("-inf")]

    # Getting 21 unique rolls with weights
    unique_rolls = []
    for i in range(1, 7):
        for j in range(i, 7):
            weight = 1 if i == j else 2
            unique_rolls.append(((i, j), weight))


    # Finding the move with the highest expected outcome
    for path, state in zip(*turns):
        score = 0

        # Saving the state
        save_state = board.state[:]
        remaining_state = dice.remaining[:]
        save_dice = dice.state[:]

        # Making the move for further calculation
        for move in path:
            board.make_move(dice, move)

        dice.turn *= -1
        for roll, weight in unique_rolls:
            dice.roll(roll)
            greedy_state = greedy_bot(board, dice, True)
            score += scorer(greedy_state, dice.turn*-1) * weight

        if score > best_move[1]:
            best_move = [path, score]

        # Loading original state
        dice.turn *= -1
        dice.state = save_dice
        dice.remaining = remaining_state
        board.state = save_state

    return best_move[0]