"""
Función de utilidad heurística para minimax con decisiones imperfectas.

Evaluación lineal desde la perspectiva de MAX (máquina), según Tema 6:
  EVAL(s) = w1·f1(s) + w2·f2(s) + w3·f3(s) + w4(s) + w5·f5(s)

f4 y f5 usan botín alcanzable en un salto (no todo el tablero).
"""

import math

from src.config import MAX, MIN
from src.game_logic.engine import get_legal_moves_for_player, get_player_energy


# Pesos de la combinación lineal (priorizan puntos >> estrellas >> energía > movilidad)
W_SCORE = 1000
W_ENERGY = 15
W_MOBILITY = 5
W_REACHABLE_STARS = 50
W_REACHABLE_LIGHTNING = 25

# Solo cuenta rayos alcanzables cuando la energía está baja
LOW_ENERGY_THRESHOLD = 3


def _reachable_star_value(state, player):
    """Valor de monedas capturables en el próximo salto legal."""
    total = 0
    for row, col in get_legal_moves_for_player(state, player):
        cell = state.board[row][col]
        if cell is not None and cell["type"] == "star":
            total += cell["value"]
    return total


def _reachable_lightning_value(state, player):
    """Valor de rayos alcanzables si el jugador necesita recargar energía."""
    if get_player_energy(state, player) > LOW_ENERGY_THRESHOLD:
        return 0

    total = 0
    for row, col in get_legal_moves_for_player(state, player):
        cell = state.board[row][col]
        if cell is not None and cell["type"] == "lightning":
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
    f4: monedas alcanzables en 1 salto (MAX − MIN)
    f5: rayos alcanzables con energía baja (MAX − MIN)
    """
    f1 = state.white_score - state.black_score
    f2 = state.white_energy - state.black_energy
    f3 = _mobility_difference(state)
    f4 = _reachable_star_value(state, MAX) - _reachable_star_value(state, MIN)
    f5 = _reachable_lightning_value(state, MAX) - _reachable_lightning_value(state, MIN)

    return (
        (W_SCORE * f1)
        + (W_ENERGY * f2)
        + (W_MOBILITY * f3)
        + (W_REACHABLE_STARS * f4)
        + (W_REACHABLE_LIGHTNING * f5)
    )


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
