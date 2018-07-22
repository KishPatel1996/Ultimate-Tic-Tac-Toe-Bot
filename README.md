# Ultimate-Tic-Tac-Toe-Bot

### About
Ultimate Tic Tac Toe is similar to the traditional tic tac toe, but with each location itself being a tic tac toe board as well.  Instructions on the game can be found on the wikipedia page below.

https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe

This is a simple program to build out different bots and test their performance against a human player.  There is a gui (only workes on Windows) to interact with the game and play against a bot!

### How to Add a Bot
Add a bot class to `bots.py` that implements `make_move()`,`set_player_id`, and has a variable `TYPE=BOT`.  Then add the class to the dictionary at the bottom of the file.  

To select a bot to versus, run `python game_gui.py` and the console will ask for the key of the bot class to instantiate.

![Screenshot](screenshot_1.PNG)

### Current Bots Implemented

##### Random Bot
Mostly used for testing of the game system.  Randomly selects a valid move
##### Minimax Tree with Heuristic and Alpha Beta Pruning
Given the high branching factor of the game, especially when any available blank space is a valid move, a simple minimax will not complete in a timely fashion.  Even with the additiona of alpha beta pruning, the search place is too large.  To compensate, a heuristic is added that prioritizes selecting blocks to complete a 3-in-a-row or work towards that goal.

The minimax search depth increases as sections of the overarching grid are taken.  This is to reduce time spent on the first few turns, and have more time spent considering next moves when the game nears its end.

##### Monte Carlo Tree Search Bot
Implemented a preliminary version of a bot that utilizes MCTS to pick move.

###### Improvement Points
* Current simulation randomly picks a move for both the player and the opponent.  Because of this, the bot will often select a move that almost guarantees the opponent will win since the both is not considering for an 'adversarial' opponent.  Improvements can be made function used to determine score, or implement a minimizing opponent.
* State space is pretty large.  Need to find a more optimal tradeoff between exploitation and exploration.

##### Reinforcement Learned Value Neural Net Bot

A fully connected feed forward network of dimensions [81, 27, 9, 1] and sigmoid activation functions.  

The creation of this bot was inspired by Anrej Kaparthy's blog post about policy gradients (found [here](http://karpathy.github.io/2016/05/31/rl/))

This network is not the same as the one implemented in Kaparthy's blog, but follows a similar methodology.  To adapt to this game, the neural network will produce a value for the given state, and the bot will look at all possible moves it can make, then the states that result from those moves, and finally the value of the new states to determine the best possible move.  
The bot will play a number of games against a simpler bot, such as the random one, and will store the moves taken during each game.  At the end of the game, the resulting score (whether the neural network is a winner (+1) or a loser (-1)) is backpropagated using the stored moves of the game.  This will slightly increase the value of the states, resulting in a higher chance that the neural network will pick a move that results in this state than others.  

After training overnight against the random player, the neural network does not perform as initially expected.  While naively playing against it shows that the network has captured some aspects of the game, such as capturing the smaller 3x3 squares, it will often lose to the minimax bot.  

###### Improvement Points
* Network structure can potentially be changed to capture the game board structure.  
* Have not spent that much time tuning hyperparameters, so further tuning can result in faster learning and better performance

