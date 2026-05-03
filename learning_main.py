import sys

import numpy as np
import torch

from robots import *



#The number of games played between learning stages
learning_stage_length=20000



def main():
    # Setting the game up
    board = Board()
    board.set()


    #storing the value of the starting state
    a=np.array(board.state)
    b=scorer(a,1)
    b=np.cbrt(np.array([b]) / 333)
    a = a / 10
    a = torch.from_numpy(a).float()


    stage_number=0
    num_of_models=0
    prev_wins=0

    dice = Dice()

    sum_of_wins = 0
    total_games = 0
    human_turn = False
    start_pos, end_pos = 0, 0
    turn = []

    # Reading
    white_bot = globals()[settings.W_Player]
    black_bot = globals()[settings.B_Player]

    #creating the model

    prev_model =BGnet()
    model = BGnet()
    model.load_state_dict(torch.load("nv_backgammon_model5311.pth15"))
    prev_model.load_state_dict(torch.load("nv_backgammon_model5311.pth15"))
    PATH = "nv_backgammon_model5311.pth15"
    prev_winrate = 0.5311
    autonomy=0.02


    #Setting up the tools
    print("Learning")
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.00005)
    state_database=[]
    reward_database=[]


    while True:
        # Making moves
        if not human_turn:
            if board.winner == 0:
                if dice.turn == 1:
                    # Check if human player
                    if settings.W_Player == "human":
                        human_turn = True
                    else:
                        dice.roll()
                        # Get the bots decision
                        turn = white_bot(board, dice,model)
                else:
                    # Check if human player
                    if settings.B_Player == "human":
                        human_turn = True
                    else:
                        dice.roll()
                        # Get the bots decision
                        turn = black_bot(board, dice,prev_model)
                if not human_turn:
                    for move in turn:
                        board.make_move(dice, move)
                    # storing decisions
                    state_database.append(board.state.copy())
                    dice.remaining = ()
                    dice.turn *= -1
            else:
                sum_of_wins += board.winner
                # 1 if the winner white
                winner_person=board.winner
                board.winner = 0
                board.set()
                total_games += 1
                if total_games % 1000 == 0:
                    print(f"Total games: {total_games}\nCurrent standing: ({settings.B_Player}){int(total_games/2-sum_of_wins/2)}:{int(total_games/2+sum_of_wins/2)}({settings.W_Player})")


                #creating database

                len_reward_database = len(reward_database)


                with torch.no_grad():
                    model.eval()
                    for current_state1 in range(len(state_database) - len(reward_database) - 1):
                        # print(model(torch.tensor(state_database[current_state1 + len_reward_database + 1]).float()/6))
                        # print((scorer(state_database[current_state1 + len_reward_database],1) / 333)**0.3)
                        reward_database.append(1 * ((0.45 - autonomy) * np.cbrt(
                            scorer(state_database[current_state1 + len_reward_database], 1) / 333) + (
                                                                0.55 + autonomy) * torch.clamp_(prev_model(
                            torch.tensor(state_database[current_state1 + len_reward_database + 1]).float() / 10), -1,
                                                                                                1)))
                    if winner_person > 0:
                        reward_database.append(torch.tensor([1.0]))
                    else:
                        reward_database.append(torch.tensor([-1.0]))

                # learing process

                if total_games % learning_stage_length == 0:

                    b = scorer(a, color=1, greedy=True)

                    with torch.no_grad():
                        model.eval()
                        print(model(a))
                        print(b)

                    # saving the improvement as white is ai bot
                    current_win_rate = (
                                                   int(total_games / 2 + sum_of_wins / 2) - prev_wins) / learning_stage_length
                    print(f'Current win rate: {current_win_rate}')

                    #for teaching vs another bot (for this AI must be white)
                    # if current_win_rate > prev_winrate + 0.001:

                    #for teaching against itself
                    # If the new bot performs better, the teacher changes:
                    if current_win_rate > 0.502:
                        prev_model.load_state_dict(torch.load(PATH))
                        autonomy += 0.01
                        prev_winrate = current_win_rate
                        print(f"New teacher model: {PATH}")
                        print(f'Autonomy: {autonomy}')
                        stage_number += 1



                    # preparing the dataset
                    x = np.array(state_database)
                    y = np.array(reward_database)

                    print(len(x))
                    print(len(y))

                    x_scaled = x / 10

                    x_scaled_tensor = torch.from_numpy(x_scaled).float()
                    y_scaled_tensor = torch.from_numpy(y).float()

                    train_dataset = TensorDataset(x_scaled_tensor, y_scaled_tensor)
                    train_loader = DataLoader(train_dataset, batch_size=256, shuffle=True)


                    #training loop
                    epochs = 10

                    for epoch in range(epochs):
                        model.train()
                        running_loss = 0.0

                        for x_batch, y_batch in train_loader:
                            optimizer.zero_grad()
                            pred = model(x_batch)
                            loss = criterion(pred, y_batch)

                            loss.backward()
                            optimizer.step()

                            running_loss += loss.item()

                        print(epoch, running_loss / len(train_loader))

                    #check the datas
                    print(max(reward_database), min(reward_database))
                    #check the value of the starting state (to avoid inflation)
                    with torch.no_grad():
                        model.eval()
                        print(model(a))
                        print(b)

                    #clearing database
                    state_database = []
                    reward_database = []

                    # saving the model
                    num_of_models += 1
                    PATH = "nv_backgammon_model.pth" + str(num_of_models)
                    torch.save(model.state_dict(), PATH)
                    print(
                        f"Model weights saved: {PATH} New winrate: {current_win_rate} This is the {num_of_models}. model. Teaching trials: {stage_number}")
                    prev_wins = total_games / 2 + sum_of_wins / 2








if __name__ == '__main__':
    main()
