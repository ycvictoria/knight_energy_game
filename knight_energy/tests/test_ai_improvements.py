"""Tests de heurística alcanzable y orden de movimientos."""

import unittest

from src.ai.heuristics import (
    W_REACHABLE_STARS,
    _reachable_star_value,
    eval_state,
)
from src.ai.move_ordering import sort_moves_best_first
from src.config import MAX, MIN
from src.models.state import GameState


class ReachableHeuristicTests(unittest.TestCase):
    def test_unreachable_star_not_counted(self):
        """Moneda lejana no infla f4 si ninguno puede capturarla en un salto."""
        state = GameState(generate_random=False)
        state.board[7][7] = {"type": "star", "value": 9}
        state.stars_count = 1

        self.assertEqual(_reachable_star_value(state, MAX), 0)
        self.assertEqual(_reachable_star_value(state, MIN), 0)

    def test_reachable_star_counts_for_one_player(self):
        state = GameState(generate_random=False)
        state.white_pos = (0, 0)
        state.board[2][1] = {"type": "star", "value": 5}
        state.stars_count = 1

        self.assertEqual(_reachable_star_value(state, MAX), 5)
        self.assertEqual(_reachable_star_value(state, MIN), 0)

    def test_eval_prefers_reachable_over_distant_star(self):
        """Posición con moneda al alcance debe evaluar mejor que moneda lejana."""
        near = GameState(generate_random=False)
        near.white_pos = (0, 0)
        near.board[2][1] = {"type": "star", "value": 6}
        near.stars_count = 1

        far = GameState(generate_random=False)
        far.white_pos = (0, 0)
        far.board[7][7] = {"type": "star", "value": 9}
        far.stars_count = 1

        self.assertGreater(eval_state(near), eval_state(far))
        self.assertAlmostEqual(eval_state(near) - eval_state(far), W_REACHABLE_STARS * 6)


class MoveOrderingTests(unittest.TestCase):
    def test_star_before_empty_square(self):
        state = GameState(generate_random=False)
        state.turn = MAX
        state.white_pos = (0, 0)
        state.board[2][1] = {"type": "star", "value": 4}
        empty = (1, 2)
        star = (2, 1)
        actions = [empty, star]

        ordered = sort_moves_best_first(state, actions)
        self.assertEqual(ordered[0], star)

    def test_higher_star_before_lower(self):
        state = GameState(generate_random=False)
        state.turn = MAX
        state.white_pos = (3, 3)
        state.board[5][4] = {"type": "star", "value": 3}
        state.board[5][2] = {"type": "star", "value": 8}
        low = (5, 4)
        high = (5, 2)
        actions = [low, high]

        ordered = sort_moves_best_first(state, actions)
        self.assertEqual(ordered[0], high)


if __name__ == "__main__":
    unittest.main()
