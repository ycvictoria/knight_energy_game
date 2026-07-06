"""
Menú inicial: nombre del jugador, dificultad y fondo decorativo.
"""

import pygame

from src.config import DIFFICULTIES, HEIGHT, TEXT_COLOR, WIDTH
from src.ui.backgrounds import draw_menu_background


class NameInputBox:
    """Campo de texto simple para capturar el nombre del jugador."""

    def __init__(self, rect, font, placeholder="Jugador"):
        self.rect = rect
        self.font = font
        self.placeholder = placeholder
        self.text = ""
        self.active = False
        self.max_length = 14

    def handle_event(self, event):
        """Procesa teclado y clic sobre el campo."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            return False

        if not self.active or event.type != pygame.KEYDOWN:
            return False

        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
            return False

        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            return True

        if event.key == pygame.K_ESCAPE:
            self.active = False
            return False

        if len(self.text) >= self.max_length:
            return False

        char = event.unicode
        if char.isprintable() and not char.isspace() or char == " ":
            if char != " " or (self.text and not self.text.endswith(" ")):
                self.text += char

        return False

    def get_name(self):
        """Nombre limpio; usa placeholder si el jugador no escribió nada."""
        cleaned = self.text.strip()
        return cleaned if cleaned else self.placeholder

    def draw(self, screen):
        """Dibuja etiqueta, caja y texto (o placeholder atenuado)."""
        label = self.font.render("Tu nombre", True, (255, 220, 120))
        screen.blit(label, (self.rect.x, self.rect.y - 22))

        fill = (85, 92, 108) if self.active else (72, 78, 92)
        border = (255, 215, 0) if self.active else (160, 170, 190)
        pygame.draw.rect(screen, fill, self.rect, border_radius=10)
        pygame.draw.rect(screen, border, self.rect, width=2, border_radius=10)

        display = self.text if self.text else self.placeholder
        color = TEXT_COLOR if self.text else (150, 155, 165)
        text_surface = self.font.render(display, True, color)
        text_rect = text_surface.get_rect(midleft=(self.rect.x + 12, self.rect.centery))
        screen.blit(text_surface, text_rect)

        if self.active:
            caret_x = text_rect.right + 2
            if not self.text:
                caret_x = self.rect.x + 12
            pygame.draw.line(
                screen,
                (255, 255, 160),
                (caret_x, self.rect.y + 8),
                (caret_x, self.rect.bottom - 8),
                2,
            )


class DifficultyMenu:
    """Pantalla de inicio con nombre del jugador y nivel de dificultad."""

    def __init__(self, fonts):
        self.fonts = fonts
        self.selected_depth = None

        button_width, button_height = 200, 40
        start_y = 340
        spacing = 52
        center_x = WIDTH // 2 - button_width // 2

        self.buttons = []
        for index, (label, key) in enumerate(
            [("Principiante", "principiante"), ("Amateur", "amateur"), ("Experto", "experto")]
        ):
            rect = pygame.Rect(center_x, start_y + index * spacing, button_width, button_height)
            self.buttons.append({"label": label, "key": key, "rect": rect})

        input_width, input_height = 260, 36
        self.name_input = NameInputBox(
            pygame.Rect(WIDTH // 2 - input_width // 2, 248, input_width, input_height),
            fonts["body"],
        )

    def handle_event(self, event):
        """
        Gestiona eventos del menú.
        Retorna profundidad minimax si el usuario confirmó con Enter en el nombre
        o eligió un botón de dificultad (tras el clic en botón).
        """
        if self.name_input.handle_event(event) and self.selected_depth is None:
            # Enter en nombre sin botón aún: no inicia partida, solo desactiva foco
            pass

        if event.type == pygame.MOUSEBUTTONDOWN:
            depth = self._depth_from_click(event.pos)
            if depth is not None:
                self.selected_depth = depth
                return depth

        return None

    def _depth_from_click(self, pos):
        for button in self.buttons:
            if button["rect"].collidepoint(pos):
                return DIFFICULTIES[button["key"]]
        return None

    def get_player_name(self):
        return self.name_input.get_name()

    def draw(self, screen):
        draw_menu_background(screen)

        title = self.fonts["title"].render("KNIGHT ENERGY", True, (255, 215, 0))
        shadow = self.fonts["title"].render("KNIGHT ENERGY", True, (120, 90, 10))
        title_x = WIDTH // 2 - title.get_width() // 2
        screen.blit(shadow, (title_x + 2, 52))
        screen.blit(title, (title_x, 50))

        subtitle = self.fonts["subtitle"].render("Elige tu nombre y la dificultad", True, TEXT_COLOR)
        screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 108))

        self.name_input.draw(screen)

        diff_label = self.fonts["label"].render("Dificultad", True, (255, 220, 120))
        screen.blit(diff_label, (WIDTH // 2 - diff_label.get_width() // 2, 308))

        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            rect = button["rect"]
            hovered = rect.collidepoint(mouse_pos)
            fill = (100, 175, 120) if hovered else (78, 130, 98)
            pygame.draw.rect(screen, fill, rect, border_radius=12)
            pygame.draw.rect(screen, (255, 230, 100), rect, width=2, border_radius=12)

            text = self.fonts["body"].render(button["label"], True, TEXT_COLOR)
            screen.blit(text, text.get_rect(center=rect.center))
