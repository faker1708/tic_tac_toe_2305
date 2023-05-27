
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import gym

import matplotlib.pyplot as plt

import pickle


class Net(nn.Module):
    def __init__(self,N_STATES,N_ACTIONS,device ):
        super(Net, self).__init__()
        # 64 32
        self.device = device

        mean = 0
        std = 0.1

        mid_width = 2**4    # 50

        self.fc1 = nn.Linear(N_STATES, mid_width)
        self.fc1.weight.data.normal_(mean, std)   # initialization

        self.out = nn.Linear(mid_width, N_ACTIONS)
        self.out.weight.data.normal_(0, 0.1)   # initialization

    def forward(self, x):
        x = x.to(self.device)
        x = self.fc1(x)
        x = F.relu(x)
        # x = self.fc2(x)
        # x = F.relu(x)
        actions_value = self.out(x)
        return actions_value

