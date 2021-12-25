from gym import core
from bot import Bot
from primitives import PIECE, check_for_win_conditions,print_board


class TixTaxEnv(core.Env):
    def initialize_space(self):
        self.board_state = []
        for _ in range(9):
            self.board_state.append([PIECE.FREE] * 9)

        self.completed_squares = [PIECE.FREE] * 9
        self.current_square = -1
    
    def __init__(self, opponent:Bot):
        super(TixTaxEnv,self).__init__()
        self.opponent = opponent
        self.initialize_space()

    def reset(self):
        self.initialize_space()
        return [self.board_state, self.current_square], False


    def _execute_move(self, action, player: PIECE):
        # assert valid action
        assert self.completed_squares[action[0]] == PIECE.FREE and self.board_state[action[0]][action[1]] == PIECE.FREE
        self.board_state[action[0]][action[1]] = player


    def change_current_square(self, action):
        if self.completed_squares[action[1]] != PIECE.FREE:
            self.current_square = -1
        else:
            self.current_square = action[1]
    def bot_turn(self):
        bot_action = self.opponent.get_action(self.board_state, self.current_square)
        self._execute_move(bot_action, PIECE.P2)
        self.completed_squares[bot_action[0]] = check_for_win_conditions(self.board_state[bot_action[0]])  
        self.change_current_square(bot_action)
     
    def step(self, action):
        # assert action is a valid one 
        self._execute_move(action, PIECE.P1)

        self.completed_squares[action[0]] = check_for_win_conditions(self.board_state[action[0]])
        game_done_check = check_for_win_conditions(self.completed_squares)

        if game_done_check != PIECE.FREE:
            rew = 0
            if game_done_check == PIECE.P1:
                rew = 1.0
            else:
                rew = -1.0
            return [self.board_state,self.current_square], rew, True

        self.change_current_square(action)
        
        # Bot's turn
        self.bot_turn()
        game_done_check = check_for_win_conditions(self.completed_squares)

        if game_done_check != PIECE.FREE:
            return [self.board_state,self.current_square], -1.0, True

        return [self.board_state,self.current_square], 0, False

