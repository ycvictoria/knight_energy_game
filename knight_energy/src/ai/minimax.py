"""
Algoritmo minimax con poda alfa-beta.

Glosario rápido:
  - get_moves_for_current_turn: casillas legales para quien tiene el turno
  - apply_move: simula un salto y devuelve el tablero después
  - reached_search_limit: True = no seguir profundizando; evaluar con heurística
  - sort_moves_best_first: ordena movimientos para que alfa-beta corte antes
"""

from src.ai.heuristics import utility
from src.ai.move_ordering import sort_moves_best_first
from src.game_logic.engine import apply_move, apply_penalty, get_moves_for_current_turn


def reached_search_limit(state, depth, max_depth):
    """
    ¿Parar de expandir el árbol aquí?
    Sí si llegamos a la profundidad máxima o la partida ya terminó.
    """
    return depth >= max_depth or state.is_terminal()


def _list_moves_to_explore(state, moves):
    """Movimientos ordenados: capturas y rayos primero (mejor poda alfa-beta)."""
    return sort_moves_best_first(state, moves)


def max_value(state, alpha, beta, depth, max_depth):
    """Nodo MAX con poda beta."""
    if reached_search_limit(state, depth, max_depth):
        return utility(state)

    moves = get_moves_for_current_turn(state)
    if not moves:
        penalized = apply_penalty(state)
        return min_value(penalized, alpha, beta, depth + 1, max_depth)

    value = float("-inf")
    for move in _list_moves_to_explore(state, moves):
        next_state = apply_move(state, move)
        value = max(value, min_value(next_state, alpha, beta, depth + 1, max_depth))
        if value >= beta:
            return value
        alpha = max(alpha, value)
    return value


def min_value(state, alpha, beta, depth, max_depth):
    """Nodo MIN con poda alpha."""
    if reached_search_limit(state, depth, max_depth):
        return utility(state)

    moves = get_moves_for_current_turn(state)
    if not moves:
        penalized = apply_penalty(state)
        return max_value(penalized, alpha, beta, depth + 1, max_depth)

    value = float("inf")
    for move in _list_moves_to_explore(state, moves):
        next_state = apply_move(state, move)
        value = min(value, max_value(next_state, alpha, beta, depth + 1, max_depth))
        if value <= alpha:
            return value
        beta = min(beta, value)
    return value


def minimax_decision(state, max_depth):
    """Elige la mejor casilla destino para MAX (máquina)."""
    best_move = None
    best_value = float("-inf")
    alpha = float("-inf")
    beta = float("inf")

    moves = get_moves_for_current_turn(state)
    if not moves:
        return None

    for move in _list_moves_to_explore(state, moves):
        next_state = apply_move(state, move)
        value = min_value(next_state, alpha, beta, depth=1, max_depth=max_depth)
        if value > best_value:
            best_value = value
            best_move = move
        alpha = max(alpha, value)

    return best_move
