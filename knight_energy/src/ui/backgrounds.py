"""
Fondos decorativos: tablero de ajedrez y detalles temáticos.

Se usan en el menú y en el panel lateral para dar aspecto de juego.
"""

import pygame

from src.config import DARK_CELL, HEIGHT, LIGHT_CELL, MENU_BG, WIDTH


def _blend(color, factor):
    """Aclara un color RGB multiplicando cada canal por factor (>1 = más claro)."""
    return tuple(min(255, int(channel * factor)) for channel in color)


def draw_checkerboard(screen, cell_size, light_color, dark_color):
    """Dibuja un patrón ajedrezado que cubre toda la superficie."""
    cols = WIDTH // cell_size + 2
    rows = HEIGHT // cell_size + 2
    for row in range(rows):
        for col in range(cols):
            color = light_color if (row + col) % 2 == 0 else dark_color
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, color, rect)


def draw_menu_background(screen):
    """
    Fondo del menú: tablero claro + velo semitransparente + adornos.
    """
    # Tablero grande y suave detrás de todo
    light = _blend(LIGHT_CELL, 1.08)
    dark = _blend(DARK_CELL, 1.05)
    draw_checkerboard(screen, 48, light, dark)

    # Velo para que el texto destaque sin perder el dibujo del tablero
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((*MENU_BG, 165))
    screen.blit(overlay, (0, 0))

    _draw_corner_stars(screen)
    _draw_corner_bolts(screen)


def draw_panel_background(screen, panel_x, panel_width):
    """Fondo del panel lateral con tablero miniatura tenue."""
    panel_rect = pygame.Rect(panel_x, 0, panel_width, HEIGHT)
    panel_surface = pygame.Surface((panel_width, HEIGHT))

    light = _blend(LIGHT_CELL, 0.35)
    dark = _blend(DARK_CELL, 0.32)
    mini_cell = 20
    for row in range(HEIGHT // mini_cell + 1):
        for col in range(panel_width // mini_cell + 1):
            color = light if (row + col) % 2 == 0 else dark
            mini_rect = pygame.Rect(col * mini_cell, row * mini_cell, mini_cell, mini_cell)
            pygame.draw.rect(panel_surface, color, mini_rect)

    dark_veil = pygame.Surface((panel_width, HEIGHT), pygame.SRCALPHA)
    dark_veil.fill((40, 44, 52, 210))
    panel_surface.blit(dark_veil, (0, 0))

    screen.blit(panel_surface, (panel_x, 0))
    pygame.draw.line(screen, (255, 215, 0), (panel_x, 0), (panel_x, HEIGHT), 2)


def _draw_corner_stars(screen):
    """Estrellas decorativas en las esquinas del menú."""
    positions = [(40, 35), (WIDTH - 55, 45), (55, HEIGHT - 50), (WIDTH - 50, HEIGHT - 40)]
    for index, (x, y) in enumerate(positions):
        radius = 10 + (index % 2) * 4
        pygame.draw.circle(screen, (255, 210, 60), (x, y), radius)
        pygame.draw.circle(screen, (180, 130, 20), (x, y), radius, 2)


def _draw_corner_bolts(screen):
    """Rayos decorativos en los bordes del menú."""
    bolts = [(120, HEIGHT - 80), (WIDTH - 130, 90), (WIDTH // 2 - 180, 50)]
    for cx, cy in bolts:
        points = [(cx, cy - 14), (cx - 10, cy + 4), (cx + 2, cy - 2), (cx - 2, cy + 14)]
        pygame.draw.polygon(screen, (255, 150, 50), points)
        pygame.draw.polygon(screen, (200, 90, 20), points, 2)
