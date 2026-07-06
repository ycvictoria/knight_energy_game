"""
Mejora 2 — Orden de movimientos (move ordering).

Por qué:
  Minimax da el mismo resultado sin importar el orden, pero alfa-beta poda antes
  si explora primero las jugadas buenas (capturas, rayos con poca energía).

Qué hace sort_moves_best_first:
  1. Monedas: mayor valor primero (9 antes que 2)
  2. Rayos: prioridad extra si energía <= 3
  3. Casillas vacías: al final
"""

from src.game_logic.engine import get_player_energy


def _move_importance_score(state, move):
    """Puntaje más alto = probar este movimiento antes en el árbol minimax."""
    row, col = move
    cell = state.board[row][col]
    if cell is None:
        return 0

    if cell["type"] == "star":
        return 1000 + cell["value"]

    if cell["type"] == "lightning":
        energy = get_player_energy(state, state.turn)
        priority = 100 + cell["value"]
        if energy <= 3:
            priority += 50  # urgente recargar
        return priority

    return 0


def sort_moves_best_first(state, moves):
    """Lista de movimientos ordenada: los más prometedores primero (mejor poda)."""
    if len(moves) <= 1:
        return moves
    return sorted(moves, key=lambda move: _move_importance_score(state, move), reverse=True)
