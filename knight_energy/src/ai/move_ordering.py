"""
Orden de movimientos para mejorar la poda alfa-beta.

Explora primero capturas de monedas (mayor valor) y rayos urgentes (poca energía).
No altera el resultado minimax; reduce nodos visitados al encontrar cortes antes.
"""

from src.game_logic.engine import get_player_energy


def _action_priority(state, action):
    """
    Prioridad mayor = explorar antes.
    Perspectiva del jugador del turno actual (MAX o MIN).
    """
    row, col = action
    cell = state.board[row][col]
    if cell is None:
        return 0

    if cell["type"] == "star":
        return 1000 + cell["value"]

    if cell["type"] == "lightning":
        energy = get_player_energy(state, state.turn)
        priority = 100 + cell["value"]
        if energy <= 3:
            priority += 50
        return priority

    return 0


def order_actions(state, actions):
    """Lista de acciones ordenada de mayor a menor prioridad."""
    if len(actions) <= 1:
        return actions
    return sorted(actions, key=lambda action: _action_priority(state, action), reverse=True)
