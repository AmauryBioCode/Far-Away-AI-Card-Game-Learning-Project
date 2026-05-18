import random
import numpy as np
import matplotlib.pyplot as plt
import pickle
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import time

#[x,x,x] = [stone, dear, pineapple]
#color: grey (w), blue (b), red (r), green (g) j'ai choisi w comme white pour gris car g est déjà pris par green
# ["points", x] (x points),  ["night", x] (x points par carte nuit),  ["bre", x] (x point par carte rouge et bleu (re = red, b = blue, g = green, y = yellow, w = gray),  
# ["color", x] (x points pour chaque 4 couleurs différentes), ["stone", x] (x points par pierre), ["parchment", x], 
# ["resources", x] (x points pour chaque 3 resources différentes)
cards_data= {
    "0": {"resources": [1,1,1], "parchment": False, "color": 'w', "night": False, "condition": None, "points": None},
    1: {"resources": [1, 1, 0], "parchment": False, "color": "r", "night": False, "condition": None, "points": None},
    2: {"resources": [2, 0, 0], "parchment": False, "color": "b", "night": False, "condition": None, "points": None},
    3: {"resources": [0, 0, 0], "parchment": False, "color": "g", "night": False, "condition": None, "points": ["points", 4]},
    4: {"resources": [1, 0, 1], "parchment": False, "color": "r", "night": False, "condition": None, "points": None},
    5: {"resources": [0, 1, 0], "parchment": False, "color": "g", "night": False, "condition": None, "points": ["points", 2]},
    6: {"resources": [1, 0, 0], "parchment": True, "color": "b", "night": False, "condition": None, "points": None},
    7: {"resources": [0, 1, 1], "parchment": False, "color": "r", "night": False, "condition": None, "points": None},
    8: {"resources": [0, 1, 0], "parchment": True, "color": "g", "night": False, "condition": None, "points": None},
    9: {"resources": [0, 0, 0], "parchment": False, "color": "b", "night": False, "condition": None, "points": ["points", 5]},
    10: {"resources": [0, 0, 0], "parchment": False, "color": "r", "night": False, "condition": None, "points": ["night", 3]},
    11: {"resources": [0, 0, 0], "parchment": False, "color": "g", "night": False, "condition": None, "points": ["parchment", 2]},
    12: {"resources": [0, 0, 1], "parchment": True, "color": "y", "night": False, "condition": None, "points": None},
    13: {"resources": [0, 0, 0], "parchment": False, "color": "b", "night": False, "condition": None, "points": ["stone", 2]},
    14: {"resources": [0, 0, 1], "parchment": False, "color": "r", "night": False, "condition": None, "points": ["night", 2]},
    15: {"resources": [0, 0, 0], "parchment": True, "color": "g", "night": False, "condition": None, "points": ["dear", 2]},
    16: {"resources": [0, 1, 0], "parchment": False, "color": "r", "night": False, "condition": None, "points": ["dear", 2]},
    17: {"resources": [1, 0, 0], "parchment": False, "color": "b", "night": False, "condition": [0, 2, 0], "points": ["stone", 3]},
    18: {"resources": [0, 1, 0], "parchment": False, "color": "g", "night": False, "condition": None, "points": ["color", 10]},
    19: {"resources": [0, 0, 1], "parchment": False, "color": "r", "night": False, "condition": None, "points": ["pineapple", 2]},
    20: {"resources": [0, 0, 0], "parchment": True, "color": "g", "night": True, "condition": [1, 0, 0], "points": ["night", 2]},
    21: {"resources": [0, 0, 0], "parchment": False, "color": "b", "night": True, "condition": [2, 0, 0], "points": ["points", 8]},
    22: {"resources": [0, 0, 0], "parchment": True, "color": "g", "night": True, "condition": None, "points": ["parchment", 1]},
    23: {"resources": [1, 1, 0], "parchment": False, "color": "r", "night": True, "condition": None, "points": ["color", 10]},
    24: {"resources": [0, 1, 0], "parchment": False, "color": "g", "night": True, "condition": [0, 1, 0], "points": ["night", 2]},
    25: {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": True, "condition": None, "points": ["gy", 1]},
    26: {"resources": [0, 1, 0], "parchment": False, "color": "r", "night": True, "condition": None, "points": ["pineapple", 3]},
    27: {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": True, "condition": None, "points": ["yb", 1]},
    28: {"resources": [1, 0, 0], "parchment": False, "color": "r", "night": True, "condition": None, "points": ["dear", 3]},
    29: {"resources": [0, 0, 1], "parchment": False, "color": "y", "night": True, "condition": None, "points": ["pineapple", 3]},
    30: {"resources": [1, 0, 0], "parchment": False, "color": "r", "night": True, "condition": None, "points": ["stone", 2]},
    31: {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": True, "condition": None, "points": ["yre", 1]},
    32: {"resources": [1, 1, 0], "parchment": False, "color": "r", "night": True, "condition": [3, 0, 0], "points": ["points", 7]},
    33: {"resources": [0, 0, 0], "parchment": True, "color": "y", "night": True, "condition": None, "points": ["pineapple", 3]},
    34: {"resources": [0, 1, 0], "parchment": False, "color": "g", "night": True, "condition": [2, 0, 0], "points": ["dear", 3]},
    35: {"resources": [0, 1, 0], "parchment": False, "color": "y", "night": True, "condition": None, "points": ["color", 10]},
    36: {"resources": [0, 0, 0], "parchment": False, "color": "r", "night": True, "condition": [0, 2, 0], "points": ["pineapple", 4]},
    37: {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": True, "condition": [0, 0, 1], "points": ["night", 3]},
    38: {"resources": [1, 0, 0], "parchment": False, "color": "g", "night": True, "condition": [0, 1, 1], "points": ["parchment", 3]},
    39: {"resources": [1, 0, 1], "parchment": False, "color": "r", "night": True, "condition": [0, 2, 0], "points": ["points", 9]},
    40: {"resources": [0, 0, 0], "parchment": False, "color": "b", "night": True, "condition": [1, 1, 1], "points": ["night", 3]},
    41: {"resources": [0, 0, 1], "parchment": False, "color": "g", "night": False, "condition": [2, 1, 0], "points": ["night", 4]},
    42: {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": False, "condition": [1, 1, 0], "points": ["gy", 2]},
    43: {"resources": [1, 0, 0], "parchment": False, "color": "b", "night": False, "condition": None, "points": ["color", 10]},
    44: {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": False, "condition": [1, 0, 1], "points": ["yb", 2]},
    45: {"resources": [1, 0, 0], "parchment": False, "color": "g", "night": False, "condition": [0, 3, 0], "points": ["points", 13]},
    46: {"resources": [0, 0, 0], "parchment": True, "color": "b", "night": False, "condition": [2, 1, 0], "points": ["points", 10]},
    47: {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": False, "condition": [0, 1, 1], "points": ["yre", 2]},
    48: {"resources": [0, 1, 0], "parchment": False, "color": "r", "night": False, "condition": None, "points": ["stone", 3]},
    49: {"resources": [0, 0, 0], "parchment": True, "color": "b", "night": False, "condition": [2, 0, 1], "points": ["points", 12]},
    50: {"resources": [1, 0, 0], "parchment": False, "color": "y", "night": False, "condition": [0, 0, 2], "points": ["g", 2]},
    51: {"resources": [1, 0, 0], "parchment": False, "color": "b", "night": False, "condition": [4, 0, 0], "points": ["points", 14]},
    52: {"resources": [0, 0, 0], "parchment": False, "color": "r", "night": False, "condition": [3, 0, 0], "points": ["dear", 4]},
    53: {"resources": [0, 1, 0], "parchment": False, "color": "y", "night": False, "condition": [0, 2, 0], "points": ["re", 4]},
    54: {"resources": [0, 1, 0], "parchment": False, "color": "g", "night": False, "condition": [0, 0, 2], "points": ["parchment", 4]},
    55: {"resources": [1, 0, 0], "parchment": True, "color": "b", "night": False, "condition": [0, 1, 2], "points": ["stone", 3]},
    56: {"resources": [0, 0, 1], "parchment": False, "color": "y", "night": False, "condition": [1, 2, 0], "points": ["b", 4]},
    57: {"resources": [0, 0, 0], "parchment": False, "color": "r", "night": False, "condition": [0, 0, 3], "points": ["stone", 4]},
    58: {"resources": [0, 0, 0], "parchment": True, "color": "g", "night": False, "condition": [0, 3, 0], "points": ["parchment", 3]},
    59: {"resources": [0, 0, 0], "parchment": True, "color": "y", "night": False, "condition": [1, 3, 0], "points": ["yre", 3]},
    60: {"resources": [0, 0, 0], "parchment": True, "color": "b", "night": False, "condition": [2, 2, 0], "points": ["points", 16]},
    61: {"resources": [0, 0, 1], "parchment": False, "color": "g", "night": False, "condition": [0, 4, 0], "points": ["points", 17]},
    62: {"resources": [0, 0, 0], "parchment": True, "color": "y", "night": False, "condition": [0, 0, 3], "points": ["yb", 3]},
    63: {"resources": [0, 0, 0], "parchment": True, "color": "g", "night": False, "condition": [0, 2, 1], "points": ["points", 15]},
    64: {"resources": [0, 0, 0], "parchment": True, "color": "b", "night": False, "condition": [2, 0, 2], "points": ["points", 18]},
    65: {"resources": [0, 0, 0], "parchment": True, "color": "y", "night": False, "condition": [0, 0, 3], "points": ["gy", 3]},
    66: {"resources": [0, 0, 0], "parchment": False, "color": "b", "night": False, "condition": [4, 0, 0], "points": ["points", 20]},
    67: {"resources": [0, 0, 0], "parchment": True, "color": "g", "night": False, "condition": [0, 2, 2], "points": ["points", 20]},
    68: {"resources": [0, 0, 0], "parchment": False, "color": "b", "night": False, "condition": [5, 0, 0], "points": ["points", 24]},
    69: {"resources": [0, 0, 0], "parchment": True, "color": "r", "night": False, "condition": None, "points": ["resources", 7]},
    70: {"resources": [0, 0, 0], "parchment": True, "color": "w", "night": False, "condition": None, "points": ["points", 6]},
    71: {"resources": [1, 0, 0], "parchment": False, "color": "g", "night": True, "condition": None, "points": ["resources", 7]},
    72: {"resources": [0, 0, 0], "parchment": True, "color": "w", "night": True, "condition": [0, 5, 0], "points": ["points",26]},
    73: {"resources": [0, 1, 0], "parchment": False, "color": "y", "night": True, "condition": [0, 0, 4], "points": ["w", 5]},
    74: {"resources": [0, 0, 1], "parchment": False, "color": "w", "night": True, "condition": None, "points": ["resources", 7]},
    75: {"resources": [0, 0, 0], "parchment": True, "color": "b", "night": True, "condition": [6, 0, 0], "points": ["points", 28]},
    76: {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": True, "condition": [2, 2, 2], "points": ["w", 4]},
}

sanctuary_data = {
 "100": {"resources": [0, 1, 0], "parchment": False, "color": "r", "night": False, "points": None},
    "102": {"resources": [0, 1, 0], "parchment": False, "color": "g", "night": False, "points": None},
    "103": {"resources": [0, 1, 0], "parchment": False, "color": "b", "night": False, "points": None},
    "104": {"resources": [0, 1, 0], "parchment": False, "color": "w", "night": False, "points": ["w", 1]},
    "105": {"resources": [0, 1, 0], "parchment": False, "color": "w", "night": False, "points": ["dear", 1]},
    "106": {"resources": [0, 1, 0], "parchment": False, "color": "w", "night": True, "points": None},
    "107": {"resources": [0, 1, 0], "parchment": False, "color": "w", "night": False, "points": ["parchment", 1]},
    "108": {"resources": [0, 1, 0], "parchment": True, "color": "w", "night": False, "points": None},
    "109": {"resources": [1, 0, 0], "parchment": False, "color": "r", "night": False, "points": None},
    "110": {"resources": [1, 0, 0], "parchment": False, "color": "b", "night": False, "points": None},
    "111": {"resources": [1, 0, 0], "parchment": False, "color": "g", "night": False, "points": None},
    "112": {"resources": [1, 0, 0], "parchment": False, "color": "y", "night": False, "points": None},
    "113": {"resources": [1, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["night", 1]},
    "114": {"resources": [1, 0, 0], "parchment": False, "color": "w", "night": True, "points": None},
    "115": {"resources": [1, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["parchment", 1]},
    "116": {"resources": [1, 0, 0], "parchment": True, "color": "w", "night": False, "points": None},
    "117": {"resources": [1, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["stone", 1]},
    "118": {"resources": [2, 0, 0], "parchment": False, "color": "w", "night": False, "points": None},
    "119": {"resources": [0, 0, 1], "parchment": False, "color": "r", "night": False, "points": None},
    "120": {"resources": [0, 0, 1], "parchment": False, "color": "b", "night": False, "points": None},
    "121": {"resources": [0, 0, 1], "parchment": False, "color": "w", "night": False, "points": ["w", 1]},
    "122": {"resources": [0, 0, 1], "parchment": False, "color": "w", "night": False, "points": ["pineapple", 1]},
    "123": {"resources": [0, 0, 1], "parchment": True, "color": "w", "night": False, "points": None},
    "124": {"resources": [0, 0, 1], "parchment": False, "color": "w", "night": True, "points": None},
    "125": {"resources": [0, 0, 0], "parchment": True, "color": "b", "night": False, "points": None},
    "126": {"resources": [0, 0, 0], "parchment": True, "color": "y", "night": False, "points": None},
    "127": {"resources": [0, 0, 0], "parchment": True, "color": "g", "night": False, "points": None},
    "128": {"resources": [0, 0, 0], "parchment": True, "color": "w", "night": False, "points": ["color", 4]},
    "129": {"resources": [0, 0, 0], "parchment": True, "color": "w", "night": False, "points": ["parchment", 1]},
    "130": {"resources": [0, 0, 0], "parchment": True, "color": "w", "night": False, "points": ["resources", 3]},
    "131": {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": True, "points": ["w", 1]},
    "132": {"resources": [0, 0, 0], "parchment": False, "color": "r", "night": True, "points": None},
    "133": {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": False, "points": ["y", 1]},
    "134": {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": False, "points": ["parchment", 1]},
    "135": {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": False, "points": ["color", 4]},
    "136": {"resources": [0, 0, 0], "parchment": False, "color": "g", "night": False, "points": ["night", 1]},
    "137": {"resources": [0, 0, 0], "parchment": False, "color": "g", "night": False, "points": ["resources", 3]},
    "138": {"resources": [0, 0, 0], "parchment": False, "color": "g", "night": False, "points": ["g", 1]},
    "139": {"resources": [0, 0, 0], "parchment": False, "color": "b", "night": False, "points": ["w", 2]},
    "140": {"resources": [0, 0, 0], "parchment": False, "color": "b", "night": False, "points": ["b", 1]},
    "141": {"resources": [0, 0, 0], "parchment": False, "color": "r", "night": False, "points": ["re", 1]},
    "142": {"resources": [0, 0, 0], "parchment": False, "color": "r", "night": False, "points": ["resources", 3]},
    "143": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["yre", 1]},
    "144": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["stone", 2]},
    "145": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["bre", 1]},
    "146": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["gy", 1]},
    "147": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["bg", 1]},
    "148": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["gre", 1]},
    "149": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["by", 1]},
    "150": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["parchment", 2]},
    "151": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["pineapple", 2]},
    "152": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["dear", 2]},
    "153": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["points", 5]},
}

class DQN(nn.Module):
    def __init__(self, input_size, output_size):
        super(DQN, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, output_size)
        )
    
    def forward(self, x):
        return self.net(x)

class AI:
    def __init__(self, filename="ai_memory.pt"):
        self.filename = filename
        self.history_p1 = []
        self.history_p2 = []
        self.epsilon_min = 0.05
        self.epsilon_decay = 0.999995
        self.epsilon = 0.5
        self.gamma = 0.95
        self.lr = 0.001
        self.replay_buffer = deque(maxlen=50000)
        self.batch_size = 64

        self.input_size = 78
        # max 3 actions (play or pick)
        self.output_size = 3

        self.model = DQN(self.input_size, self.output_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
        self.loss_fn = nn.MSELoss()

        self.load_memory()

    def state_to_tensor(self, state):
        #turns_left, res, night, parchment, h_stone, h_dear, h_pine, h_cond, h_pts, h_night = state
        #flat = [turns_left, res[0], res[1], res[2], night, parchment, h_stone, h_dear, h_pine, h_cond, h_pts, h_night]
        return torch.tensor(state, dtype=torch.float32)
    

    def choose_action(self, player, game, mode, player_id="p1", nb_actions=None):
        state = player.get_state(game)
        history = self.history_p1 if player_id == "p1" else self.history_p2

        if mode == "play":
            possible_actions = list(range(len(player.cards_in_hand)))
        elif mode == "pick":
            if nb_actions is None:
                nb_actions = len(game.cards.cards_on_board)
            possible_actions = list(range(nb_actions))

        if random.random() < self.epsilon:
            action = random.choice(possible_actions)
            history.append((state, mode, action))
            return action

        with torch.no_grad():
            q_values = self.model(self.state_to_tensor(state))

        valid_actions = [a for a in possible_actions if a < self.output_size]
        if not valid_actions:
            valid_actions = possible_actions

        best_action = max(valid_actions, key=lambda a: q_values[a].item())
        history.append((state, mode, best_action))
        return best_action

    def store_transition(self, state, action, reward, next_state, done):
        self.replay_buffer.append((state, action, reward, next_state, done))

    def train_step(self):
        if len(self.replay_buffer) < self.batch_size:
            return

        batch = random.sample(self.replay_buffer, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states_t = torch.stack([self.state_to_tensor(s) for s in states])
        next_states_t = torch.stack([self.state_to_tensor(s) for s in next_states])
        actions_t = torch.tensor(actions, dtype=torch.long)
        rewards_t = torch.tensor(rewards, dtype=torch.float32)
        dones_t = torch.tensor(dones, dtype=torch.float32)

        current_q = self.model(states_t).gather(1, actions_t.unsqueeze(1)).squeeze(1)

        with torch.no_grad():
            next_q = self.model(next_states_t).max(1)[0]
            target_q = rewards_t + self.gamma * next_q * (1 - dones_t)

        loss = self.loss_fn(current_q, target_q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def learn_small_reward(self, reward, next_state, player_id="p1"):
        history = self.history_p1 if player_id == "p1" else self.history_p2
        if len(history) == 0:
            return

        state, mode, action = history[-1]
        action = min(action, self.output_size - 1)

        self.store_transition(state, action, reward, next_state, done=0)
        self.train_step()

    def learn_final_reward(self, reward, player_id="p1"):
        history = self.history_p1 if player_id == "p1" else self.history_p2
        if len(history) == 0:
            return
        state, mode, action = history[-1]
        action = min(action, self.output_size - 1)
        self.store_transition(state, action, reward, state, done=1)
        self.train_step()
        if player_id == "p1":
            self.history_p1 = []
        else:
            self.history_p2 = []

    def update_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save_memory(self):
        torch.save({
            "model": self.model.state_dict(),
            "optimizer": self.optimizer.state_dict(),
            "epsilon": self.epsilon
        }, self.filename)

    def load_memory(self):
        try:
            data = torch.load(self.filename)
            self.model.load_state_dict(data["model"])
            self.optimizer.load_state_dict(data["optimizer"])
            self.epsilon = data["epsilon"]
        except FileNotFoundError:
            pass

class Cards:
    """Manage the deck of available cards and the cards currently on the board."""
    def __init__(self):
        self.card_info = cards_data
        self.card_pack = list(cards_data.keys())
        self.sanctuary_info = sanctuary_data
        self.sanctuary_pack = list(sanctuary_data.keys())
        self.cards_on_board = []

    def card_taken(self, number):
        """Remove a card from the card pack after it has been drawn or used.

        Args:
            number: The card number to remove from the card pack."""
        self.card_pack.remove(number)
    
    def sanctuary_taken(self, number):
        """Remove a card from the card pack after it has been drawn or used.

        Args:
            number: The card number to remove from the card pack."""
        self.sanctuary_pack.remove(number)

    def add_parchment(self, number, type):
        if type == "card":
            if self.card_info[number]["parchment"] == True:
                return True
        if type == "sanctuary":
            if self.sanctuary_info[number]["parchment"] == True:
                return True
        return False
    
    def draw_card(self):
        """Draw a random card from the card pack and remove it from the pack.

        Returns:
            The number of the card that was drawn."""
        number = random.choice(self.card_pack)
        self.card_taken(number)
        return number
    
    def draw_sanctuary(self, nb_parchment):
        """Draw a random card from the sanctuary pack and remove it from the pack.

        Returns:
            The number of the card that was drawn."""
        sanctuary_drawn = []
        for i in range(nb_parchment + 1):
            sanctuary_drawn.append(random.choice(self.sanctuary_pack))
        number = sanctuary_drawn[random.randint(0, len(sanctuary_drawn) - 1)]
        self.sanctuary_taken(number)
        return number

    def refill_board(self):
        """Refill the board until it contains 3 cards or the card pack is empty."""
        while len(self.cards_on_board) < 3 and len(self.card_pack) > 0:
            self.cards_on_board.append(self.draw_card())

    def count_resources_sanctuary(self, sanctuary_in_hand):
        total_resources = {"resources": [0, 0, 0], "color": [], "night": 0}
        for s in sanctuary_in_hand:
            sanctuary_card = self.sanctuary_info[str(s)]
            total_resources["resources"][0] += sanctuary_card["resources"][0]
            total_resources["resources"][1] += sanctuary_card["resources"][1]
            total_resources["resources"][2] += sanctuary_card["resources"][2]

            total_resources["color"].append(sanctuary_card["color"])

            if sanctuary_card["night"]:
                total_resources["night"] += 1

        return total_resources

    def count_resources_one_card(self, card):
        return {
            "resources": card["resources"].copy(),
            "color": [card["color"]],
            "night": 1 if card["night"] else 0
        }

    def count_points(self, c, total_resources, nb_parchment):
        
        if c in self.card_info:
            card = self.card_info[c]
        else:
            card = self.sanctuary_info[c]

        condition = card.get("condition", None)
        points = card["points"]

        # Check condition
        if condition is not None:
            for i in range(3):
                if total_resources["resources"][i] < condition[i]:
                    return 0

        # No points
        if points is None:
            return 0

        point_type = points[0]
        value = points[1]

        # Fixed points
        if point_type == "points":
            return value

        # Points for blue, green, yellow, red cards
        if point_type == "color":
            nb_blue = total_resources["color"].count("b")
            nb_green = total_resources["color"].count("g")
            nb_yellow = total_resources["color"].count("y")
            nb_red = total_resources["color"].count("re")
            nb_sets = min(nb_blue, nb_green, nb_yellow, nb_red)
            return value * nb_sets

        # Points for night
        if point_type == "night":
            return value * total_resources["night"]

        if point_type in ["b", "g", "y", "re", "w", "bg", "by", "bre", "gy", "gre", "yre"]:
            selected_colors = []

            if "re" in point_type:
                selected_colors.append("re")
                point_type_without_red = point_type.replace("re", "")
            else:
                point_type_without_red = point_type

            for color in ["b", "g", "y"]:
                if color in point_type_without_red:
                    selected_colors.append(color)

            score = 0
            for color in total_resources["color"]:
                if color in selected_colors:
                    score += value

            return score

        # Stone = first resource
        if point_type == "stone":
            return value * total_resources["resources"][0]

        # Deer = second resource
        if point_type == "dear":
            return value * total_resources["resources"][1]

        # Pineapple = third resource
        if point_type == "pineapple":
            return value * total_resources["resources"][2]

        # Parchment
        if point_type == "parchment":
            return value * nb_parchment

        # Sets of 3 different resources
        if point_type == "resources":
            return value * min(total_resources["resources"])

        return 0



class Player:
    """Represent a player with cards in hand and cards already played."""
    def __init__(self, cards):
        """Initialize a player with 3 cards drawn from the given card deck.

        Args:
            cards: A Cards object used to draw the player's starting hand."""
        self.number_last_card = 100
        self.sanctuary_in_hand = []
        self.cards_in_hand = []
        self.cards_played = []
        self.nb_parchment = 0
        self.total_resources = {"resources": [0, 0, 0], "color": [], "night": 0}
        self.points = 0

        while len(self.cards_in_hand) < 3:
            self.cards_in_hand.append(cards.draw_card())

    def calculate_current_points(self, cards):
        # same as calculate_points but without modifying self.points
        total_resources = cards.count_resources_sanctuary(self.sanctuary_in_hand)
        points = 0
        for c in reversed(self.cards_played):
            c_data = cards.count_resources_one_card(cards.card_info[c])
            total_resources["resources"][0] += c_data["resources"][0]
            total_resources["resources"][1] += c_data["resources"][1]
            total_resources["resources"][2] += c_data["resources"][2]
            total_resources["color"].extend(c_data["color"])
            if c_data["night"]:
                total_resources["night"] += 1
            points += cards.count_points(c, total_resources, self.nb_parchment)
        for s in self.sanctuary_in_hand:
            points += cards.count_points(s, total_resources, self.nb_parchment)
        return points
    
    def play_card(self, index, cards, game):
        """Play a card from the player's hand.

        The selected card is removed from the player's hand and added to the
        list of cards the player has already played.

        Args:
            index: The index of the card to play in the player's hand.

        Returns:
            The number of the card that was played."""
        number = self.cards_in_hand.pop(index)
        self.cards_played.append(number)

        if cards.add_parchment(number, "card") == True:
            self.nb_parchment = self.nb_parchment + 1

        if self.number_last_card < int(number):
            sanctuary = cards.draw_sanctuary(self.nb_parchment)

            if sanctuary is not None:
                self.sanctuary_in_hand.append(sanctuary)
                if cards.add_parchment(sanctuary, "sanctuary") == True:
                    self.nb_parchment = self.nb_parchment + 1
                #reward = self.count_completed_conditions(game.cards, sanctuary, action = "played")
                #ai.learn_small_reward(reward)
        
        self.number_last_card = int(number)

        return number
    
    def get_state(self, game):
        resources = game.cards.count_resources_sanctuary(self.sanctuary_in_hand)

        for c in self.cards_played:
            card_data = game.cards.card_info[c]
            resources["resources"][0] += card_data["resources"][0]
            resources["resources"][1] += card_data["resources"][1]
            resources["resources"][2] += card_data["resources"][2]
            resources["color"].append(card_data["color"])
            if card_data["night"]:
                resources["night"] += 1

        turns_left = game.get_nb_turns_left()
        res = [min(r, 6) for r in resources["resources"]]
        night = min(resources["night"], 5)
        parchment = min(self.nb_parchment, 4)

        hand_features = []
        for c in self.cards_in_hand:
            hand_features.extend(self.encode_card(c, game.cards))

        board_features = []
        for c in game.cards.cards_on_board:
            board_features.extend(self.encode_card(c, game.cards))

        # Safety padding in case hand/board has fewer than 3 cards
        CARD_FEATURE_SIZE = 12

        while len(hand_features) < 3 * CARD_FEATURE_SIZE:
            hand_features.extend([0] * CARD_FEATURE_SIZE)

        while len(board_features) < 3 * CARD_FEATURE_SIZE:
            board_features.extend([0] * CARD_FEATURE_SIZE)

        hand_features = hand_features[:3 * CARD_FEATURE_SIZE]
        board_features = board_features[:3 * CARD_FEATURE_SIZE]

        return tuple(
            [turns_left]
            + res
            + [night, parchment]
            + hand_features
            + board_features
        )
    def count_completed_conditions(self, cards, new_card=None, action="played"):
        # Temporarily add the card if we're evaluating a pick
        if action == "picked" and new_card is not None:
            self.cards_played.append(new_card)

        total_resources = cards.count_resources_sanctuary(self.sanctuary_in_hand)
        for c in self.cards_played:
            if c in cards.card_info:
                card_data = cards.card_info[c]
            else:
                card_data = cards.sanctuary_info[c]
            total_resources["resources"][0] += card_data["resources"][0]
            total_resources["resources"][1] += card_data["resources"][1]
            total_resources["resources"][2] += card_data["resources"][2]

        completed = 0
        for c in self.cards_played:
            if c in cards.card_info:
                card_data = cards.card_info[c]
            else:
                card_data = cards.sanctuary_info[c]
            condition = card_data.get("condition", None)
            if condition is not None:
                if all(total_resources["resources"][i] >= condition[i] for i in range(3)):
                    completed += 1

        # Undo the temporary addition
        if action == "picked" and new_card is not None:
            self.cards_played.remove(new_card)

        return completed
    
    def encode_card(self, card_id, cards):
        card = cards.card_info[card_id]
        points = card["points"]
        condition = card["condition"]

        return [
            card["resources"][0],
            card["resources"][1],
            card["resources"][2],
            int(card["parchment"]),
            int(card["night"]),
            int(card["color"] == "r"),
            int(card["color"] == "b"),
            int(card["color"] == "g"),
            int(card["color"] == "y"),
            int(card["color"] == "w"),
            0 if points is None else points[1],
            int(condition is not None),
        ]

    def calculate_points (self, cards):
        #print("s: ", self.sanctuary_in_hand)
        #print("s: ", self.cards_played)

        self.total_resources = cards.count_resources_sanctuary(self.sanctuary_in_hand)
        #print("ressources sanctuary: ", self.total_resources)
        for c in reversed(self.cards_played):
            c_data = cards.count_resources_one_card(cards.card_info[c])
            self.total_resources["resources"][0] += c_data["resources"][0]
            self.total_resources["resources"][1] += c_data["resources"][1]
            self.total_resources["resources"][2] += c_data["resources"][2]
            self.total_resources["color"].extend(c_data["color"])
            if c_data["night"]:
                self.total_resources["night"] += 1

            self.points = self.points + cards.count_points(c, self.total_resources, self.nb_parchment)

        for s in self.sanctuary_in_hand:
            self.points = self.points + cards.count_points(s, self.total_resources, self.nb_parchment)
        
        #print("total ressources : ", self.total_resources)
        return self.points

class Game:
    """Manage the overall game state, including players, turns, and cards."""
    def reset(self):
        """Reset the game to its initial state.

        Creates a new card deck, initializes two players, sets player 1 as the
        current player, and resets the number of turns left."""
        self.cards = Cards()
        self.player1 = Player(self.cards)
        self.player2 = Player(self.cards)
        self.current_player = self.player1
        self.turns_left = 8
    
    def get_nb_turns_left(self):
        """Return the number of turns left in the game.

        Returns:
            The number of turns remaining."""
        return self.turns_left
    
    def set_turns(self):
        self.turns_left = self.turns_left - 1
        #print(self.turns_left)

    def switch_player(self):
        """Switch the current player to the other player."""
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def play_phase(self, p1_card_index, p2_card_index):
        p1_card = self.player1.play_card(p1_card_index, self.cards, self)
        p2_card = self.player2.play_card(p2_card_index, self.cards, self)

        if int(p1_card) < int(p2_card):
            self.first_picker = self.player1
            self.second_picker = self.player2
        else:
            self.first_picker = self.player2
            self.second_picker = self.player1

        #print("P1 played:", p1_card)
        #print("P2 played:", p2_card)
    
    def draw_phase(self, first_choice_index, second_choice_index):
        first_card = self.cards.cards_on_board.pop(first_choice_index)
        self.first_picker.cards_in_hand.append(first_card)

        second_card = self.cards.cards_on_board.pop(second_choice_index)
        self.second_picker.cards_in_hand.append(second_card)

        self.cards.refill_board()

        return first_card, second_card

if __name__ == "__main__":
    wins = 0
    draws = 0
    losses = 0
    ai = AI()
    ai.epsilon = 0.5
    nb_game = 0
    list_points_1 = []
    total_points_1 = 0
    list_points_2 = []
    total_points_2 = 0
    start = time.time()
    while nb_game < 200:
        nb_game = nb_game + 1
        game = Game()
        state = game.reset()

        while game.get_nb_turns_left() > 0:

            game.cards.refill_board()

            #play a card
            p1_index = ai.choose_action(game.player1, game, "play", player_id="p1")
            p2_index = ai.choose_action(game.player2, game, "play", player_id="p2")
            points_before = game.player1.calculate_current_points(game.cards)
            game.play_phase(p1_index, p2_index)
            after_state = game.player1.get_state(game)
            points_after = game.player1.calculate_current_points(game.cards)
            ai.learn_small_reward((points_after - points_before) / 50.0, after_state, player_id="p1")

            #pick a card
            points_before = game.player1.calculate_current_points(game.cards)
            if game.first_picker == game.player1:
                first_choice = ai.choose_action(game.player1, game, "pick", player_id="p1", nb_actions=len(game.cards.cards_on_board))
                ia_card_picked = game.cards.cards_on_board[first_choice] 
                second_choice = ai.choose_action(game.player2, game, "pick", player_id="p2", nb_actions=len(game.cards.cards_on_board)-1)
            else:
                first_choice = ai.choose_action(game.player2, game, "pick", player_id="p2", nb_actions=len(game.cards.cards_on_board))
                second_choice = ai.choose_action(game.player1, game, "pick", player_id="p1", nb_actions=len(game.cards.cards_on_board)-1)
                ia_card_picked = game.cards.cards_on_board[second_choice]

            game.draw_phase(first_choice, second_choice)
            after_state = game.player1.get_state(game)
            points_after = game.player1.calculate_current_points(game.cards)
            ai.learn_small_reward((points_after - points_before) / 50.0, after_state, player_id="p1")

            #print("P1 hand:", game.player1.cards_in_hand)
            #print("P2 hand:", game.player2.cards_in_hand)
            
            #print("First picker:", "P1" if game.first_picker == game.player1 else "P2")

            game.set_turns()
            if game.get_nb_turns_left() < 1:
                points_player1 = game.player1.calculate_points(game.cards)
                points_player2 = game.player2.calculate_points(game.cards)
                list_points_1.append(points_player1)
                list_points_2.append(points_player2)
                total_points_1 += points_player1
                total_points_2 += points_player2

                if points_player1 > points_player2:
                    wins += 1
                elif points_player1 == points_player2:
                    draws += 1
                else:
                    losses += 1

                reward_p1 = points_player1 / 50.0
                reward_p2 = points_player2 / 50.0
                ai.learn_final_reward(points_player1 / 50.0, player_id="p1")
                ai.learn_final_reward(points_player2 / 50.0, player_id="p2")
                ai.update_epsilon()

        if nb_game % 10 == 0:
            total = wins + draws + losses
            if total > 0:
                mean_p1 = total_points_1 / nb_game
                mean_p2 = total_points_2 / nb_game
                print(f"{nb_game} games | epsilon: {ai.epsilon:.4f} | Win: {wins/total*100:.1f}% | mean P1: {mean_p1:.1f} | mean P2: {mean_p2:.1f}")
                wins = draws = losses = 0

             
    
    ai.save_memory()
    elapsed = time.time() - start
    print(f"1000 games: {elapsed:.1f}s")
    print(f"Estimated for 100k games: {elapsed * 100 / 60:.1f} minutes")

    print("epsilon:", ai.epsilon)

    print("mean PLAYER 1: ", total_points_1/(nb_game))
    print("mean PLAYER 2: ", total_points_2/(nb_game))
    print("median PLAYER 1: ", np.median(list_points_1))
    print("median PLAYER 2: ", np.median(list_points_2))
    print("min: ", np.min(list_points_1))
    print("min: ", np.min(list_points_2))
    bins = list(range(0, 101, 5))  # 0, 10, 20, ..., 100

    counts_1 = []
    counts_2 = []

    for start in bins[:-1]:
        end = start + 4

        count_1 = sum(start <= value <= end for value in list_points_1)
        count_2 = sum(start <= value <= end for value in list_points_2)

        counts_1.append(count_1)
        counts_2.append(count_2)

    count_100_plus_1 = sum(value >= 100 for value in list_points_1)
    count_100_plus_2 = sum(value >= 100 for value in list_points_2)

    counts_1.append(count_100_plus_1)
    counts_2.append(count_100_plus_2)

    labels = [f"{start}-{start + 4}" for start in bins[:-1]]
    labels.append("100+")

    print("counts player 1:", counts_1)
    print("counts player 2:", counts_2)

    percentages_1 = [count / len(list_points_1) * 100 for count in counts_1]
    percentages_2 = [count / len(list_points_2) * 100 for count in counts_2]

    print("percentages player 1:", percentages_1)
    print("percentages player 2:", percentages_2)

    plt.bar(labels, counts_1)
    plt.xlabel("Value range")
    plt.ylabel("How many values")
    plt.title("Player 1")
    plt.xticks(rotation=45)
    plt.show()

    plt.bar(labels, counts_2)
    plt.xlabel("Value range")
    plt.ylabel("How many values")
    plt.title("Player 2")
    plt.xticks(rotation=45)
    plt.show()