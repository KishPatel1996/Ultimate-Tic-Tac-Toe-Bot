from game import Game


class Game_Manager:

    def __init__(self, player_one, player_two):
        self.player_one = player_one
        self.player_two = player_two
        self.game = Game()
        self.first_player_turn = True

    def run_game(self):
        if self.first_player_turn:
            success = self.player_one.make_move(self.game)
        else:
            success = self.player_two.make_move(self.game)

        if success is not None:
            self.first_player_turn = not self.first_player_turn
        else:
            print('No action taken.')
        return success
