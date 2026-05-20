import torch
import random
from CONSTANTS import *
from DQN import DQN
import numpy as np
from State import State
import numpy as np
import time

epsilon_start = 1
epsilon_final = 0.01
epsilon_decay = 1000

class DQN_Agent:
    
    def __init__(self, env, start = None, final = None, decay = None, device = torch.device('cpu')) -> None:
        self.DQN = DQN(device=device)
        # print(device, '1')
        self.device = device
        self.env = env
        self.epsilon_start = start
        self.epsilon_final = final
        self.epsilon_decay = decay
        
    
    def get_Action(self, events = None, state = None, train = False, epoch = 0):
        actions, boards = self.env.get_legal_actions(state)
        dqn_states = state.get_dqn_states(boards)

        piece = state.current_piece
        ret_state = [0, piece]
        
        
        if train:
            epsilon = self.epsilon_greedy(epoch)
            rnd = random.random()
            if rnd < epsilon:
                idx = random.randrange(len(actions))
                ret_state[0] = state.new_piece(boards[idx],piece=piece)
                return actions[idx], ret_state

        
        np_batch = np.stack(dqn_states)

        tensor_batch = torch.from_numpy(np_batch).to(device=self.device, dtype=torch.float32)

        with torch.no_grad():
            Q_values = self.DQN(tensor_batch)
        
        state_indx = torch.argmax(Q_values)

        # rnd = random.SystemRandom().randint(0, len(actions) - 1)
        # state_indx = rnd
        
        ret_state[0] = state.new_piece(boards[state_indx],piece=piece)
        return actions[state_indx], ret_state

    def Q(self, next_states):
        return self.DQN(next_states).to(self.device)
    
    
    def get_Actions(self, next_states):
        states_dqn = []
        for state in next_states:
            _, boards = self.env.get_legal_actions(state)
            dqn_states = State().get_dqn_states(boards)

            np_batch = np.stack(dqn_states)
            tensor_batch = torch.from_numpy(np_batch).to(device=self.device,dtype=torch.float32)

            with torch.no_grad():
                Q_values = self.DQN(tensor_batch)
            
            state_indx = torch.argmax(Q_values)

            states_dqn.append(dqn_states[state_indx])

        states_dqn_tensor = torch.from_numpy(np.stack(states_dqn)).to(torch.float32)

        return states_dqn_tensor
    

    # def epsilon_greedy(self,epoch, start = epsilon_start, final=epsilon_final, decay=epsilon_decay):
    def epsilon_greedy(self,epoch):
        start = self.epsilon_start
        final = self.epsilon_final
        decay = self.epsilon_decay
        if epoch < decay:
            return start - (start - final) * epoch/decay
        return final
    
