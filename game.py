import random

#[x,x,x] = [stone, dear, pineapple]
#color: grey (w), blue (b), red (r), green (g) j'ai choisi w comme white pour gris car g est déjà pris par green
# ["points", x] (x points),  ["night", x] (x points par carte nuit),  ["reb", x] (x point par carte rouge et bleu (re = red, b = blue, g = green, y = yellow, w = gray),  
# ["color", x] (x points pour chaque 4 couleurs différentes), ["stone", x] (x points par pierre), ["parchment", x], 
# ["ressources", x] (x points pour chaque 3 ressources différentes)
cards_data= {
    "0": {"ressources": [1,1,1], "parchment": False, "color": 'w', "night": False, "condition": None, "points": None},
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
    69: {"resources": [0, 0, 0], "parchment": True, "color": "r", "night": False, "condition": None, "points": ["ressources", 7]},
    70: {"resources": [0, 0, 0], "parchment": True, "color": "w", "night": False, "condition": None, "points": ["points", 6]},
    71: {"resources": [1, 0, 0], "parchment": False, "color": "g", "night": True, "condition": None, "points": ["ressources", 7]},
    72: {"resources": [0, 0, 0], "parchment": True, "color": "w", "night": True, "condition": [0, 5, 0], "points": 26},
    73: {"resources": [0, 1, 0], "parchment": False, "color": "y", "night": True, "condition": [0, 0, 4], "points": ["w", 5]},
    74: {"resources": [0, 0, 1], "parchment": False, "color": "w", "night": True, "condition": None, "points": ["ressources", 7]},
    75: {"resources": [0, 0, 0], "parchment": True, "color": "b", "night": True, "condition": [6, 0, 0], "points": ["points", 28]},
    76: {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": True, "condition": [2, 2, 2], "points": ["w", 4]},
}

sanctuary_data = {
 "a": {"resources": [0, 1, 0], "parchment": False, "color": "r", "night": False, "points": None},
    "b": {"resources": [0, 1, 0], "parchment": False, "color": "g", "night": False, "points": None},
    "c": {"resources": [0, 1, 0], "parchment": False, "color": "b", "night": False, "points": None},
    "d": {"resources": [0, 1, 0], "parchment": False, "color": "w", "night": False, "points": ["w", 1]},
    "e": {"resources": [0, 1, 0], "parchment": False, "color": "w", "night": False, "points": ["dear", 1]},
    "f": {"resources": [0, 1, 0], "parchment": False, "color": "w", "night": True, "points": None},
    "g": {"resources": [0, 1, 0], "parchment": False, "color": "w", "night": False, "points": ["parchment, 1"]},
    "h": {"resources": [0, 1, 0], "parchment": True, "color": "w", "night": False, "points": None},
    "i": {"resources": [1, 0, 0], "parchment": False, "color": "r", "night": False, "points": None},
    "j": {"resources": [1, 0, 0], "parchment": False, "color": "b", "night": False, "points": None},
    "k": {"resources": [1, 0, 0], "parchment": False, "color": "g", "night": False, "points": None},
    "l": {"resources": [1, 0, 0], "parchment": False, "color": "y", "night": False, "points": None},
    "m": {"resources": [1, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["night", 1]},
    "n": {"resources": [1, 0, 0], "parchment": False, "color": "w", "night": True, "points": None},
    "o": {"resources": [1, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["parchment, 1"]},
    "p": {"resources": [1, 0, 0], "parchment": True, "color": "w", "night": False, "points": None},
    "q": {"resources": [1, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["stone", 1]},
    "r": {"resources": [2, 0, 0], "parchment": False, "color": "w", "night": False, "points": None},
    "s": {"resources": [0, 0, 1], "parchment": False, "color": "r", "night": False, "points": None},
    "t": {"resources": [0, 0, 1], "parchment": False, "color": "b", "night": False, "points": None},
    "u": {"resources": [0, 0, 1], "parchment": False, "color": "w", "night": False, "points": ["w", 1]},
    "v": {"resources": [0, 0, 1], "parchment": False, "color": "w", "night": False, "points": ["pineapple", 1]},
    "w": {"resources": [0, 0, 1], "parchment": True, "color": "w", "night": False, "points": None},
    "x": {"resources": [0, 0, 1], "parchment": False, "color": "w", "night": True, "points": None},
    "y": {"resources": [0, 0, 0], "parchment": True, "color": "b", "night": False, "points": None},
    "z": {"resources": [0, 0, 0], "parchment": True, "color": "y", "night": False, "points": None},
    "aa": {"resources": [0, 0, 0], "parchment": True, "color": "g", "night": False, "points": None},
    "ab": {"resources": [0, 0, 0], "parchment": True, "color": "w", "night": False, "points": ["color", 4]},
    "ac": {"resources": [0, 0, 0], "parchment": True, "color": "w", "night": False, "points": ["parchment", 1]},
    "ad": {"resources": [0, 0, 0], "parchment": True, "color": "w", "night": False, "points": ["ressources", 3]},
    "ae": {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": True, "points": ["w", 1]},
    "af": {"resources": [0, 0, 0], "parchment": False, "color": "r", "night": True, "points": None},
    "ag": {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": False, "points": ["y", 1]},
    "ah": {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": False, "points": ["parchment", 1]},
    "ai": {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": False, "points": ["color", 4]},
    "aj": {"resources": [0, 0, 0], "parchment": False, "color": "g", "night": False, "points": ["night", 1]},
    "ak": {"resources": [0, 0, 0], "parchment": False, "color": "g", "night": False, "points": ["ressources", 3]},
    "al": {"resources": [0, 0, 0], "parchment": False, "color": "g", "night": False, "points": ["g", 1]},
    "am": {"resources": [0, 0, 0], "parchment": False, "color": "b", "night": False, "points": ["w", 2]},
    "an": {"resources": [0, 0, 0], "parchment": False, "color": "b", "night": False, "points": ["b", 1]},
    "ao": {"resources": [0, 0, 0], "parchment": False, "color": "r", "night": False, "points": ["re", 1]},
    "ap": {"resources": [0, 0, 0], "parchment": False, "color": "r", "night": False, "points": ["ressources", 3]},
    "aq": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["yre", 1]},
    "ar": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["stone", 2]},
    "as": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["bre", 1]},
    "aq": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["yg", 1]},
    "ar": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["gb", 1]},
    "as": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["gre", 1]},
    "aq": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["yb", 1]},
    "ar": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["parchment", 2]},
    "as": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["pineapple", 2]},
    "aq": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["dear", 2]},
    "ar": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["points", 5]},
}

class Cards:
    """Manage the deck of available cards and the cards currently on the board."""
    def __init__(self):
        self.card_pack = list(cards_data.keys())
        self.cards_on_board = []

    def card_taken(self, number):
        """Remove a card from the card pack after it has been drawn or used.

        Args:
            number: The card number to remove from the card pack."""
        self.card_pack.remove(number)

    def draw_card(self):
        """Draw a random card from the card pack and remove it from the pack.

        Returns:
            The number of the card that was drawn."""
        number = random.choice(self.card_pack)
        self.card_taken(number)
        return number

    def refill_board(self):
        """Refill the board until it contains 3 cards or the card pack is empty."""
        while len(self.cards_on_board) < 3 and len(self.card_pack) > 0:
            self.cards_on_board.append(self.draw_card())


class Player:
    """Represent a player with cards in hand and cards already played."""
    def __init__(self, cards):
        """Initialize a player with 3 cards drawn from the given card deck.

        Args:
            cards: A Cards object used to draw the player's starting hand."""
        self.cards_in_hand = []
        self.cards_played = []

        while len(self.cards_in_hand) < 3:
            self.cards_in_hand.append(cards.draw_card())

    def play_card(self, index):
        """Play a card from the player's hand.

        The selected card is removed from the player's hand and added to the
        list of cards the player has already played.

        Args:
            index: The index of the card to play in the player's hand.

        Returns:
            The number of the card that was played."""
        number = self.cards_in_hand.pop(index)
        self.cards_played.append(number)
        return number


class Game:
    """Manage the overall game state, including players, turns, and cards."""
    def reset(self):
        """Reset the game to its initial state.

        Creates a new card deck, initializes two players, sets player 1 as the
        current player, and resets the number of turns left.

        Returns:
            The current game state."""
        self.cards = Cards()
        self.player1 = Player(self.cards)
        self.player2 = Player(self.cards)
        self.current_player = self.player1
        self.turns_left = 8
        return self.get_state()
    
    def get_nb_turns_left(self):
        """Return the number of turns left in the game.

        Returns:
            The number of turns remaining."""
        return self.turns_left

    def switch_player(self):
        """Switch the current player to the other player."""
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1


if __name__ == "__main__":
    game = Game()
    state = game.reset()

    while game.get_nb_turns_left() > 8:
        game.cards.refill_board()
    