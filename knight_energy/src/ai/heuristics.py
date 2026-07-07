"""
Heurística para minimax (decisiones imperfectas).

Mejora 1 — Botín alcanzable:
  f4/f5 solo cuentan monedas y rayos alcanzables en 1 salto legal.

Mejora 3 — Gestión de energía:
  Pesos de energía/rayos más altos, umbral amplio y penalización por crisis
  energética (sin rayo alcanzable) para evitar −3 pts por quedarse sin movimientos.

EVAL(s) = w1·f1 + w2·f2 + w3·f3 + w4·f4 + w5·f5 + ajuste_crisis
"""

import math

from src.config import MAX, MIN
from src.game_logic.engine import get_legal_moves_for_player, get_player_energy


# Pesos: puntos dominan; energía y rayos más relevantes que antes
W_SCORE = 1000
W_ENERGY = 35
W_MOBILITY = 5
W_REACHABLE_STARS = 50
W_REACHABLE_LIGHTNING = 50

LOW_ENERGY_THRESHOLD = 6  # f5: valorar rayos alcanzables con energía <= este valor
ENERGY_CRISIS_LEVEL = 2  # f6: alerta si energía <= este valor y no hay rayo cerca


def _reachable_star_value(state, player):
    """f4: monedas que este jugador puede capturar en su próximo salto."""
    total = 0
    for row, col in get_legal_moves_for_player(state, player):
        cell = state.board[row][col]
        if cell is not None and cell["type"] == "star":
            total += cell["value"]
    return total


def _has_reachable_lightning(state, player):
    """¿Hay algún rayo alcanzable en un salto?"""
    for row, col in get_legal_moves_for_player(state, player):
        cell = state.board[row][col]
        if cell is not None and cell["type"] == "lightning":
            return True
    return False


def _reachable_lightning_value(state, player):
    """f5: valor de rayos alcanzables cuando conviene recargar."""
    if get_player_energy(state, player) > LOW_ENERGY_THRESHOLD:
        return 0

    total = 0
    for row, col in get_legal_moves_for_player(state, player):
        cell = state.board[row][col]
        if cell is not None and cell["type"] == "lightning":
            total += cell["value"]
    return total


def _energy_crisis_adjustment(state):
    """
    Penaliza crisis energética sin rayo cercano (anticipa penalización −3).
    Desde la perspectiva de MAX: malo para blanco, bueno para negro.
    """
    adjustment = 0

    if state.white_energy <= ENERGY_CRISIS_LEVEL and not _has_reachable_lightning(state, MAX):
        adjustment -= (ENERGY_CRISIS_LEVEL + 1 - state.white_energy) * 80

    if state.black_energy <= ENERGY_CRISIS_LEVEL and not _has_reachable_lightning(state, MIN):
        adjustment += (ENERGY_CRISIS_LEVEL + 1 - state.black_energy) * 80

    return adjustment


def _mobility_difference(state):
    """f3: cuántos movimientos legales tiene MAX menos los de MIN."""
    white_moves = len(get_legal_moves_for_player(state, MAX))
    black_moves = len(get_legal_moves_for_player(state, MIN))
    return white_moves - black_moves


def eval_state(state):
    """
    EVAL(s) desde la perspectiva de MAX (máquina).
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
        + _energy_crisis_adjustment(state)
    )


def utility(state):
    """Terminal: ±∞ si hay ganador; si no, heurística eval_state."""
    if state.is_terminal():
        score_diff = state.white_score - state.black_score
        if score_diff > 0:
            return math.inf
        if score_diff < 0:
            return -math.inf
        return 0

    return eval_state(state)
