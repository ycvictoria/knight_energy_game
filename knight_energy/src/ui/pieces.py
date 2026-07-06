"""
Dibujo de piezas del tablero (caballos).

Usa el símbolo Unicode de ajedrez si la fuente lo soporta; si no,
dibuja una silueta vectorial simple de caballo.
"""

import pygame

from src.config import CELL_SIZE

# Símbolos Unicode de caballo blanco y negro
WHITE_KNIGHT_GLYPH = "\u2658"
BLACK_KNIGHT_GLYPH = "\u265e"

KNIGHT_FONT_CANDIDATES = [
    "Segoe UI Symbol",
    "DejaVu Sans",
    "Arial Unicode MS",
    "FreeSerif",
    "arial",
]


def _create_knight_font(size=50):
    """Busca una fuente del sistema que renderice bien el glifo de caballo."""
    for font_name in KNIGHT_FONT_CANDIDATES:
        font = pygame.font.SysFont(font_name, size)
        probe = font.render(WHITE_KNIGHT_GLYPH, True, (0, 0, 0))
        if probe.get_width() > 8:
            return font
    return pygame.font.SysFont("arial", size)


def _draw_knight_vector(screen, center_x, center_y, fill_color, outline_color):
    """
    Silueta de respaldo cuando la fuente no tiene glifo de caballo.
    Forma estilizada: cuerpo + cuello + cabeza de caballo vistos de perfil.
    """
    cx, cy = center_x, center_y
    scale = CELL_SIZE / 75.0

    # Cuerpo y base
    body = pygame.Rect(int(cx - 18 * scale), int(cy + 2 * scale), int(36 * scale), int(16 * scale))
    pygame.draw.ellipse(screen, fill_color, body)
    pygame.draw.ellipse(screen, outline_color, body, 2)

    # Cuello
    neck_points = [
        (cx - 4 * scale, cy + 2 * scale),
        (cx + 6 * scale, cy - 18 * scale),
        (cx + 14 * scale, cy - 16 * scale),
        (cx + 2 * scale, cy + 4 * scale),
    ]
    pygame.draw.polygon(screen, fill_color, neck_points)
    pygame.draw.polygon(screen, outline_color, neck_points, 2)

    # Cabeza y hocico
    head_points = [
        (cx + 10 * scale, cy - 18 * scale),
        (cx + 26 * scale, cy - 14 * scale),
        (cx + 24 * scale, cy - 6 * scale),
        (cx + 14 * scale, cy - 8 * scale),
        (cx + 12 * scale, cy - 16 * scale),
    ]
    pygame.draw.polygon(screen, fill_color, head_points)
    pygame.draw.polygon(screen, outline_color, head_points, 2)

    # Crin (detalle)
    pygame.draw.arc(
        screen,
        outline_color,
        pygame.Rect(int(cx - 2 * scale), int(cy - 28 * scale), int(22 * scale), int(20 * scale)),
        0.8,
        2.4,
        2,
    )


def draw_knight(screen, position, is_white, knight_font=None):
    """
    Dibuja un caballo en la casilla (fila, columna).
    is_white: True para caballo blanco (máquina), False para negro (humano).
    """
    row, col = position
    center_x = col * CELL_SIZE + CELL_SIZE // 2
    center_y = row * CELL_SIZE + CELL_SIZE // 2

    fill = (245, 245, 245) if is_white else (30, 30, 30)
    outline = (20, 20, 20) if is_white else (220, 220, 220)
    glyph = WHITE_KNIGHT_GLYPH if is_white else BLACK_KNIGHT_GLYPH

    if knight_font is None:
        knight_font = _create_knight_font()

    sprite = knight_font.render(glyph, True, fill)
    if sprite.get_width() <= 8:
        _draw_knight_vector(screen, center_x, center_y, fill, outline)
        return

    # Sombra/contorno suave para legibilidad sobre casillas claras y oscuras
    shadow = knight_font.render(glyph, True, outline)
    sprite_rect = sprite.get_rect(center=(center_x, center_y))
    shadow_rect = shadow.get_rect(center=(center_x + 1, center_y + 1))
    screen.blit(shadow, shadow_rect)
    screen.blit(sprite, sprite_rect)
