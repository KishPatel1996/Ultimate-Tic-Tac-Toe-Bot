import numpy as np

from primitives import create_flat_mask
class ObservationSpace:
    def transform_game_output_to_obs(self, game_space):
        pass

    def get_dimension(self) -> int:
        pass


class OnlyGameBoardSpace(ObservationSpace):

    def transform_game_output_to_obs(self, game_space):
        
        return create_flat_mask(game_space[0])

    def get_dimension(self) -> int:
        return 81


obs_mapper = {
    "OnlyGameBoardSpace": OnlyGameBoardSpace
}