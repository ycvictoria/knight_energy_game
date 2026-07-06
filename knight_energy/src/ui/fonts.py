"""
Fuentes con estilo de juego casual para la interfaz.

Prioriza tipografías redondeadas disponibles en Windows; si no existen,
usa Arial como respaldo.
"""

import pygame

# Orden de preferencia: aspecto divertido / arcade
TITLE_FONT_CANDIDATES = ["Trebuchet MS", "Comic Sans MS", "Segoe UI", "Arial"]
BODY_FONT_CANDIDATES = ["Trebuchet MS", "Verdana", "Segoe UI", "Arial"]
LABEL_FONT_CANDIDATES = ["Verdana", "Trebuchet MS", "Segoe UI", "Arial"]


def _pick_font(candidates, size, bold=False):
    """Elige la primera fuente disponible de la lista de candidatos."""
    for name in candidates:
        path = pygame.font.match_font(name, bold=bold)
        if path:
            return pygame.font.Font(path, size)
    return pygame.font.SysFont("arial", size, bold=bold)


def load_game_fonts():
    """
    Carga el set de fuentes del juego con tamaños compactos.
    Retorna dict con claves: title, subtitle, body, label, tiny, big.
    """
    return {
        "title": _pick_font(TITLE_FONT_CANDIDATES, 38, bold=True),
        "subtitle": _pick_font(BODY_FONT_CANDIDATES, 17),
        "body": _pick_font(BODY_FONT_CANDIDATES, 16),
        "label": _pick_font(LABEL_FONT_CANDIDATES, 14, bold=True),
        "tiny": _pick_font(LABEL_FONT_CANDIDATES, 12),
        "big": _pick_font(TITLE_FONT_CANDIDATES, 30, bold=True),
        "panel_title": _pick_font(TITLE_FONT_CANDIDATES, 15, bold=True),
    }
