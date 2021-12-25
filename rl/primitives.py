import numpy as np
from enum import Enum
import itertools

class PIECE(Enum):
    FREE=0
    P1=1
    P2=2
    DRAW=3

def piece_mapper(piece:PIECE) -> float:
            if piece == PIECE.P1:
                return 1.0
            elif piece == PIECE.P2:
                return -1.0
            else:
                return 0.0


def check_for_win_conditions(board) -> PIECE:
        win_conditions = [
            [0,1,2],
            [3,4,5],
            [6,7,8],
            [0,3,6],
            [1,4,7],
            [2,5,8],
            [0,4,8],
            [2,4,6]
        ]

        for cond in win_conditions:
            if board[cond[0]] == board[cond[1]] == board[cond[2]] and board[cond[0]] in [PIECE.P1,
            PIECE.P2]:
                return board[cond[0]]
        #Check for draw status
        return PIECE.FREE if PIECE.FREE in board else PIECE.DRAW


def convert_mapper(*args):
    return [convert_to_print_friendly(x) for x in args]
def convert_to_print_friendly(piece: PIECE) -> str:
    if piece == PIECE.FREE:
        return " "
    elif piece == PIECE.P1:
        return "X"
    else:
        return "O"

        
def print_board(board):

    for start_index in [0,3,6]:
        for inner in [0,3,6]:
            # for inner_increment in range(3):
            print("{}{}{}|{}{}{}|{}{}{}".format(*convert_mapper(*board[start_index][inner:inner+3],
            *board[start_index+1][inner:inner+3],
            *board[start_index+2][inner:inner+3])))
        print('-----------')
    print()


def create_flat_mask(board) -> np.array:
    return np.asarray(list(map(piece_mapper,itertools.chain(*board))),dtype=np.float)

def create_mask_from_board(board, current_position: int) -> np.array:
    if current_position != -1:
        # mask out all other 
        mask = np.zeros(81)
        mask[current_position*9:current_position*9+9] = 1.0
    else:
        mask = np.ones(81)

    completed_squares = set()
    for i,miniboard in enumerate(board):
        if check_for_win_conditions(miniboard) != PIECE.FREE:
            completed_squares.add(i)

    for i in range(mask.shape[0]):
        j,k = i // 9, i % 9

        if mask[i] != 0.0 and (j in completed_squares or board[j][k] != PIECE.FREE):
            mask[i] = 0
    return mask