"""
Renderizado gráfico del tablero, panel lateral y pantallas de estado.
"""

import pygame

from src.config import (
    BLACK,
    BOARD_PIXELS,
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
from src.game_logic.engine import get_winner
from src.ui.backgrounds import draw_menu_background, draw_panel_background
from src.ui.pieces import _create_knight_font, draw_knight


class GameRenderer:
    """Encapsula todo el dibujo en pantalla del juego."""

    def __init__(self, fonts):
        self.fonts = fonts
        self.knight_font = _create_knight_font(44)

    def draw_game(self, screen, state, valid_moves, highlight_moves, player_name, penalty_message=None):
        screen.fill(BLACK)
        self._draw_board(screen, state, valid_moves if highlight_moves else [])
        self._draw_panel(screen, state, player_name, penalty_message)

    def _draw_board(self, screen, state, valid_moves):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = LIGHT_CELL if (row + col) % 2 == 0 else DARK_CELL
                if (row, col) in valid_moves:
                    color = HIGHLIGHT_COLOR
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, color, rect)

                item = state.board[row][col]
                if item is not None:
                    self._draw_cell_item(screen, row, col, item)

        draw_knight(screen, state.white_pos, is_white=True, knight_font=self.knight_font)
        draw_knight(screen, state.black_pos, is_white=False, knight_font=self.knight_font)

    def _draw_cell_item(self, screen, row, col, item):
        center_x = col * CELL_SIZE + CELL_SIZE // 2
        center_y = row * CELL_SIZE + CELL_SIZE // 2
        tiny = self.fonts["tiny"]

        if item["type"] == "star":
            pygame.draw.circle(screen, (255, 215, 0), (center_x, center_y), 13)
            pygame.draw.circle(screen, (200, 160, 0), (center_x, center_y), 13, 2)
            label = tiny.render(str(item["value"]), True, BLACK)
            screen.blit(label, (col * CELL_SIZE + 8, row * CELL_SIZE + 6))
        elif item["type"] == "lightning":
            points = [
                (center_x, row * CELL_SIZE + 10),
                (col * CELL_SIZE + 15, center_y + 5),
                (center_x + 5, center_y),
                (center_x - 5, row * CELL_SIZE + CELL_SIZE - 10),
            ]
            pygame.draw.polygon(screen, (255, 140, 0), points)
            label = tiny.render(str(item["value"]), True, WHITE)
            screen.blit(label, (col * CELL_SIZE + 8, row * CELL_SIZE + 8))

    def _draw_panel(self, screen, state, player_name, penalty_message):
        panel_width = WIDTH - BOARD_PIXELS
        panel_x = BOARD_PIXELS
        draw_panel_background(screen, panel_x, panel_width)

        # Título en dos líneas para que quepa en el panel estrecho
        title_line1 = self.fonts["panel_title"].render("KNIGHT", True, (255, 215, 0))
        title_line2 = self.fonts["panel_title"].render("ENERGY", True, (255, 215, 0))
        screen.blit(title_line1, (panel_x + 12, 18))
        screen.blit(title_line2, (panel_x + 12, 36))

        label = self.fonts["label"]
        tiny = self.fonts["tiny"]

        # Máquina
        screen.blit(label.render("Maquina", True, (200, 220, 255)), (panel_x + 12, 78))
        screen.blit(tiny.render(f"Pts: {state.white_score}", True, TEXT_COLOR), (panel_x + 16, 98))
        screen.blit(tiny.render(f"NRG: {state.white_energy}", True, (190, 190, 190)), (panel_x + 16, 114))

        # Humano (nombre del jugador)
        display_name = player_name[:12] + ".." if len(player_name) > 14 else player_name
        screen.blit(label.render(display_name, True, (255, 200, 140)), (panel_x + 12, 148))
        screen.blit(tiny.render(f"Pts: {state.black_score}", True, TEXT_COLOR), (panel_x + 16, 168))
        screen.blit(tiny.render(f"NRG: {state.black_energy}", True, (190, 190, 190)), (panel_x + 16, 184))

        # Turno actual
        if state.turn == MAX:
            turn_text = "Turno: Maquina"
            turn_color = (130, 200, 255)
        else:
            turn_text = f"Turno: {display_name}"
            turn_color = (120, 255, 160)

        turn_surf = self.fonts["body"].render(turn_text, True, turn_color)
        screen.blit(turn_surf, (panel_x + 12, 228))

        stars = tiny.render(f"Estrellas: {state.stars_count}", True, (200, 200, 200))
        screen.blit(stars, (panel_x + 12, 258))

        if penalty_message:
            # Partir mensaje largo en líneas si hace falta
            banner = tiny.render(penalty_message[:28], True, (255, 100, 100))
            screen.blit(banner, (panel_x + 12, 290))

    def draw_game_over(self, screen, state, player_name):
        draw_menu_background(screen)

        winner = get_winner(state)
        if winner == MAX:
            message = "Gano la Maquina"
        elif winner == MIN:
            message = f"Ganaste, {player_name}!"
        else:
            message = "Empate"

        title = self.fonts["big"].render(message, True, (255, 230, 100))
        shadow = self.fonts["big"].render(message, True, (80, 60, 10))
        detail = self.fonts["body"].render(
            f"Maquina {state.white_score}  —  {player_name} {state.black_score}",
            True,
            TEXT_COLOR,
        )
        hint = self.fonts["tiny"].render("Cierra la ventana para salir", True, (180, 180, 180))

        center_y = HEIGHT // 2
        tx = WIDTH // 2 - title.get_width() // 2
        screen.blit(shadow, (tx + 2, center_y - 48))
        screen.blit(title, (tx, center_y - 50))
        screen.blit(detail, (WIDTH // 2 - detail.get_width() // 2, center_y + 8))
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, center_y + 44))

    @staticmethod
    def is_board_click(pos):
        mouse_x, mouse_y = pos
        return mouse_x < BOARD_PIXELS and mouse_y < BOARD_PIXELS

    @staticmethod
    def board_cell_from_click(pos):
        mouse_x, mouse_y = pos
        return mouse_y // CELL_SIZE, mouse_x // CELL_SIZE
