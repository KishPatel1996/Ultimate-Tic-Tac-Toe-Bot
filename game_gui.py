from game_manager import Game_Manager

from tkinter import *




class Human_Player:
    TYPE='HUMAN'
    def make_move(self, game):
        pass



class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.buttons = []
        self.generate_screen()
        self.pack(expand=1)

    def button_function(self, block, space, button):
        print('{} {}'.format(block, space))
        button.config(activeforeground='red', fg='red', bg='red')
        self.update()


    def generate_screen(self):
        block = 0
        for x,y in [[0,0], [0,4], [0,8], [4,0], [4,4], [4,8], [8,0], [8,4], [8,8]]:
            new_button_arr = []
            i = 0
            j = 0
            for k in range(0,9):
                button = Button(self, text=" ", bg='blue',
                 fg='cyan', height=1, width=1, command=lambda block=block, k=k: self.button_function(block,k, button))
                button.grid(row=x+i, column=y+j, sticky= S+N+E+W)
                j = j + 1
                if j >=3:
                    j = 0
                    i = i + 1
                new_button_arr.append(button)
            self.buttons.append(new_button_arr)
            block = block + 1
        #add overarching grids






root = Tk()
app = Application(master=root)
app.mainloop()

# command line for players
