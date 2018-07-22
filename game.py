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
        self.ownership = [-1] * 9
        self.board = -1 * np.ones((9,9), dtype=np.uint8)

    def copy(self):
        game_copy = Game()
        game_copy.player= self.player
        game_copy.game_done = self.game_done
        game_copy.inner_board_section = self.inner_board_section
        game_copy.board = np.copy(self.board)
        game_copy.ownership = self.ownership[:]
        return game_copy
        
    def __eq__(self, other):
        running_check = True
        running_check = running_check and self.player == other.player
        running_check = running_check and self.inner_board_section == other.inner_board_section
        running_check = running_check and np.array_equal(self.board, other.board)
        return running_check

    def get_possible_moves(self):
        possible_move_pairs = []
        if self.inner_board_section != -1:
            for j in range(9):
                if self.board[self.inner_board_section][j] == -1:
                    possible_move_pairs.append([self.inner_board_section, j])
        else:
            for i in range(9):
                if self.ownership[i] != -1:
                    continue
                for j in range(9):
                    if self.board[i][j] == -1:
                        possible_move_pairs.append([i,j])
        return possible_move_pairs

    def take_action(self, inner_board_section, space_location):
        if self.game_done == -1:
            if not self.check_move(inner_board_section, space_location):
                print('Invalid Move.  Pick another place.')
                return None
            self.board[inner_board_section, space_location] = self.player
            self.inner_board_section = space_location
            inner_block_winner = self.block_winner_condition(self.board[inner_board_section])
            if inner_block_winner != -1:
                self.ownership[inner_board_section] = inner_block_winner
                outer_block = self.block_winner_condition(self.ownership)
                if outer_block != -1:
                    self.game_done = outer_block
                    return [inner_board_section, space_location]
                elif not self.possible_to_win_check():
                    self.game_done = 2
                    return [inner_board_section, space_location]
            self.player = 1 - self.player
            if self.ownership[space_location] != -1:
                self.inner_board_section = -1
            else:
                self.inner_board_section = space_location
            return [inner_board_section, space_location]
        return None

    def simulate_action(self, inner_board_section, space_location):
        if self.game_done == -1:
            if self.check_move(inner_board_section, space_location):
                board_copy = np.copy(self.board)
                board_copy[inner_board_section, space_location] = self.player
                return board_copy

    def check_move(self, inner_board_section, space_location):
        if min(inner_board_section, space_location) < 0 or max(inner_board_section, space_location) > 8:
            return False
        if self.inner_board_section == -1 and self.ownership[inner_board_section] != -1:
            return False
        if self.inner_board_section != -1:
            return self.inner_board_section == inner_board_section and self.board[inner_board_section][space_location] == -1
        return self.board[inner_board_section][space_location] == -1

    def is_game_finished(self):
        # -1 for going
        # 0 for first player
        # 1 for second player
        # 2 for tie
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
        for winning_combo in self.winning_combinations:
            player_one_count = 0
            player_two_count = 0
            for grid in winning_combo:
                if self.ownership[grid] == 0:
                    player_one_count = player_one_count + 1
                elif self.ownership[grid] == 1:
                    player_two_count = player_two_count + 1
            
            #only one spot taken.  Still a chance for a winner
            if player_one_count + player_two_count <= 1:
                return True

            # one player owns two and the other is free.  Chance
            if (player_one_count == 2 and player_two_count == 0) or \
               (player_two_count == 2 and player_one_count == 0):
               return True
        return False

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
