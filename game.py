import numpy as np

class Game:

    # winning combinations
    winning_combinations = [
    # 3 rows
    [0,1,2],
    [3,4,5],
    [6,7,8],
    # 3 columns
    [0,3,6],
    [1,4,7],
    [2,5,8],
    # 2 diagonals
    [0,4,8],
    [2,4,6]
    ]

    def __init__(self):
        # first player is internally represented with a 0 and second with a 1
        # empty spots are a -1
        self.player = 0
        self.game_done = -1
        self.inner_board_section = -1
        self.board = []
        self.ownership = [-1] * 9
        self.board = -1 * np.ones((9,9))


    def get_possible_moves(self):
        possible_move_pairs = []
        if self.inner_board_section != -1:
            for j in range(9):
                if self.board[self.inner_board_section][j] == -1:
                    possible_move_pairs.append([self.inner_board_section, j])
        else:
            for i in range(9):
                for j in range(9):
                    if self.board[i][j] == -1:
                        possible_move_pairs.append([i,j])
        return possible_move_pairs

    def take_action(self, inner_board_section, space_location):
        if self.game_done == -1:
            if not self.check_move(inner_board_section, space_location):
                print('Invalid Move.  Pick another place.')
                return False
            self.board[inner_board_section, space_location] = self.player
            self.inner_board_section = space_location
            inner_block_winner = self.block_winner_condition(self.board[inner_board_section])
            if inner_block_winner != -1:
                self.inner_board_section = -1
                self.ownership[inner_board_section] = inner_block_winner
                outer_block = self.block_winner_condition(self.ownership)
                if outer_block != -1:
                    self.game_done = outer_block
            self.player = 1 - self.player
            return True
        return False

    def check_move(self, inner_board_section, space_location):
        if min(inner_board_section, space_location) < 0 or max(inner_board_section, space_location) > 8:
            return False
        if self.inner_board_section != -1:
            return self.inner_board_section == inner_board_section and self.board[inner_board_section][space_location] == -1
        return self.board[inner_board_section][space_location] == -1

    def is_game_finished(self):
        return self.game_done

    def block_winner_condition(self, array_of_squares):
        # Same function to check larger grid and smaller grid
        # possible winning combinations
        # 0 for first player, 1 for second, 2 for tie (used in encompassing grid)
        # -1 for no conditions met
        for c in Game.winning_combinations:
            if array_of_squares[c[0]] != -1 and array_of_squares[c[0]] != 2:
                if array_of_squares[c[0]] == array_of_squares[c[1]] == array_of_squares[c[2]]:
                    return array_of_squares[c[0]]
        # check for tie condition
        for i in range(len(array_of_squares)):
            if array_of_squares[i] == -1:
                return -1
        # tie condition met
        return 2

    def possible_to_win_check(self):
        pass

    def print_board(self):
        board_order = [[0,1,2], [3,4,5], [6,7,8]]
        board_string ='''
        {}||{}||{}
        {}||{}||{}
        {}||{}||{}
        ---------------------------------------------------------
        {}||{}||{}
        {}||{}||{}
        {}||{}||{}
        ---------------------------------------------------------
        {}||{}||{}
        {}||{}||{}
        {}||{}||{}
        '''.format(self.board[0][board_order[0]],self.board[1][board_order[0]],self.board[2][board_order[0]],
                   self.board[0][board_order[1]],self.board[1][board_order[1]],self.board[2][board_order[1]],
                   self.board[0][board_order[2]],self.board[1][board_order[2]],self.board[2][board_order[2]],
                   self.board[3][board_order[0]],self.board[4][board_order[0]],self.board[5][board_order[0]],
                   self.board[3][board_order[1]],self.board[4][board_order[1]],self.board[5][board_order[1]],
                   self.board[3][board_order[2]],self.board[4][board_order[2]],self.board[5][board_order[2]],
                   self.board[5][board_order[0]],self.board[6][board_order[0]],self.board[7][board_order[0]],
                   self.board[5][board_order[1]],self.board[6][board_order[1]],self.board[7][board_order[1]],
                   self.board[5][board_order[2]],self.board[6][board_order[2]],self.board[7][board_order[2]],
                )

        print(board_string)
        return
