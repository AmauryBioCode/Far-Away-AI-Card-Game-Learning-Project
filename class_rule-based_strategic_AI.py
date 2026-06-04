import random

import pickle



from data import cards_data, sanctuary_data





class AI:

    """Rule-based AI with condition strategy, point-type tie-breaks, and final-turn scoring.



    Strategy:

    1. Rounds 1 and 2:

       - play and pick the card with the biggest condition.



    2. Rounds 3 to 7:

       - play and pick resources that help complete unfinished conditions.

       - if several cards are tied, use the point-types of cards already played

         to decide what kind of card is most useful. This tie-break is not used

         on round 1 and not used on the final turn.



    3. Round 8, the last turn:

       - ignore the old condition/resource strategy for playing.

       - test every card in hand and play the one that gives the highest final score.



    Tie-break after the point-type logic:

    - choose the smallest card number higher than the last card played.

    - if impossible, choose the smallest card number.

    """



    COLOR_TO_INT = {"w": 0, "b": 1, "r": 2, "re": 2, "g": 3, "y": 4}



    # Final tie order requested by you.

    # Lower number = higher priority.

    POINT_TYPE_PRIORITY = {

        "pineapple": 0,

        "dear": 1,

        "stone": 2,

        "parchment": 3,

        "night": 4,

        "re": 5,

        "b": 6,

        "g": 7,

        "y": 8,

        "w": 9,

    }



    def __init__(self, filename="ai_memory_v4.pkl"):

        self.filename = filename

        self.history = []



        # Kept so the rest of your program still works.

        # choose_action() is deterministic/rule-based.

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



    def is_last_turn(self, game):

        return game.get_nb_turns_left() == 1



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

        """Return the missing resources for condition cards already played."""

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



            if any(missing):

                needed[0] += missing[0]

                needed[1] += missing[1]

                needed[2] += missing[2]



        return needed



    def needed_resource_score(self, player, game, card_number):

        """Score a card by how many missing resources it gives."""

        needed = self.get_unfinished_condition_need(player, game)

        card = self.get_card_data(game, card_number)

        resources = card["resources"]



        # If there is no unfinished condition, fall back to most total resources.

        if sum(needed) == 0:

            return sum(resources)



        useful_resources = 0

        for i in range(3):

            useful_resources += min(resources[i], needed[i])



        return useful_resources



    def strategic_score(self, player, game, card_number):

        """Main non-final-turn score used by the AI."""

        round_number = self.get_round_number(game)



        if round_number <= 2:

            return self.condition_score(game, card_number)



        return self.needed_resource_score(player, game, card_number)



    def final_turn_score(self, player, game, card_number):

        """Score a possible final card by simulating the final points.



        This does not modify the real player. It only tests what the score would

        be if this card were added to cards_played.

        """

        return game.cards.calculate_points_for(

            player,

            extra_played_card=card_number,

            extra_sanctuary=None,

        )



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



    def break_tie_by_card_number(self, player, available_cards, candidate_actions):

        """Apply the original numeric tie-break rule."""

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



    def point_type_categories(self, point_type):

        """Convert a points type into the thing that card wants more of.



        Examples:

        - ["pineapple", 3] wants pineapple resources.

        - ["night", 2] wants night cards.

        - ["bre", 1] wants blue or red cards.

        - ["gy", 1] wants green or yellow cards.

        """

        if point_type in ["pineapple", "dear", "stone", "parchment", "night"]:

            return [point_type]



        # A "color" card wants color diversity. We let any non-grey color help.

        if point_type == "color":

            return ["re", "b", "g", "y"]



        # A "resources" card wants sets of all resources.

        if point_type == "resources":

            return ["pineapple", "dear", "stone"]



        categories = []

        remaining = point_type



        # Your red is sometimes written as "r" in card colors and "re" in points.

        if "re" in remaining:

            categories.append("re")

            remaining = remaining.replace("re", "")



        for color in ["b", "g", "y", "w"]:

            if color in remaining:

                categories.append(color)



        return categories



    def played_point_type_stats(self, player, game):

        """Count what the already-played point cards want.



        Majority rule:

        - first compare how many played cards want each category.

        - if tied, compare total point value.

        - if still tied, use pineapple, dear, stone, parchment, night, rest.

        """

        stats = {}



        for c in player.cards_played:

            card_data = self.get_card_data(game, c)

            points = card_data.get("points")



            if points is None:

                continue



            point_type, value = points

            categories = self.point_type_categories(point_type)



            for category in categories:

                if category not in stats:

                    stats[category] = {"count": 0, "value": 0}



                stats[category]["count"] += 1

                stats[category]["value"] += value



        return stats



    def card_can_help_point_type(self, game, card_number, category):

        """Return True if this candidate card helps the selected point type."""

        card = self.get_card_data(game, card_number)

        resources = card["resources"]



        if category == "pineapple":

            return resources[2] > 0

        if category == "dear":

            return resources[1] > 0

        if category == "stone":

            return resources[0] > 0

        if category == "parchment":

            return bool(card.get("parchment", False))

        if category == "night":

            return bool(card.get("night", False))

        if category == "re":

            return card.get("color") in ["r", "re"]

        if category in ["b", "g", "y", "w"]:

            return card.get("color") == category



        return False



    def break_tie_by_played_point_types(self, player, game, available_cards, candidate_actions):

        """Use the point cards already played to break a tie.



        Example:

        - if most played point cards are ["pineapple", x], choose a tied card

          that gives pineapple.

        - if no tied card gives pineapple, try the next best point type.

        """

        stats = self.played_point_type_stats(player, game)



        if not stats:

            return None



        ranked_categories = sorted(

            stats.keys(),

            key=lambda category: (

                -stats[category]["count"],

                -stats[category]["value"],

                self.POINT_TYPE_PRIORITY.get(category, 100),

            )

        )



        for category in ranked_categories:

            matching_actions = [

                action for action in candidate_actions

                if self.card_can_help_point_type(game, available_cards[action], category)

            ]



            if matching_actions:

                return self.break_tie_by_card_number(player, available_cards, matching_actions)



        return None



    def choose_action(self, player, game, mode, available_cards=None):

        """Choose an index from available_cards.



        For mode == "play", available_cards defaults to the player's hand.

        For mode == "pick", available_cards defaults to the board.

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



        # Last turn: override the old condition/resource strategy for playing.

        # The AI tests the final points of every card in hand.

        if player.is_ai and mode == "play" and self.is_last_turn(game):

            scores = [

                self.final_turn_score(player, game, available_cards[action])

                for action in possible_actions

            ]

        else:

            scores = [

                self.strategic_score(player, game, available_cards[action])

                for action in possible_actions

            ]



        best_score = max(scores)



        candidate_actions = [

            action for action, score in zip(possible_actions, scores)

            if score == best_score

        ]



        # Every turn except last AND except the first round:

        # if the AI hesitates, use the point-type majority logic from

        # the cards already played.

        use_point_type_tie_break = (

            player.is_ai

            and not self.is_last_turn(game)

            and self.get_round_number(game) > 1

            and len(candidate_actions) > 1

        )



        if use_point_type_tie_break:

            point_type_action = self.break_tie_by_played_point_types(

                player,

                game,

                available_cards,

                candidate_actions,

            )



            if point_type_action is not None:

                best_action = point_type_action

            else:

                best_action = self.break_tie_by_card_number(player, available_cards, candidate_actions)

        else:

            best_action = self.break_tie_by_card_number(player, available_cards, candidate_actions)



        chosen_card = available_cards[best_action]

        self.history.append(self.make_key(player, game, mode, chosen_card))



        return best_action



    def learn_small_reward(self, reward):

        """Kept for compatibility."""

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



    def draw_sanctuary(self, nb_parchment, player=None, final_turn=False):

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



        if player is None:

            number = random.choice(sanctuary_drawn)

        elif final_turn and getattr(player, "is_ai", False):

            number = self.choose_best_final_sanctuary(sanctuary_drawn, player)

        else:

            number = self.choose_best_sanctuary(sanctuary_drawn, player)



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



        self.total_resources = cards.count_resources_sanctuary(self.sanctuary_in_hand)

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

    

    def draw_phase(self, first_choice_index, second_choice_index):

        first_card = self.cards.cards_on_board.pop(first_choice_index)

        self.first_picker.cards_in_hand.append(first_card)



        second_card = self.cards.cards_on_board.pop(second_choice_index)

        self.second_picker.cards_in_hand.append(second_card)



        self.cards.refill_board()



        return first_card, second_card

