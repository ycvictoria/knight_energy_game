"""
Heurística para minimax (decisiones imperfectas).

Mejora 1 — Botín alcanzable:
  Antes: sumaba TODAS las monedas del tablero (aunque fueran lejanas).
  Ahora: f4/f5 solo cuentan monedas y rayos alcanzables en 1 salto legal.

Evaluación lineal desde la perspectiva de MAX (máquina), según Tema 6:
  EVAL(s) = w1·f1 + w2·f2 + w3·f3 + w4·f4 + w5·f5
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

LOW_ENERGY_THRESHOLD = 3  # f5: rayos solo cuentan si energía <= este valor


def _reachable_star_value(state, player):
    """f4: monedas que este jugador puede capturar en su próximo salto."""
    total = 0
    for row, col in get_legal_moves_for_player(state, player):
        cell = state.board[row][col]
        if cell is not None and cell["type"] == "star":
            total += cell["value"]
    return total


def _reachable_lightning_value(state, player):
    """f5: rayos alcanzables cuando hace falta energía."""
    if get_player_energy(state, player) > LOW_ENERGY_THRESHOLD:
        return 0

    total = 0
    for row, col in get_legal_moves_for_player(state, player):
        cell = state.board[row][col]
        if cell is not None and cell["type"] == "lightning":
            total += cell["value"]
    return total


def _mobility_difference(state):
    """f3: cuántos movimientos legales tiene MAX menos los de MIN."""
    white_moves = len(get_legal_moves_for_player(state, MAX))
    black_moves = len(get_legal_moves_for_player(state, MIN))
    return white_moves - black_moves


def eval_state(state):
    """
    EVAL(s) = w1·Δpuntos + w2·Δenergía + w3·Δmovilidad + w4·Δmonedas_cercanas + w5·Δrayos_cercanos
    Siempre desde la perspectiva de MAX (máquina).
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
    """Terminal: ±∞ si hay ganador; si no, heurística eval_state."""
    if state.is_terminal():
        score_diff = state.white_score - state.black_score
        if score_diff > 0:
            return math.inf
        if score_diff < 0:
            return -math.inf
        return 0

    return eval_state(state)
