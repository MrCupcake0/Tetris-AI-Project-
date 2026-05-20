import pygame
from Graphics import *
import numpy as np
import tetrominos
import secrets
import State
graphics = Graphics()

class Environment:
    
    def __init__(self, state = None, train = False):
        self.state = state
        self.train = train
        state.score = 0
        self.end_of_game = 0    
        self.timer = 0
        self.fast_fall_timer = 0
        self.fall_speed = 48
        self.fast_fall_speed = 3
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.stop = False
        state.new_piece(state.board, self.screen)
        pygame.display.set_caption('Tetris')
        
    def is_end_of_game(self):
        for r in range(2):
            for c in range(8):
                if self.state.board[r][c+2] != 0 and self.state.board[r][c+2] != -1:
                    self.end_of_game = 1
        return self.end_of_game == 1

    
    def restart(self, state):
        state.board = np.zeros((ROWS,COLUMNS))
        state.score = 0
        self.end_of_game = 0    
        self.timer = 0
        self.fast_fall_timer = 0
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.stop = False
        return state.new_piece(state.board, self.screen)
        
    
    def draw(self, state, action):
        if self.end_of_game == 1:
            return True
        if state.current_piece == 0:
            state.new_piece(state.board, self.screen)
        if type(action) == tuple:
            temp = state.current_piece 
            self.draw_dqn(state, action)
            graphics(state, temp)
            state.new_piece(state.board, self.screen)
            if not self.train:
                self.clear_line(state.board)
        else:
            graphics(state, self.state.current_piece)

        if not type(action) == tuple:
            self.move(action, state.board)
        self.update_timer(state.board)
        pygame.display.update()
        done = self.is_end_of_game()
        return done
    
    def draw_dqn(self, state, action):
        board = state.board
        for i in range(4):
            self.move(1, board)
        for i in range(action[1]):
            self.rotate(board)
        for i in range(action[0]):
            self.move(2, board)
        state.board = self.hard_drop(board, state.current_piece)



    def get_legal_actions(self, state): #NOT FINISHED NEED TO FIX, maybe finished

        if type(state) == list:
            board = state[0]
            curr = state[1]
        else:
            curr = state.current_piece
            board = state.board.copy()

        actions = []
        boards = []
        
        r = 4
        length = 3
        if curr == 1:
            r = 2
            length = 1
        elif curr == 2:
            r = 1
            length = 2
        elif curr == 4 or curr == 5:
            r = 2

        
            
        for i in range(4):
            self.move(action=1, board=board)
        for column in range(COLUMNS + 1 - length):
            for rotation in range(r):
                board_temp = board.copy()
                actions.append((column, rotation))
                for j in range(rotation):
                    self.rotate(board_temp)
                for k in range(column):
                    self.move(action=2, board=board_temp)   
                board_temp = self.hard_drop(board_temp, curr)
                boards.append(board_temp)

        # if curr != 1 and curr != 2:
        #     last_board = board_temp
        #     board = np.where(last_board == curr, -1, last_board)
        #     for i in range(int(r/2)):
        #         board_temp = board.copy()
        #         self.move(action=2, board=board_temp)
        #         self.lock_piece(board_temp, curr)
        #         boards.append(board_temp)
        #         if i == 0:
        #             actions.append((8,1))
        #         else:
        #             actions.append((8,3))
        #         self.rotate(board=board)
        #         self.rotate(board=board)

        if curr != 1 and curr != 2:
            for i in range(int(r/2)):
                board_temp = board.copy()
                self.rotate(board_temp)
                if i == 0:
                    actions.append((8,1))
                else:
                    actions.append((8,3))
                    self.rotate(board_temp)
                    self.rotate(board_temp)
                for i in range(COLUMNS + 1 - length):
                    self.move(2,board_temp)
                board_temp = self.hard_drop(board_temp, curr)
                boards.append(board_temp)
        
        return actions, boards
    
    def hard_drop(self, board, curr):
        piece = []
        bottoms = {}

        for r in range(ROWS):
            for c in range(COLUMNS):
                if board[r][c] == -1:
                    piece.append((r, c))
                    bottoms[c] = max(bottoms.get(c, 0), r)

        
        if not piece:
            return board
        drop = ROWS 
        
        for c, bottom in bottoms.items():
            dist = 0
            for i in range(bottom + 1, ROWS):
                if board[i][c] != 0 and board[i][c] != -1:
                    break
                dist += 1
            drop = min(drop, dist)

        for r, c in piece:
            board[r][c] = 0
            
        for r, c in piece:
            new_r = r + drop
            board[new_r][c] = curr
            
        
        return board
    
    def reward(self, state, after_state, end_of_game, board):
        if end_of_game:
            return -100.0  
        
        cleared = self.clear_line(board)
        lines_cleared = np.power(cleared, 2.0) 

        # State differences
        height = after_state[0] - state[0]
        bumpiness = after_state[1] - state[1]
        holes = after_state[2] - state[2]
        # max_col = after_state[12] - state[12]

        reward = 0.1 + lines_cleared - holes * 0.5 - bumpiness * 0.05  - height * 0.03 
        
        return reward

    def move(self, action, board):
        
        if action == 1 and self.is_valid(board,col=-1):
            self.move_left(board)
        elif action == 2 and self.is_valid(board,col=1):
            self.move_right(board)
        elif action == 3 and self.is_valid_down(board):
            self.move_down(board)
        elif action == 4:
            self.rotate(board)
        elif action == 11:
            print(self.state.get_state(self.state.board))
        if action != 7 and self.stop:
            self.stop = False
        # elif action == 6:
        elif action == 7 and self.fast_fall_timer >= self.fast_fall_speed and not self.stop:
            if self.is_valid_down(board):
                self.move_down(board)
            self.fast_fall_timer = 0
            self.timer = 0

    def update_timer(self,board):
        self.timer +=1
        self.fast_fall_timer +=1

        if self.timer >= self.fall_speed:
            if self.is_valid_down(board):
                self.move_down(board)
            self.timer = 0

    def rotate(self, board):
        
        piece_cells = []
        for r in range(ROWS):
            for c in range(COLUMNS):
                if board[r, c] == -1:
                    piece_cells.append((r, c))

        if not piece_cells:
            return  
        rows = [r for r, _ in piece_cells]
        cols = [c for _, c in piece_cells]

        min_r, max_r = min(rows), max(rows)
        min_c, max_c = min(cols), max(cols)

        height = max_r - min_r + 1
        width = max_c - min_c + 1

        piece = np.zeros((height, width), int)
        for r, c in piece_cells:
            piece[r - min_r, c - min_c] = -1

        rotated = np.rot90(piece, -1)

        for r in range(rotated.shape[0]):
            for c in range(rotated.shape[1]):
                if rotated[r, c] != 0:
                    new_r = min_r + r
                    new_c = min_c + c

                    if new_r < 0 or new_r >= ROWS or new_c < 0 or new_c >= COLUMNS:
                        return 

                    if board[new_r, new_c] != 0 and (new_r, new_c) not in piece_cells:
                        return

        for r, c in piece_cells:
            board[r, c] = 0

        for r in range(rotated.shape[0]):
            for c in range(rotated.shape[1]):
                if rotated[r, c] != 0:
                    board[min_r + r, min_c + c] = -1
                    
    def is_valid_down(self, board):
        valid = True
        for c in range(COLUMNS):
            for r in range(ROWS -1, -1 , -1):
                if board[r][c] == -1:
                    if r + 1 == ROWS or board[r+1][c] != 0:
                        valid = False
                    else:
                        break
        if not valid:
            self.lock_piece(board)
        return valid
    
    def is_valid(self, board, col = 0):
        for c in range(COLUMNS):
            for r in range(ROWS):
                if board[r][c] == -1:
                    if col == -1:
                        if c == 0:
                            return False
                        elif board[r][c-1] != 0 and board[r][c-1] != -1:
                            return False
                    elif col == 1:
                        if c == COLUMNS - 1: 
                            return False
                        elif board[r][c+1] != 0 and board[r][c+1] !=-1:
                            return False
        return True


    def move_left(self, board):
        for r in range(ROWS):
            for c in range(COLUMNS):
                if board[r][c] == -1:
                    board[r][c - 1] = board[r][c] 
                    board[r][c] = 0
      
    def move_right(self, board):
        for r in range(ROWS - 1, -1, -1):
            for c in range(COLUMNS - 1, -1, -1):
                if board[r][c] == -1:
                    board[r][c + 1] = board[r][c] 
                    board[r][c] = 0
                    
    def lock_piece(self, board, piece = None):
        if piece:
            self.state.current_piece = piece
        for r in range(ROWS):
            for c in range(COLUMNS):
                if board[r][c] == -1:
                    board[r][c] = self.state.current_piece
        if not piece: #doesn't happen when the function is called through hard drop
            self.clear_line(board)
            self.state.current_piece = 0
            self.stop = True

    def move_down(self, board):
        # Iterate from bottom to top to prevent overwriting
        for row in range(ROWS - 2, -1, -1):  # Start from second-to-last row
           for col in range(COLUMNS):
               if board[row, col] == -1:
                   board[row + 1, col] = board[row, col]  # Move block down
                   board[row, col] = 0  # Clear old position


    def clear_line(self, board):
        new_board = np.zeros_like(board)
        full_row = ROWS - 1
        for r in range(ROWS - 1 , -1, -1):
            if not np.all(board[r] != 0):
                new_board[full_row] = board[r]
                full_row -= 1
        if full_row > -1:
            self.state.score += full_row + 1
        board[:,:] = new_board[:,:]
        return full_row + 1
        

    def __call__(self, board, action):
        return self.draw(board, action)
