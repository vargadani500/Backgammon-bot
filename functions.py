import random
import settings


class Board:
    def __init__(self):
        # State #
        # 0-23 is the board from white house to black house
        # 24 is removed whites
        # 25 is removed blacks
        # 26 is white bear off
        # 27 is black bear off
        self.state = [0] * 28
        self.winner = 0

    def set(self):
        self.winner = 0
        self.state = [0] * 28
        self.state[0] = 2
        self.state[5] = -5
        self.state[7] = -3
        self.state[11] = 5
        self.state[12] = -5
        self.state[16] = 3
        self.state[18] = 5
        self.state[23] = -2


    def get_valid_moves(self, dice):
        state = [i*dice.turn for i in self.state] # Same color will be pos
        valid_moves = []

        # General case
        if all(i < 1 for i in state[24:26]):
            for d in set(dice.remaining):
                if dice.turn == 1: # White
                    for i in range(24-d):
                        if state[i] > 0 and state[i+d] >= -1:
                            valid_moves.append((i, i+d, d))
                else: # Black
                    for i in range(23, d-1, -1):
                        if state[i] > 0 and state[i-d] >= -1:
                            valid_moves.append((i, i-d, d))

        # if we have a piece removed
        else:
            for d in set(dice.remaining):
                if dice.turn == 1:
                    if state[24] > 0 and state[d-1] >= -1:
                        valid_moves.append((24, d-1, d))
                else:
                    if state[25] > 0 and state[24-d] >= -1:
                        valid_moves.append((25, 24-d, d))

        # Bear off for white
        if dice.turn == 1 and all(i < 1 for i in state[:18]) and state[24] == 0:
            for d in set(dice.remaining):
                if state[24-d] > 0:
                    valid_moves.append((24-d, 26, d))
                # Overshoot for white
                elif all(i < 1 for i in state[18:24 - d]):
                    for p in range(24 - d + 1, 24):
                        if state[p] > 0:
                            valid_moves.append((p, 26, d))
                            break
        # Bear off for black
        elif dice.turn == -1 and all(i < 1 for i in state[6:24]) and state[25] == 0:
            for d in set(dice.remaining):
                if state[d-1] > 0:
                    valid_moves.append((d-1, 27, d))
                # Overshoot for black
                elif all(i < 1 for i in state[d:6]):
                    for p in range(d - 2, -1, -1):
                        if state[p] > 0:
                            valid_moves.append((p, 27, d))
                            break
        return valid_moves


    def make_move(self, dice, move):
        # Checking for hits
        if self.state[move[0]] * self.state[move[1]] < 0:
            # Moving the removed piece in its new place
            self.state[move[1]] += dice.turn
            if dice.turn == 1:
                self.state[25] -= dice.turn
            else:
                self.state[24] -= dice.turn

        # Moving the piece
        self.state[move[0]] -= dice.turn
        self.state[move[1]] += dice.turn

        # Checking for win
        if self.state[26] == 15:
            self.winner = 1
        elif self.state[27] == -15:
            self.winner = -1

        # Removing the used dice
        dice.remaining.remove(move[2])

        # Returning board state
        return self.state


    def get_valid_turns(self, dice):
        # A set for caching
        all_paths_found = []
        seen_states = set()
        
        # First we find all possible paths
        def search_paths(board, c_dice, path):

            # Making sure we don't calculate the same position twice (Common for doubles)
            state = (tuple(board.state), tuple(c_dice.remaining))
            if state in seen_states:
                return

            # If this is a new state, then adding it to the set
            seen_states.add(state)

            # Closing down paths
            moves = board.get_valid_moves(c_dice)
            if not moves:
                current = tuple(board.state)
                all_paths_found.append((path, current))
                return

            # Discovering new paths
            for move in moves:
                # Saving state
                save_state = board.state[:]
                remaining_state = c_dice.remaining[:]
                
                # Making the move on the board
                board.make_move(c_dice, move)

                # Recursive call
                search_paths(board, c_dice, path + [move])

                # Reloading state
                board.state = save_state
                c_dice.remaining = remaining_state

        # Doing the search
        search_paths(self, dice, [])

        # Determining the longest move, cause we have to make a move just as long according to the rules
        max_path_length = max([len(path) for path, state in all_paths_found])
        unique_paths = []
        unique_states = []

        # Returning nothing, if there are no legal moves
        if max_path_length == 0:
            return unique_paths, unique_states
        
        # Removing duplicates
        for path, state in all_paths_found:
            if len(path) == max_path_length and state not in unique_states:
                unique_states.append(state)
                unique_paths.append(path)
        return unique_paths, unique_states


class Dice:
    def __init__(self, x=0, y=0):
        # The turn color is 1 for white, -1 for black
        if settings.starter == 0:
            self.turn = random.choice([1, -1])
        else:
            self.turn = settings.starter
        self.x = x
        self.y = y
        self.remaining = []
        self.state = (6, 6)

    def roll(self, value=None,first=False):
        self.remaining = []
        if value is None:
            self.state = (random.randint(1, 6), random.randint(1, 6))
        elif first:
            self.state = random.sample(range(1, 7), 2)
        else:
            self.state = (value[0], value[1])
        if self.state[0] == self.state[1]:
            self.remaining = [self.state[0]] * 4
        else:
            self.remaining = list(self.state)


    def __str__(self):
        # This is for printing
        return f"{self.state[0]}, {self.state[1]}"
