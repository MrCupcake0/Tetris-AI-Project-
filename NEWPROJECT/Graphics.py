import pygame
from CONSTANTS import * 
import tetrominos
import Home_screen


class Graphics:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.surface = pygame.Surface((WIDTH,HEIGHT))
        self.square = pygame.Surface((SQUARE_SIZE,SQUARE_SIZE))
        pygame.display.set_caption('Tetris')

    def draw(self, state, piece):
        self.piece = piece
        self.surface.fill(BLACK)
        # self.draw_Lines()
        self.draw_pieces(state.board)
        self.screen.blit(self.surface,(0,0))
        Home_screen.Home_screen(self.screen).score(state.score)
        pygame.display.update()
        

    # def print_board(self, board):
    #     for row in board:
    #         print(" ".join(map(str, row.astype(int))))  # Convert floats to ints for display
    #     print("\n")

    def draw_Lines(self):
        for i in range(COLUMNS + 1):
            pygame.draw.line(self.surface, BLACK, (8 + i * DISTANCE, 0), (i * DISTANCE, HEIGHT ), LINES_WIDTH)
        for i in range(ROWS + 1):
            pygame.draw.line(self.surface,BLACK,(0 + i * DISTANCE),(WIDTH, i * DISTANCE),LINES_WIDTH)

    def draw_pieces(self, state):
        board = state
        for row in range(ROWS):
            for col in range(COLUMNS):
                if board[row,col] != 0:
                    self.draw_piece((row,col), state)

    def draw_piece(self, row_col, state):
        if state[row_col] == -1:
            color = tetrominos.COLORS[self.piece]
        else:
            color = tetrominos.COLORS[state[row_col]]
        self.square.fill(color)

        x, y = self.calc_pos(row_col)
        self.surface.blit(self.square,(x,y))

    def calc_pos(self, row_col):
        row , col = row_col
        x = LINES_WIDTH + col * DISTANCE
        y = LINES_WIDTH + row * DISTANCE
        return x, y


    def __call__(self, state, current_piece):
        self.draw(state,current_piece)
