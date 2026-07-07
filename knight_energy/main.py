"""
Punto de entrada del juego Knight Energy.

Máquina: minimax con alfa-beta. Humano: clic. Movimientos con salto animado.
"""

import sys

import pygame

from src.ai.minimax import minimax_decision
from src.config import HEIGHT, MAX, MIN, WIDTH
from src.game_logic.engine import (
    apply_penalty,
    can_player_move,
    get_moves_for_current_turn,
    is_game_over,
    must_skip_turn,
)
from src.models.state import GameState
from src.ui.animation import animate_knight_jump, animate_penalty_feedback
from src.ui.feedback import describe_move, describe_penalty, describe_turn_hint
from src.ui.fonts import load_game_fonts
from src.ui.menu import DifficultyMenu
from src.ui.renderer import GameLog, GameRenderer


def run_menu(screen, clock, fonts):
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


def apply_move_with_animation(
    screen,
    clock,
    renderer,
    state,
    move,
    player,
    player_name,
):
    """Salto animado, etiquetas flotantes y actualización del registro de eventos."""
    from_cell = state.white_pos if player == MAX else state.black_pos
    float_labels, log_lines, after_state = describe_move(state, move, player, player_name)
    renderer.game_log.add_many(log_lines)

    animate_knight_jump(
        screen,
        clock,
        renderer,
        state,
        from_cell,
        move,
        player,
        player_name,
        float_labels,
    )

    return after_state


def show_penalty_animation(screen, clock, renderer, state, player_name):
    """Penalización al inicio de turno cuando el jugador actual no puede mover."""
    player = state.turn
    float_labels, log_lines = describe_penalty(state, player, player_name)
    renderer.game_log.add_many(log_lines)
    animate_penalty_feedback(screen, clock, renderer, state, player, player_name, float_labels)
    return apply_penalty(state)


def resolve_turn_start(screen, clock, renderer, state, player_name):
    """
    Al iniciar un turno: si el jugador no tiene energía/movimientos, -3 pts y pasa turno.
    Solo se evalúa aquí, nunca al terminar el movimiento anterior.
    """
    if is_game_over(state) or not must_skip_turn(state):
        return state

    return show_penalty_animation(screen, clock, renderer, state, player_name)


def run_game(screen, clock, renderer, player_name, max_depth):
    state = GameState(generate_random=True)
    game_over = False
    machine_turn_pending = True
    renderer.game_log = GameLog()
    renderer.game_log.add("Partida iniciada. La Maquina mueve primero.")

    while True:
        if not game_over:
            state = resolve_turn_start(screen, clock, renderer, state, player_name)
            if is_game_over(state):
                game_over = True
            elif state.turn == MAX and can_player_move(state, MAX):
                machine_turn_pending = True

        if not game_over and machine_turn_pending and state.turn == MAX:
            if can_player_move(state, MAX):
                renderer.draw_game(
                    screen,
                    state,
                    get_moves_for_current_turn(state),
                    False,
                    player_name,
                    status_message="Pensando...",
                )
                pygame.display.flip()

                ai_move = minimax_decision(state, max_depth)

                if ai_move is not None:
                    state = apply_move_with_animation(
                        screen, clock, renderer, state, ai_move, MAX, player_name
                    )
                    if not is_game_over(state) and state.turn == MIN and can_player_move(state, MIN):
                        renderer.game_log.add(describe_turn_hint(state, player_name))
                else:
                    state = resolve_turn_start(screen, clock, renderer, state, player_name)
                    if is_game_over(state):
                        game_over = True
                    elif state.turn == MIN and can_player_move(state, MIN):
                        renderer.game_log.add(describe_turn_hint(state, player_name))
                    elif state.turn == MAX and can_player_move(state, MAX):
                        machine_turn_pending = True

            machine_turn_pending = False

            if is_game_over(state):
                game_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                if renderer.is_restart_click(event.pos):
                    return True

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and state.turn == MIN:
                if not renderer.is_board_click(event.pos):
                    continue

                move = renderer.board_cell_from_click(event.pos)
                if move not in get_moves_for_current_turn(state):
                    continue

                state = apply_move_with_animation(
                    screen, clock, renderer, state, move, MIN, player_name
                )

                if is_game_over(state):
                    game_over = True
                elif state.turn == MAX:
                    machine_turn_pending = True

        if game_over:
            renderer.draw_game_over(screen, state, player_name)
        elif not (machine_turn_pending and state.turn == MAX):
            valid_moves = get_moves_for_current_turn(state)
            highlight = state.turn == MIN
            status = None
            if state.turn == MIN and valid_moves:
                status = "Elige casilla verde"
            renderer.draw_game(
                screen,
                state,
                valid_moves,
                highlight,
                player_name,
                status_message=status,
            )

        pygame.display.flip()
        clock.tick(60)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Knight Energy")
    clock = pygame.time.Clock()

    fonts = load_game_fonts()
    renderer = GameRenderer(fonts)

    while True:
        max_depth, player_name = run_menu(screen, clock, fonts)
        run_game(screen, clock, renderer, player_name, max_depth)


if __name__ == "__main__":
    main()
