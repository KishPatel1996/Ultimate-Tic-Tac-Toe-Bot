BOT = 'BOT'
import math
from random import random
class Random_Bot:
    TYPE = BOT
    def make_move(self, game):
        poss_moves = game.get_possible_moves()
        print(poss_moves)
        picked_move = poss_moves[math.floor(random() * len(poss_moves))]
        print("ROBOT MOVE -- {}".format(picked_move))
        return picked_move


bot_dict = {
    'random': Random_Bot
}