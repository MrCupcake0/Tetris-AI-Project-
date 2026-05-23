import torch
import torch.nn as nn
import torch.nn.functional as F
from CONSTANTS import *
import copy
# if torch.cuda.is_available():
#     device = torch.device('cuda')
# else:
#     device = torch.device('cpu')
input_size = 12
gamma = 0.99


class DQN(nn.Module):
    def __init__(self,device = torch.device('cpu')) -> None:
        super().__init__()
        self.device = device
        # print(device)
        self.linear1 = nn.Linear(input_size, 32)
        self.linear2 = nn.Linear(32, 64)
        self.output = nn.Linear(64, 1)
        self.MSELoss = nn.MSELoss()

        self.to(self.device)
        
    def forward(self, x):
        # print(f"Input x device: {x.device}")
        # print(f"Layer weight device: {self.linear1.weight.device}")
        x = self.linear1(x)
        x = F.leaky_relu(x)
        x = self.linear2(x)
        x = F.leaky_relu(x)
        x = self.output(x)

        return x
    
    def loss (self, Q_values, rewards, Q_next_Values, dones ):
        Q_new = rewards.to(self.device) + gamma * Q_next_Values * (1- dones.to(self.device))
        return self.MSELoss(Q_values, Q_new)
    
    
    def __call__(self, state):
        return self.forward(state).to(self.device)
    
    def toTensor(self, state):
        array = state.reshape(-1)
        tensor = torch.tensor(array, dtype=torch.float32)
        return tensor
    
    def copy (self):
        return copy.deepcopy(self)
