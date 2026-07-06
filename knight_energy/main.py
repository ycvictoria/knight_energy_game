"""
Punto de entrada del juego Knight Energy — Paso 4.

La máquina (MAX / caballo blanco) juega con minimax; el humano (MIN) con clic.
"""

import sys

import pygame

from src.ai.minimax import minimax_decision
from src.config import HEIGHT, MAX, MIN, PENALTY_POINTS, WIDTH
from src.game_logic.engine import (
    apply_penalty,
    can_player_move,
    get_valid_actions,
    is_game_over,
    result_state,
)
from src.models.state import GameState
from src.ui.fonts import load_game_fonts
from src.ui.menu import DifficultyMenu
from src.ui.renderer import GameRenderer


def resolve_turn_start(state, player_name):
    """Verifica si el jugador del turno puede mover; aplica penalización si no."""
    if is_game_over(state):
        return state, None, True

    if can_player_move(state, state.turn):
        return state, None, False

    penalized = apply_penalty(state)
    if state.turn == MAX:
        message = f"Penalizacion Maquina -{PENALTY_POINTS}"
    else:
        message = f"Penalizacion {player_name} -{PENALTY_POINTS}"

    if is_game_over(penalized):
        return penalized, message, True

    return penalized, message, False


def run_menu(screen, clock, fonts):
    """Bucle del menú hasta elegir dificultad. Retorna (profundidad, nombre)."""
    menu = DifficultyMenu(fonts)
    selected_depth = None

    while selected_depth is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            depth = menu.handle_event(event)
            if depth is not None:
                selected_depth = depth

        menu.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    return selected_depth, menu.get_player_name()


def execute_machine_turn(state, max_depth, player_name):
    """
    Ejecuta el turno de la máquina con minimax.
    Retorna (estado, mensaje_penalizacion, fin_de_partida).
    """
    ai_move = minimax_decision(state, max_depth)

    if ai_move is not None:
        state = result_state(state, ai_move)
    else:
        state, message, game_over = resolve_turn_start(state, player_name)
        return state, message, game_over

    if is_game_over(state):
        return state, None, True

    state, message, game_over = resolve_turn_start(state, player_name)
    return state, message, game_over


def run_game(screen, clock, renderer, player_name, max_depth):
    """Bucle principal: máquina con minimax, humano con clic."""
    state = GameState(generate_random=True)
    game_over = False
    penalty_message = None
    penalty_timer = 0
    machine_turn_pending = True  # MAX inicia según el enunciado

    state, penalty_message, game_over = resolve_turn_start(state, player_name)
    if penalty_message:
        penalty_timer = 90
        if state.turn == MIN:
            machine_turn_pending = False

    while True:
        # Turno automático de la máquina (una vez por cambio de turno a MAX)
        if not game_over and machine_turn_pending and state.turn == MAX:
            valid_moves = get_valid_actions(state)
            renderer.draw_game(
                screen, state, valid_moves, False, player_name, "Pensando..."
            )
            pygame.display.flip()

            state, msg, game_over = execute_machine_turn(state, max_depth, player_name)
            machine_turn_pending = False

            if msg:
                penalty_message = msg
                penalty_timer = 90

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Solo el humano (MIN) mueve con el mouse
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and state.turn == MIN:
                if not renderer.is_board_click(event.pos):
                    continue

                clicked_row, clicked_col = renderer.board_cell_from_click(event.pos)
                valid_moves = get_valid_actions(state)

                if (clicked_row, clicked_col) in valid_moves:
                    state = result_state(state, (clicked_row, clicked_col))

                    if is_game_over(state):
                        game_over = True
                    else:
                        state, msg, game_over = resolve_turn_start(state, player_name)
                        if msg:
                            penalty_message = msg
                            penalty_timer = 90
                        if state.turn == MAX and not game_over:
                            machine_turn_pending = True

        if game_over:
            renderer.draw_game_over(screen, state, player_name)
        elif not (machine_turn_pending and state.turn == MAX):
            valid_moves = get_valid_actions(state)
            highlight = state.turn == MIN
            renderer.draw_game(
                screen, state, valid_moves, highlight, player_name, penalty_message
            )

            if penalty_timer > 0:
                penalty_timer -= 1
                if penalty_timer == 0:
                    penalty_message = None

        pygame.display.flip()
        clock.tick(60)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Knight Energy")
    clock = pygame.time.Clock()

    fonts = load_game_fonts()
    renderer = GameRenderer(fonts)

    max_depth, player_name = run_menu(screen, clock, fonts)
    run_game(screen, clock, renderer, player_name, max_depth)


if __name__ == "__main__":
    main()
