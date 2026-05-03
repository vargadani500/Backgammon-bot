from functions import *

# State
# 0-23 is the board from white house to black house
# 24 is removed whites
# 25 is removed blacks
# 26 is white bear off
# 27 is black bear off

# turn = (path, state)

def inversion(state):
    count = 0
    for i in range(26):
        if state[i] < 0: # if black
            whites = sum(abs(state[j]) for j in range(i) if state[j] > 0)
            count -= whites*state[i]
    return count


def scorer(state, color, greedy = True):
    score = 0 # Positive favors white
    w_pips = state[24] * -25
    b_pips = state[25] * -25
    for i, cell in enumerate(state[:24]):
        # Pip count
        if cell > 0:
            dist = 24 - i
            w_pips -= cell * dist
            score -= cell * (dist ** 2) / 100 # Against stragglers
        if cell < 0:
            dist = i + 1
            b_pips -= cell * dist
            score += abs(cell) * (dist ** 2) / 100 # Against stragglers

        # Anchor counting
        if cell < -1 and i > 17 and (w_pips + b_pips) > 20:
            score -= (23 - i) * 2
        elif cell > 1 and i < 6 and (w_pips + b_pips) < -20:
            score += i * 2

        # Pieces in danger
        if greedy:
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

    # Bearing off
    score += state[26] * 5  # White
    score += state[27] * 5  # Black

    # Hits
    if color*(w_pips + b_pips) > 20: # Winning (Defense)
        # Bearing off logic
        if color == 1:
            if sum(state[i] for i in range(0, 18) if state[i] > 0) == 0:
                # all pieces in the house ultra defensive
                score -= state[24] * 100 # White
                score -= state[25] * 5 # Black
            else:
                score -= state[24] * 10
                score -= state[25] * 5
        if color == -1:
            if sum(state[i] for i in range(6, 24) if state[i] < 0) == 0:
                # all pieces in the house ultra defensive
                score -= state[24] * 5
                score -= state[25] * 100
            else:
                score -= state[24] * 5
                score -= state[25] * 10
    else: # Losing (Hitting is encouraged)
        if color == 1:
            score -= state[24] * 10
            score -= state[25] * 20
        if color == -1:
            score -= state[24] * 20
            score -= state[25] * 10

    return score*color


# Getting 21 unique rolls with weights
def get_rolls():
    unique_rolls = []
    for i in range(1, 7):
        for j in range(i, 7):
            weight = 1 if i == j else 2
            unique_rolls.append(((i, j), weight))
    return unique_rolls


def human():
    raise Exception("This is shouldn't be called upon")


def random_bot(board, dice,model):
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


def hard_bot(board, dice):
    # Expectiminimax algorithm (2-ply)
    turns = board.get_valid_turns(dice)
    best_move = [[], float("-inf")]

    # Finding the move with the highest expected outcome
    for path, state in zip(*turns):
        score = 0

        # Saving the state
        save_winner = board.winner
        save_state = board.state[:]
        remaining_state = dice.remaining[:]
        save_dice = dice.state[:]

        # Making the move for further calculation
        for move in path:
            board.make_move(dice, move)

        dice.turn *= -1
        for roll, weight in get_rolls():
            dice.roll(roll)
            greedy_state = greedy_bot(board, dice, model,True)
            score += scorer(greedy_state, dice.turn*-1, False) * weight

        if score > best_move[1]:
            best_move = [path, score]

        # Loading original state
        dice.turn *= -1
        dice.state = save_dice
        dice.remaining = remaining_state
        board.state = save_state
        board.winner = save_winner

    return best_move[0]





#the rate of moves left before winning
#white=pos is the bot
def potential(board_state):
    neg=0
    pos=0
    for i in range(24):
        if board_state[i] > 0:
            pos += board_state[i]*(i+1)
        elif board_state[i] < 0:
            neg -= board_state[i]*(24-i)
    pos += board_state[24]*25
    neg += board_state[25]*25
    if neg!=0:
        pot = 1-pos/neg
    else:
        pot=-1
    return pot
#output is positive if the bot is leading


def botond(board, dice):
    best_movee = [[], float("-inf")]

    agressivness= potential(board.state)

    mainpaths=board.get_valid_turns(dice)

    try_dice=Dice()
    try_dice.turn= -1*dice.turn
    try_board=Board()

    #the value of mainpaths
    for num in range(len(mainpaths[1])):
        states=mainpaths[1][num]


        rolls=[]
        for i in range(6):
            for j in range(6-i):

                #one enemy roll
                try_board.state = list(states)
                try_board.winner = board.winner
                try_dice.roll((i+1,j+1))
                experimental_states=try_board.get_valid_turns(try_dice)
                if len(experimental_states[1])>0:
                    rolls.append( min(potential(enemy_board) for enemy_board in experimental_states[1]))
                else:
                    rolls.append(agressivness)

        #counting
        exp_value= sum(rolls)
        rolls.sort(reverse=True)
        agr_exp_value=sum(rolls[0:(1+int(min(len(rolls),(len(rolls)+agressivness*len(rolls)))))])


        #agressive strategy
        crashes=0
        #pos is the bot

        neg=0
        for i in states[0:23]:
            if i>0:
                crashes+=i*neg
            elif i<0:
                neg+=-i
        crashes+=states[24]*neg
        crashes+=states[25]*(15-states[26])

        #final value
        finval=exp_value+agr_exp_value+crashes*agressivness*0.1
        if finval>best_movee[1]:
            best_movee[0]=mainpaths[0][num]
            best_movee[1]=finval

    return best_movee[0]


import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset

import torch.optim as optim

#creating the model

#old version
"""class BGnet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(28, 256)
        self.fc2 = nn.Linear(256, 256)
        self.fc3 = nn.Linear(256, 128)
        self.fc4 = nn.Linear(128, 1)

        self.ln1 = nn.LayerNorm(256)
        self.ln2 = nn.LayerNorm(256)
        self.ln3 = nn.LayerNorm(128)

    def forward(self, x):
        x = F.gelu(self.ln1(self.fc1(x)))
        x = F.gelu(self.ln2(self.fc2(x)))
        x = F.gelu(self.ln3(self.fc3(x)))
        x = self.fc4(x)
        return x"""


#new version
class ResidualBlock(nn.Module):
    def __init__(self, size):
        super().__init__()
        self.fc = nn.Linear(size, size)
        self.ln = nn.LayerNorm(size)

    def forward(self, x):
        h = self.fc(x)
        h = self.ln(h)
        h = F.gelu(h)
        return x + h


class BGnet(nn.Module):
    def __init__(self, input_size=28):
        super().__init__()

        self.input_layer = nn.Linear(input_size, 256)
        self.ln_in = nn.LayerNorm(256)

        self.res_blocks = nn.Sequential(
            *[ResidualBlock(256) for _ in range(4)]
        )

        self.fc_reduce1 = nn.Linear(256, 128)
        self.ln_reduce1 = nn.LayerNorm(128)

        self.fc_reduce2 = nn.Linear(128, 64)
        self.ln_reduce2 = nn.LayerNorm(64)

        self.output_layer = nn.Linear(64, 1)

    def forward(self, x):
        x = F.gelu(self.ln_in(self.input_layer(x)))
        x = self.res_blocks(x)
        x = F.gelu(self.ln_reduce1(self.fc_reduce1(x)))
        x = F.gelu(self.ln_reduce2(self.fc_reduce2(x)))
        return self.output_layer(x)


#creating the model
model = BGnet()
model.load_state_dict(torch.load("nv_backgammon_model5311.pth15"))

def ai_bot(board, dice,return_state=False):

    #greedy bot's pattern

    turns = board.get_valid_turns(dice)
    best_move = [[], float("-inf"), board.state]

    # inverting the board
    if dice.turn>0:
        scaled_states = torch.tensor(turns[1]).float() / 10
    else:
        scaled_states=[]
        for i in turns[1]:
            scaled_states.append(i[:24][::-1]+(i[25],i[24],i[27],i[26]))
        scaled_states = torch.tensor(scaled_states).float() / -10

    # Finding the move with the highest score
    if len(scaled_states)==0:
        if return_state:
            if dice.turn > 0:
                return model(torch.tensor(board.state).float() / 10)
            else:

                return model(torch.tensor(board.state[:24][::-1] + (board.state[25], board.state[24], board.state[27], board.state[26])).float() / -10)
        else:
            return []
    scores=model(scaled_states)
    for i in range(len(scores)):
        if scores[i] > best_move[1]:
            best_move = [turns[0][i], scores[i], turns[1][i]]

    if return_state:
        return best_move[1]

    return best_move[0]



def hard_ai_bot(board, dice):
    #hard bot's pattern
    # Expectiminimax algorithm (2-ply)
    turns = board.get_valid_turns(dice)
    best_move = [[], float("inf")]

    # Finding the move with the highest expected outcome
    for path, state in zip(*turns):
        score = 0

        # Saving the state
        save_winner = board.winner
        save_state = board.state[:]
        remaining_state = dice.remaining[:]
        save_dice = dice.state[:]

        # Making the move for further calculation
        for move in path:
            board.make_move(dice, move)

        dice.turn *= -1
        for roll, weight in get_rolls():
            dice.roll(roll)
            score += ai_bot(board, dice, model,True) * weight

        if score < best_move[1]:
            best_move = [path, score]

        # Loading original state
        dice.turn *= -1
        dice.state = save_dice
        dice.remaining = remaining_state
        board.state = save_state
        board.winner = save_winner

    return best_move[0]
