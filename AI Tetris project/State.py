import numpy as np
from CONSTANTS import *
import secrets
import pygame
import tetrominos 



class State:
    
    def __init__(self, board = None, curr = None, end = None, score = None):
        if board:
            self.board = board
        else:
            self.board = np.zeros((ROWS,COLUMNS), dtype=int)
        if curr:
            self.current_piece = curr
        else: 
            self.current_piece = secrets.choice(range(1,8))
        if end:
            self.end_of_game = end
        else:
            self.end_of_game = 0
        if score:
            self.score = score
        else:
            self.score = 0
        self.cleared =  0

    
    def new_piece(self, board , screen = None, piece = None):
        if piece is not None:
            rnd = piece
        else:
            rnd = secrets.choice(range(1,8))

        # rnd = 7
        # rnd1 = random.SystemRandom(0,7)
        new_piece = list(tetrominos.TETROMINOES.values())[rnd - 1]
        color = tetrominos.COLORS[rnd]
        rects = []
        row, col = new_piece.shape
        x = LINES_WIDTH + DISTANCE * 3
        y = LINES_WIDTH
        for r in range(row):
            for c in range(col):
                if new_piece[r][c] == 1:
                    rect = pygame.Rect(
                        x + c * DISTANCE,
                        y + r * DISTANCE,
                        SQUARE_SIZE,SQUARE_SIZE)
                    rects.append((rect,color))
                    board[r][c+3] = -1
        if screen is not None:
            for rect, color in rects:
                pygame.draw.rect(screen, color, rect)
        self.current_piece = rnd
        return board

        
        
    def get_dqn_states(self, boards):
        dqn_states = []
        for br in boards:
            dqn_states.append(self.get_state(br))
        return dqn_states

    
    def get_state(self, board = None):
        
        
        # board[19,0] = 1
        # board[18,0] = 1
        # board[19,1] = 1
        # board[18,1] = 1

        if board is None:
            board = self.board

        
        
        col_height = []
        holes = 0

        for c in range(COLUMNS):
            for r in range(ROWS):
                if board[r, c] != 0 and board[r, c] != -1:
                    col_height.append(r)
                    break
            if len(col_height) == c:
                col_height.append(ROWS)
        
        for c in range(COLUMNS):
            top = False
            for r in range(col_height[c], ROWS):
                if board[r, c] != -1 and board[r,c] != 0:
                    if not top:
                        top = True
                elif top:
                     holes += 1
                     
        col_height = np.array(col_height) - ROWS
        col_height = np.abs(col_height)
        
        height = np.sum(col_height)
        
        bumpiness = np.sum(np.abs(np.diff(col_height)))

        max_col = max(col_height)
        
 
    
        state = np.concatenate([col_height,[ bumpiness, holes]]).astype(np.float32)

        # state = np.array([height, bumpiness, holes]).astype(np.float32)
        
        return state
    

        
    def copy(self):
        new_board = self.board.copy()
        new_piece = self.current_piece
        new_end = self.end_of_game
        new_score = self.score
        return State(new_board, new_piece, new_end, new_score)

    
        

    
# s = State()

# State().get_state(1)
