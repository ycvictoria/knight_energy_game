"""
Función de utilidad heurística para minimax con decisiones imperfectas.

Evaluación lineal desde la perspectiva de MAX (máquina), según Tema 6:
  EVAL(s) = w1·f1(s) + w2·f2(s) + w3·f3(s) + w4·f4(s)
"""

import math

from src.config import MAX, MIN
from src.game_logic.engine import get_legal_moves_for_player


# Pesos de la combinación lineal (priorizan puntos >> estrellas >> energía > movilidad)
W_SCORE = 1000
W_ENERGY = 15
W_MOBILITY = 5
W_STARS = 50


def _remaining_stars_value(state):
    """f4: suma de valores de estrellas aún presentes en el tablero."""
    total = 0
    for row in state.board:
        for cell in row:
            if cell is not None and cell["type"] == "star":
                total += cell["value"]
    return total


def _mobility_difference(state):
    """f3: movilidad de MAX menos movilidad de MIN (siempre perspectiva MAX)."""
    white_moves = len(get_legal_moves_for_player(state, MAX))
    black_moves = len(get_legal_moves_for_player(state, MIN))
    return white_moves - black_moves


def eval_state(state):
    """
    Heurística en nodos de corte (decisiones imperfectas).

    f1: diferencia de puntajes (blanco - negro)
    f2: diferencia de energía (blanco - negro)
    f3: diferencia de movilidad legal
    f4: valor total de estrellas restantes (proxy de botín futuro para MAX)
    """
    f1 = state.white_score - state.black_score
    f2 = state.white_energy - state.black_energy
    f3 = _mobility_difference(state)
    f4 = _remaining_stars_value(state)

    return (W_SCORE * f1) + (W_ENERGY * f2) + (W_MOBILITY * f3) + (W_STARS * f4)


def utility(state):
    """
    Utilidad en hojas del árbol minimax.
    Terminales: ±∞ según ganador (Tema 6); no terminales: EVAL(s).
    """
    if state.is_terminal():
        score_diff = state.white_score - state.black_score
        if score_diff > 0:
            return math.inf
        if score_diff < 0:
            return -math.inf
        return 0

    return eval_state(state)
