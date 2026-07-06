"""
Iconos y efectos visuales: monedas, rayos y etiquetas flotantes.
"""

import pygame

from src.config import CELL_SIZE, INITIAL_ENERGY, TEXT_COLOR


def draw_mini_lightning(screen, center_x, center_y, size=14, color=(255, 160, 50)):
    """Rayo pequeño para feedback de energía."""
    half = size // 2
    points = [
        (center_x, center_y - half),
        (center_x - half + 2, center_y + 2),
        (center_x + 2, center_y - 2),
        (center_x - 2, center_y + half),
    ]
    pygame.draw.polygon(screen, color, points)
    pygame.draw.polygon(screen, (180, 90, 20), points, 1)


def draw_mini_coin(screen, center_x, center_y, radius=11):
    """Moneda dorada para feedback de puntos."""
    pygame.draw.circle(screen, (255, 210, 60), (center_x, center_y), radius)
    pygame.draw.circle(screen, (180, 130, 20), (center_x, center_y), radius, 2)
    pygame.draw.circle(screen, (255, 235, 130), (center_x - 3, center_y - 3), radius // 3)


def draw_board_coin(screen, center_x, center_y, value, font):
    """Moneda en el tablero con valor de puntos."""
    draw_mini_coin(screen, center_x, center_y, radius=14)
    label = font.render(str(value), True, (40, 30, 0))
    screen.blit(label, label.get_rect(center=(center_x, center_y)))


def draw_board_lightning(screen, row, col, value, font):
    """Rayo en el tablero con valor de energía."""
    center_x = col * CELL_SIZE + CELL_SIZE // 2
    center_y = row * CELL_SIZE + CELL_SIZE // 2
    draw_mini_lightning(screen, center_x, center_y - 4, size=18, color=(255, 150, 40))
    label = font.render(str(value), True, (255, 255, 255))
    screen.blit(label, (col * CELL_SIZE + 8, row * CELL_SIZE + 8))


def _fade_color(color, alpha_ratio):
    return tuple(min(255, int(c * alpha_ratio)) for c in color)


def draw_floating_effects(screen, labels, font, frame_index, total_frames):
    """
    Dibuja efectos flotantes separados verticalmente para evitar solapamiento.
    label: {kind: 'energy'|'points', value: int, cell: (r,c), slot: int}
    """
    alpha_ratio = max(0.2, 1.0 - (frame_index / max(1, total_frames)) * 0.85)
    drift_y = frame_index * 1.1

    for label in labels:
        row, col = label["cell"]
        slot = label.get("slot", 0)
        value = label["value"]
        kind = label["kind"]

        # Separación: cada etiqueta en un carril distinto (arriba/centro/abajo + ligero desplazamiento X)
        base_x = col * CELL_SIZE + CELL_SIZE // 2 + (slot - 1) * 28
        base_y = row * CELL_SIZE + CELL_SIZE // 3 - slot * 26 - drift_y

        sign = "+" if value > 0 else ""
        text = f"{sign}{value}"
        text_color = _fade_color(label.get("color", (255, 255, 255)), alpha_ratio)

        icon_x = base_x - 16
        if kind == "energy":
            draw_mini_lightning(
                screen,
                icon_x,
                int(base_y),
                size=12,
                color=_fade_color((255, 160, 50), alpha_ratio),
            )
        else:
            draw_mini_coin(screen, icon_x, int(base_y), radius=10)

        shadow = font.render(text, True, (20, 20, 20))
        text_surf = font.render(text, True, text_color)
        text_x = icon_x + 10
        text_y = int(base_y) - 8
        screen.blit(shadow, (text_x + 1, text_y + 1))
        screen.blit(text_surf, (text_x, text_y))


def draw_points_badge(screen, x, y, points, font, label_font):
    """Puntos dentro de un círculo dorado."""
    center = (x + 22, y + 22)
    pygame.draw.circle(screen, (255, 210, 60), center, 22)
    pygame.draw.circle(screen, (160, 120, 30), center, 22, 2)
    title = label_font.render("Points", True, (255, 230, 150))
    screen.blit(title, (x + 46, y + 4))
    value = font.render(str(points), True, (35, 25, 0))
    screen.blit(value, value.get_rect(center=center))


def draw_energy_bar(
    screen,
    x,
    y,
    width,
    current,
    label_font,
    value_font,
    maximum=INITIAL_ENERGY,
):
    """Barra de energía con etiqueta 'Energy'."""
    screen.blit(label_font.render("Energy", True, (150, 210, 255)), (x, y))

    bar_y = y + 18
    bar_h = 14
    pygame.draw.rect(screen, (50, 55, 65), (x, bar_y, width, bar_h), border_radius=4)
    pygame.draw.rect(screen, (90, 100, 115), (x, bar_y, width, bar_h), width=1, border_radius=4)

    fill_max = max(maximum, current, 1)
    fill_w = int(width * min(current, fill_max) / fill_max)
    if fill_w > 0:
        fill_color = (80, 180, 255) if current > 2 else (255, 160, 70)
        pygame.draw.rect(screen, fill_color, (x, bar_y, fill_w, bar_h), border_radius=4)

    value = value_font.render(f"{current}", True, TEXT_COLOR)
    screen.blit(value, (x + width + 6, bar_y - 1))
