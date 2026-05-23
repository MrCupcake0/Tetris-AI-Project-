import torch
import random
from CONSTANTS import *
from DQN import DQN
import numpy as np
from State import State
import numpy as np
import time






# class bla:
#     def get_Action(self, events = None, state = None, train = False, epoch = 0):
#         actions, boards = self.env.get_legal_actions(state)
#         dqn_states = state.get_dqn_states(boards)

#         piece = state.current_piece
#         ret_state = [0, piece] 


#         if train:
#             epsilon = self.epsilon_greedy(epoch)
#             rnd = random.random() 
#             if rnd < epsilon:
#                 idx = random.randrange(len(actions))
#                 ret_state[0] = state.new_piece(boards[idx],piece=piece)
#                 return actions[idx], ret_state
            

#         np_batch = np.stack(dqn_states)

#         tensor_batch = torch.from_numpy(np_batch).to(dtype=torch.float32)

#         with torch.no_grad():
#             Q_values = self.DQN(tensor_batch)

#         state_indx = torch.argmax(Q_values)
        
#         # rnd = random.SystemRandom().randint(0, len(actions) - 1)
#         # state_indx = rnd

#         ret_state[0] = state.new_piece(boards[state_indx],piece=piece)
#         return actions[state_indx], ret_state
    

