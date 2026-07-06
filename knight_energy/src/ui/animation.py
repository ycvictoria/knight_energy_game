"""
Animaciones de movimiento (salto en L) y etiquetas flotantes en el tablero.
"""

import math
import sys

import pygame

from src.config import CELL_SIZE, MAX
from src.ui.effects import draw_floating_effects


def _ease_in_out(t):
    """Suaviza inicio y fin del movimiento (0 <= t <= 1)."""
    return t * t * (3.0 - 2.0 * t)


def _jump_position(from_cell, to_cell, progress):
    """
    Posición interpolada con arco parabólico (salto de caballo).
    progress: 0 en origen, 1 en destino.
    Retorna (row, col, jump_offset_y en pixeles).
    """
    eased = _ease_in_out(progress)
    fr, fc = from_cell
    tr, tc = to_cell

    row = fr + (tr - fr) * eased
    col = fc + (tc - fc) * eased

    jump_height = 38.0
    jump_offset_y = math.sin(progress * math.pi) * jump_height

    return row, col, jump_offset_y


def _pump_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def animate_knight_jump(
    screen,
    clock,
    renderer,
    state,
    from_cell,
    to_cell,
    player,
    player_name,
    float_labels,
    frames=48,
):
    """
    Anima el salto del caballo en arco hacia to_cell.
    Al aterrizar muestra las etiquetas flotantes unos frames extra.
    """
    is_white = player == MAX
    float_frames = 40
    float_font = renderer.float_font

    for frame in range(1, frames + 1):
        progress = frame / frames
        row, col, jump_y = _jump_position(from_cell, to_cell, progress)

        white_override = (row, col) if is_white else None
        black_override = (row, col) if not is_white else None

        _pump_events()
        renderer.draw_game(
            screen,
            state,
            [],
            False,
            player_name,
            white_override=white_override,
            black_override=black_override,
            jump_offset_white=jump_y if is_white else 0,
            jump_offset_black=jump_y if not is_white else 0,
        )
        pygame.display.flip()
        clock.tick(50)

    for float_frame in range(float_frames):
        _pump_events()
        renderer.draw_game(
            screen,
            state,
            [],
            False,
            player_name,
            white_override=to_cell if is_white else None,
            black_override=to_cell if not is_white else None,
        )
        draw_floating_effects(screen, float_labels, float_font, float_frame, float_frames)
        pygame.display.flip()
        clock.tick(50)


def animate_penalty_feedback(
    screen,
    clock,
    renderer,
    state,
    player,
    player_name,
    float_labels,
):
    """Animación corta cuando hay penalización sin movimiento."""
    float_frames = 44
    float_font = renderer.float_font
    is_white = player == MAX

    for float_frame in range(float_frames):
        _pump_events()
        renderer.draw_game(
            screen,
            state,
            [],
            False,
            player_name,
            white_override=state.white_pos if is_white else None,
            black_override=state.black_pos if not is_white else None,
        )
        draw_floating_effects(screen, float_labels, float_font, float_frame, float_frames)
        pygame.display.flip()
        clock.tick(50)
