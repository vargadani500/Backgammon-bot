import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset

import torch.optim as optim

from functions import *
from robots import *
#setting up model




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


class BGnetV2(nn.Module):
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


model = BGnetV2()

#creating dataset

x=[]
y=[]

for i in range(4000000):
    a=np.random.randint(-6, 6, size=28)
    x.append(a.copy())
    b=scorer(a, color=1, greedy = True)
    y.append(b)

x=np.array(x)
y=np.array(y)

#preparing dataset

x_scaled=x/10
y_scaled=np.cbrt(y/333)

print(max(y_scaled))

x_scaled_tensor=torch.from_numpy(x_scaled).float()
y_scaled_tensor=torch.from_numpy(y_scaled).float().unsqueeze(1)

train_dataset = TensorDataset(x_scaled_tensor, y_scaled_tensor)
train_loader = DataLoader(train_dataset, batch_size=256, shuffle=True)






criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)

epochs = 40

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

    print(epoch,running_loss/len(train_loader))

model.load_state_dict(torch.load("nv_backgammon_model509.pth4"))
talalat=0

for _ in range(10000):
    x=[]
    y=[]


    for i in range(30):
        a=np.random.randint(-6, 6, size=28)
        x.append(a.copy())
        b=scorer(a, color=1, greedy = True)
        y.append(b)

    x=np.array(x)
    y=np.array(y)

    #preparing dataset

    x_scaled = x / 10
    y_scaled = np.cbrt(y / 333)



    x_scaled_tensor=torch.from_numpy(x_scaled).float()
    y_scaled_tensor=torch.from_numpy(y_scaled).float().unsqueeze(1)

    """a=np.random.randint(-6, 6, size=28)
    b=scorer(a, color=1, greedy = True)
    a=a/6
    a=torch.from_numpy(a).float()
    
    print(a)
    print(x_scaled_tensor)"""


    with torch.no_grad():
        model.eval()
        pred = model(x_scaled_tensor)
        loss = criterion(pred, y_scaled_tensor)
        """print(model(a))
        print(b/1000)"""


    maxp=-100
    helyp=0
    maxy=-100
    helyy=0

    for i in range(30):
        if pred[i]>maxp:
            maxp=pred[i]
            helyp=i
        if y_scaled_tensor[i]>maxy:
            maxy=y_scaled_tensor[i]
            helyy=i
    if helyy==helyp:
        talalat+=1

print(talalat)

print(loss.item())
if input()=="s":
    PATH = "nv_backgammon_model_masolo.pth"
    torch.save(model.state_dict(), PATH)


