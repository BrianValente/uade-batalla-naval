import pygame
import re
from pygame import Surface
from typing import Optional


class TextInput:
    def __init__(
        self,
        pos: tuple[int, int],
        font: pygame.font.Font,
        text: str = "",
        base_color: tuple[int, int, int] = (255, 255, 255),
        selected_color: tuple[int, int, int] = (0, 255, 0),
        regex: Optional[str] = None,
    ):
        self.pos = pos
        self.font = font
        self.text = text
        self.base_color = base_color
        self.selected_color = selected_color
        self.selected = False
        self.max_length = 20
        self.regex = re.compile(regex) if regex else None
        self.previous_valid_text = text

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if clicked inside text input
            text_surface = self.font.render(self.text, True, self.base_color)
            text_rect = text_surface.get_rect(center=self.pos)
            text_rect.inflate_ip(20, 20)  # Make clickable area a bit larger
            self.selected = text_rect.collidepoint(event.pos)

        elif event.type == pygame.KEYDOWN and self.selected:
            if event.key == pygame.K_BACKSPACE:
                new_text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.selected = False
                return
            elif len(self.text) < self.max_length:
                new_text = self.text + event.unicode
            else:
                return

            # Validate against regex if pattern exists
            if self.regex:
                if new_text == "" or self.regex.match(new_text):
                    self.text = new_text
                    self.previous_valid_text = new_text
            else:
                self.text = new_text

    def draw(self, screen: Surface):
        color = self.selected_color if self.selected else self.base_color
        text_surface = self.font.render(self.text, True, color)
        text_rect = text_surface.get_rect(center=self.pos)

        # Draw background rect when selected
        if self.selected:
            bg_rect = text_rect.inflate(20, 20)
            pygame.draw.rect(screen, (50, 50, 50), bg_rect)
            pygame.draw.rect(screen, color, bg_rect, 2)

        screen.blit(text_surface, text_rect)

    def get_text(self) -> str:
        return self.text
