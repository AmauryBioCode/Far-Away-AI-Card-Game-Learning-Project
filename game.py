import random
import numpy as np
import matplotlib.pyplot as plt
import pickle

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

class AI:
    """Rule-based AI for your new strategy.

    Strategy:
    1. Rounds 1 and 2:
       - play and pick the card with the biggest condition.
       - "Biggest condition" means the largest sum of required resources.
         Example: [2, 1, 0] has value 3.

    2. Rounds 3 to 8:
       - look at the AI cards already played.
       - find condition cards whose conditions are not completed yet.
       - choose cards that give the missing resources for those conditions.
       - if there is no unfinished condition, fall back to most total resources.

    Tie-break:
    - If several cards have the same score, choose the smallest card number
      that is higher than the last card played.
    - If none is higher than the last card played, choose the smallest card number.
    """

    COLOR_TO_INT = {"w": 0, "b": 1, "r": 2, "re": 2, "g": 3, "y": 4}

    def __init__(self, filename="ai_memory_v3.pkl"):
        self.filename = filename
        self.history = []

        # These are kept so the rest of your program still works.
        # But choose_action() below is now deterministic/rule-based.
        self.epsilon_min = 0.05
        self.epsilon_decay = 0.999995

        self.q_table = self.load_memory()

    def load_memory(self):
        try:
            with open(self.filename, "rb") as file:
                data = pickle.load(file)
                self.epsilon = data.get("epsilon", 0.0)
                return data.get("q_table", {})
        except FileNotFoundError:
            self.epsilon = 0.0
            return {}

    def save_memory(self):
        data = {
            "q_table": self.q_table,
            "epsilon": self.epsilon,
        }
        with open(self.filename, "wb") as file:
            pickle.dump(data, file)

    def update_epsilon(self):
        # Kept for compatibility with your main loop.
        # The AI is rule-based now, so epsilon is not used in choose_action().
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def get_card_data(self, game, card_number):
        """Return the data dictionary for a normal card or sanctuary card."""
        if card_number in game.cards.card_info:
            return game.cards.card_info[card_number]
        return game.cards.sanctuary_info[str(card_number)]

    def card_number_value(self, card_number):
        """Numeric value printed on the card."""
        return int(card_number)

    def get_round_number(self, game):
        """The game starts with turns_left = 8.

        turns_left = 8 -> round 1
        turns_left = 7 -> round 2
        turns_left = 6 -> round 3
        ...
        turns_left = 1 -> round 8
        """
        return 9 - game.get_nb_turns_left()

    def condition_score(self, game, card_number):
        """How big the card condition is.

        Cards with no condition have score 0.
        """
        card = self.get_card_data(game, card_number)
        condition = card.get("condition")

        if condition is None:
            return 0

        return sum(condition)

    def get_current_resources(self, player, game):
        """Resources the player already has from sanctuaries and played cards."""
        total = game.cards.count_resources_sanctuary(player.sanctuary_in_hand)
        resources = total["resources"].copy()

        for c in player.cards_played:
            card_data = self.get_card_data(game, c)
            resources[0] += card_data["resources"][0]
            resources[1] += card_data["resources"][1]
            resources[2] += card_data["resources"][2]

        return resources

    def get_unfinished_condition_need(self, player, game):
        """Return the missing resources for condition cards already played.

        Example:
        current resources = [1, 0, 0]
        played condition card needs [2, 1, 0]
        missing resources = [1, 1, 0]

        If several played condition cards are unfinished, the missing resources
        are added together.
        """
        current_resources = self.get_current_resources(player, game)
        needed = [0, 0, 0]

        for c in player.cards_played:
            card_data = self.get_card_data(game, c)
            condition = card_data.get("condition")

            if condition is None:
                continue

            missing = [
                max(0, condition[i] - current_resources[i])
                for i in range(3)
            ]

            # Only count cards whose condition is not already completed.
            if any(missing):
                needed[0] += missing[0]
                needed[1] += missing[1]
                needed[2] += missing[2]

        return needed

    def needed_resource_score(self, player, game, card_number):
        """Score a card by how many missing resources it gives.

        During the last 6 rounds, the AI should not just take any resource.
        It should prefer resources that help complete unfinished conditions.
        """
        needed = self.get_unfinished_condition_need(player, game)
        card = self.get_card_data(game, card_number)
        resources = card["resources"]

        # If there is no unfinished condition, fall back to the previous behavior:
        # pick/play the card with the most total resources.
        if sum(needed) == 0:
            return sum(resources)

        # Count only resources that are actually useful for unfinished conditions.
        useful_resources = 0
        for i in range(3):
            useful_resources += min(resources[i], needed[i])

        return useful_resources

    def strategic_score(self, player, game, card_number):
        """Main score used by the AI."""
        round_number = self.get_round_number(game)

        if round_number <= 2:
            return self.condition_score(game, card_number)

        return self.needed_resource_score(player, game, card_number)

    def card_features(self, game, card_number):
        """Small hashable description of a card for the Q-table history."""
        card = self.get_card_data(game, card_number)

        resources = tuple(card["resources"])
        condition = tuple(card.get("condition") or (-1, -1, -1))
        points = card.get("points") or ("none", 0)

        return (
            resources,
            int(card.get("parchment", False)),
            self.COLOR_TO_INT.get(card.get("color"), -1),
            int(card.get("night", False)),
            condition,
            points[0],
            points[1],
        )

    def make_key(self, player, game, mode, card_number):
        return (player.get_state(game), mode, self.card_features(game, card_number))

    def break_tie(self, player, available_cards, candidate_actions):
        """Apply your tie-break rule.

        First preference:
        - the smallest card number higher than the last card played.

        If impossible:
        - the smallest card number.
        """
        last_value = int(player.number_last_card)

        higher_than_last = [
            action for action in candidate_actions
            if self.card_number_value(available_cards[action]) > last_value
        ]

        if higher_than_last:
            return min(
                higher_than_last,
                key=lambda action: self.card_number_value(available_cards[action])
            )

        return min(
            candidate_actions,
            key=lambda action: self.card_number_value(available_cards[action])
        )

    def choose_action(self, player, game, mode, available_cards=None):
        """Choose an index from available_cards.

        For mode == "play", available_cards defaults to the player's hand.
        For mode == "pick", available_cards defaults to the board.

        It returns an INDEX, so it still works with play_card() and draw_phase().
        """
        if mode == "play":
            if available_cards is None:
                available_cards = player.cards_in_hand

        elif mode == "pick":
            if available_cards is None:
                available_cards = game.cards.cards_on_board

        else:
            raise ValueError(f"Unknown mode: {mode}")

        possible_actions = list(range(len(available_cards)))
        if not possible_actions:
            raise ValueError("AI has no available actions")

        scores = []
        for action in possible_actions:
            card_number = available_cards[action]
            score = self.strategic_score(player, game, card_number)
            scores.append(score)

        best_score = max(scores)

        candidate_actions = [
            action for action, score in zip(possible_actions, scores)
            if score == best_score
        ]

        best_action = self.break_tie(player, available_cards, candidate_actions)

        chosen_card = available_cards[best_action]
        self.history.append(self.make_key(player, game, mode, chosen_card))

        return best_action

    def learn_small_reward(self, reward):
        """Kept for compatibility.

        The new AI chooses with rules, not randomness. This still records Q-values
        if you want to look at them later, but choose_action() does not depend on
        them anymore.
        """
        if not self.history:
            return

        learning_rate = 0.1
        key = self.history[-1]

        old_value = self.q_table.get(key, 0.0)
        self.q_table[key] = old_value + learning_rate * (reward - old_value)

    def learn_final_reward(self, reward):
        """Kept for compatibility with your main loop."""
        learning_rate = 0.1
        gamma = 0.95

        for i, key in enumerate(reversed(self.history)):
            discounted_reward = reward * (gamma ** i)
            old_value = self.q_table.get(key, 0.0)
            self.q_table[key] = old_value + learning_rate * (discounted_reward - old_value)

        self.history = []

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
            nb_red = total_resources["color"].count("r") + total_resources["color"].count("re")
            nb_sets = min(nb_blue, nb_green, nb_yellow, nb_red)
            return value * nb_sets

        # Points for night
        if point_type == "night":
            return value * total_resources["night"]

        if point_type in ["b", "g", "y", "re", "w", "bg", "by", "bre", "gy", "gre", "yre"]:
            selected_colors = []

            if "re" in point_type:
                selected_colors.extend(["r", "re"])
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
            #resources["color"].append(card_data["color"])
            #if card_data["night"]:
            #    resources["night"] += 1

        turns_left = game.get_nb_turns_left()
        res = tuple(r for r in resources["resources"])
        #night = min(resources["night"], 5)
        #parchment = min(self.nb_parchment, 4)

        # how many cards in hand have conditions? how many give points?
        hand_has_condition = sum(1 for c in self.cards_in_hand if game.cards.card_info[c]["condition"] is not None)
        hand_has_points = sum(1 for c in self.cards_in_hand if game.cards.card_info[c]["points"] is not None)

        #return (turns_left, res, night, parchment, hand_has_condition, hand_has_points)
        return (turns_left, res, hand_has_condition, hand_has_points)
    
    def get_total_ressources(self, game):
        resources = game.cards.count_resources_sanctuary(self.sanctuary_in_hand)

        for c in self.cards_played:
            card_data = game.cards.card_info[c]
            resources["resources"][0] += card_data["resources"][0]
            resources["resources"][1] += card_data["resources"][1]
            resources["resources"][2] += card_data["resources"][2]
        
        return resources["resources"][0] + resources["resources"][1] + resources["resources"][2]

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

    def calculate_points (self, cards):
        self.points = 0
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
    resources_1 = 0
    resources_2 = 0
    total_games = 200000
    while nb_game < total_games:
        nb_game = nb_game + 1
        game = Game()
        state = game.reset()

        while game.get_nb_turns_left() > 0:

            game.cards.refill_board()

            # --- Play phase ---
            p1_index = ai.choose_action(game.player1, game, "play")
            p2_index = random.randrange(len(game.player2.cards_in_hand))

            # Peek at p1's card resources BEFORE playing
            p1_card_num = game.player1.cards_in_hand[p1_index]
            p1_play_resources = game.cards.card_info[p1_card_num]["resources"]

            game.play_phase(p1_index, p2_index)
            ai.learn_small_reward(sum(p1_play_resources))  # reward = resources gained by playing

            # --- Pick phase ---
            # Important: if the AI picks second, it must choose from the board
            # AFTER the first picker has removed a card. We simulate that board
            # here before asking the AI to choose.
            if game.first_picker == game.player1:
                first_choice = ai.choose_action(game.player1, game, "pick")
                ia_card_picked = game.cards.cards_on_board[first_choice]

                remaining_board = game.cards.cards_on_board.copy()
                remaining_board.pop(first_choice)
                second_choice = random.randrange(len(remaining_board))
            else:
                first_choice = random.randrange(len(game.cards.cards_on_board))

                remaining_board = game.cards.cards_on_board.copy()
                remaining_board.pop(first_choice)

                # second_choice is an index in the board AFTER first_choice is popped,
                # which is exactly what draw_phase() expects.
                second_choice = ai.choose_action(
                    game.player1,
                    game,
                    "pick",
                    available_cards=remaining_board,
                )
                ia_card_picked = remaining_board[second_choice]

            picked_resources = game.cards.card_info[ia_card_picked]["resources"]
            ai.learn_small_reward(sum(picked_resources))  # reward = resources gained by picking

            game.draw_phase(first_choice, second_choice)
            game.set_turns()

            if game.get_nb_turns_left() < 1:
                points_player1 = game.player1.calculate_points(game.cards)
                points_player2 = game.player2.calculate_points(game.cards)
                list_points_1.append(points_player1)
                list_points_2.append(points_player2)
                total_points_1 += points_player1
                total_points_2 += points_player2
                resources_1 += game.player1.get_total_ressources(game)
                resources_2 += game.player2.get_total_ressources(game)

                if points_player1 > points_player2:
                    wins += 1
                elif points_player1 == points_player2:
                    draws += 1
                else:
                    losses += 1

                final_reward = points_player1 - points_player2
                ai.learn_final_reward(final_reward)
                ai.update_epsilon()

        if nb_game % 10000 == 0:
            total = wins + draws + losses
            print(f"{nb_game/total_games*100:.1f}% | epsilon: {ai.epsilon:.4f} | resources_1: {resources_1/nb_game} | resources_2: {resources_2/nb_game} | epsilon: {ai.epsilon:.4f} | Q-table: {len(ai.q_table)} | Win: {wins/total*100:.1f}% Draw: {draws/total*100:.1f}% Loss: {losses/total*100:.1f}%")
            wins = draws = losses = 0  # reset for next window

                
    
    ai.save_memory()

    print("epsilon:", ai.epsilon)
    print("memory size:", len(ai.q_table))

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