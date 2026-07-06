"""
Punto de entrada del juego Knight Energy — Paso 2.

Modo humano vs humano con reglas completas del PDF:
energía, penalización por no poder mover, y fin de partida correcto.
"""

import sys

import pygame

from src.config import (
    BLACK,
    BOARD_SIZE,
    CELL_SIZE,
    DARK_CELL,
    HEIGHT,
    HIGHLIGHT_COLOR,
    LIGHT_CELL,
    MAX,
    MIN,
    PENALTY_POINTS,
    TEXT_COLOR,
    WHITE,
    WIDTH,
)
from src.game_logic.engine import (
    apply_penalty,
    can_player_move,
    get_valid_actions,
    get_winner,
    is_game_over,
    result_state,
)
from src.models.state import GameState


def draw_board(screen, state, valid_moves, font, penalty_message=None):
    """Dibuja tablero, ítems, caballos y datos básicos."""
    screen.fill(BLACK)

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = LIGHT_CELL if (row + col) % 2 == 0 else DARK_CELL

            if (row, col) in valid_moves:
                color = HIGHLIGHT_COLOR

            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)

            item = state.board[row][col]
            if item is not None:
                center_x = col * CELL_SIZE + CELL_SIZE // 2
                center_y = row * CELL_SIZE + CELL_SIZE // 2

                if item["type"] == "star":
                    pygame.draw.circle(screen, (255, 215, 0), (center_x, center_y), 15)
                    label = font.render(str(item["value"]), True, BLACK)
                    screen.blit(label, (col * CELL_SIZE + 10, row * CELL_SIZE + 8))
                elif item["type"] == "lightning":
                    points = [
                        (center_x, row * CELL_SIZE + 10),
                        (col * CELL_SIZE + 15, center_y + 5),
                        (center_x + 5, center_y),
                        (center_x - 5, row * CELL_SIZE + CELL_SIZE - 10),
                    ]
                    pygame.draw.polygon(screen, (255, 140, 0), points)
                    label = font.render(str(item["value"]), True, WHITE)
                    screen.blit(label, (col * CELL_SIZE + 10, row * CELL_SIZE + 10))

    wr, wc = state.white_pos
    pygame.draw.circle(
        screen,
        (245, 245, 245),
        (wc * CELL_SIZE + CELL_SIZE // 2, wr * CELL_SIZE + CELL_SIZE // 2),
        22,
    )
    pygame.draw.circle(
        screen,
        BLACK,
        (wc * CELL_SIZE + CELL_SIZE // 2, wr * CELL_SIZE + CELL_SIZE // 2),
        22,
        2,
    )

    br, bc = state.black_pos
    pygame.draw.circle(
        screen,
        (35, 35, 35),
        (bc * CELL_SIZE + CELL_SIZE // 2, br * CELL_SIZE + CELL_SIZE // 2),
        22,
    )
    pygame.draw.circle(
        screen,
        WHITE,
        (bc * CELL_SIZE + CELL_SIZE // 2, br * CELL_SIZE + CELL_SIZE // 2),
        22,
        2,
    )

    turn_label = "Blanco (MAX)" if state.turn == MAX else "Negro (MIN)"
    info_lines = [
        f"Turno: {turn_label}",
        f"Blanco — Puntos: {state.white_score}  Energia: {state.white_energy}",
        f"Negro  — Puntos: {state.black_score}  Energia: {state.black_energy}",
    ]
    for i, line in enumerate(info_lines):
        text = font.render(line, True, TEXT_COLOR)
        screen.blit(text, (10, HEIGHT - 80 + i * 24))

    # Mensaje temporal cuando se aplica penalización (−3 puntos, pierde turno)
    if penalty_message:
        banner = font.render(penalty_message, True, (255, 80, 80))
        screen.blit(banner, (10, HEIGHT - 110))


def draw_game_over(screen, state, big_font, font):
    """Pantalla de fin de partida con ganador o empate."""
    screen.fill(BLACK)

    winner = get_winner(state)
    if winner == MAX:
        message = "Gana Blanco (MAX)"
    elif winner == MIN:
        message = "Gana Negro (MIN)"
    else:
        message = "Empate"

    title = big_font.render(message, True, TEXT_COLOR)
    detail = font.render(
        f"Marcador final — Blanco: {state.white_score} | Negro: {state.black_score}",
        True,
        TEXT_COLOR,
    )
    hint = font.render("Cierra la ventana para salir.", True, TEXT_COLOR)

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 40))
    screen.blit(detail, (WIDTH // 2 - detail.get_width() // 2, HEIGHT // 2 + 10))
    screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 50))


def resolve_turn_start(state):
    """
    Al inicio del turno de un jugador, verifica si puede mover.
    Si no puede y el rival sí, aplica penalización y pasa al otro.
    Retorna (nuevo_estado, mensaje_penalizacion o None, fin_de_partida).
    """
    if is_game_over(state):
        return state, None, True

    if can_player_move(state, state.turn):
        return state, None, False

    # Jugador actual no puede mover: penalización según el PDF
    penalized = apply_penalty(state)
    player_name = "Blanco" if state.turn == MAX else "Negro"
    message = f"Penalizacion: {player_name} -{PENALTY_POINTS} pts (sin movimiento)"

    if is_game_over(penalized):
        return penalized, message, True

    return penalized, message, False


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Knight Energy — Paso 2 (Humano vs Humano)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)
    big_font = pygame.font.SysFont("Arial", 36)

    state = GameState(generate_random=True)
    game_over = False
    penalty_message = None
    penalty_timer = 0  # frames restantes para mostrar el aviso de penalización

    # Resolver turno inicial (por si algún jugador no puede mover desde el inicio)
    state, penalty_message, game_over = resolve_turn_start(state)
    if penalty_message:
        penalty_timer = 90  # ~1.5 s a 60 FPS

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if mouse_x >= BOARD_SIZE * CELL_SIZE or mouse_y >= BOARD_SIZE * CELL_SIZE:
                    continue

                clicked_row = mouse_y // CELL_SIZE
                clicked_col = mouse_x // CELL_SIZE
                valid_moves = get_valid_actions(state)

                if (clicked_row, clicked_col) in valid_moves:
                    state = result_state(state, (clicked_row, clicked_col))

                    if is_game_over(state):
                        game_over = True
                    else:
                        # Tras mover, comprobar si el siguiente jugador puede actuar
                        state, msg, game_over = resolve_turn_start(state)
                        if msg:
                            penalty_message = msg
                            penalty_timer = 90

        if game_over:
            draw_game_over(screen, state, big_font, font)
        else:
            valid_moves = get_valid_actions(state)
            draw_board(screen, state, valid_moves, font, penalty_message)

            if penalty_timer > 0:
                penalty_timer -= 1
                if penalty_timer == 0:
                    penalty_message = None

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
