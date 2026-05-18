import random
import numpy as np
import matplotlib.pyplot as plt
#[x,x,x] = [stone, dear, pineapple]
#color: grey (w), blue (b), red (r), green (g) j'ai choisi w comme white pour gris car g est déjà pris par green
# ["points", x] (x points),  ["night", x] (x points par carte nuit),  ["reb", x] (x point par carte rouge et bleu (re = red, b = blue, g = green, y = yellow, w = gray),  
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
    25: {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": True, "condition": None, "points": ["yg", 1]},
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
    42: {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": False, "condition": [1, 1, 0], "points": ["yg", 2]},
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
    65: {"resources": [0, 0, 0], "parchment": True, "color": "y", "night": False, "condition": [0, 0, 3], "points": ["yg", 3]},
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
    "146": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["yg", 1]},
    "147": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["gb", 1]},
    "148": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["gre", 1]},
    "149": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["yb", 1]},
    "150": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["parchment", 2]},
    "151": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["pineapple", 2]},
    "152": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["dear", 2]},
    "153": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["points", 5]},
}

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

    def play_card(self, index, cards):
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
        
        self.number_last_card = int(number)

        return number
    
    def calculate_points (self, cards):
        #print("s: ", self.sanctuary_in_hand)
        #print("s: ", self.cards_played)

        self.total_resources = cards.count_resources_sanctuary(self.sanctuary_in_hand)
        #print("ressources sanctuary: ", self.total_resources)
        for c in self.cards_played:
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
        p1_card = self.player1.play_card(p1_card_index, self.cards)
        p2_card = self.player2.play_card(p2_card_index, self.cards)

        if int(p1_card) < int(p2_card):
            self.first_picker = self.player1
            self.second_picker = self.player2
        else:
            self.first_picker = self.player2
            self.second_picker = self.player1

        #print("P1 played:", p1_card)
        #print("P2 played:", p2_card)
    
    def draw_phase(self, first_choice_index, second_choice_index):
        # First picker chooses one card from the board
        first_card = self.cards.cards_on_board.pop(first_choice_index)
        self.first_picker.cards_in_hand.append(first_card)

        # Second picker chooses one card from the remaining board
        second_card = self.cards.cards_on_board.pop(second_choice_index)
        self.second_picker.cards_in_hand.append(second_card)

        self.cards.refill_board()


if __name__ == "__main__":
    nb_game = 0
    list_points = []
    total_points = 0
    while nb_game < 200000:
        nb_game = nb_game + 1
        game = Game()
        state = game.reset()

        while game.get_nb_turns_left() > 0:

            game.cards.refill_board()

            #play a card
            p1_index = random.randint(0, 2) #always three cards in hand
            p2_index = random.randint(0, 2)
            game.play_phase(p1_index, p2_index)

            #picl a card
            first_choice = random.randint(0, len(game.cards.cards_on_board) - 1)
            second_choice = random.randint(0, len(game.cards.cards_on_board) - 2)
            game.draw_phase(first_choice, second_choice)

            #print("P1 hand:", game.player1.cards_in_hand)
            #print("P2 hand:", game.player2.cards_in_hand)
            
            #print("First picker:", "P1" if game.first_picker == game.player1 else "P2")

            game.set_turns()
            if game.get_nb_turns_left() < 1:
                points_player1 = game.player1.calculate_points(game.cards)
                points_player2 = game.player2.calculate_points(game.cards)
                #print(points_player1)
                #print(points_player2)
                list_points.append(points_player1)
                list_points.append(points_player2)
                total_points = total_points + points_player1 + points_player2
    
    print("mean: ", total_points/(nb_game*2))
    print("median: ", np.median(list_points))
    print("min: ", np.min(list_points))
    print("max: ", np.max(list_points))
    bins = list(range(0, 101, 5))  # 0, 10, 20, ..., 100
    counts = []

    for start in bins[:-1]:
        end = start + 4
        count = sum(start <= value <= end for value in list_points)
        counts.append(count)

    count_100_plus = sum(value >= 100 for value in list_points)
    counts.append(count_100_plus)

    labels = [f"{start}-{start + 4}" for start in bins[:-1]]
    labels.append("100+")
    print("counts: ", counts)
    percentages = [count / len(list_points) * 100 for count in counts]
    print("percentages:", percentages)
    plt.bar(labels, counts)
    plt.xlabel("Value range")
    plt.ylabel("How many values")
    plt.title("Random cards")
    plt.xticks(rotation=45)
    plt.show()
