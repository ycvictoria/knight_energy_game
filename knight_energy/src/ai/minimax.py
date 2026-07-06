"""
Algoritmo minimax con poda alfa-beta (Paso 5).

MINIMAX-DECISION con profundidad límite y evaluación heurística en el corte.
"""

from src.ai.heuristics import utility
from src.game_logic.engine import apply_penalty, get_valid_actions, result_state


def cutoff_test(state, depth, max_depth):
    """
    Prueba de corte: profundidad alcanzada o estado terminal.
    depth cuenta plies desde la raíz (1 = primer movimiento del rival).
    """
    return depth >= max_depth or state.is_terminal()


def max_value(state, alpha, beta, depth, max_depth):
    """Nodo MAX con poda beta."""
    if cutoff_test(state, depth, max_depth):
        return utility(state)

    actions = get_valid_actions(state)
    if not actions:
        penalized = apply_penalty(state)
        return min_value(penalized, alpha, beta, depth + 1, max_depth)

    value = float("-inf")
    for action in actions:
        successor = result_state(state, action)
        value = max(value, min_value(successor, alpha, beta, depth + 1, max_depth))
        if value >= beta:
            return value
        alpha = max(alpha, value)
    return value


def min_value(state, alpha, beta, depth, max_depth):
    """Nodo MIN con poda alpha."""
    if cutoff_test(state, depth, max_depth):
        return utility(state)

    actions = get_valid_actions(state)
    if not actions:
        penalized = apply_penalty(state)
        return max_value(penalized, alpha, beta, depth + 1, max_depth)

    value = float("inf")
    for action in actions:
        successor = result_state(state, action)
        value = min(value, max_value(successor, alpha, beta, depth + 1, max_depth))
        if value <= alpha:
            return value
        beta = min(beta, value)
    return value


def minimax_decision(state, max_depth):
    """
    MINIMAX-DECISION(state): mejor acción para MAX en la raíz con alfa-beta.
    Retorna None si MAX no tiene movimientos legales.
    """
    best_action = None
    best_value = float("-inf")
    alpha = float("-inf")
    beta = float("inf")

    actions = get_valid_actions(state)
    if not actions:
        return None

    for action in actions:
        successor = result_state(state, action)
        value = min_value(successor, alpha, beta, depth=1, max_depth=max_depth)
        if value > best_value:
            best_value = value
            best_action = action
        alpha = max(alpha, value)

    return best_action
