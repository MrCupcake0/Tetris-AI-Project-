from collections import deque
import random
import torch
from Environment import Environment
import numpy as np




class ReplayBuffer:
    def __init__(self, capacity= 10000) -> None:
        self.buffer = deque(maxlen=capacity)

    def push (self, state, action, reward, next_state, next_state_dqn, done):
        self.buffer.append((state, action, reward, next_state, next_state_dqn, done))


    def sample (self, batch_size):
        states, actions, rewards, next_states, next_states_dqn, dones = zip(*random.sample(self.buffer, batch_size))
        # states = torch.vstack(state_tensors)
        # actions= torch.vstack(action_tensor)
        np_batch = np.stack(rewards)
        rewards_tensor = torch.from_numpy(np_batch).to(torch.float32).reshape(-1,1)
        # next_states = torch.vstack(next_state_tensors)
        np_batch = np.stack(next_states_dqn)
        next_states_dqn_tensor = torch.from_numpy(np_batch).to(torch.float32)
        np_batch = np.stack(dones)
        dones_tensor = torch.from_numpy(np_batch).to(torch.float32).reshape(-1,1)
        return states, actions, rewards_tensor, next_states, next_states_dqn_tensor, dones_tensor

            
    # def sample (self, batch_size):
    #     if (batch_size > self.__len__()):
    #         batch_size = self.__len__()
    #     state_tensors, action_tensor, reward_tensors, next_states, next_state_tensors_dqn, dones = zip(*random.sample(self.buffer, batch_size))
    #     states = torch.vstack(state_tensors)
    #     actions = torch.vstack(action_tensor)
    #     rewards = torch.vstack(reward_tensors)
    #     next_states_dqn = torch.vstack(next_state_tensors_dqn)
    #     done_tensor = torch.tensor(dones).long().reshape(-1,1)
    #     return states, actions, rewards, next_states, next_states_dqn, done_tensor

    def __len__(self):
        return len(self.buffer)

    def toTensor (self ,state):
        array = state.reshape(-1)
        tensor = torch.tensor(array, dtype=torch.float32)
        return tensor