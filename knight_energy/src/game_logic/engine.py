from src.config import BOARD_SIZE, MAX, MIN, PENALTY_POINTS

# Desplazamientos en L de un caballo de ajedrez: (dfila, dcolumna)
KNIGHT_OFFSETS = [
    (1, 2),
    (1, -2),
    (-1, 2),
    (-1, -2),
    (2, 1),
    (2, -1),
    (-2, 1),
    (-2, -1),
]


def get_player_energy(state, player):
    """Energía disponible del jugador MAX (blanco) o MIN (negro)."""
    return state.white_energy if player == MAX else state.black_energy


def get_player_position(state, player):
    """Obtiene la posición del caballo según el jugador (MAX=blanco, MIN=negro)."""
    return state.white_pos if player == MAX else state.black_pos


def get_opponent(player):
    """Devuelve el contrincante de MAX o MIN."""
    return MIN if player == MAX else MAX


def get_current_player(state):
    """Jugador al que le corresponde mover en este estado."""
    return state.turn


def get_knight_moves(row, col):
    """
    Devuelve todas las casillas alcanzables en L desde (row, col) dentro del tablero.
    No filtra energía ni ocupación; eso se aplica en capas superiores.
    """
    moves = []
    for dr, dc in KNIGHT_OFFSETS:
        nr, nc = row + dr, col + dc
        if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
            moves.append((nr, nc))
    return moves


def _filter_occupied_squares(state, player, moves):
    """
    Elimina casillas ocupadas por el caballo enemigo.
    Convención del proyecto: los caballos no pueden compartir casilla.
    """
    opponent_pos = get_player_position(state, get_opponent(player))
    return [move for move in moves if move != opponent_pos]


def get_legal_moves_for_player(state, player):
    """
    Movimientos legales completos para un jugador concreto:
    - Debe tener energía > 0 (cada movimiento cuesta 1 unidad).
    - Debe ser un salto en L dentro del tablero.
    - No puede aterrizar sobre el caballo rival.
    """
    if get_player_energy(state, player) <= 0:
        return []

    row, col = get_player_position(state, player)
    raw_moves = get_knight_moves(row, col)
    return _filter_occupied_squares(state, player, raw_moves)


def get_moves_for_current_turn(state):
    """Casillas legales para el jugador cuyo turno es ahora (quien debe mover)."""
    return get_legal_moves_for_player(state, state.turn)


def can_player_move(state, player):
    """Indica si el jugador tiene al menos un movimiento legal disponible."""
    return len(get_legal_moves_for_player(state, player)) > 0


def both_players_without_energy(state):
    """Ambos jugadores sin energía: fin de partida por puntos."""
    return state.white_energy <= 0 and state.black_energy <= 0


def must_skip_turn(state):
    """True si al iniciar su turno el jugador actual no puede mover."""
    return not can_player_move(state, state.turn)


def is_game_over(state):
    """
    Fin de partida según el PDF:
    - No quedan casillas con puntos (estrellas), o
    - Ambos sin energía, o
    - Ninguno de los dos jugadores puede realizar movimientos legales.
    """
    if state.stars_count == 0:
        return True
    if both_players_without_energy(state):
        return True
    return not can_player_move(state, MAX) and not can_player_move(state, MIN)


def get_winner(state):
    """
    Determina el resultado final comparando puntajes acumulados.
    Retorna MAX, MIN o None si hay empate.
    """
    if state.white_score > state.black_score:
        return MAX
    if state.black_score > state.white_score:
        return MIN
    return None


def apply_penalty(state):
    """
    Aplica penalización cuando un jugador no puede mover en su turno:
    pierde el turno y se descuentan PENALTY_POINTS puntos (PDF: 3 puntos).
    """
    next_state = state.clone()

    if next_state.turn == MAX:
        next_state.white_score -= PENALTY_POINTS
    else:
        next_state.black_score -= PENALTY_POINTS

    next_state.turn = get_opponent(next_state.turn)
    return next_state


def apply_move(state, target_cell):
    """
    Ejecuta un salto del caballo a target_cell=(fila, col) y devuelve el tablero resultante.
    Resta 1 energía, recoge moneda/rayo si hay, y pasa el turno al rival.
    (Formalismo IA: Result(estado, movimiento))
    """
    next_state = state.clone()
    target_row, target_col = target_cell
    current_player = next_state.turn

    # Mover el caballo del jugador actual y descontar 1 de energía
    if current_player == MAX:
        next_state.white_pos = (target_row, target_col)
        next_state.white_energy -= 1
    else:
        next_state.black_pos = (target_row, target_col)
        next_state.black_energy -= 1

    # Recoger ítem si la casilla destino tiene estrella o rayo
    cell = next_state.board[target_row][target_col]
    if cell is not None:
        if cell["type"] == "star":
            if current_player == MAX:
                next_state.white_score += cell["value"]
            else:
                next_state.black_score += cell["value"]
            next_state.stars_count -= 1
        elif cell["type"] == "lightning":
            if current_player == MAX:
                next_state.white_energy += cell["value"]
            else:
                next_state.black_energy += cell["value"]

        # La casilla se consume y no puede usarse de nuevo
        next_state.board[target_row][target_col] = None

    # Alternar turno
    next_state.turn = get_opponent(current_player)
    return next_state
