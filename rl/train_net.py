import argparse
import torch
import numpy as np
from base_game import TixTaxEnv
from nn_model import TorchModelWrapper,create_mask_from_board
from obs_space import OnlyGameBoardSpace
from bot import RandomBot
from tqdm import tqdm 

def collect_experience_single_run(game:TixTaxEnv, model: TorchModelWrapper):
    # Return list of log 
    obs, is_done = game.reset()

    obs_list, action_list, masks_list, rew_list = [],[],[],[]

    while not is_done:
        obs_transformed = model.obs_space.transform_game_output_to_obs(obs)
        mask = create_mask_from_board(obs[0], obs[1])
        action = model.sample_action(obs_transformed, mask)

        #Put action into game
        converted_action = [action // 9, action % 9]

        obs, reward, is_done = game.step(converted_action)
        #Store intermediaries in a list
        obs_list.append(obs_transformed)
        action_list.append(action)
        masks_list.append(mask)
        rew_list.append(reward)
    
    return obs_list, action_list, masks_list, rew_list



def compute_returns(sequence, gamma=0.99):
    seq = np.asanyarray(sequence)
    reward = seq[::-1]
    for i in range(1, len(reward)):
        reward[i] = gamma * reward[i-1] + reward[i]
    return reward[::-1]

def compute_training_loss(model: torch.nn.Module, obs, actions, masks, rewards):
    model_out = model(torch.from_numpy(obs).float())
    model_out = torch.exp(model_out) * torch.from_numpy(masks).int()
    model_out = model_out / model_out.sum(axis=1)[:,None]

    model_out = torch.log(model_out.gather(1,torch.from_numpy(actions).long()[:,None]).reshape(-1))

    return -(model_out * torch.from_numpy(rewards)).mean()


def train_model(game:TixTaxEnv, model: TorchModelWrapper, batch_size: int, epochs=100):

    model.train()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    win_percentages = []

    for _ in tqdm(range(epochs)):
        obs, actions, masks, rewards = [],[],[],[]

        game_count = 0
        win_count = 0
        while len(obs) < batch_size:
            o, a, m, r = collect_experience_single_run(game, model)
            game_count += 1
            if r[-1] > 0:
                #win count increases
                win_count += 1
            
            discounted_rewards = compute_returns(r)
            obs.extend(o)
            actions.extend(a)
            masks.extend(m)
            rewards.extend(discounted_rewards)

        win_percentages.append(win_count/game_count)
        
        #Train model
        obs, actions, masks, rewards = np.asarray(obs), np.asarray(actions), np.asarray(masks), np.asarray(rewards)

        optimizer.zero_grad()
        loss = compute_training_loss(model, obs, actions, masks, rewards)
        loss.backward()
        optimizer.step()
    model.eval()
    return model, win_percentages


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to train a neural net model")
    parser.add_argument("--num_epochs", type=int, default=10000)
    parser.add_argument('--batch_size', type=int, default=10000)

    args = parser.parse_args()

    model = TorchModelWrapper(OnlyGameBoardSpace())

    game = TixTaxEnv(RandomBot())

    trained_model, win_percentage = train_model(game, model, args.batch_size, args.num_epochs)

    print(win_percentage)

