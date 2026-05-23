import numpy as np

TETROMINOES = {

    1: np.array([[1, 1, 1, 1]]),  # CYAN (I)

    2: np.array([[0, 1, 1, 0],    # YELLOW (O)
                 [0, 1, 1, 0]]),

    3: np.array([[1, 1, 1],       # PURPLE (T)
                 [0, 1, 0]]),

    4: np.array([[0, 1, 1],       # GREEN (S)
                 [1, 1, 0]]),

    5: np.array([[1, 1, 0],       # RED (Z)
                 [0, 1, 1]]),

    6: np.array([[1, 1, 1],       # BLUE (J)
                 [0, 0, 1]]),

    7: np.array([[1, 1, 1],       # ORANGE (L)
                 [1, 0, 0]])
}

COLORS = {
    1: (0, 255, 255),   # CYAN (I)
    2: (255, 255, 0),   # YELLOW (O)
    3: (128, 0, 128),   # PURPLE (T)
    4: (0, 255, 0),     # GREEN (S)
    5: (255, 0, 0),     # RED (Z)
    6: (0, 0, 255),     # BLUE (J)
    7: (255, 165, 0),   # ORANGE (L)
}


