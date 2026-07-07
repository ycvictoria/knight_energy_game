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
from src.ui.effects import draw_board_coin, draw_board_lightning, draw_energy_bar, draw_points_badge
from src.ui.pieces import _create_knight_font, draw_knight_at


class GameLog:
    """Registro de eventos recientes mostrados en el panel lateral."""

    def __init__(self, max_lines=7):
        self.max_lines = max_lines
        self.lines = []

    def add(self, line):
        self.lines.append(line)
        if len(self.lines) > self.max_lines:
            self.lines = self.lines[-self.max_lines :]

    def add_many(self, lines):
        for line in lines:
            self.add(line)


class GameRenderer:
    """Encapsula todo el dibujo en pantalla del juego."""

    def __init__(self, fonts):
        self.fonts = fonts
        self.knight_font = _create_knight_font(44)
        self.float_font = pygame.font.SysFont("Verdana", 15, bold=True)
        self.stat_value_font = pygame.font.SysFont("Verdana", 18, bold=True)
        self.stat_label_font = pygame.font.SysFont("Verdana", 13, bold=True)
        self.game_log = GameLog()
        self.game_log.add("Partida iniciada. La Maquina mueve primero.")

    def draw_game(
        self,
        screen,
        state,
        valid_moves,
        highlight_moves,
        player_name,
        status_message=None,
        white_override=None,
        black_override=None,
        jump_offset_white=0,
        jump_offset_black=0,
    ):
        screen.fill(BLACK)
        self._draw_board(
            screen,
            state,
            valid_moves if highlight_moves else [],
        )
        white_pos = white_override if white_override is not None else state.white_pos
        black_pos = black_override if black_override is not None else state.black_pos
        draw_knight_at(
            screen,
            white_pos,
            is_white=True,
            knight_font=self.knight_font,
            jump_offset_y=jump_offset_white,
        )
        draw_knight_at(
            screen,
            black_pos,
            is_white=False,
            knight_font=self.knight_font,
            jump_offset_y=jump_offset_black,
        )
        self._draw_panel(screen, state, player_name, status_message)

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

    def _draw_cell_item(self, screen, row, col, item):
        center_x = col * CELL_SIZE + CELL_SIZE // 2
        center_y = row * CELL_SIZE + CELL_SIZE // 2
        tiny = self.fonts["tiny"]

        if item["type"] == "star":
            draw_board_coin(screen, center_x, center_y, item["value"], tiny)
        elif item["type"] == "lightning":
            draw_board_lightning(screen, row, col, item["value"], tiny)

    def _wrap_log_line(self, text, font, max_width):
        """Parte líneas largas para el panel estrecho."""
        words = text.split()
        if not words:
            return [""]

        lines = []
        current = words[0]
        for word in words[1:]:
            test = f"{current} {word}"
            if font.size(test)[0] <= max_width:
                current = test
            else:
                lines.append(current)
                current = word
        lines.append(current)
        return lines

    def _draw_panel(self, screen, state, player_name, status_message):
        panel_width = WIDTH - BOARD_PIXELS
        panel_x = BOARD_PIXELS
        draw_panel_background(screen, panel_x, panel_width)

        title_line1 = self.fonts["panel_title"].render("KNIGHT", True, (255, 215, 0))
        title_line2 = self.fonts["panel_title"].render("ENERGY", True, (255, 215, 0))
        screen.blit(title_line1, (panel_x + 10, 12))
        screen.blit(title_line2, (panel_x + 10, 28))

        label = self.fonts["label"]
        micro = pygame.font.SysFont("Verdana", 11)

        # Maquina: badge de puntos + barra de energia
        screen.blit(label.render("Maquina", True, (200, 220, 255)), (panel_x + 10, 54))
        draw_points_badge(
            screen,
            panel_x + 10,
            72,
            state.white_score,
            self.stat_value_font,
            self.stat_label_font,
        )
        draw_energy_bar(
            screen,
            panel_x + 10,
            118,
            panel_width - 50,
            state.white_energy,
            self.stat_label_font,
            self.stat_value_font,
        )

        pygame.draw.line(
            screen, (90, 95, 110), (panel_x + 8, 160), (panel_x + panel_width - 8, 160), 1
        )

        display_name = player_name[:10] + ".." if len(player_name) > 12 else player_name
        screen.blit(label.render(display_name, True, (255, 200, 140)), (panel_x + 10, 178))
        draw_points_badge(
            screen,
            panel_x + 10,
            196,
            state.black_score,
            self.stat_value_font,
            self.stat_label_font,
        )
        draw_energy_bar(
            screen,
            panel_x + 10,
            242,
            panel_width - 50,
            state.black_energy,
            self.stat_label_font,
            self.stat_value_font,
        )

        if state.turn == MAX:
            turn_text = "Turno: Maquina"
            turn_color = (130, 200, 255)
        else:
            turn_text = f"Turno: {display_name}"
            turn_color = (120, 255, 160)

        screen.blit(micro.render(turn_text, True, turn_color), (panel_x + 10, 278))
        screen.blit(
            micro.render(f"Monedas restantes: {state.stars_count}", True, (190, 190, 190)),
            (panel_x + 10, 294),
        )

        if status_message:
            status_color = (255, 200, 120) if "Pensando" in status_message else (255, 130, 130)
            status = micro.render(status_message[:30], True, status_color)
            screen.blit(status, (panel_x + 10, 312))

        pygame.draw.line(
            screen, (90, 95, 110), (panel_x + 8, 334), (panel_x + panel_width - 8, 334), 1
        )
        screen.blit(micro.render("Eventos:", True, (255, 220, 120)), (panel_x + 10, 344))

        log_y = 362
        max_text_width = panel_width - 20
        visible_lines = []
        for entry in self.game_log.lines:
            visible_lines.extend(self._wrap_log_line(entry, micro, max_text_width))

        for line in visible_lines[-8:]:
            color = (210, 210, 215)
            if "Penalizacion" in line or "penalizacion" in line.lower():
                color = (255, 140, 140)
            elif "+ " in line or "captura" in line or "toma rayo" in line:
                color = (180, 235, 180)
            screen.blit(micro.render(line, True, color), (panel_x + 10, log_y))
            log_y += 14
            if log_y > HEIGHT - 16:
                break

    def draw_game_over(self, screen, state, player_name):
        draw_menu_background(screen)

        winner = get_winner(state)
        if winner == MAX:
            message = "Gano la Maquina"
            reason = "La Maquina acumulo mas puntos."
        elif winner == MIN:
            message = f"Ganaste, {player_name}!"
            reason = f"{player_name} supero a la Maquina en puntos."
        else:
            message = "Empate"
            reason = "Ambos jugadores empataron en puntos."

        title = self.fonts["big"].render(message, True, (255, 230, 100))
        shadow = self.fonts["big"].render(message, True, (80, 60, 10))
        detail = self.fonts["body"].render(
            f"Maquina {state.white_score}  —  {player_name} {state.black_score}",
            True,
            TEXT_COLOR,
        )
        why = self.fonts["tiny"].render(reason, True, (200, 200, 200))

        center_y = HEIGHT // 2
        tx = WIDTH // 2 - title.get_width() // 2
        screen.blit(shadow, (tx + 2, center_y - 48))
        screen.blit(title, (tx, center_y - 50))
        screen.blit(detail, (WIDTH // 2 - detail.get_width() // 2, center_y + 8))
        screen.blit(why, (WIDTH // 2 - why.get_width() // 2, center_y + 34))

        button_width, button_height = 220, 42
        button_rect = pygame.Rect(
            WIDTH // 2 - button_width // 2,
            center_y + 62,
            button_width,
            button_height,
        )
        hovered = button_rect.collidepoint(pygame.mouse.get_pos())
        fill = (100, 175, 120) if hovered else (78, 130, 98)
        pygame.draw.rect(screen, fill, button_rect, border_radius=12)
        pygame.draw.rect(screen, (255, 230, 100), button_rect, width=2, border_radius=12)
        button_label = self.fonts["body"].render("Jugar de nuevo", True, TEXT_COLOR)
        screen.blit(button_label, button_label.get_rect(center=button_rect.center))

        self.game_over_restart_rect = button_rect
        return button_rect

    def is_restart_click(self, pos):
        return hasattr(self, "game_over_restart_rect") and self.game_over_restart_rect.collidepoint(pos)

    @staticmethod
    def is_board_click(pos):
        mouse_x, mouse_y = pos
        return mouse_x < BOARD_PIXELS and mouse_y < BOARD_PIXELS

    @staticmethod
    def board_cell_from_click(pos):
        mouse_x, mouse_y = pos
        return mouse_y // CELL_SIZE, mouse_x // CELL_SIZE
