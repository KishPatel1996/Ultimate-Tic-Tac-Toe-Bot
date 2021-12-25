import configparser
from argparse import ArgumentParser
from base_game import TixTaxEnv
from bot import RandomBot,UserBot
from obs_space import OnlyGameBoardSpace
from nn_model import TorchModelWrapper
from primitives import print_board

obs_mapper = {
    'OnlyGameBoardSpace': OnlyGameBoardSpace
}

agent_mapper = {
    'RandomBot': RandomBot,
    'UserBot': UserBot,
    'TorchModelWrapper':TorchModelWrapper
}

if __name__ == "__main__":


    parser = ArgumentParser(description="Script to visualize a game")
    parser.add_argument("--config_file_path", type=str, required=True)
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config_file_path)

    p1_agent = agent_mapper[config['BASE']['Player']]
    p2_agent = agent_mapper[config['BASE']['Opponent']]

    if "Player configs" in config:
        player_1 = p1_agent(**dict(config['Player configs']))
    else:
        player_1 = p1_agent()


    if "Opponent configs" in config:
        player_2 = p2_agent(**dict(config['Opponent configs']))
    else:
        player_2 = p2_agent()
    
    # player_1 = RandomBot()
    # player_2 = RandomBot()

    game = TixTaxEnv(player_2)

    game_is_done=False
    while not game_is_done:
        player_action = player_1.get_action(game.board_state, game.current_square)

        game_out = game.step(player_action)
        print_board(game_out[0][0])

        game_is_done = game_out[-1]