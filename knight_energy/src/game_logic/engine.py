from src.config import BOARD_SIZE, MAX, MIN

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


def get_knight_moves(row, col):
    """
    Devuelve todas las casillas alcanzables en L desde (row, col) dentro del tablero.
    No considera energía ni ocupación; eso se filtra en pasos posteriores.
    """
    moves = []
    for dr, dc in KNIGHT_OFFSETS:
        nr, nc = row + dr, col + dc
        if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
            moves.append((nr, nc))
    return moves


def get_player_position(state, player):
    """Obtiene la posición del caballo según el jugador (MAX=blanco, MIN=negro)."""
    return state.white_pos if player == MAX else state.black_pos


def get_current_player(state):
    """Jugador al que le corresponde mover en este estado."""
    return state.turn


def get_valid_actions(state):
    """
    Acciones legales para el jugador del turno actual.
    Paso 1: solo movimientos en L dentro del tablero (sin filtro de energía aún).
    """
    row, col = get_player_position(state, state.turn)
    return get_knight_moves(row, col)


def result_state(state, action):
    """
    Aplica la acción (movimiento a action=(fila, col)) y devuelve el nuevo estado.
    Implementa Result(s, a) del formalismo de juegos del Tema 6.
    """
    next_state = state.clone()
    target_row, target_col = action

    # Mover el caballo del jugador actual y descontar 1 de energía
    if next_state.turn == MAX:
        next_state.white_pos = (target_row, target_col)
        next_state.white_energy -= 1
    else:
        next_state.black_pos = (target_row, target_col)
        next_state.black_energy -= 1

    # Recoger ítem si la casilla destino tiene estrella o rayo
    cell = next_state.board[target_row][target_col]
    if cell is not None:
        if cell["type"] == "star":
            if next_state.turn == MAX:
                next_state.white_score += cell["value"]
            else:
                next_state.black_score += cell["value"]
            next_state.stars_count -= 1
        elif cell["type"] == "lightning":
            if next_state.turn == MAX:
                next_state.white_energy += cell["value"]
            else:
                next_state.black_energy += cell["value"]

        # La casilla se consume y no puede usarse de nuevo
        next_state.board[target_row][target_col] = None

    # Alternar turno
    next_state.turn = MIN if next_state.turn == MAX else MAX
    return next_state
