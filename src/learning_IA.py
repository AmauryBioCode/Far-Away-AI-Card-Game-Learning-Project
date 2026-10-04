"""Train the learning AI (player 1) against a random opponent (player 2).

All outputs (training log, summary, raw scores and plots) are written to
results/learning_IA/.
"""

import json
import logging
import random
from dataclasses import dataclass, field
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from class_learning_IA import AI, Game

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
TOTAL_GAMES = 200_000
REPORT_EVERY = 10_000
BIN_WIDTH = 5
MAX_SCORE_BIN = 100  # scores >= this value go into the last bin ("100+")

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results" / "learning_IA"
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------
@dataclass
class TrainingStats:
    points_1: list = field(default_factory=list)
    points_2: list = field(default_factory=list)
    resources_1: float = 0
    resources_2: float = 0
    # Win/draw/loss counters for the current reporting window only
    wins: int = 0
    draws: int = 0
    losses: int = 0

    def record_game(self, points_1, points_2, resources_1, resources_2):
        self.points_1.append(points_1)
        self.points_2.append(points_2)
        self.resources_1 += resources_1
        self.resources_2 += resources_2

        if points_1 > points_2:
            self.wins += 1
        elif points_1 == points_2:
            self.draws += 1
        else:
            self.losses += 1

    def window_rates(self):
        """Return win, draw and loss percentages for the current window."""
        total = self.wins + self.draws + self.losses
        return tuple(100 * n / total for n in (self.wins, self.draws, self.losses))

    def reset_window(self):
        self.wins = self.draws = self.losses = 0


# ---------------------------------------------------------------------------
# Game loop
# ---------------------------------------------------------------------------
def play_phase(game, ai):
    """Player 1 (AI) and player 2 (random) each play a card from their hand."""
    p1_index = ai.choose_action(game.player1, game, "play")
    p2_index = random.randrange(len(game.player2.cards_in_hand))
    game.play_phase(p1_index, p2_index)


def pick_phase(game, ai):
    """Both players pick a card from the board.

    The second picker chooses from the board AFTER the first picker's card has
    been removed, so second_choice is an index into that reduced board, which
    is exactly what draw_phase() expects.
    """
    board = game.cards.cards_on_board

    if game.first_picker == game.player1:
        first_choice = ai.choose_action(game.player1, game, "pick")
        second_choice = random.randrange(len(board) - 1)
    else:
        first_choice = random.randrange(len(board))
        remaining_board = board[:first_choice] + board[first_choice + 1:]
        second_choice = ai.choose_action(game.player1, game, "pick",
                                         available_cards=remaining_board)

    game.draw_phase(first_choice, second_choice)


def play_game(ai, stats):
    """Play one full game, record the result and let the AI learn from it."""
    game = Game()
    game.reset()
    game.ai = ai

    while game.get_nb_turns_left() > 0:
        game.cards.refill_board()
        play_phase(game, ai)
        pick_phase(game, ai)
        game.set_turns()

    stats.record_game(game.player1.calculate_points(game.cards),
                      game.player2.calculate_points(game.cards),
                      game.player1.get_total_ressources(game),
                      game.player2.get_total_ressources(game))

    # Learn from the links created by player 1's cards, not from the score difference.
    ai.learn_from_links(game.player1, game.cards)
    ai.update_epsilon()


def log_progress(nb_game, total_games, ai, stats):
    win, draw, loss = stats.window_rates()
    logger.info(f"{nb_game / total_games:6.1%} | "
                f"epsilon: {ai.epsilon:.4f} | "
                f"resources_1: {stats.resources_1 / nb_game:.2f} | "
                f"resources_2: {stats.resources_2 / nb_game:.2f} | "
                f"Q-table: {len(ai.q_table)} | "
                f"card-values: {len(ai.card_values)} | "
                f"link-values: {len(ai.link_values)} | "
                f"rewarded-links: {ai.rewarded_context_link_count} | "
                f"no-link penalties: {ai.useless_penalty_count} | "
                f"Win: {win:.1f}% Draw: {draw:.1f}% Loss: {loss:.1f}%")


def train(ai, total_games):
    stats = TrainingStats()
    for nb_game in range(1, total_games + 1):
        play_game(ai, stats)
        if nb_game % REPORT_EVERY == 0:
            log_progress(nb_game, total_games, ai, stats)
            stats.reset_window()
    return stats


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
def score_distribution(points):
    """Count scores in bins of BIN_WIDTH (0-4, 5-9, ...) plus a final '100+' bin."""
    edges = np.arange(0, MAX_SCORE_BIN + 2 * BIN_WIDTH, BIN_WIDTH)  # 0, 5, ..., 105
    counts, _ = np.histogram(np.minimum(points, MAX_SCORE_BIN), bins=edges)
    labels = [f"{s}-{s + BIN_WIDTH - 1}" for s in edges[:-2]] + [f"{MAX_SCORE_BIN}+"]
    percentages = counts / len(points) * 100
    return labels, counts, percentages


def summarize(points):
    points = np.asarray(points)
    labels, counts, percentages = score_distribution(points)
    distribution = {label: {"count": int(count), "percentage": round(float(pct), 2)}
                    for label, count, pct in zip(labels, counts, percentages)}
    return {"mean": float(points.mean()),
            "median": float(np.median(points)),
            "min": points.min().item(),
            "max": points.max().item(),
            "distribution": distribution}


def save_histogram(points, title, path):
    labels, counts, _ = score_distribution(points)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(labels, counts)
    ax.set_xlabel("Score range")
    ax.set_ylabel("Number of games")
    ax.set_title(title)
    ax.tick_params(axis="x", labelrotation=45)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def save_results(ai, stats, results_dir):
    summary = {"games": len(stats.points_1),
               "epsilon": float(ai.epsilon),
               "memory_size": len(ai.q_table),
               "player_1": summarize(stats.points_1),
               "player_2": summarize(stats.points_2)}
    with open(results_dir / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    np.savetxt(results_dir / "scores.csv",
               np.column_stack([stats.points_1, stats.points_2]),
               delimiter=",", header="player_1,player_2", comments="", fmt="%g")

    for player, points in ((1, stats.points_1), (2, stats.points_2)):
        save_histogram(points, f"Player {player} score distribution",
                       results_dir / f"score_distribution_player{player}.png")

    logger.info(f"\nepsilon: {summary['epsilon']:.4f} | memory size: {summary['memory_size']}")
    for player in ("player_1", "player_2"):
        s = summary[player]
        logger.info(f"{player}: mean {s['mean']:.2f} | median {s['median']:.1f} | "
                    f"min {s['min']} | max {s['max']}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def setup_logging(log_file):
    """Print messages to the console and also write them to log_file."""
    handlers = [logging.StreamHandler(),
                logging.FileHandler(log_file, mode="w", encoding="utf-8")]
    logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=handlers)



RESULTS_DIR.mkdir(parents=True, exist_ok=True)
setup_logging(RESULTS_DIR / "training_log.txt")

ai = AI(filename=RESULTS_DIR / "ai_memory_link_learning.pkl")
stats = train(ai, TOTAL_GAMES)
ai.save_memory()
save_results(ai, stats, RESULTS_DIR)

logger.info(f"\nResults saved to {RESULTS_DIR}")