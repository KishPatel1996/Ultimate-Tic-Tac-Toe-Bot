from game_manager import Game_Manager
import numpy as np
from tkinter import *
from random import random
import math
from bots import *
HUMAN = 'HUMAN'

class Human_Player:
    TYPE = HUMAN
    def __init__(self):
        self.cur_action = None
    def make_move(self, game):
        return self.cur_action

    def set_player_id(self, player_id):
        self.player_id = player_id




class Application(Frame):
    def __init__(self, master, first_player, second_player):
        super().__init__(master)
        self.buttons = []
        self.generate_screen()
        self.pack(expand=1)
        self.first_player = first_player
        self.second_player = second_player
        self.gm = Game_Manager(first_player, second_player)
        self.board_spot_taken = np.zeros((9,9), dtype=np.uint8)
        if self.first_player.TYPE == BOT:
            block,space = self.gm.run_game()
            self.buttons[block][space].config(bg='#DF5B56', state=DISABLED )
            self.board_spot_taken[block,space]=1
            self.gray_out_unselectable_buttons()
            self.update()


    def button_function(self, block, space, button):
        print('{} {}'.format(block, space))
        if self.first_player.TYPE == HUMAN:
            self.first_player.cur_action = [block, space]
        else:
            self.second_player.cur_action = [block, space]
        move_output = self.gm.run_game()
        # check for valid move
        if move_output is None:
            return
        button.config(bg='#402DC8', state=DISABLED )
        self.board_spot_taken[block,space]=1
        self.update()
        if self.game_done_check():
            return
        block, space = self.gm.run_game()
        self.buttons[block][space].config(bg='#DF5B56', state=DISABLED )
        self.board_spot_taken[block,space]=1
        self.gray_out_unselectable_buttons()
        self.update()
        self.game_done_check()
        print(self.gm.game.get_possible_moves())

        
    def gray_out_unselectable_buttons(self):
        curr_section = self.gm.current_board_section()
        button_state = NORMAL
        color = 'gainsboro'
        for i in range(self.board_spot_taken.shape[0]):
            if i == curr_section or curr_section == -1:
                color = 'gainsboro'
                button_state = NORMAL
            else:
                color = 'dim grey'
                button_state = DISABLED
            for j in range(self.board_spot_taken.shape[1]):
                if self.board_spot_taken[i,j] == 0:
                    self.buttons[i][j].config(bg=color, state=button_state)

    def game_done_check(self):
        game_done_check = self.gm.game_outcome()
        if game_done_check > -1:
            if game_done_check == 2:
                print('Game was Tied')
            else:
                print('{} won'.format(self.first_player.TYPE if game_done_check == 0 else self.second_player.TYPE))
            for button_array in self.buttons:
                for b in button_array:
                    b.config(state=DISABLED)
            self.update()
            return True

        return False

    def generate_screen(self):
        block = 0
        for x,y in [[0,0], [0,4], [0,8], [4,0], [4,4], [4,8], [8,0], [8,4], [8,8]]:
            new_button_arr = []
            i = 0
            j = 0
            for k in range(0,9):
                button = Button(self, text="", bg='gainsboro',
                  height=2, width=4)
                button.config(command=lambda bl=block, k=k, b=button: self.button_function(bl,k, b))
                button.grid(row=x+i, column=y+j, sticky= S+N+E+W)
                j = j + 1
                if j >=3:
                    j = 0
                    i = i + 1
                new_button_arr.append(button)
            self.buttons.append(new_button_arr)
            block = block + 1
        #add overarching grids
        for x in [3,7]:
            for i in range(11):
                l = Label(self, bg='black', height=1, width=2)
                l.grid(row=i, column=x, sticky=S+N+E+W)
                l =  Label(self, bg='black', height=1, width=1)
                l.grid( row=x, column=i, sticky=S+N+E+W)
        



root = Tk()
hb = Human_Player()
print('Bots to choose from: {}'.format(list(bot_dict.keys())))
bot_key = input('Pick a bot from this list: ').strip().lower()
while bot_key not in bot_dict:
    print('Bot not found.  Choose again from {}'.format(list(bot_dict.keys())))
    bot_key = input().strip().lower()
bot = bot_dict[bot_key]()
app = Application(root, bot, hb)
app.mainloop()

# command line for players
