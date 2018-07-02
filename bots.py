BOT = 'BOT'
import math
from random import random
class Random_Bot:
    TYPE = BOT
    def __init__(self):
        self.player_id = None

    def set_player_id(self, player_id):
        self.player_id = player_id

    def make_move(self, game):
        poss_moves = game.get_possible_moves()
        print(poss_moves)
        picked_move = poss_moves[math.floor(random() * len(poss_moves))]
        print("ROBOT MOVE -- {}".format(picked_move))
        return picked_move

class Alpha_Beta_Heuristic_Bot:
    TYPE = BOT

    def __init__(self):
        self.player_id = None

    def set_player_id(self, player_id):
        self.player_id = player_id
        print('BOT ID: {}'.format(self.player_id))

    def make_move(self, game):
        depth = 4
        for x in  game.ownership:
            if x != -1:
                depth = depth + 1
        depth = min(depth, 9)
        score, move = self.alpha_beta_tree_traversal(game, -1e6, 1e6, True, 0, depth)
        print('Best score: {}'.format(score))
        return move

    def alpha_beta_tree_traversal(self, game_state, alpha, beta,
         isMaximizer, depth, maxDepth):
        # poss_moves = game_state.get_possible_moves()
        # if len(poss_moves) == 0 or game_state.game_done:
        if game_state.game_done != -1:
            # leaf node
            outcome = game_state.game_done
            if outcome == self.player_id:
                return 10000, None
            elif outcome == 2:
                return 0, None
            elif outcome == 1 - self.player_id:
                return -10000, None
            else:
                raise RuntimeError('No possible moves left, but no ending reached')
        
        # check if maxDepth reached
        if depth >= maxDepth:
            score = self.heuristic(game_state)
            # print('Heuristic Score: {}'.format(score))
            return score, None

        poss_moves = game_state.get_possible_moves()
        if isMaximizer:
            curr_max_value = -1e6
            best_action = None
            for move_set in poss_moves:
                updated_game_state = game_state.copy()
                if updated_game_state.take_action(move_set[0], move_set[1]) is None:
                    return -1e6, None
                child_output = self.alpha_beta_tree_traversal(updated_game_state,
                    alpha, beta, False, depth + 1, maxDepth)[0]
                if child_output > curr_max_value:
                    curr_max_value = child_output
                    best_action = move_set
                    alpha = max(alpha, child_output)
                    if (beta <= alpha):
                        # print('Trim triggered')
                        return beta, None

            return curr_max_value, best_action
        else:
            curr_min_value = 1e6
            best_action = None
            for move_set in poss_moves:
                updated_game_state = game_state.copy()
                if updated_game_state.take_action(move_set[0], move_set[1]) is None:
                    return 1e6, None
                child_output = self.alpha_beta_tree_traversal(updated_game_state,
                    alpha, beta, True, depth + 1, maxDepth)[0]
                if child_output < curr_min_value:
                    curr_min_value = child_output
                    best_action = move_set
                    beta = min(beta, child_output)
                    if beta <= alpha:
                        # print('Trim triggered')
                        return alpha, None
            return curr_min_value, best_action

    def random_traversal(self, game_state, iteration_count):
        #normalizes output of games_won - games_lost
        game_won = 0
        game_lost = 0
        for _ in range(iteration_count):
            gs = game_state.copy()
            while gs.game_done == -1:
                poss_moves = gs.get_possible_moves()
                if len(poss_moves) is 0:
                    print('Should not be here')
                random_move = poss_moves[math.floor(random() * len(poss_moves))]
                gs.take_action(random_move[0], random_move[1])
            if gs.game_done == self.player_id:
                game_won = game_won + 1
            elif gs.game_done == 1 - self.player_id:
                game_lost = game_lost + 1
        return (game_won - game_lost) / iteration_count

    def heuristic(self,game_state):
        # game not done so no need to check for complete winners
        # award +- 1000 for 2 larger grids in a row
        # 100 for single larger grid 
        # 10 for a 2 in a row in a smaller section

        current_player_score = 0
        enemy_score = 0

        counted_in_double = set()

        #check for 2 in a row for larger grid
        for combo in game_state.winning_combinations:
            player = 0
            enemy = 0
            player_set = set()
            enemy_set = set()
            for grid in combo:
                if game_state.ownership[grid] == self.player_id:
                    player = player + 1
                    player_set.add(grid)
                elif game_state.ownership[grid] == 1 - self.player_id:
                    enemy = enemy + 1
                    enemy_set.add(grid)
            if player == 2:
                current_player_score = current_player_score + 1000
                counted_in_double = counted_in_double.union(player_set)
            elif enemy == 2:
                enemy_score = enemy_score + 1000
                counted_in_double = counted_in_double.union(enemy_set)

        #check uncounted single grid

        for i in range(9):
            if i not in counted_in_double:
                owner = game_state.ownership[i]
                if owner == self.player_id:
                    current_player_score = current_player_score + 100

                elif owner == 1 - self.player_id:
                    enemy_score = enemy_score + 100
                else:
                    #unowned grid.  Check for inner matching
                    checked_spaces = set()
                    for combo in game_state.winning_combinations:
                        player = 0
                        enemy = 0
                        player_set = set()
                        enemy_set = set()
                        for grid in combo:
                            if game_state.board[i][grid] == self.player_id:
                                player = player + 1
                                player_set.add(grid)
                            elif game_state.board[i][grid] == 1 - self.player_id:
                                enemy = enemy + 1
                                enemy_set.add(grid)
                        if player == 2:
                            current_player_score = current_player_score + 10
                            checked_spaces = counted_in_double.union(player_set)
                        elif enemy == 2:
                            enemy_score = enemy_score + 10
                            checked_spaces = counted_in_double.union(enemy_set)
        return current_player_score - enemy_score


                


        


bot_dict = {
    'random': Random_Bot,
    'ab': Alpha_Beta_Heuristic_Bot
}