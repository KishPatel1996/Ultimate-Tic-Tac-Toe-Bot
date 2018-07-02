from game import Game


class Game_Manager:

    def __init__(self, player_one, player_two):
        self.player_one = player_one
        self.player_two = player_two
        self.game = Game()
        self.first_player_turn = True
        self.player_one.set_player_id(0)
        self.player_two.set_player_id(1)

    def run_game(self):
        if self.first_player_turn:
            move = self.player_one.make_move(self.game.copy())
        else:
            move = self.player_two.make_move(self.game.copy())

        if move is not None:
            block, space = move
            action_output = self.game.take_action(block, space)
            if action_output is None:
                return None
            self.first_player_turn = not self.first_player_turn
        else:
            print('No action taken.')
        return move

    def game_outcome(self):
        return self.game.is_game_finished()

    def current_board_section(self):
        return self.game.inner_board_section
