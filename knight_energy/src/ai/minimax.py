"""
Algoritmo minimax sin poda (Paso 4).

Implementa MINIMAX-DECISION del Tema 6 con profundidad límite
y evaluación heurística en nodos de corte.
"""

from src.ai.heuristics import utility
from src.game_logic.engine import apply_penalty, get_valid_actions, result_state


def cutoff_test(state, depth, max_depth):
    """
    Prueba de corte: profundidad alcanzada o estado terminal.
    depth cuenta plies desde la raíz (1 = primer movimiento del rival).
    """
    return depth >= max_depth or state.is_terminal()


def max_value(state, depth, max_depth):
    """Nodo MAX: elige el máximo entre sus sucesores."""
    if cutoff_test(state, depth, max_depth):
        return utility(state)

    actions = get_valid_actions(state)
    if not actions:
        # Sin movimientos legales: penalización y pasa el turno a MIN
        penalized = apply_penalty(state)
        return min_value(penalized, depth + 1, max_depth)

    value = float("-inf")
    for action in actions:
        successor = result_state(state, action)
        value = max(value, min_value(successor, depth + 1, max_depth))
    return value


def min_value(state, depth, max_depth):
    """Nodo MIN: elige el mínimo entre sus sucesores (mejor para el humano)."""
    if cutoff_test(state, depth, max_depth):
        return utility(state)

    actions = get_valid_actions(state)
    if not actions:
        penalized = apply_penalty(state)
        return max_value(penalized, depth + 1, max_depth)

    value = float("inf")
    for action in actions:
        successor = result_state(state, action)
        value = min(value, max_value(successor, depth + 1, max_depth))
    return value


def minimax_decision(state, max_depth):
    """
    MINIMAX-DECISION(state): retorna la mejor acción para MAX en la raíz.
    Retorna None si MAX no tiene movimientos legales (se aplica penalización fuera).
    """
    best_action = None
    best_value = float("-inf")

    actions = get_valid_actions(state)
    if not actions:
        return None

    for action in actions:
        successor = result_state(state, action)
        value = min_value(successor, depth=1, max_depth=max_depth)
        if value > best_value:
            best_value = value
            best_action = action

    return best_action
