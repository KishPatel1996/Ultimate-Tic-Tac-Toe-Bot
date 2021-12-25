import torch
import torch.nn as nn
import numpy as np
from random import choices

from bot import Bot
from obs_space import obs_mapper
from primitives import create_mask_from_board



class TorchModelWrapper(nn.Module,Bot):
    def __init__(self, obs_space: str, model_path: str = None) -> None:
        super(TorchModelWrapper,self).__init__()
        super(Bot,self).__init__()

        self.obs_space = obs_mapper[obs_space]()
        h_dim = 64
        self.model= nn.Sequential(
            nn.Linear(self.obs_space.get_dimension(), h_dim),
            nn.Tanh(),
            nn.Linear(h_dim,h_dim),
            nn.Tanh(),
            nn.Linear(h_dim,81).float()
        )
        

        if model_path != None:
            self.load_state_dict(torch.load(model_path))
            self.eval()


    def get_action(self, board_state, valid_square) -> int:
        action_mask = create_mask_from_board(board_state, valid_square)
        transformed_obs = self.obs_space.transform_game_output_to_obs([board_state,valid_square])
        net_output = self.deterministic_action(transformed_obs, action_mask)
        return [net_output //9, net_output % 9 ]


    def forward(self, x):
        return self.model(x)
    
    def get_masked_log_proba(self, obs, action_mask):
        model_out = self.model(torch.from_numpy(obs).float())
        exp_masked = torch.exp(model_out) * torch.from_numpy(action_mask).int()
        return exp_masked/ exp_masked.sum()

    def sample_action(self, obs, action_mask) -> int:
        # Returns location to put a piece
        masked_logs = self.get_masked_log_proba(obs, action_mask).detach().numpy()
        sample = choices(population=range(81),weights=masked_logs,k=1)[0]
        return sample

    def deterministic_action(self, obs, action_mask) -> int:
        masked_logs = self.get_masked_log_proba(obs, action_mask).detach().numpy()
        return np.argmax(masked_logs)