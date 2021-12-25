from typing import List
from random import random

from primitives import PIECE, check_for_win_conditions, create_mask_from_board, print_board

class Bot:
    def __init__(self, **kwargs):
        pass
    def get_action(self, board_state, valid_square) -> int:
        pass


class UserBot(Bot):

    def get_action(self, board_state, valid_square) -> int:
        print_board(board_state)
        flat_mask = create_mask_from_board(board_state,valid_square)
        valid_actions = [[i// 9, i % 9] for i, x in enumerate(flat_mask) if x == 1.0]
        print(f"The valid actions are {valid_actions}")
        return eval(input("Enter user position >>> "))

class RandomBot(Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_action(self, board_state, current_square) -> int:
        if current_square == -1:
            #collect all free positions
            free_spots = []
            for i,row in enumerate(board_state):
                if check_for_win_conditions(row) == PIECE.FREE:
                    free_spots.extend([[i, x] for x in _get_valid_positions(row)])
            return free_spots[int(random() * len(free_spots))]#[int(randint(0,8)), int(randint(0,8))]
        else:
            free_spots = _get_valid_positions(board_state[current_square])
            return [current_square, free_spots[int(random() * len(free_spots))]]


def _get_valid_positions(square) -> List[int]:
    return [i for i,x in enumerate(square) if x == PIECE.FREE]