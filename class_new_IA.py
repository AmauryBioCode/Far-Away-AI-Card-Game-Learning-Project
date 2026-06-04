import random
import pickle
from data import cards_data, sanctuary_data





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

        """Initialize the link-learning AI and load any previously saved memory.



        Sets up the learning hyper-parameters (learning rate, epsilon and its

        decay, the context-link weights and bonuses, and the useless-choice

        penalty) together with the three tables that make up the AI's memory:

        the state-action Q-table, the per-card-type values and the contextual

        link values. Any memory previously written to disk is then loaded.



        Args:

            filename: Path of the pickle file used to load and save memory.

        """

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



        # Context links are now ADDED, not averaged.

        # This means a card with 3 useful links can be better than a card with

        # only 1 useful link.

        self.context_link_weight = 1.00



        # Extra reward multiplier when a chosen card had several useful context

        # links at the moment it was chosen.

        # Example: 4 useful links -> reward * (1 + 4 * 0.12) = reward * 1.48

        # The cap prevents huge explosions late in the game.

        self.multi_link_bonus_per_link = 0.12

        self.multi_link_bonus_cap = 1.00

        self.rewarded_context_link_count = 0



        # Penalty is now conservative: it applies ONLY when the card/sanctuary

        # created no useful context link at all after the first turn, and only

        # if it also received no positive final reward.

        self.useless_choice_penalty = -0.10

        self.useless_penalty_count = 0



        self.epsilon = 1.0

        self.load_memory()



    def load_memory(self):

        """Load the AI's memory (epsilon and value tables) from the pickle file.



        If the file does not exist yet, start fresh with empty value tables and

        a fully exploratory epsilon of 1.0.

        """

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

        """Save the AI's current memory to the pickle file.



        Persists epsilon, the Q-table, the per-card values and the link values

        so that learning can resume in a later run.

        """

        data = {

            "epsilon": self.epsilon,

            "q_table": self.q_table,

            "card_values": self.card_values,

            "link_values": self.link_values,

        }

        with open(self.filename, "wb") as file:

            pickle.dump(data, file)



    def update_epsilon(self):

        """Decay the exploration rate by one step, clamped at the minimum.



        Multiplies epsilon by the decay factor unless it has already reached

        epsilon_min, in which case it is left at the minimum.

        """

        if self.epsilon > self.epsilon_min:

            self.epsilon *= self.epsilon_decay

            if self.epsilon < self.epsilon_min:

                self.epsilon = self.epsilon_min



    def get_card_data(self, game, card_number):

        """Return the data dictionary for a card, normal or sanctuary.



        Looks the card up in the normal card table first and falls back to the

        sanctuary table (keyed by string) if it is not found there.



        Args:

            game: The current game, used to reach the card tables.

            card_number: The card identifier to look up.



        Returns:

            The card's data dictionary (resources, color, points, etc.).

        """

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

        """Build the Q-table key for a (state, action) pair.



        Combines the player's current state, the mode ("play" or "pick") and the

        card's feature signature, so the AI learns about card types in context

        rather than about fixed board positions.



        Returns:

            A hashable tuple usable as a key in the Q-table.

        """

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



    def context_link_count_bonus(self, context_link_count):

        """Return a small multiplier bonus for choices with many useful links.



        More useful links should be better, but the bonus is capped so the AI

        does not overvalue one card only because many context cards exist late

        in the game.

        """

        if context_link_count <= 0:

            return 0.0



        return min(

            self.multi_link_bonus_cap,

            context_link_count * self.multi_link_bonus_per_link,

        )



    def has_relevant_context_to_help(self, player, game):

        """Return True when there is already something useful to support.



        The useless-choice penalty should not apply just because there are no

        possible links yet. It applies only when the AI already has a played card

        or sanctuary card that could be supported:

            - an unfinished condition card

            - a scoring card based on resources, color, night, or parchment



        Fixed-point cards like ["points", 5] are ignored because they do not

        need support from another card.

        """

        if game.get_nb_turns_left() == 8:

            # First turn: do not punish exploration.

            return False



        current_resources = self.current_resource_totals(player, game)

        context_cards = player.cards_played + player.sanctuary_in_hand



        for existing_card in context_cards:

            existing_data = self.get_card_data(game, existing_card)



            condition = existing_data.get("condition")

            if condition is not None:

                missing = [

                    max(0, condition[i] - current_resources[i])

                    for i in range(3)

                ]

                if any(missing):

                    return True



            points = existing_data.get("points")

            if points is not None and points[0] != "points":

                return True



        return False



    def fixed_points_card_already_satisfied_by_sanctuaries(self, player, game, card_number):

        """Return True for fixed-points played cards already unlocked by sanctuaries.



        This prevents the no-link penalty from hitting a card like:

            condition = [...]

            points = ["points", x]



        when the condition is already fulfilled by sanctuary cards alone.

        Such a card may create no context link, because ["points", x] does not

        need a support category like night/parchment/color/resource, but it is

        still a good play if the sanctuary cards already satisfy its condition.

        """

        card_data = self.get_card_data(game, card_number)

        points = card_data.get("points")

        condition = card_data.get("condition")



        if points is None or points[0] != "points":

            return False



        if condition is None:

            return False



        sanctuary_resources = game.cards.count_resources_sanctuary(

            player.sanctuary_in_hand

        )["resources"]



        return all(

            sanctuary_resources[i] >= condition[i]

            for i in range(3)

        )



    def should_apply_useless_penalty(self, player, game, mode, card_number, context_link_keys):

        """Return True when the chosen card deserves the small no-link penalty.



        This is checked at the moment the AI chooses a card or sanctuary.

        The penalty applies only after the first turn, only if there was already

        a condition/point card to support, and only if the chosen card created no

        condition link and no point-type link.



        Exception:

        - when the AI PLAYS a fixed-points card whose condition is already

          fulfilled by sanctuary resources, do not penalize it. The card does

          not need a context link because its points are already unlocked.

        """

        if (

            mode == "play"

            and self.fixed_points_card_already_satisfied_by_sanctuaries(

                player,

                game,

                card_number,

            )

        ):

            return False



        return (

            game.get_nb_turns_left() < 8

            and self.has_relevant_context_to_help(player, game)

            and len(context_link_keys) == 0

        )



    def context_link_value(self, player, game, mode, card_number):

        """Estimated value of learned links between current context and candidate.



        Important change: this is now a SUM, not an average.

        So if a candidate supports several already-played cards, all those

        learned links increase the candidate value.

        """

        keys = self.context_link_keys(player, game, mode, card_number)



        if not keys:

            return 0.0



        return sum(self.link_values.get(key, 0.0) for key in keys)



    def estimated_value(self, player, game, mode, card_number):

        """Estimate the total value of choosing a card in the current state.



        Sums three learned signals: the state-action Q-value, the value of the

        card type on its own, and the weighted value of the contextual links the

        card would create with cards the player already has.



        Returns:

            The combined estimated value as a float.

        """

        state_key = self.make_key(player, game, mode, card_number)

        feature_key = (mode, self.card_features(game, card_number))



        base_value = self.q_table.get(state_key, 0.0)

        card_value = self.card_values.get(feature_key, 0.0)

        link_value = self.context_link_value(player, game, mode, card_number)



        return base_value + card_value + self.context_link_weight * link_value



    def remember_choice(self, player, game, mode, card_number):

        """Record a choice in the history so it can be rewarded after the game.



        Stores the state key, the feature key and the context links that existed

        at the moment of the choice, plus a flag marking the choice as a candidate

        for the conservative "useless choice" penalty (only applied later if the

        card never earns a positive final reward).

        """

        context_keys = self.context_link_keys(player, game, mode, card_number)

        no_link_penalty_candidate = self.should_apply_useless_penalty(

            player,

            game,

            mode,

            card_number,

            context_keys,

        )



        self.history.append({

            "card": str(card_number),

            "mode": mode,

            "state_key": self.make_key(player, game, mode, card_number),

            "feature_key": (mode, self.card_features(game, card_number)),



            # Context links that existed at the moment of the choice.

            # If the card later proves useful, having more links gives a larger

            # reward and all those links learn positive value.

            "context_link_keys": context_keys,



            # Conservative penalty flag. It is applied later ONLY if the card

            # got no positive final reward. A useful card is never punished just

            # because it did not help every possible link.

            "no_link_penalty_candidate": no_link_penalty_candidate,

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

        """Accumulate a positive reward for a card in the rewards dictionary.



        Non-positive amounts are ignored. The card number is stored as a string

        key and the amount is added to any reward the card already has.

        """

        if amount <= 0:

            return

        key = str(card_number)

        rewards[key] = rewards.get(key, 0.0) + float(amount)



    def all_player_cards(self, player):

        """Return a combined copy of the player's played cards and sanctuary cards."""

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

        """List the player's cards that supply a given resource.



        Args:

            player: The player whose cards are inspected.

            cards: The Cards object used to look up card data.

            resource_index: 0 for stone, 1 for deer, 2 for pineapple.



        Returns:

            A list of (card_number, amount) tuples for every card that provides

            at least one unit of that resource.

        """

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

        """Expand a scoring point-type into the card categories that feed it.



        For example "resources" maps to the three resource types, "color" maps to

        the four scoring colors, and a combined color code such as "gre" is split

        into its individual color categories.



        Returns:

            A list of category strings relevant to that point type.

        """

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

        """Return whether a card's color counts toward a color category.



        Treats "re" as matching both plain red ("r") and red-counting ("re")

        cards; every other category requires an exact color match.

        """

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

            positive_reward = card_rewards.get(entry["card"], 0.0)

            context_keys = entry.get("context_link_keys", [])

            context_link_count = len(context_keys)



            if positive_reward > 0:

                # More useful links -> more reward.

                # This is the important change: a card that supported several

                # conditions/point cards gets a stronger learning signal than a

                # card that supported only one.

                link_bonus = self.context_link_count_bonus(context_link_count)

                reward = positive_reward * (1.0 + link_bonus)



                if context_link_count > 0:

                    self.rewarded_context_link_count += context_link_count



            elif entry.get("no_link_penalty_candidate", False):

                # Small penalty only for choices that helped nothing and also

                # ended the game with no positive link reward.

                reward = self.useless_choice_penalty

                self.useless_penalty_count += 1



            else:

                reward = 0.0



            old_q = self.q_table.get(entry["state_key"], 0.0)

            self.q_table[entry["state_key"]] = old_q + self.learning_rate * (reward - old_q)



            old_card_value = self.card_values.get(entry["feature_key"], 0.0)

            self.card_values[entry["feature_key"]] = old_card_value + self.learning_rate * (reward - old_card_value)



            # Learn whether this candidate card was good in the context where

            # it was chosen. Each useful context link receives the same boosted

            # reward. Because future link values are summed, more learned links

            # make a candidate more attractive.

            for context_key in context_keys:

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

        """Initialize the deck from the card and sanctuary data.



        Builds the lookup tables and the draw packs for both normal cards and

        sanctuary cards, and starts with an empty board.

        """

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

        """Return whether the given card carries a parchment symbol.



        Args:

            number: The card or sanctuary identifier.

            type: "card" to look in the normal card table, "sanctuary" for the

                sanctuary table.



        Returns:

            True if that card has a parchment, otherwise False.

        """

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

        """Sum the resources, colors and night symbols of some sanctuary cards.



        Args:

            sanctuary_in_hand: The sanctuary card numbers to total up.



        Returns:

            A dict with the combined "resources" list, the list of "color" values

            and the "night" count.

        """

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

        """Return the resource contribution of a single card's data dictionary.



        Returns:

            A dict with a copy of the card's "resources", its "color" as a

            one-item list, and "night" set to 1 for a night card else 0.

        """

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

        """Compute the points scored by one card given the current totals.



        Handles every scoring rule: fixed points, points per resource type, per

        color set, per night card, per color combination, per parchment, and sets

        of three different resources. A card whose resource condition is not met

        scores zero.



        Args:

            c: The card or sanctuary identifier being scored.

            total_resources: The accumulated resources, colors and night count so

                far (cards are scored in reverse play order).

            nb_parchment: The player's current parchment count.



        Returns:

            The number of points the card scores.

        """

        

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

        """Build the compact state tuple the AI uses as a Q-table key.



        The state captures the turns left, the player's current resource totals,

        and how many cards in hand carry a condition or award points.



        Returns:

            A tuple (turns_left, resources, hand_has_condition, hand_has_points).

        """

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

        """Return the total number of resources the player currently controls.



        Sums the resources from the player's sanctuary cards and played cards

        across all three resource types.

        """

        resources = game.cards.count_resources_sanctuary(self.sanctuary_in_hand)



        for c in self.cards_played:

            card_data = game.cards.card_info[c]

            resources["resources"][0] += card_data["resources"][0]

            resources["resources"][1] += card_data["resources"][1]

            resources["resources"][2] += card_data["resources"][2]

        

        return resources["resources"][0] + resources["resources"][1] + resources["resources"][2]



    def count_completed_conditions(self, cards, new_card=None, action="played"):

        """Count how many of the player's condition cards are currently satisfied.



        When evaluating a potential pick, the candidate card is temporarily added

        before counting and removed again afterwards, so the player's real state

        is left unchanged.



        Args:

            cards: The Cards object used to look up card data.

            new_card: Optional card to test as if it had just been taken.

            action: "picked" to include new_card in the evaluation, otherwise the

                card is ignored.



        Returns:

            The number of played condition cards whose resource requirement is met.

        """

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

        """Compute and store the player's final score for the game.



        Accumulates resources, colors and night symbols across the sanctuary

        cards and played cards (scored in reverse play order) and sums the points

        of every card. The result is stored in self.points and self.total_resources.



        Returns:

            The player's total points.

        """

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

        """Decrease the number of turns left by one."""

        self.turns_left = self.turns_left - 1

        #print(self.turns_left)



    def switch_player(self):

        """Switch the current player to the other player."""

        if self.current_player == self.player1:

            self.current_player = self.player2

        else:

            self.current_player = self.player1



    def play_phase(self, p1_card_index, p2_card_index):

        """Play one card from each player and decide the pick order.



        Each player plays the card at the given index. The player who played the

        lower-numbered card becomes the first picker for the draw phase; the other

        becomes the second picker.



        Args:

            p1_card_index: Index of the card player 1 plays from hand.

            p2_card_index: Index of the card player 2 plays from hand.

        """

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

        """Resolve the draw: each picker takes a card and the board is refilled.



        The first picker takes the card at first_choice_index, then the second

        picker takes the card at second_choice_index from the board as it stands

        after the first card was removed. The board is then refilled.



        Args:

            first_choice_index: Board index chosen by the first picker.

            second_choice_index: Board index chosen by the second picker, relative

                to the board after the first card is removed.



        Returns:

            A tuple (first_card, second_card) of the two cards taken.

        """

        first_card = self.cards.cards_on_board.pop(first_choice_index)

        self.first_picker.cards_in_hand.append(first_card)



        second_card = self.cards.cards_on_board.pop(second_choice_index)

        self.second_picker.cards_in_hand.append(second_card)



        self.cards.refill_board()



        return first_card, second_card