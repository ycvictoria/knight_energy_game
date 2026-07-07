"""
Orden de movimientos (move ordering) para mejorar la poda alfa-beta.

Explora primero capturas valiosas; con poca energía prioriza rayos sobre monedas pequeñas.
"""

from src.ai.heuristics import LOW_ENERGY_THRESHOLD
from src.game_logic.engine import get_player_energy

LOW_ENERGY_ORDERING = 4  # por debajo de esto, rayos antes que monedas pequeñas


def _move_importance_score(state, move):
    """Puntaje más alto = probar este movimiento antes en el árbol minimax."""
    row, col = move
    cell = state.board[row][col]
    if cell is None:
        return 0

    energy = get_player_energy(state, state.turn)

    if cell["type"] == "lightning":
        if energy <= LOW_ENERGY_ORDERING:
            return 1250 + cell["value"]
        priority = 100 + cell["value"]
        if energy <= LOW_ENERGY_THRESHOLD:
            priority += 80
        return priority

    if cell["type"] == "star":
        return 1000 + cell["value"]

    return 0


def sort_moves_best_first(state, moves):
    """Lista de movimientos ordenada: los más prometedores primero (mejor poda)."""
    if len(moves) <= 1:
        return moves
    return sorted(moves, key=lambda move: _move_importance_score(state, move), reverse=True)
