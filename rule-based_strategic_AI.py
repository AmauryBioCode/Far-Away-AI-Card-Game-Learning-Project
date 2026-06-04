import random

import numpy as np

import matplotlib.pyplot as plt

import importlib



from data import cards_data, sanctuary_data



# The class file name contains hyphens, which are not valid in a normal

# `import` statement, so the classes are loaded with importlib instead.

_classes = importlib.import_module("class_rule-based_strategic_AI")

AI = _classes.AI

Cards = _classes.Cards

Player = _classes.Player

Game = _classes.Game



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
