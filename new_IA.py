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
    """Self-learning AI based on card links, not hand-written strategy.

    This version removes the hard-coded strategy rules.

    It learns from links at the end of each game:
    - condition card completed by resource cards
    - stone/dear/pineapple point cards linked to resource cards
    - night point cards linked to night cards
    - parchment point cards linked to parchment cards
    - color point cards linked to useful color cards

    The AI begins mostly random because epsilon starts high.
    Over many games, actions that created useful links receive higher values.
    """

    COLOR_TO_INT = {"w": 0, "b": 1, "r": 2, "re": 2, "g": 3, "y": 4}

    def __init__(self, filename="ai_memory_link_learning.pkl"):
        self.filename = filename
        self.history = []

        self.learning_rate = 0.08
        self.epsilon_min = 0.05
        self.epsilon_decay = 0.99997

        self.q_table = {}
        self.card_values = {}

        # Learned values for contextual links:
        # "I already have card A, and candidate card B supports it."
        # This is what lets the AI learn combinations, not only individual cards.
        self.link_values = {}
        self.context_link_weight = 0.75

        self.epsilon = 1.0
        self.load_memory()

    def load_memory(self):
        try:
            with open(self.filename, "rb") as file:
                data = pickle.load(file)
                self.epsilon = data.get("epsilon", 1.0)
                self.q_table = data.get("q_table", {})
                self.card_values = data.get("card_values", {})
                self.link_values = data.get("link_values", {})
        except FileNotFoundError:
            self.epsilon = 1.0
            self.q_table = {}
            self.card_values = {}
            self.link_values = {}

    def save_memory(self):
        data = {
            "epsilon": self.epsilon,
            "q_table": self.q_table,
            "card_values": self.card_values,
            "link_values": self.link_values,
        }
        with open(self.filename, "wb") as file:
            pickle.dump(data, file)

    def update_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            if self.epsilon < self.epsilon_min:
                self.epsilon = self.epsilon_min

    def get_card_data(self, game, card_number):
        if card_number in game.cards.card_info:
            return game.cards.card_info[card_number]
        return game.cards.sanctuary_info[str(card_number)]

    def card_features(self, game, card_number):
        """Hashable description of the card.

        This lets the AI learn about card TYPES, not only card positions.
        """
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

    def current_resource_totals(self, player, game):
        """Resources the player already has before choosing the candidate card.

        This is used only to detect whether a candidate card helps an unfinished
        condition that is already on the table.
        """
        resources = game.cards.count_resources_sanctuary(player.sanctuary_in_hand)["resources"].copy()

        for c in player.cards_played:
            card_data = self.get_card_data(game, c)
            resources[0] += card_data["resources"][0]
            resources[1] += card_data["resources"][1]
            resources[2] += card_data["resources"][2]

        return resources

    def categories_from_point_type(self, point_type):
        """Convert point types into the things that can support them.

        Examples:
            "pineapple" -> ["pineapple"]
            "night"     -> ["night"]
            "yre"       -> ["y", "re"]
            "color"     -> ["b", "g", "y", "re"]
        """
        if point_type in ["stone", "dear", "pineapple", "parchment", "night"]:
            return [point_type]

        if point_type == "resources":
            return ["stone", "dear", "pineapple"]

        if point_type == "color":
            return ["b", "g", "y", "re"]

        categories = []
        remaining = point_type

        if "re" in remaining:
            categories.append("re")
            remaining = remaining.replace("re", "")

        for color in ["b", "g", "y", "w"]:
            if color in remaining:
                categories.append(color)

        return categories

    def candidate_matches_category(self, candidate_data, category):
        """Return True when the candidate card supports this scoring category."""
        resources = candidate_data["resources"]

        if category == "stone":
            return resources[0] > 0
        if category == "dear":
            return resources[1] > 0
        if category == "pineapple":
            return resources[2] > 0
        if category == "parchment":
            return candidate_data.get("parchment", False)
        if category == "night":
            return candidate_data.get("night", False)
        if category == "re":
            return candidate_data.get("color") in ["r", "re"]

        # b, g, y, w
        return candidate_data.get("color") == category

    def context_link_keys(self, player, game, mode, candidate_card):
        """Return learned context-link keys for this possible choice.

        This does not force a strategy. It only says which links are possible.
        The values of these links are learned later from rewards.

        Examples of learned links:
            - condition card needing dear + candidate giving dear
            - ["night", 3] card already played + candidate with night=True
            - ["parchment", 4] card already played + candidate with parchment=True
            - color scorer already played + candidate with matching color
        """
        candidate_data = self.get_card_data(game, candidate_card)
        candidate_features = self.card_features(game, candidate_card)
        current_resources = self.current_resource_totals(player, game)

        keys = []

        # Use cards already placed/owned as the context.
        # cards_played is the most important part. sanctuary_in_hand is included
        # because a sanctuary can also be a scoring card or support future links.
        context_cards = player.cards_played + player.sanctuary_in_hand

        for existing_card in context_cards:
            if str(existing_card) == str(candidate_card):
                continue

            existing_data = self.get_card_data(game, existing_card)
            existing_features = self.card_features(game, existing_card)

            # 1) Candidate helps an unfinished condition already played/owned.
            condition = existing_data.get("condition")
            if condition is not None:
                missing = [
                    max(0, condition[i] - current_resources[i])
                    for i in range(3)
                ]

                useful_resources = [
                    min(candidate_data["resources"][i], missing[i])
                    for i in range(3)
                ]

                for resource_index, useful_amount in enumerate(useful_resources):
                    if useful_amount > 0:
                        resource_name = ["stone", "dear", "pineapple"][resource_index]
                        keys.append((
                            mode,
                            "condition",
                            resource_name,
                            existing_features,
                            candidate_features,
                        ))

            # 2) Candidate matches how an already played/owned card makes points.
            points = existing_data.get("points")
            if points is not None:
                point_type, value = points

                if point_type != "points":
                    for category in self.categories_from_point_type(point_type):
                        if self.candidate_matches_category(candidate_data, category):
                            keys.append((
                                mode,
                                "points",
                                category,
                                existing_features,
                                candidate_features,
                            ))

        return keys

    def context_link_value(self, player, game, mode, card_number):
        """Estimated value of learned links between current context and candidate."""
        keys = self.context_link_keys(player, game, mode, card_number)

        if not keys:
            return 0.0

        # Average avoids making the value explode when many context cards exist.
        total = sum(self.link_values.get(key, 0.0) for key in keys)
        return total / len(keys)

    def estimated_value(self, player, game, mode, card_number):
        state_key = self.make_key(player, game, mode, card_number)
        feature_key = (mode, self.card_features(game, card_number))

        base_value = self.q_table.get(state_key, 0.0)
        card_value = self.card_values.get(feature_key, 0.0)
        link_value = self.context_link_value(player, game, mode, card_number)

        return base_value + card_value + self.context_link_weight * link_value

    def remember_choice(self, player, game, mode, card_number):
        self.history.append({
            "card": str(card_number),
            "mode": mode,
            "state_key": self.make_key(player, game, mode, card_number),
            "feature_key": (mode, self.card_features(game, card_number)),

            # Context links that existed at the moment of the choice.
            # These links get reward only if the chosen card later proves useful.
            "context_link_keys": self.context_link_keys(player, game, mode, card_number),
        })

    def choose_action(self, player, game, mode, available_cards=None):
        """Choose an index from the hand or board.

        No strategic rule is hard-coded here. The AI either explores randomly
        or exploits values learned from previous link rewards.
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

        if random.random() < self.epsilon:
            action = random.choice(possible_actions)
        else:
            values = [
                self.estimated_value(player, game, mode, available_cards[action])
                for action in possible_actions
            ]
            best_value = max(values)
            best_actions = [
                action for action, value in zip(possible_actions, values)
                if value == best_value
            ]
            action = random.choice(best_actions)

        self.remember_choice(player, game, mode, available_cards[action])
        return action

    def choose_sanctuary(self, player, game, sanctuary_options):
        """Choose a sanctuary card using the same learned values.

        Player 2 does not use this. Player 2 still receives random sanctuaries.
        """
        possible_actions = list(range(len(sanctuary_options)))
        if not possible_actions:
            return None

        if random.random() < self.epsilon:
            action = random.choice(possible_actions)
        else:
            values = [
                self.estimated_value(player, game, "sanctuary", sanctuary_options[action])
                for action in possible_actions
            ]
            best_value = max(values)
            best_actions = [
                action for action, value in zip(possible_actions, values)
                if value == best_value
            ]
            action = random.choice(best_actions)

        chosen = sanctuary_options[action]
        self.remember_choice(player, game, "sanctuary", chosen)
        return chosen

    def add_reward(self, rewards, card_number, amount):
        if amount <= 0:
            return
        key = str(card_number)
        rewards[key] = rewards.get(key, 0.0) + float(amount)

    def all_player_cards(self, player):
        return player.cards_played.copy() + player.sanctuary_in_hand.copy()

    def final_totals_from_cards(self, cards, all_cards):
        """Return final resource/color/night/parchment totals for a card list.

        This helper is used both for the real final hand and for simulations
        where we remove one sanctuary card to see what it helped.
        """
        resources = [0, 0, 0]
        colors = []
        night_cards = []
        parchment_cards = []

        for c in all_cards:
            data = cards.get_card_data(c)
            resources[0] += data["resources"][0]
            resources[1] += data["resources"][1]
            resources[2] += data["resources"][2]
            colors.append(data["color"])

            if data.get("night", False):
                night_cards.append(c)

            if data.get("parchment", False):
                parchment_cards.append(c)

        return {
            "resources": resources,
            "color": colors,
            "night": len(night_cards),
            "night_cards": night_cards,
            "parchment_cards": parchment_cards,
            "nb_parchment": len(parchment_cards),
        }

    def final_totals(self, player, cards):
        """Return final totals using all cards owned by the player."""
        return self.final_totals_from_cards(cards, self.all_player_cards(player))

    def final_totals_without_card(self, player, cards, excluded_card):
        """Return final totals after removing one specific card.

        This lets the AI ask:
            "What would the final links look like if this sanctuary was absent?"
        """
        all_cards_without = [
            c for c in self.all_player_cards(player)
            if str(c) != str(excluded_card)
        ]

        return self.final_totals_from_cards(cards, all_cards_without)

    def points_with_totals(self, cards, scoring_card, totals):
        """Calculate how many points one card makes with given final totals."""
        total_resources_for_points = {
            "resources": totals["resources"].copy(),
            "color": totals["color"].copy(),
            "night": totals["night"],
        }

        return cards.count_points(
            scoring_card,
            total_resources_for_points,
            totals["nb_parchment"],
        )

    def reward_sanctuary_help_links(self, rewards, player, cards):
        """Give extra reward to sanctuary cards that helped another card score.

        The previous link rewards already rewarded resources in general. This
        new reward is more direct: for each sanctuary, we remove it mentally and
        compare the score/condition completion of every other card.

        If removing the sanctuary makes another card lose points or lose a
        completed condition, the sanctuary receives reward for that link.
        """
        full_totals = self.final_totals(player, cards)

        for sanctuary_card in player.sanctuary_in_hand:
            totals_without_sanctuary = self.final_totals_without_card(
                player,
                cards,
                sanctuary_card,
            )

            for helped_card in self.all_player_cards(player):
                # A sanctuary can help another card, not itself.
                if str(helped_card) == str(sanctuary_card):
                    continue

                helped_data = cards.get_card_data(helped_card)
                condition = helped_data.get("condition")
                points = helped_data.get("points")

                # 1) Condition help:
                # Reward the sanctuary if this condition is completed with the
                # sanctuary but not completed without it.
                if condition is not None:
                    completed_with = all(
                        full_totals["resources"][i] >= condition[i]
                        for i in range(3)
                    )
                    completed_without = all(
                        totals_without_sanctuary["resources"][i] >= condition[i]
                        for i in range(3)
                    )

                    if completed_with and not completed_without:
                        condition_reward = 5 + sum(condition)

                        if points is not None:
                            condition_reward += max(
                                0,
                                self.points_with_totals(
                                    cards,
                                    helped_card,
                                    full_totals,
                                ),
                            )

                        self.add_reward(rewards, sanctuary_card, condition_reward)

                # 2) Point help:
                # Reward the sanctuary by the exact number of points another
                # card loses when this sanctuary is removed.
                if points is not None:
                    points_with = self.points_with_totals(
                        cards,
                        helped_card,
                        full_totals,
                    )
                    points_without = self.points_with_totals(
                        cards,
                        helped_card,
                        totals_without_sanctuary,
                    )

                    point_difference = points_with - points_without

                    if point_difference > 0:
                        self.add_reward(rewards, sanctuary_card, point_difference)

    def resource_providers(self, player, cards, resource_index):
        providers = []
        for c in self.all_player_cards(player):
            data = cards.get_card_data(c)
            amount = data["resources"][resource_index]
            if amount > 0:
                providers.append((c, amount))
        return providers

    def reward_resource_providers(self, rewards, providers, needed_units, total_reward):
        """Reward cards that provide a resource.

        If only 2 stones are needed, only 2 stone units receive credit.
        """
        if needed_units <= 0 or total_reward <= 0:
            return

        remaining = needed_units
        reward_per_unit = total_reward / needed_units

        for card_number, amount in providers:
            if remaining <= 0:
                break
            useful_units = min(amount, remaining)
            self.add_reward(rewards, card_number, useful_units * reward_per_unit)
            remaining -= useful_units

    def point_type_categories(self, point_type):
        if point_type in ["pineapple", "dear", "stone", "parchment", "night"]:
            return [point_type]
        if point_type == "color":
            return ["re", "b", "g", "y"]
        if point_type == "resources":
            return ["stone", "dear", "pineapple"]

        categories = []
        remaining = point_type
        if "re" in remaining:
            categories.append("re")
            remaining = remaining.replace("re", "")
        for color in ["b", "g", "y", "w"]:
            if color in remaining:
                categories.append(color)
        return categories

    def color_matches(self, card_color, category):
        if category == "re":
            return card_color in ["r", "re"]
        return card_color == category

    def reward_point_links(self, rewards, scoring_card, point_type, value, points_made, player, cards, totals):
        """Reward the card that scores and the cards that made it score."""
        if points_made <= 0:
            return

        # The scoring card itself deserves credit because it created the scoring rule.
        self.add_reward(rewards, scoring_card, points_made)

        if point_type == "points":
            return

        if point_type == "stone":
            providers = self.resource_providers(player, cards, 0)
            self.reward_resource_providers(rewards, providers, totals["resources"][0], points_made)
            return

        if point_type == "dear":
            providers = self.resource_providers(player, cards, 1)
            self.reward_resource_providers(rewards, providers, totals["resources"][1], points_made)
            return

        if point_type == "pineapple":
            providers = self.resource_providers(player, cards, 2)
            self.reward_resource_providers(rewards, providers, totals["resources"][2], points_made)
            return

        if point_type == "parchment":
            for c in totals["parchment_cards"]:
                self.add_reward(rewards, c, value)
            return

        if point_type == "night":
            for c in totals["night_cards"]:
                self.add_reward(rewards, c, value)
            return

        if point_type == "resources":
            nb_sets = min(totals["resources"])
            if nb_sets > 0:
                for resource_index in range(3):
                    providers = self.resource_providers(player, cards, resource_index)
                    self.reward_resource_providers(
                        rewards,
                        providers,
                        nb_sets,
                        points_made / 3,
                    )
            return

        # Color links: re, b, g, y, w, bg, by, bre, gy, gre, yre, color.
        categories = self.point_type_categories(point_type)
        for c in self.all_player_cards(player):
            data = cards.get_card_data(c)
            if any(self.color_matches(data["color"], category) for category in categories):
                self.add_reward(rewards, c, value)

    def compute_link_rewards(self, player, cards):
        """Analyze the final game and reward useful card links.

        This is the heart of the learning system.
        It does not reward 'winning'. It rewards the relationships that made
        cards useful.
        """
        rewards = {}
        totals = self.final_totals(player, cards)
        total_resources_for_points = {
            "resources": totals["resources"].copy(),
            "color": totals["color"].copy(),
            "night": totals["night"],
        }

        for scoring_card in self.all_player_cards(player):
            data = cards.get_card_data(scoring_card)
            condition = data.get("condition")
            points = data.get("points")

            condition_completed = True
            if condition is not None:
                condition_completed = all(
                    totals["resources"][i] >= condition[i]
                    for i in range(3)
                )

            # Reward condition links only when the condition is completed.
            if condition is not None and condition_completed:
                # A completed condition is itself a valuable link.
                condition_reward = 5 + sum(condition)
                if points is not None:
                    condition_reward += max(0, cards.count_points(
                        scoring_card,
                        total_resources_for_points,
                        totals["nb_parchment"],
                    ))

                self.add_reward(rewards, scoring_card, condition_reward)

                for resource_index in range(3):
                    needed = condition[resource_index]
                    if needed > 0:
                        providers = self.resource_providers(player, cards, resource_index)
                        self.reward_resource_providers(
                            rewards,
                            providers,
                            needed,
                            condition_reward / max(1, sum(condition)),
                        )

            # If the card has no points, there is no scoring link to learn.
            if points is None:
                continue

            # If the condition is not completed, this card did not score.
            if not condition_completed:
                continue

            point_type, value = points
            points_made = cards.count_points(
                scoring_card,
                total_resources_for_points,
                totals["nb_parchment"],
            )

            self.reward_point_links(
                rewards,
                scoring_card,
                point_type,
                value,
                points_made,
                player,
                cards,
                totals,
            )

        # Extra learning signal:
        # sanctuary cards get direct reward when removing that sanctuary would
        # make another card lose points or lose a completed condition.
        self.reward_sanctuary_help_links(rewards, player, cards)

        return rewards

    def learn_from_links(self, player, cards):
        """Update the AI from the links created during the finished game."""
        card_rewards = self.compute_link_rewards(player, cards)

        for entry in self.history:
            reward = card_rewards.get(entry["card"], 0.0)

            old_q = self.q_table.get(entry["state_key"], 0.0)
            self.q_table[entry["state_key"]] = old_q + self.learning_rate * (reward - old_q)

            old_card_value = self.card_values.get(entry["feature_key"], 0.0)
            self.card_values[entry["feature_key"]] = old_card_value + self.learning_rate * (reward - old_card_value)

            # Learn whether this candidate card was good in the context where it
            # was chosen. If the card later helped score, all matching context
            # links receive positive reward. If it did not help, those links move
            # back toward zero.
            for context_key in entry.get("context_link_keys", []):
                old_link_value = self.link_values.get(context_key, 0.0)
                self.link_values[context_key] = old_link_value + self.learning_rate * (reward - old_link_value)

        total_link_reward = sum(card_rewards.values())
        self.history = []
        return total_link_reward

    def learn_small_reward(self, reward):
        """No-op kept for compatibility.

        We do NOT use immediate resource rewards anymore, because this version
        should learn from card links instead of hand-written resource hints.
        """
        return

    def learn_final_reward(self, reward):
        """No-op kept for compatibility.

        We do NOT learn from the score difference against Player 2 anymore.
        """
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
    
    def get_card_data(self, number):
        """Return the data dictionary for a normal card or sanctuary card."""
        if number in self.card_info:
            return self.card_info[number]
        return self.sanctuary_info[str(number)]

    def get_player_resources_for_conditions(self, player):
        """Resources the player currently has from sanctuary cards and played cards.

        This is used when choosing a sanctuary card, because the sanctuary should
        help complete the condition cards that are already played.
        """
        total = self.count_resources_sanctuary(player.sanctuary_in_hand)
        resources = total["resources"].copy()

        for c in player.cards_played:
            card_data = self.get_card_data(c)
            resources[0] += card_data["resources"][0]
            resources[1] += card_data["resources"][1]
            resources[2] += card_data["resources"][2]

        return resources

    def get_unfinished_condition_cards(self, player):
        """Return condition cards already played but not completed yet.

        Each result is:
            (card_number, missing_resources)

        missing_resources uses your normal order:
            [stone, dear, pineapple]
        """
        current_resources = self.get_player_resources_for_conditions(player)
        unfinished = []

        for c in player.cards_played:
            card_data = self.get_card_data(c)
            condition = card_data.get("condition")

            if condition is None:
                continue

            missing = [
                max(0, condition[i] - current_resources[i])
                for i in range(3)
            ]

            if any(missing):
                unfinished.append((c, missing))

        return unfinished

    def primary_missing_resource_priority(self, missing):
        """Priority of the resource still needed by a condition card.

        You asked for this order:
            pineapple, dear, stone

        Because resources are stored as:
            [stone, dear, pineapple]

        the priority checks indexes:
            pineapple = 2
            dear      = 1
            stone     = 0
        """
        if missing[2] > 0:
            return 0  # pineapple first
        if missing[1] > 0:
            return 1  # dear second
        if missing[0] > 0:
            return 2  # stone third
        return 3

    def sanctuary_choice_score(self, sanctuary_number, player):
        """Score one sanctuary option.

        The sanctuary tries to help complete unfinished condition cards.

        Priority:
        1. Help an unfinished condition.
        2. Complete an unfinished condition.
        3. Prefer the condition card with the fewest resources still needed.
        4. If still tied, prefer needs in this order:
           pineapple, dear, stone.
        5. Prefer the sanctuary that gives useful resources in that same order.
        """
        sanctuary = self.sanctuary_info[str(sanctuary_number)]
        sanctuary_resources = sanctuary["resources"]
        unfinished = self.get_unfinished_condition_cards(player)

        # If there is no condition to complete, choose the sanctuary with the
        # most resources, with pineapple > dear > stone as the tie-break order.
        if not unfinished:
            return (
                0,
                sum(sanctuary_resources),
                sanctuary_resources[2],  # pineapple
                sanctuary_resources[1],  # dear
                sanctuary_resources[0],  # stone
                -int(sanctuary_number),
            )

        best_score_for_this_sanctuary = None

        for condition_card, missing_before in unfinished:
            missing_after = [
                max(0, missing_before[i] - sanctuary_resources[i])
                for i in range(3)
            ]

            useful = [
                missing_before[i] - missing_after[i]
                for i in range(3)
            ]

            useful_total = sum(useful)
            completed_after = 1 if sum(missing_after) == 0 else 0
            resources_still_needed_before = sum(missing_before)
            resources_still_needed_after = sum(missing_after)
            priority = self.primary_missing_resource_priority(missing_before)

            score = (
                1 if useful_total > 0 else 0,
                completed_after,
                -resources_still_needed_before,
                -priority,
                useful[2],              # useful pineapple
                useful[1],              # useful dear
                useful[0],              # useful stone
                -resources_still_needed_after,
                -int(sanctuary_number),
            )

            if best_score_for_this_sanctuary is None or score > best_score_for_this_sanctuary:
                best_score_for_this_sanctuary = score

        return best_score_for_this_sanctuary

    def choose_best_sanctuary(self, sanctuary_options, player):
        """Choose the best sanctuary from the drawn sanctuary options."""
        return max(
            sanctuary_options,
            key=lambda sanctuary_number: self.sanctuary_choice_score(sanctuary_number, player)
        )

    def choose_best_final_sanctuary(self, sanctuary_options, player):
        """Last-turn sanctuary choice for the AI.

        On the final turn, the AI ignores the old condition sanctuary strategy and
        simply chooses the sanctuary that gives the highest final score.
        """
        return max(
            sanctuary_options,
            key=lambda sanctuary_number: (
                self.calculate_points_for(player, extra_sanctuary=sanctuary_number),
                -int(sanctuary_number),
            )
        )

    def draw_sanctuary(self, nb_parchment, player=None, final_turn=False, ai=None, game=None):
        """Draw sanctuary options, then choose the best one.

        The number of options is nb_parchment + 1, like before.

        If player is provided, the sanctuary is chosen strategically to help
        complete the player's played condition cards.

        If player is not provided, it falls back to a random choice.
        """
        if len(self.sanctuary_pack) == 0:
            return None

        nb_options = min(nb_parchment + 1, len(self.sanctuary_pack))
        sanctuary_drawn = random.sample(self.sanctuary_pack, nb_options)

        if player is not None and getattr(player, "is_ai", False) and ai is not None and game is not None:
            number = ai.choose_sanctuary(player, game, sanctuary_drawn)
        else:
            # Player 2, or any player without an AI object, stays random.
            number = random.choice(sanctuary_drawn)

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

    def calculate_points_for(self, player, extra_played_card=None, extra_sanctuary=None):
        """Pure point simulation used by the AI.

        It calculates what the player's points would be after adding one tested
        played card and/or one tested sanctuary card.

        Important: this does NOT change player.cards_played, player.sanctuary_in_hand,
        player.nb_parchment, player.total_resources, or player.points.
        """
        played_cards = player.cards_played.copy()
        sanctuary_cards = player.sanctuary_in_hand.copy()
        nb_parchment = player.nb_parchment

        if extra_played_card is not None:
            played_cards.append(extra_played_card)
            if self.add_parchment(extra_played_card, "card"):
                nb_parchment += 1

        if extra_sanctuary is not None:
            sanctuary_cards.append(extra_sanctuary)
            if self.add_parchment(extra_sanctuary, "sanctuary"):
                nb_parchment += 1

        total_resources = self.count_resources_sanctuary(sanctuary_cards)
        points = 0

        for c in reversed(played_cards):
            c_data = self.count_resources_one_card(self.card_info[c])
            total_resources["resources"][0] += c_data["resources"][0]
            total_resources["resources"][1] += c_data["resources"][1]
            total_resources["resources"][2] += c_data["resources"][2]
            total_resources["color"].extend(c_data["color"])

            if c_data["night"]:
                total_resources["night"] += 1

            points += self.count_points(c, total_resources, nb_parchment)

        for s in sanctuary_cards:
            points += self.count_points(s, total_resources, nb_parchment)

        return points

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
    def __init__(self, cards, is_ai=False):
        """Initialize a player with 3 cards drawn from the given card deck.

        Args:
            cards: A Cards object used to draw the player's starting hand.
            is_ai: True only for the AI player. This is used so the AI can
                choose sanctuary cards strategically while the random opponent
                still receives random sanctuary cards.
        """
        self.is_ai = is_ai
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
            # Only the AI player gets the strategic sanctuary choice.
            # The random opponent keeps the old random sanctuary choice.
            if self.is_ai:
                sanctuary = cards.draw_sanctuary(
                    self.nb_parchment,
                    player=self,
                    final_turn=(game.get_nb_turns_left() == 1),
                    ai=getattr(game, "ai", None),
                    game=game,
                )
            else:
                sanctuary = cards.draw_sanctuary(self.nb_parchment, player=None)

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
        self.player1 = Player(self.cards, is_ai=True)
        self.player2 = Player(self.cards, is_ai=False)
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
        game.ai = ai

        while game.get_nb_turns_left() > 0:

            game.cards.refill_board()

            # --- Play phase ---
            p1_index = ai.choose_action(game.player1, game, "play")
            p2_index = random.randrange(len(game.player2.cards_in_hand))

            game.play_phase(p1_index, p2_index)

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

                # Learn from links created by Player 1's cards, not from score difference.
                ai.learn_from_links(game.player1, game.cards)
                ai.update_epsilon()

        if nb_game % 10000 == 0:
            total = wins + draws + losses
            print(f"{nb_game/total_games*100:.1f}% | epsilon: {ai.epsilon:.4f} | resources_1: {resources_1/nb_game} | resources_2: {resources_2/nb_game} | epsilon: {ai.epsilon:.4f} | Q-table: {len(ai.q_table)} | card-values: {len(ai.card_values)} | link-values: {len(ai.link_values)} | Win: {wins/total*100:.1f}% Draw: {draws/total*100:.1f}% Loss: {losses/total*100:.1f}%")
            wins = draws = losses = 0  # reset for next window

                
    
    ai.save_memory()

    print("epsilon:", ai.epsilon)
    print("memory size:", len(ai.q_table))

    print("mean PLAYER 1: ", total_points_1/(nb_game))
    print("mean PLAYER 2: ", total_points_2/(nb_game))
    print("median PLAYER 1: ", np.median(list_points_1))
    print("median PLAYER 2: ", np.median(list_points_2))
    print("min: ", np.min(list_points_1))
    print("max: ", np.max(list_points_1))
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