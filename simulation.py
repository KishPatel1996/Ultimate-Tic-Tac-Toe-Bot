import numpy as np

from game import Game
import pickle

def sigmoid(x):
    return 1. / (1 + np.exp(-x))

from bots import *

class Simulation:
    def __init__(self, enemy_bot, pickle_file=None):
        self.enemy_bot = enemy_bot()
        if pickle_file is None:
            self.current_player = {'W1': np.random.randn(81* 27).reshape((27,81)) * np.sqrt(27),
                                'W2': np.random.randn((27*9)).reshape((9,27)) * np.sqrt(9),
                                'W3': np.random.randn(9).reshape((1,9))}
        else:
            with open(pickle_file, 'rb') as f_in:
                self.current_player = pickle.load(f_in)
        self.batch_count = 25

        self.reward_decay = 0.99
        self.learning_rate = 1e-3
        self.player_id = None
        self.rms_prop_decay = 0.99



    def feed_foward(self, initial): 
        h1 = np.dot(self.current_player['W1'], initial)
        # h1[h1 < 0] = 0
        h1 = sigmoid(h1)
        h2 = np.dot(self.current_player['W2'], h1)
        # h2[h2<0] = 0
        h2 = sigmoid(h2)
        value = np.dot(self.current_player['W3'], h2)[0,0]
        value = sigmoid(value)

        return value, [initial, h1, h2, value ]

    def back_prop(self, reward, inter_states, grad_buffer):
        curr_reward = reward
        for state in reversed(inter_states):
            deriv_of_sig = state[3] * (1 - state[3])

            dW3 = (curr_reward * deriv_of_sig * state[2]).T
            grad_buffer['W3'] += dW3
            delta_2 = curr_reward * deriv_of_sig * self.current_player['W3'].T * state[2] * (1 - state[2])
            dW2 = np.outer(delta_2, state[1])
            grad_buffer['W2'] += dW2
            delta_1 = np.dot(self.current_player['W2'].T, delta_2) * state[1] * (1 - state[1])
            dW1 = np.outer(delta_1, state[0]) 
            grad_buffer['W1'] += dW1

            curr_reward = curr_reward * self.reward_decay


    def relu_deriv(self, x):
        x = np.copy(x)
        x[x > 0] = 1
        return x

    def simulate(self, save_weights=True):
        rms_prop_cache = {x: np.zeros(y.shape) for x,y in self.current_player.items()}
        grad_buffer = {x: np.zeros(y.shape) for x,y in self.current_player.items()}
        opponent_start = False
        episode_count = 0
        win_count = 0
        epoch_count = 1
        while True:
            game = Game()
            if opponent_start:
                self.enemy_bot.set_player_id(0)
                self.player_id = 1
                opponent_start = False
                oppo_move = self.enemy_bot.make_move(game)
                game.take_action(oppo_move[0], oppo_move[1])
            else:
                self.enemy_bot.set_player_id(1)
                self.player_id = 0
                opponent_start = True
            inter_states = []
            # check if needed
            output_inter = []
            while game.game_done == -1:
                move_arr = []
                value_arr = []
                hidden_states = []
                total_value = 0
                for move in game.get_possible_moves():
                    move_arr.append(move)
                    new_state = game.simulate_action(move[0], move[1]).reshape((-1,1))
                    new_state[new_state == -1] = 2
                    new_state[new_state == 1 - self.player_id] = -1
                    new_state[new_state == self.player_id] = 1
                    new_state[new_state == 2] = 0
                    v, hs = self.feed_foward(new_state)
                    value_arr.append(v)
                    total_value = total_value + v
                    hidden_states.append(hs)
                # print(value_arr)
                weighted_sample_index = np.random.choice(len(move_arr), p=np.array(value_arr)/ total_value )
                move_to_take = move_arr[weighted_sample_index]
                hs = hidden_states[weighted_sample_index]
                inter_states.append(hs)

                game.take_action(move_to_take[0], move_to_take[1])
                if game.game_done == -1:
                    oppo_move = self.enemy_bot.make_move(game)
                    game.take_action(oppo_move[0], oppo_move[1])
            reward = None
            if game.game_done == self.player_id:
                reward = 1
                win_count += 1
            elif game.game_done == 2:
                reward = -0.5
            else:
                reward = -1

            self.back_prop(reward, inter_states, grad_buffer)

            episode_count = episode_count + 1

            if episode_count % self.batch_count == 0:
                print('Epoch {} Win Rate: {:2f}%'.format(epoch_count, win_count / episode_count * 100))
                for k in self.current_player:
                    curr_grad = grad_buffer[k]
                    rms_prop_cache[k] = self.rms_prop_decay * rms_prop_cache[k] + (1 - self.rms_prop_decay) * curr_grad**2
                    self.current_player[k] += self.learning_rate * curr_grad / np.sqrt(rms_prop_cache[k] + 1e-5)
                    grad_buffer[k] = np.zeros_like(self.current_player[k])
            
                if save_weights:
                    with open('C:/personal_projects/Tix-Tax-Bots/neural_net_weights.pkl', 'wb') as f_out:
                        pickle.dump(self.current_player, f_out, pickle.HIGHEST_PROTOCOL)

                episode_count = 0
                win_count = 0
                epoch_count += 1





        



        

