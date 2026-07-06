"""
Punto de entrada del juego Knight Energy — Paso 1.

Modo actual: humano vs humano (ambos jugadores hacen clic).
Sirve para validar tablero, movimientos en L y recolección de ítems
antes de conectar la IA y la interfaz completa.
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
    TEXT_COLOR,
    WHITE,
    WIDTH,
)
from src.game_logic.engine import get_valid_actions, result_state
from src.models.state import GameState


def draw_board(screen, state, valid_moves, font):
    """Dibuja tablero, ítems, caballos y datos básicos (UI mínima del Paso 1)."""
    screen.fill(BLACK)

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            # Patrón ajedrezado
            color = LIGHT_CELL if (row + col) % 2 == 0 else DARK_CELL

            # Resaltar casillas válidas para el jugador del turno
            if (row, col) in valid_moves:
                color = HIGHLIGHT_COLOR

            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)

            # Dibujar estrella (puntos) o rayo (energía) si existe en la casilla
            item = state.board[row][col]
            if item is not None:
                center_x = col * CELL_SIZE + CELL_SIZE // 2
                center_y = row * CELL_SIZE + CELL_SIZE // 2

                if item["type"] == "star":
                    pygame.draw.circle(screen, (255, 215, 0), (center_x, center_y), 15)
                    label = font.render(str(item["value"]), True, BLACK)
                    screen.blit(label, (col * CELL_SIZE + 10, row * CELL_SIZE + 8))
                elif item["type"] == "lightning":
                    # Forma simple de rayo
                    points = [
                        (center_x, row * CELL_SIZE + 10),
                        (col * CELL_SIZE + 15, center_y + 5),
                        (center_x + 5, center_y),
                        (center_x - 5, row * CELL_SIZE + CELL_SIZE - 10),
                    ]
                    pygame.draw.polygon(screen, (255, 140, 0), points)
                    label = font.render(str(item["value"]), True, WHITE)
                    screen.blit(label, (col * CELL_SIZE + 10, row * CELL_SIZE + 10))

    # Caballo blanco (MAX / jugador 1 en este modo de prueba)
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

    # Caballo negro (MIN / jugador 2 en este modo de prueba)
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

    # Texto informativo en la parte inferior (panel lateral llegará en Paso 3)
    turn_label = "Blanco (MAX)" if state.turn == MAX else "Negro (MIN)"
    info_lines = [
        f"Turno: {turn_label}",
        f"Blanco — Puntos: {state.white_score}  Energia: {state.white_energy}",
        f"Negro  — Puntos: {state.black_score}  Energia: {state.black_energy}",
    ]
    for i, line in enumerate(info_lines):
        text = font.render(line, True, TEXT_COLOR)
        screen.blit(text, (10, HEIGHT - 80 + i * 24))


def draw_game_over(screen, state, big_font, font):
    """Pantalla simple de fin de partida (Paso 1: solo por estrellas agotadas)."""
    screen.fill(BLACK)

    if state.white_score > state.black_score:
        message = "Gana Blanco (MAX)"
    elif state.black_score > state.white_score:
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


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Knight Energy — Paso 1 (Humano vs Humano)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)
    big_font = pygame.font.SysFont("Arial", 36)

    # Tablero aleatorio según el enunciado
    state = GameState(generate_random=True)
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Solo aceptar clics sobre el tablero 8x8
                if mouse_x >= BOARD_SIZE * CELL_SIZE or mouse_y >= BOARD_SIZE * CELL_SIZE:
                    continue

                clicked_row = mouse_y // CELL_SIZE
                clicked_col = mouse_x // CELL_SIZE
                valid_moves = get_valid_actions(state)

                if (clicked_row, clicked_col) in valid_moves:
                    state = result_state(state, (clicked_row, clicked_col))

                    if state.is_terminal():
                        game_over = True

        if game_over:
            draw_game_over(screen, state, big_font, font)
        else:
            valid_moves = get_valid_actions(state)
            draw_board(screen, state, valid_moves, font)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
