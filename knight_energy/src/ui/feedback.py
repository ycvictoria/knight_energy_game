"""
Genera textos de feedback para movimientos, ítems y penalizaciones.
"""

from src.config import MAX, MIN, PENALTY_POINTS
from src.game_logic.engine import can_player_move, get_player_energy, result_state


def _actor_name(player, player_name):
    return "Maquina" if player == MAX else player_name


def describe_move(before_state, move, player, player_name):
    """
    Calcula etiquetas flotantes y mensajes de panel para un movimiento.
    Retorna (float_labels, log_lines, after_state).
    float_labels: lista de dict {text, color, cell}
    """
    after_state = result_state(before_state, move)
    actor = _actor_name(player, player_name)
    cell = before_state.board[move[0]][move[1]]

    float_labels = [
        {"kind": "energy", "value": -1, "color": (255, 170, 90), "cell": move, "slot": 0},
    ]
    log_lines = [f"{actor} salta a la casilla (gasta 1 de energia)."]

    if cell is not None:
        if cell["type"] == "star":
            float_labels.append(
                {
                    "kind": "points",
                    "value": cell["value"],
                    "color": (255, 230, 80),
                    "cell": move,
                    "slot": 1,
                }
            )
            log_lines.append(f"{actor} captura moneda: +{cell['value']} puntos.")
        elif cell["type"] == "lightning":
            float_labels.append(
                {
                    "kind": "energy",
                    "value": cell["value"],
                    "color": (120, 210, 255),
                    "cell": move,
                    "slot": 1,
                }
            )
            log_lines.append(f"{actor} toma rayo: +{cell['value']} energia.")

    return float_labels, log_lines, after_state


def describe_penalty(state, player, player_name):
    """Feedback cuando un jugador no puede mover (sin energia o bloqueado)."""
    actor = _actor_name(player, player_name)
    energy = get_player_energy(state, player)
    pos = state.white_pos if player == MAX else state.black_pos

    if energy <= 0:
        reason = f"{actor} no tiene energia para mover."
    elif not can_player_move(state, player):
        reason = f"{actor} no tiene casillas validas."
    else:
        reason = f"{actor} no puede jugar."

    float_labels = [
        {
            "kind": "points",
            "value": -PENALTY_POINTS,
            "color": (255, 90, 90),
            "cell": pos,
            "slot": 0,
        },
    ]
    log_lines = [
        reason,
        f"Penalizacion: -{PENALTY_POINTS} pts y pierde el turno.",
    ]
    return float_labels, log_lines


def describe_turn_hint(state, player_name):
    """Mensaje contextual al inicio del turno de un jugador."""
    if state.turn == MAX:
        if get_player_energy(state, MAX) <= 0:
            return "Maquina sin energia: aplicara penalizacion."
        return "Maquina calculando jugada..."
    name = player_name
    if get_player_energy(state, MIN) <= 0:
        return f"{name}: sin energia, recibiras -{PENALTY_POINTS} pts."
    return f"Tu turno, {name}. Elige una casilla verde."
